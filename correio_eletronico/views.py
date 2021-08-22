from django.http import JsonResponse, Http404
from django.shortcuts import render


# Create your views here.
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from correio_eletronico.api.serializers import VerificarCorreioEletronicoSerializer
from correio_eletronico.models import CorreioEletronico

