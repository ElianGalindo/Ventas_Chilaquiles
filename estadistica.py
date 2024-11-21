# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 08:44:04 2024

@author: elian
"""

# estadisticas.py

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

plt.ioff()
# Función para mostrar las estadísticas de sabores populares en la GUI
def mostrar_grafico_sabores(canvas):
    conexion = sqlite3.connect('ventas2.db')
    df = pd.read_sql_query("SELECT * FROM ventas", conexion)
    conexion.close()

    sabores_populares = df.groupby('Sabor')['Cantidad'].sum()

    colors = ['deepskyblue', 'darkorchid', 'sienna', 'brown', 'red', 'yellow', 'lightyellow']
   
    fig, ax = plt.subplots(figsize=(8, 6))
    sabores_populares.plot(kind='bar', color=colors, ax=ax)
    ax.set_title('Sabores Populares')
    ax.set_xticklabels(sabores_populares.index, rotation=50)

    canvas_fig = FigureCanvasTkAgg(fig, master=canvas)
    canvas_fig.draw()
    canvas_fig.get_tk_widget().place(x=10, width=1200, height=895)
    
# Función para mostrar las estadísticas de salsas populares en la GUI
def mostrar_grafico_salsas(canvas):
    conexion = sqlite3.connect('ventas2.db')
    df = pd.read_sql_query("SELECT * FROM ventas", conexion)
    conexion.close()

    salsas_populares = df.groupby('Salsa')['Cantidad'].sum()

    colors = ['navajowhite', 'darkred', 'goldenrod', 'red', 'forestgreen']

    fig, ax = plt.subplots(figsize=(8, 6))
    salsas_populares.plot(kind='bar', color=colors, ax=ax)
    ax.set_title('Salsas Populares')
    ax.set_xticklabels(salsas_populares.index, rotation=50)
    
    canvas_fig = FigureCanvasTkAgg(fig, master=canvas)
    canvas_fig.draw()
    canvas_fig.get_tk_widget().place(x=10, width=1200, height=895)
    
# Función para mostrar el gráfico de ventas por mes
def mostrar_grafico_ventas_por_mes(canvas):
    conexion = sqlite3.connect('ventas2.db')
    df = pd.read_sql_query("SELECT * FROM ventas", conexion)
    conexion.close()

    # Agrupar por mes y sumar la cantidad
    ventas_por_mes = df.groupby('Mes')['Cantidad'].sum()

    fig, ax = plt.subplots(figsize=(8, 6))
    ventas_por_mes.plot(kind='bar', color='orange', ax=ax)
    ax.set_title('Ventas por Mes')
    ax.set_ylabel('Cantidad Vendida')
    ax.set_xticklabels(ventas_por_mes.index, rotation=45)

    canvas_fig = FigureCanvasTkAgg(fig, master=canvas)
    canvas_fig.draw()
    canvas_fig.get_tk_widget().place(x=10, width=1200, height=895)

# Función para mostrar el gráfico de ventas por día de la semana
def mostrar_grafico_ventas_por_dia(canvas):
    conexion = sqlite3.connect('ventas2.db')
    df = pd.read_sql_query("SELECT * FROM ventas", conexion)
    conexion.close()

    # Agrupar por día de la semana y sumar la cantidad
    ventas_por_dia = df.groupby('Dia de la semana')['Cantidad'].sum()

    fig, ax = plt.subplots(figsize=(8, 6))
    ventas_por_dia.plot(kind='bar', color='green', ax=ax)
    ax.set_title('Ventas por Día de la Semana')
    ax.set_ylabel('Cantidad Vendida')
    ax.set_xticklabels(ventas_por_dia.index, rotation=45)

    canvas_fig = FigureCanvasTkAgg(fig, master=canvas)
    canvas_fig.draw()
    canvas_fig.get_tk_widget().place(x=10, width=1200, height=895)

# Función para mostrar el gráfico de picos de venta por hora
def mostrar_grafico_picos_por_hora(canvas):
    conexion = sqlite3.connect('ventas2.db')
    df = pd.read_sql_query("SELECT * FROM ventas", conexion)
    conexion.close()

    df['Hora'] = pd.to_datetime(df['Hora'], format='%H:%M:%S').dt.hour

    # Agrupar por hora y sumar la cantidad
    ventas_por_hora = df.groupby('Hora')['Cantidad'].sum()

    fig, ax = plt.subplots(figsize=(8, 6))
    ventas_por_hora.plot(kind='line', color='red', marker='o', ax=ax)
    ax.set_title('Picos de Venta por Hora')
    ax.set_xlabel('Hora del Día')
    ax.set_xticks(range(8, 14))

    canvas_fig = FigureCanvasTkAgg(fig, master=canvas)
    canvas_fig.draw()
    canvas_fig.get_tk_widget().place(x=10, width=1200, height=895)
