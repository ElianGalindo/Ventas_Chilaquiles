# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 16:59:14 2024

@author: elian
"""

import tkinter as tk
from tkinter import ttk
import ventas
import agregar_venta
import estadistica
import clustering
import sentimientos
import inventario
from PIL import Image, ImageTk
global bg_image, bg
global bg_image2, bg2

# Función para limpiar el frame antes de cambiar de sección
def limpiar_frame():
    for widget in canvas.winfo_children():
        widget.destroy()
        
# Función para mostrar los datos de ventas
def mostrar_datos_ventas():
    limpiar_frame()
    ventas.mostrar_datos_ventas(canvas)

    
#Funcion para agregar nueva venta
def agregar_ventas():
    limpiar_frame()
    agregar_venta.agregar_nueva_venta(canvas)
    

#Funcion para mostrar el inventario
def mostrar_inventario():
    limpiar_frame()
    inventario.mostrar_inventario(canvas)
    
# Función para el apartado de estadísticas
def mostrar_estadisticas():
    limpiar_frame()
    notebook = ttk.Notebook(canvas)
    notebook.place(x=100, y=10, width=1300, height=925)

    sabores_frame = tk.Frame(notebook, bg="gainsboro")
    salsas_frame = tk.Frame(notebook, bg='gainsboro')
    mes_frame = tk.Frame(notebook, bg="gainsboro")
    dia_frame = tk.Frame(notebook, bg="gainsboro")
    hora_frame = tk.Frame(notebook, bg="gainsboro")

    notebook.add(sabores_frame, text='Sabores Populares')
    notebook.add(salsas_frame, text='Salsas Populares')
    notebook.add(mes_frame, text='Ventas por Mes')
    notebook.add(dia_frame, text='Ventas por Día')
    notebook.add(hora_frame, text='Picos por Hora')

    estadistica.mostrar_grafico_sabores(sabores_frame)
    estadistica.mostrar_grafico_salsas(salsas_frame)
    estadistica.mostrar_grafico_ventas_por_mes(mes_frame)
    estadistica.mostrar_grafico_ventas_por_dia(dia_frame)
    estadistica.mostrar_grafico_picos_por_hora(hora_frame)
    

# Función para el apartado de clustering
def mostrar_clustering():
    limpiar_frame()
    clustering.mostrar_clustering_sabores(canvas)

# Función para el análisis de sentimientos
def mostrar_analisis_sentimientos():
    limpiar_frame()
    sentimientos.mostrar_analisis_sentimientos(canvas)
    

# Crear la ventana principal
root = tk.Tk()
root.title("Análisis de Ventas y Comentarios")

#frame para los botones de navegación
botones_frame = tk.Frame(root, bg='#f1c40f')
botones_frame.pack(side="left", fill="y")

bg_image2 = Image.open("C:/Users/elian/OneDrive/Documentos/9na inscripcion/Mineria de datos/GUI/imagenes/lateral.jpeg")
bg_image2 = bg_image2.resize((350, 1000), Image.ANTIALIAS)  # Redimensionar la imagen para ajustarla a la ventana
bg2 = ImageTk.PhotoImage(bg_image2)
canvas = tk.Canvas(botones_frame, width=350, height=1000)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg2, anchor="nw")
canvas.image = bg2

#botones de navegación
boton_ventas = tk.Button(botones_frame, text="Datos de Ventas", command=mostrar_datos_ventas, relief="raised", width=30)
boton_ventas.place(x=30, y=300)

boton_agregar = tk.Button(botones_frame, text="Agregar Venta", command=agregar_ventas, relief="raised", width=30)
boton_agregar.place(x=30, y=400)

boton_inventario = tk.Button(botones_frame, text="Inventario", command=mostrar_inventario, relief="raised", width=30)
boton_inventario.place(x=30, y=500)

boton_estadisticas = tk.Button(botones_frame, text="Estadísticas", command=mostrar_estadisticas, relief="raised", width=30)
boton_estadisticas.place(x=30, y=600)

boton_clustering = tk.Button(botones_frame, text="Clustering", command=mostrar_clustering, relief="raised", width=30)
boton_clustering.place(x=30, y=700)

boton_sentimientos = tk.Button(botones_frame, text="Análisis de Sentimientos", command=mostrar_analisis_sentimientos, relief="raised", width=30)
boton_sentimientos.place(x=30, y=800)

#frame para mostrar el contenido
contenido_frame = tk.Frame(root)
contenido_frame.pack(side="right", fill="both", expand=True)

bg_image = Image.open("C:/Users/elian/OneDrive/Documentos/9na inscripcion/Mineria de datos/GUI/imagenes/fondo.jpeg")
bg_image = bg_image.resize((1700, 1000), Image.ANTIALIAS)
bg = ImageTk.PhotoImage(bg_image)
canvas = tk.Canvas(contenido_frame, width=1700, height=900)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg, anchor="nw")
canvas.image = bg


# Ejecutar la aplicación
root.mainloop()

