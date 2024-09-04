# parking/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UsuarioFrecuente
from .forms import LoginForm

def home(request):
    return render(request, 'home.html')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            contraseña = form.cleaned_data['contraseña']
            try:
                usuario = UsuarioFrecuente.objects.get(email=email, contraseña=contraseña)
                # Aquí puedes establecer la sesión del usuario
                request.session['usuario_id'] = usuario.id_usuario
                return redirect('home')
            except UsuarioFrecuente.DoesNotExist:
                messages.error(request, 'Email o contraseña incorrectos')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})