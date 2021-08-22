from django.db import models

from usuarios.models import User
from django.core.mail import EmailMessage
from django.utils.crypto import get_random_string
from django.conf import settings

class CorreioEletronico(models.Model):
    destino = models.CharField(max_length=200)
    mensagem = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    codigo_verificador = models.CharField(max_length=4, null=True, blank=True)

    def __str__(self):
        return self.destino

    def enviar_correio_eletronico(self, destino):
        subject = 'Codigo de verificação'
        self.codigo_verificador = get_random_string(length=5)
        self.mensagem = "Seu código verificador é: " + str(self.codigo_verificador)
        email_from = settings.DEFAULT_FROM_EMAIL

        self.destino = destino
        recipient_list = [destino, ]

        msg = EmailMessage(subject,self.mensagem , to=[self.destino])
        msg.send()

        self.save()

