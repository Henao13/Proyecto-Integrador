import pandas as pd
import random
import string

def generar_placa_colombiana(tipo_vehiculo):
    letras = ''.join(random.choices(string.ascii_uppercase, k=3))
    if tipo_vehiculo == 'Automóvil':
        numeros = ''.join(random.choices(string.digits, k=3))
    elif tipo_vehiculo == 'Moto':
        numeros = ''.join(random.choices(string.digits, k=2)) + ''.join(random.choices(string.ascii_uppercase, k=1))
    return letras + numeros

def generar_usuarios_frecuentes(n_vehiculos, n_usuarios):
    # Generar DataFrame de Vehículos
    tipos_vehiculo = ['Automóvil', 'Moto']
    tipo_vehiculo = [random.choice(tipos_vehiculo) for _ in range(n_vehiculos)]
    id_vehiculo = [generar_placa_colombiana(tipo) for tipo in tipo_vehiculo]
    
    df_vehiculos = pd.DataFrame({
        'id_vehiculo': id_vehiculo,
        'tipo_vehiculo': tipo_vehiculo
    })
    
    # Generar DataFrame de Usuarios Frecuentes
    id_usuario = [f'USR-{i+1:05d}' for i in range(n_usuarios)]
    nombres = [f'Usuario_{i+1}' for i in range(n_usuarios)]
    saldos = [round(random.uniform(0, 1000), 2) for _ in range(n_usuarios)]
    contraseñas = [''.join(random.choices(string.ascii_letters + string.digits, k=8)) for _ in range(n_usuarios)]
    emails = [f'usuario{i+1}@example.com' for i in range(n_usuarios)]
    id_vehiculo_fk = random.choices(df_vehiculos['id_vehiculo'].tolist(), k=n_usuarios)
    
    df_usuarios = pd.DataFrame({
        'id_usuario': id_usuario,
        'id_vehiculo': id_vehiculo_fk,
        'nombre_U': nombres,
        'saldo': saldos,
        'contraseña': contraseñas,
        'email': emails
    })
    
    return df_vehiculos, df_usuarios

# Ejemplo de uso con 10 vehículos y 15 usuarios
n_vehiculos = 10
n_usuarios = 15
df_vehiculos, df_usuarios = generar_usuarios_frecuentes(n_vehiculos, n_usuarios)

# Guardar los DataFrames en archivos tipo.txt y usuarios_frecuentes.txt
df_vehiculos.to_csv('usuarios.txt', sep='\t', index=False)
df_usuarios.to_csv('usuarios_frecuentes.txt', sep='\t', index=False)

print("Los archivos usuarios.txt y usuarios_frecuentes.txt han sido guardados con éxito.")
