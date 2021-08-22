from django.db import models

from usuarios.models import User
from django.core.mail import send_mail
from django.utils.crypto import get_random_string


class CorreioEletronico(models.Model):
    destino = models.CharField(max_length=200)
    mensagem = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    codigo_verificador = models.CharField(max_length=4, null=True, blank=True)

    def __str__(self):
        return self.destino

    def enviar_correio_eletronico(self, destino):
        self.destino = destino
        self.codigo_verificador = get_random_string(length=5)

        self.mensagem = "Seu código verificador é: " + str(self.codigo_verificador)

        send_mail(
            'Código de Confirmação',
            self.mensagem,
            'contato@fcred.com.br',
            self.destino,
            fail_silently=False,
        )

        self.save()

