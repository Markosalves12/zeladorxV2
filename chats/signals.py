from django.db.models.signals import post_save
from django.dispatch import receiver
from chats.models import MensagemJardinagem
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=MensagemJardinagem)
def enviar_notificacao_nova_mensagem(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'chat_{instance.chat.id}',
            {
                'type': 'chat_message',
                'message': instance.conteudo,
                'user': instance.usuario.username,
            }
        )