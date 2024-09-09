# parking/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import UsuarioFrecuente
from .forms import LoginForm, SaldoForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from decimal import Decimal, InvalidOperation
from .decorators import usuario_login_requerido

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

@usuario_login_requerido
def saldo(request):
    usuario_id = request.session['usuario_id']
    usuario = UsuarioFrecuente.objects.get(id_usuario=usuario_id)
    
    if request.method == 'POST':
        form = SaldoForm(request.POST)
        if form.is_valid():
            try:
                saldo = Decimal(form.cleaned_data['saldo'])
                usuario.saldo += saldo
                usuario.save()
                messages.success(request, 'Saldo añadido correctamente.')
            except InvalidOperation:
                messages.error(request, 'Saldo inválido.')
        else:
            messages.error(request, 'Formulario inválido.')
    else:
        form = SaldoForm()
    
    return render(request, 'saldo.html', {'form': form, 'usuario': usuario})