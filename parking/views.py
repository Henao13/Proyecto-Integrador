from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import UsuarioFrecuente
from .forms import LoginForm
from decimal import Decimal, InvalidOperation

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

def simular_transaccion_view(request, id_usuario):
    # Obtener el usuario por su ID
    user = UsuarioFrecuente.objects.get(id_usuario=id_usuario)

    if request.method == "POST":
        # Obtener la cantidad desde el formulario
        cantidad = request.POST.get('cantidad', 0)

        try:
            # Convertir la cantidad a Decimal
            cantidad = Decimal(cantidad)

            # Aumentar el saldo del usuario
            user.saldo += cantidad
            user.save()

            # Devolver la nueva cantidad como respuesta JSON
            return JsonResponse({"nuevo saldo": str(user.saldo)})  # Convertir a string para JSON

        except (ValueError, InvalidOperation):
            # Manejar el caso en que la cantidad no sea un número válido
            return JsonResponse({"error": "La cantidad debe ser un número válido."}, status=400)

    # Renderizar la plantilla y pasar el objeto usuario al contexto
    return render(request, 'saldo.html', {'user': user})