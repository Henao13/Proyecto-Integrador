# parking/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import UsuarioFrecuente, Tarifa
from .forms import LoginForm, SaldoForm, PaymentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from decimal import Decimal, InvalidOperation
from .decorators import usuario_login_requerido
from django.utils import timezone

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


@usuario_login_requerido
def payment(request):
    usuario_id = request.session['usuario_id']
    usuario = UsuarioFrecuente.objects.get(id_usuario=usuario_id)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            tipo_tarifa = form.cleaned_data['tipo_tarifa']
            saldo = Decimal(form.cleaned_data['saldo'])
            
            # Definir los valores de las tarifas
            tarifas_valores = {
                'Pagar día': Decimal('14000'),
                'Pagar hora': Decimal('3500'),
                'Recargar saldo': saldo  
            }
            
            # Obtener el valor de la tarifa seleccionada
            valor_tarifa = tarifas_valores.get(tipo_tarifa, Decimal('0.00'))
            
            if tipo_tarifa == 'Recargar saldo':
                if saldo > 0:
                    usuario.saldo += saldo
                    usuario.save()
                    
                    
                    tarifa = Tarifa.objects.create(
                        id_tarifa=tipo_tarifa,  
                        cost=saldo,
                    )
                    
                    messages.success(request, f'Saldo de ${saldo} recargado con éxito. Saldo actualizado.')
                    return redirect('home')
                else:
                    messages.error(request, 'Monto inválido.')
            else:
                if usuario.saldo >= valor_tarifa:
                    usuario.saldo -= valor_tarifa
                    usuario.save()
                    
                    # Crear una nueva tarifa
                    tarifa = Tarifa.objects.create(
                        id_tarifa=tipo_tarifa,  # Usar el tipo de tarifa como ID
                        cost=valor_tarifa,
                    )
                    
                    messages.success(request, f'Pago de ${valor_tarifa} realizado con éxito. Saldo actualizado.')
                    return redirect('home')
                else:
                    messages.error(request, 'Saldo insuficiente.')
                    # Mostrar el formulario nuevamente si no hay saldo suficiente
                    return render(request, 'payment.html', {'form': form, 'usuario': usuario})
        else:
            messages.error(request, 'Formulario inválido.')
    else:
        form = PaymentForm()
    
    return render(request, 'payment.html', {'form': form, 'usuario': usuario})