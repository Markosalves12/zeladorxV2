random_password = get_random_string(
    length=12
)

enviar_notificacao(
    destinatario=[self.email],
    assunto="Novo gestor",
    contexto={
        'username': self.username,
        'email': self.email,
        'cargo': 'gestor',
        'empresa': self.EmpresaSecundaria,
        'senha': random_password
    },
    template='notifications/adicao_gestor.html'
)

self.password = make_password(random_password)