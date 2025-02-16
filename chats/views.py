from django.shortcuts import render, redirect, get_object_or_404
from chats.forms_jardinagem import ForumJardinagemForms, MensagemJardinagemForm
from django.contrib import messages
from chats.models import ForumJardinagem, MensagemJardinagem
from django.db.models import Q
from django.http import JsonResponse
from gerente.models import Gerente


def chats_jardinagem(request, id_random):
    forms = ForumJardinagemForms(request=request, userid=id_random)
    mensagemforms = MensagemJardinagemForm
    chats = ForumJardinagem.objects.filter(
        Q(criador__id_random=id_random) | Q(participantes__id_random=id_random)
    ).distinct()

    # Criar um dicionário para associar mensagens a cada chat
    mensagens_por_chat = {
        chat.id_random: MensagemJardinagem.objects.filter(forum=chat).order_by("enviado_em")
        for chat in chats
    }

    if request.method == 'POST':
        form = ForumJardinagemForms(request.POST, request.FILES, request=request, userid=id_random)
        if form.is_valid():
            form.save()
            messages.info(
                request=request,
                message=f'Chat {form.cleaned_data["nome"]} criado!'
            )
            return redirect('chats_jardinagem', id_random)

        messages.error(request, "Algo deu errado.")

    return render(
        request,
        'chats/chats.html',
        {
            'app_name': 'Chats Jardinagem',
            'forms': forms,
            'chats': chats,
            'mensagemforms': mensagemforms,
            'mensagens_por_chat': mensagens_por_chat,
            'id_random': id_random
        }
    )


def get_mensagens(request, chat_id):
    chat = get_object_or_404(ForumJardinagem, id=chat_id)
    mensagens = chat.mensagens.all().order_by('-enviado_em')[:10]  # Pega as 10 últimas mensagens

    # Serialize the messages data
    mensagens_data = [
        {
            'username': mensagem.remetente.username,
            'conteudo': mensagem.conteudo,
            'enviado_em': mensagem.enviado_em.strftime('%d %b %Y %H:%M'),
            'arquivo': mensagem.arquivo.url if mensagem.arquivo else None,
            'id_random': mensagem.remetente.id_random
        }
        for mensagem in mensagens
    ]

    return JsonResponse({'mensagens': mensagens_data})


def enviar_mensagem(request, chat_id, id_random):
    chat = get_object_or_404(ForumJardinagem, id=chat_id)

    if request.method == 'POST':
        form = MensagemJardinagemForm(request.POST, request.FILES)
        if form.is_valid():
            mensagem = form.save(commit=False)
            mensagem.forum = chat
            mensagem.remetente = Gerente.objects.get(id_random=id_random)

            if 'arquivo' in request.FILES:
                mensagem.arquivo = request.FILES['arquivo']

            mensagem.save()
            # messages.success(request, "Mensagem enviada com sucesso!")
        else:
            messages.error(request, "Erro ao enviar mensagem.")

    return redirect('chats_jardinagem', id_random=id_random)


def carregar_mensagens(request, chat_id):
    chat = get_object_or_404(ForumJardinagem, id_random=chat_id)
    mensagens = MensagemJardinagem.objects.filter(forum=chat).order_by('enviado_em')

    mensagens_json = [
        {
            "remetente": mensagem.remetente.username,
            "conteudo": mensagem.conteudo,
            "enviado_em": mensagem.enviado_em.strftime("%d %b %Y %H:%M"),
            "arquivo_url": mensagem.arquivo.url if mensagem.arquivo else None,
            "posicao": "right" if mensagem.remetente.id_random == request.GET.get("id_random") else "left"
        }
        for mensagem in mensagens
    ]

    return JsonResponse({"mensagens": mensagens_json})
