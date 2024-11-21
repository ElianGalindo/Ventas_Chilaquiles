# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 16:06:02 2024

@author: elian
"""
# ventas.py
import pandas as pd
import sqlite3
from tkinter import ttk, Scrollbar, Frame, Entry, Button, VERTICAL, HORIZONTAL

def conectar_db():
    return sqlite3.connect('ventas2.db')

def mostrar_datos_ventas(contenido_frame):
    search_frame = Frame(contenido_frame)
    search_frame.pack(fill="x")

    search_entry = Entry(search_frame, width=30)
    search_entry.pack(side="left", padx=5)
    search_button = Button(search_frame, text="Buscar", command=lambda: actualizar_datos(search_entry.get()))
    search_button.pack(side="left")

    tree_frame = Frame(contenido_frame)
    tree_frame.pack(fill="both", expand=True)

    tree = ttk.Treeview(tree_frame, selectmode="browse")
    scrollbar_y = Scrollbar(tree_frame, orient=VERTICAL, command=tree.yview)
    scrollbar_x = Scrollbar(tree_frame, orient=HORIZONTAL, command=tree.xview)

    tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    tree.grid(row=0, column=0, sticky="nsew")
    scrollbar_y.grid(row=0, column=1, sticky="ns")
    scrollbar_x.grid(row=1, column=0, sticky="ew")

    tree_frame.grid_rowconfigure(0, weight=1)
    tree_frame.grid_columnconfigure(0, weight=1)

    # Función para actualizar datos en el Treeview con el filtro
    def actualizar_datos(filtro=""):
        conexion = conectar_db()

        if filtro:
            query = f"""
                SELECT Telefono AS ID, Nombre, Sabor, Fecha, "Dia de la semana", Mes, Hora, Precio, Salsa, Queso, Crema, Frijoles, Cebolla, SUM(Cantidad) AS Cantidad
                FROM ventas
                WHERE Nombre LIKE '%{filtro}%' OR Telefono LIKE '%{filtro}%'
                GROUP BY Telefono, Nombre, Sabor, Fecha, "Dia de la semana", Mes, Hora, Precio, Cantidad, Salsa, Queso, Crema, Frijoles, Cebolla
                ORDER BY Fecha
            """
        else:
            query = """
                SELECT Telefono AS ID, Nombre, Sabor, Fecha, "Dia de la semana", Mes, Hora, Precio, Salsa, Queso, Crema, Frijoles, Cebolla, SUM(Cantidad) AS Cantidad
                FROM ventas
                GROUP BY Telefono, Nombre, Sabor, Fecha, "Dia de la semana", Mes, Hora, Precio, Cantidad, Salsa, Queso, Crema, Frijoles, Cebolla
                ORDER BY Fecha
            """

        df_ventas = pd.read_sql_query(query, conexion)
        conexion.close()

        tree["columns"] = list(df_ventas.columns)
        tree["show"] = "headings"
        
        for column in df_ventas.columns:
            tree.heading(column, text=column)
            tree.column(column, anchor="center", width=100)  
        
        tree.delete(*tree.get_children())
        for _, row in df_ventas.iterrows():
            tree.insert("", "end", values=list(row))

    actualizar_datos()

    # Actualizar datos automáticamente cuando se borra el contenido del campo de búsqueda
    search_entry.bind("<KeyRelease>", lambda event: actualizar_datos(search_entry.get()))
