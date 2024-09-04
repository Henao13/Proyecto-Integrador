from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UsuarioFrecuente
from .forms import LoginForm

def home(request):
    usuario = None
    if 'usuario_id' in request.session:
        usuario_id = request.session['usuario_id']
        usuario = UsuarioFrecuente.objects.get(id_usuario=usuario_id)
    
    return render(request, 'home.html', {'usuario': usuario})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            id_vehiculo = form.cleaned_data['id_vehiculo']
            contraseña = form.cleaned_data['contraseña']
            try:
                usuario = UsuarioFrecuente.objects.get(id_vehiculo=id_vehiculo, contraseña=contraseña)
                request.session['usuario_id'] = usuario.id_usuario
                return redirect('home')
            except UsuarioFrecuente.DoesNotExist:
                messages.error(request, 'Placa o contraseña incorrectos')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    if 'usuario_id' in request.session:
        del request.session['usuario_id']
    return redirect('home')
