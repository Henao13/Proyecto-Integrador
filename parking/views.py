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
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from VirtualParking import settings

# Cargar las variables de entorno desde key.env
load_dotenv('key.env')
gemini_api_key = os.getenv('GENAI_API_KEY')
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

# Configurar la clave API
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Función para enviar el correo de recarga de saldo
def enviar_correo_recarga(usuario_email, monto_recargado):
    if not settings.SENDGRID_API_KEY:
        print("Error: La clave API de SendGrid no está configurada.")
        return

    if not usuario_email:
        print("Error: El correo electrónico del usuario no está especificado.")
        return

    mensaje = Mail(
        from_email='tucorreo@dominio.com',  # Cambia esto al correo verificado en SendGrid
        to_emails=usuario_email,
        subject='Recarga de Saldo Exitosa',
        html_content=f'<p>Estimado usuario,</p><p>Se ha recargado exitosamente un monto de ${monto_recargado} a su cuenta.</p>'
    )
    
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(mensaje)
        print("Correo enviado con éxito. Estado:", response.status_code)
    except Exception as e:
        print("Error al enviar el correo:", e)

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
    contenido_limpio = contenido.replace("**", "").replace("##", "").strip()

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
    usuario_id = request.session['usuario_id']
    usuario = UsuarioFrecuente.objects.get(id_usuario=usuario_id)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            tipo_tarifa = form.cleaned_data['tipo_tarifa']
            saldo = Decimal(form.cleaned_data['saldo']) if tipo_tarifa == 'Recargar saldo' else Decimal('0.00')

            tarifas_valores = {
                'Pagar día': Decimal('14000'),
                'Pagar hora': Decimal('3500'),
                'Recargar saldo': saldo  
            }

            if tipo_tarifa == 'Pagar día':
                valor_tarifa = tarifas_valores[tipo_tarifa]
                if usuario.saldo >= valor_tarifa:
                    usuario.saldo -= valor_tarifa
                    usuario.save()
                    messages.success(request, f'Pago de ${valor_tarifa} realizado con éxito. Saldo actualizado.')
                    return redirect('home')
                else:
                    messages.error(request, 'Saldo insuficiente para realizar este pago.')

            elif tipo_tarifa == 'Pagar hora':
                valor_tarifa = tarifas_valores[tipo_tarifa]
                if usuario.saldo >= valor_tarifa:
                    usuario.saldo -= valor_tarifa
                    usuario.save()
                    messages.success(request, f'Pago de ${valor_tarifa} realizado con éxito. Saldo actualizado.')
                    return redirect('home')
                else:
                    messages.error(request, 'Saldo insuficiente para realizar este pago.')

            elif tipo_tarifa == 'Recargar saldo':
                if saldo > 0:
                    usuario.saldo += saldo
                    usuario.save()
                    enviar_correo_recarga(usuario.email, saldo)
                    messages.success(request, f'Saldo de ${saldo} recargado con éxito. Saldo actualizado.')
                    return redirect('home')
                else:
                    messages.error(request, 'Monto inválido.')
            else:
                messages.error(request, 'Tipo de tarifa no válido.')
        else:
            messages.error(request, 'Formulario inválido.')
    else:
        form = PaymentForm()

    return render(request, 'payment.html', {'form': form, 'usuario': usuario})
