from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.http import HttpResponse
from .forms import SignUpForm, LoginForm

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import SignUpForm

from django.contrib.auth.models import Group

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Guardar el usuario
            User = form.save()

            # Añadir el usuario al grupo predeterminado (usuarios)
            group, created = Group.objects.get_or_create(name='usuarios')  # Crea el grupo si no existe
            User.groups.add(group)

            # Mostrar mensaje de éxito y redirigir
            messages.success(request, f'¡Registro exitoso! Bienvenido, {User.username}.')
            return redirect('/')  # Redirige a la página principal (ajústalo a tus necesidades)
        else:
            messages.error(request, 'Por favor corrige los errores del formulario, debe contener letras y números.')
    else:
        form = SignUpForm()

    return render(request, 'pages/register.html', {'form': form})
                    
       
def loginV (request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if  form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data['password']
            user = authenticate(request, username = username, password = password)
            if user is not None:

                print(user.groups)
                if user.groups.filter(name='Administracion').exists():
                    login(request, user)
                    messages.success(request, f'¡Inicio exitoso! Bienvenido, {user}.')
                    return render(request, 'pages/adminfunciones.html', {'form': form})

                elif user.groups.filter(name='usuarios').exists():
                    login(request, user)
                    messages.success(request, f'¡Inicio exitoso! Bienvenido, {user}.')
                    return render(request, 'pages/index.html', {'form': form})
                else: 
                    messages.error(request, 'La cuenta no es admin ni usuario')
    
            else:
                print(form)
                messages.error(request, 'Usuario o contraseña incorrecta')
    else:
        form = LoginForm()
    return render(request, 'pages/login.html', {'form': form})


def cerrar_sesion(request):
    logout(request)
    return redirect ('/')

    

def forgotpassword(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            associated_users = User.objects.filter(email=email)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Recuperación de contraseña para CineMax"
                    email_template_name = "pages/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': 'localhost:8000',  # Cambia esto por tu dominio en producción
                        'site_name': 'CineMax',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',  # Cambia a 'https' en producción
                    }
                    email = render_to_string(email_template_name, c)
                    send_mail(subject, email, 'user@example.com', [user.email], fail_silently=False)
                messages.success(request, 'Se ha enviado un correo con instrucciones para recuperar tu contraseña.')
                return redirect('login')
            else:
                messages.error(request, 'No existe una cuenta asociada a este correo electrónico.')
    else:
        form = PasswordResetForm()
    return render(request, 'pages/forgotpassword.html', {'form': form})
