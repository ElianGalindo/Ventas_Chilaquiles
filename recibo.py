# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 11:55:31 2024

@author: elian
"""

import os
from datetime import datetime

# Función para generar un recibo en formato de texto
def generar_recibo(telefono, nombre, ventas):
    # Crear una carpeta para guardar los recibos si no existe
    if not os.path.exists("recibos"):
        os.makedirs("recibos")

    # Nombre del archivo con base en la fecha y hora actual
    now = datetime.now()
    fecha_hora = now.strftime("%Y%m%d_%H%M%S")
    recibo_nombre = f"recibos/recibo_{telefono}_{fecha_hora}.txt"
    
    # Escribir el recibo en un archivo de texto
    with open(recibo_nombre, "w", encoding="utf-8") as f:
        f.write("---------- RECIBO DE COMPRA ----------\n")
        f.write(f"Fecha: {now.strftime('%Y-%m-%d')}\n")
        f.write(f"Hora: {now.strftime('%H:%M:%S')}\n")
        f.write(f"Cliente: {nombre}\n")
        f.write(f"Teléfono: {telefono}\n")
        f.write("--------------------------------------\n")
        total_venta = 0
        for venta in ventas:
            sabor = venta["sabor"]
            salsa = venta["salsa"]
            queso = venta["toppings"]["Queso"]
            crema = venta["toppings"]["Crema"]
            frijoles = venta["toppings"]["Frijoles"]
            cebolla = venta["toppings"]["Cebolla"]
            cantidad = venta["cantidad"].get()
            precio = venta["precio"].get()
            f.write(f"\nSabor: {sabor}\n")
            f.write(f"Salsa: {salsa}\n")
            f.write(f"Toppings: Queso - {queso}, Crema - {crema}, Frijoles - {frijoles}, Cebolla - {cebolla}\n")
            f.write(f"Cantidad: {cantidad}\n")
            f.write(f"Precio: ${precio}\n")
            f.write("--------------------------------------\n")
            total_venta += float(precio)
        
        f.write(f"\nTOTAL: ${total_venta}\n")
        f.write("--------------------------------------\n")
        f.write("¡Gracias por su compra!\n")

    print(f"Recibo generado: {recibo_nombre}")
