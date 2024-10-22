# parking/views.py
import google.generativeai as genai
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
from dotenv import load_dotenv
import os



# Cargar las variables de entorno desde key.env
load_dotenv('key.env')
gemini_api_key = os.getenv('GENAI_API_KEY')

# Configurar la clave API
genai.configure(api_key=gemini_api_key)
model= genai.GenerativeModel(model_name="gemini-1.5-flash")

def home(request):
    usuario = None
    if 'usuario_id' in request.session:
        usuario_id = request.session['usuario_id']
        usuario = UsuarioFrecuente.objects.get(id_usuario=usuario_id)

    # Generar instrucciones usando la API de Gemini
    prompt = "7 pasos para realizar un depósito en un sistema de parqueo y enuméralos."
    instrucciones = model.generate_content(prompt)

    # Extraer el contenido y eliminar el formato no deseado
    contenido = instrucciones.candidates[0].content.parts[0].text
    # Limpiar el contenido eliminando caracteres de formato como '**' y '##'
    contenido_limpio = contenido.replace("**", "").replace("##", "").strip()

    # Dividir el contenido por saltos de línea
    pasos = [line.strip() for line in contenido_limpio.split('\n') if line]

    return render(request, 'home.html', {'usuario': usuario, 'pasos': pasos})



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
    # Obtener el usuario de la sesión
    usuario_id = request.session['usuario_id']
    usuario = UsuarioFrecuente.objects.get(id_usuario=usuario_id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            tipo_tarifa = form.cleaned_data['tipo_tarifa']
            saldo = Decimal(form.cleaned_data['saldo']) if tipo_tarifa == 'Recargar saldo' else Decimal('0.00')

            # Definir los valores de las tarifas
            tarifas_valores = {
                'Pagar día': Decimal('14000'),
                'Pagar hora': Decimal('3500'),
                'Recargar saldo': saldo  
            }

            # Debug: Mostrar el tipo de tarifa seleccionada
            print(f'Tipo de tarifa seleccionada: {tipo_tarifa}')

            # Manejo de pago por tarifa
            if tipo_tarifa == 'Pagar día':
                valor_tarifa = tarifas_valores[tipo_tarifa]  # Obtener el valor de la tarifa

                # Debug: Mostrar el saldo antes de realizar el pago
                print(f'Saldo del usuario antes del pago: {usuario.saldo}')
                print(f'Valor de la tarifa seleccionada: {valor_tarifa}')

                if usuario.saldo >= 14000:  # Verifica que el saldo sea suficiente
                    try:
                        usuario.saldo -= 14000  # Descuenta el saldo

                        # Debug: Mostrar el saldo después de realizar el pago
                        print(f'Saldo del usuario después del pago: {usuario.saldo}')

                        usuario.save()  # Guarda los cambios
                        messages.success(request, f'Pago de ${valor_tarifa} realizado con éxito. Saldo actualizado.')
                        return redirect('home')
                    except InvalidOperation:
                        messages.error(request, 'Operación inválida al descontar el saldo.')
                else:
                    messages.error(request, 'Saldo insuficiente para realizar este pago.')

            elif tipo_tarifa == 'Pagar hora':
                valor_tarifa = tarifas_valores[tipo_tarifa]  # Obtener el valor de la tarifa

                # Debug: Mostrar el saldo antes de realizar el pago
                print(f'Saldo del usuario antes del pago: {usuario.saldo}')
                print(f'Valor de la tarifa seleccionada: {valor_tarifa}')

                if usuario.saldo >= 3500:  # Verifica que el saldo sea suficiente
                    try:
                        usuario.saldo -= 3500  # Descuenta el saldo

                        # Debug: Mostrar el saldo después de realizar el pago
                        print(f'Saldo del usuario después del pago: {usuario.saldo}')

                        usuario.save()  # Guarda los cambios
                        messages.success(request, f'Pago de ${valor_tarifa} realizado con éxito. Saldo actualizado.')
                        return redirect('home')
                    except InvalidOperation:
                        messages.error(request, 'Operación inválida al descontar el saldo.')
                else:
                    messages.error(request, 'Saldo insuficiente para realizar este pago.')

            elif tipo_tarifa == 'Recargar saldo':
                if saldo > 0:
                    try:
                        usuario.saldo += saldo  # Sumar el saldo
                        usuario.save()  # Guardar cambios
                        messages.success(request, f'Saldo de ${saldo} recargado con éxito. Saldo actualizado.')
                        return redirect('home')
                    except InvalidOperation:
                        messages.error(request, 'Operación inválida al recargar el saldo.')
                else:
                    messages.error(request, 'Monto inválido.')
            else:
                messages.error(request, 'Tipo de tarifa no válido.')
        else:
            # Debug: Mostrar errores de validación
            print("Errores en el formulario:", form.errors)
            messages.error(request, 'Formulario inválido.')
    else:
        form = PaymentForm()

    return render(request, 'payment.html', {'form': form, 'usuario': usuario})