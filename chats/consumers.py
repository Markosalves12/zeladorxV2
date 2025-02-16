import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ForumJardinagem, MensagemJardinagem
from gerente.models import Gerente
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.forum_id = self.scope["url_route"]["kwargs"]["forum_id"]
        self.room_group_name = f"chat_{self.forum_id}"

        # Adiciona o WebSocket ao grupo
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Remove o WebSocket do grupo
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Recebe mensagem do WebSocket"""
        data = json.loads(text_data)
        remetente_id_random = data["remetente_id_random"]
        conteudo = data["conteudo"]
        tipo = data.get("tipo", "texto")  # Padrão: texto

        # Salvar no banco
        mensagem = await self.salvar_mensagem(remetente_id_random, conteudo, tipo)

        # Enviar para o grupo WebSocket
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "remetente": mensagem.remetente.nome,  # Ajuste para mostrar o nome do Gerente
                "conteudo": mensagem.conteudo,
                "tipo": mensagem.tipo,
                "enviado_em": str(mensagem.enviado_em),
            },
        )

    async def chat_message(self, event):
        """Envia mensagem para WebSocket"""
        await self.send(text_data=json.dumps(event))

    @sync_to_async
    def salvar_mensagem(self, remetente_id_random, conteudo, tipo):
        """Salva a mensagem no banco de dados"""
        remetente = Gerente.objects.get(id_random=remetente_id_random)
        forum = ForumJardinagem.objects.get(id_random=self.forum_id)  # Ajustando para buscar pelo id_random
        return MensagemJardinagem.objects.create(
            forum=forum, remetente=remetente, conteudo=conteudo, tipo=tipo
        )
