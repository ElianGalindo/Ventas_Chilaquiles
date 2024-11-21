# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 15:30:17 2024

@author: elian
"""
import tkinter as tk
from tkinter import ttk
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


nltk.download('vader_lexicon')


df = pd.read_excel('C:/Users/elian/OneDrive/Documentos/9na inscripcion/Mineria de datos/GUI/reseñas.xlsx')

analyzer = SentimentIntensityAnalyzer()


def obtener_sentimiento_vader(texto):
    scores = analyzer.polarity_scores(texto)
    if scores['compound'] > 0:
        return 'Positivo'
    elif scores['compound'] < 0:
        return 'Negativo'
    else:
        return 'Positivo' if scores['compound'] >= 0 else 'Negativo'


df['Sentimiento'] = df['Comentario'].apply(obtener_sentimiento_vader)

# Filtrar los comentarios por tipo
comentarios_positivos = df[df['Sentimiento'] == 'Positivo']
comentarios_negativos = df[df['Sentimiento'] == 'Negativo']

#palabras clave
palabras_clave = ['sabor', 'salsa', 'sabrosos', 'ricos', 'salsas']

# Buscar palabras clave en los comentarios
comentarios_por_palabra = {palabra: [] for palabra in palabras_clave}
for palabra in palabras_clave:
    for index, row in df.iterrows():
        if palabra in row['Comentario'].lower():
            comentarios_por_palabra[palabra].append(row['Comentario'])


def mostrar_analisis_sentimientos(canvas):

    for widget in canvas.winfo_children():
        widget.destroy()
        
    notebook = ttk.Notebook(canvas)
    notebook.pack(fill="both", expand=True)

    # Pestaña 1: Todos los comentarios
    frame_todos = tk.Frame(notebook, bg="white")
    notebook.add(frame_todos, text="Todos los comentarios")
    mostrar_comentarios_en_frame(frame_todos, df['Comentario'])

    # Pestaña 2: Comentarios positivos
    frame_positivos = tk.Frame(notebook, bg="white")
    notebook.add(frame_positivos, text="Comentarios Positivos")
    mostrar_comentarios_en_frame(frame_positivos, comentarios_positivos['Comentario'])

    # Pestaña 3: Comentarios negativos
    frame_negativos = tk.Frame(notebook, bg="white")
    notebook.add(frame_negativos, text="Comentarios Negativos")
    mostrar_comentarios_en_frame(frame_negativos, comentarios_negativos['Comentario'])

    # Pestaña 4: Comentarios con palabras clave
    frame_palabras = tk.Frame(notebook, bg="white")
    notebook.add(frame_palabras, text="Comentarios por Palabra Clave")
    mostrar_comentarios_palabras_clave(frame_palabras, comentarios_por_palabra)


def mostrar_comentarios_en_frame(frame, comentarios):
    canvas_frame = tk.Canvas(frame)
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas_frame.yview)
    canvas_frame.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas_frame.pack(side="left", fill="both", expand=True)

    contenido_frame = tk.Frame(canvas_frame)
    canvas_frame.create_window((0, 0), window=contenido_frame, anchor="nw")

    def ajustar_scroll(event):
        canvas_frame.configure(scrollregion=canvas_frame.bbox("all"))
    contenido_frame.bind("<Configure>", ajustar_scroll)

    for comentario in comentarios:
        label = tk.Label(contenido_frame, text=comentario, wraplength=600, bg="white", justify="left", anchor="nw")
        label.pack(fill="both", padx=10, pady=5)

# Función para mostrar comentarios por palabras clave
def mostrar_comentarios_palabras_clave(frame, comentarios_por_palabra):
    for palabra, comentarios in comentarios_por_palabra.items():
        label_palabra = tk.Label(frame, text=f"Comentarios que contienen '{palabra}':", bg="white", anchor="w", font=("Arial", 10, "bold"))
        label_palabra.pack(fill="both", padx=10, pady=5)

        if comentarios:
            for comentario in comentarios:
                label_comentario = tk.Label(frame, text=comentario, wraplength=600, bg="white", justify="left", anchor="nw")
                label_comentario.pack(fill="both", padx=10, pady=2)
        else:
            label_no_comentario = tk.Label(frame, text="No hay comentarios que contengan esta palabra clave.", bg="white", justify="left")
            label_no_comentario.pack(fill="both", padx=10, pady=2)



