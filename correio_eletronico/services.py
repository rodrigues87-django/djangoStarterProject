import random

from django.core.mail import send_mail
from app27go_back.settings import EMAIL_HOST_USER
from correio_eletronico.models import CorreioEletronico


def enviar_correio_eletronico(user):
    correio_eletronico = CorreioEletronico(user=user)
    correio_eletronico.titulo = "Bem vindo ao 27go"
    correio_eletronico.origem = EMAIL_HOST_USER
    correio_eletronico.codigo_verificador = str(random.randint(1000, 9999))
    correio_eletronico.correio_eletronico = 'Seu código de confirmação: ' + correio_eletronico.codigo_verificador
    send_mail(correio_eletronico.titulo, correio_eletronico.correio_eletronico, correio_eletronico.origem,
              [correio_eletronico.user.email], fail_silently=False, )
    correio_eletronico.save()


def verificar_correio_eletronico(correio_eletronico):
    try:
        CorreioEletronico.objects.get(user=correio_eletronico.user, codigo_verificador=correio_eletronico.codigo_verificador)
        return True

    except CorreioEletronico.DoesNotExist:
        return False
