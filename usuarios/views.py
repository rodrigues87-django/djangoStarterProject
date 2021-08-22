from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
# Create your views here.
from django.views.decorators.csrf import csrf_protect
from rest_framework import generics
from rest_framework.permissions import AllowAny

from correio_eletronico.models import CorreioEletronico
from middlewares.loginMiddleware import login_exempt
from usuarios.api.serializers import UsuariosSerializer
from usuarios.forms import UserForm
from .models import User


def index(request):
    return render(request, 'dashboard.html')


@login_exempt
def chekLoginView(request):
    if request.user.is_authenticated:
        return redirect(index)
    else:
        return redirect(login_user)


@login_exempt
def login_user(request):
    return render(request, 'auth-login.html')


@login_exempt
@csrf_protect
def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(chekLoginView)
        else:
            messages.error(request, "Usuário e senha inválido. Favor tentar novamente.")
            return redirect('/usuarios/login')


@login_exempt
def forgot_password(request):
    return render(request,'auth-forgot-password.html')


@login_exempt
def register(request):
    return render(request, 'auth-register.html')


@login_exempt
@csrf_protect
def submit_register(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password2 is not password:
            messages.error(request, "senhas nao conferem")
            return redirect('/usuarios/register/')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(chekLoginView)
        else:

            correio_eletronico = CorreioEletronico()

            correio_eletronico.enviar_correio_eletronico(username)

            return redirect('/usuarios/login')

def confirmation_code(request):
    return render(request, 'confirmation_code.html')

class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UsuariosSerializer
    permission_classes = (AllowAny,)


def base(request):
    return render(request, 'base.html')


@csrf_protect
def submit_login_google(request):
    print("teste funcao")
    if request.POST and request.is_ajax():
        first_name = request.POST.get('first_name')
        imagem_url = request.POST.get('imagem_url')
        email = request.POST.get('email')

        password = User.objects.make_random_password()

        try:
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            user = authenticate(username=user.email, password=password)
            if user is not None:
                login(request, user)
                print("usuario logado...redirecionado para pagina inicial: " + password)

        except User.DoesNotExist:

            User.objects.create(first_name="first_name", imagem_url="imagem_url", email=email, password=password)
            user = authenticate(username=email, password=password)
            print("Usuario criado e esta autenticado")

    print("não entrou no post")
    return redirect('/')


@login_required
def logout(request):
    if request.user.is_authenticated:
        django_logout(request)
        return redirect('/usuarios/login/')
    else:
        messages.error(request, "Usuário não está logado")
        return redirect('/usuarios/login/')


def list_usuarios(request):
    try:
        usuario = User.objects.get(usuario=request.user.id)
    except User.DoesNotExist:
        usuario = User.objects.create(nome="Minha Dieta", usuario=request.user)

    return render(request, 'usuarios_lista.html', {'usuario': usuario})


def create_usuario(request):
    form = UserForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('list_usuarios')
    return render(request, 'site/usuarios/usuario-form.html', {'form': form})


def update_usuario(request, id):
    usuario = User.objects.get(id=id)
    form = UserForm(request.POST or None, instance=usuario)
    if form.is_valid():
        form.save()
        return redirect('list_usuarios')
    return render(request, 'site/usuarios/usuario-form.html', {'form': form, 'usuario': usuario})


def delete_usuario(request, id):
    usuario = User.objects.get(id=id)

    if request.method == "POST":
        print("delete usuario post")
        usuario.delete()
        return redirect('list_usuarios')

    return render(request, 'site/usuarios/confirm-usuario-delete.html', {'usuario': usuario})
