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

def generar_dataframe(n):
    # Tipos de vehículos disponibles
    tipos_vehiculo = ['Automóvil', 'Moto']
    
    # Generar los datos para el DataFrame
    tipo_vehiculo = [random.choice(tipos_vehiculo) for _ in range(n)]
    id_vehiculo = [generar_placa_colombiana(tipo) for tipo in tipo_vehiculo]
    
    # Crear el DataFrame
    df = pd.DataFrame({
        'id_vehiculo': id_vehiculo,
        'tipo_vehiculo': tipo_vehiculo
    })
    
    return df

# Ejemplo de uso con 10 filas
n = 10
df = generar_dataframe(n)

# Guardar el DataFrame en un archivo tipo.txt
df.to_csv('tipo.txt', sep='\t', index=False)

print("El archivo tipo.txt ha sido guardado con éxito.")
