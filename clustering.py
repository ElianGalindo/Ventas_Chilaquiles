# -*- coding: utf-8 -*-
"""
Created on Sun Oct  6 16:52:13 2024

@author: elian
"""

import tkinter as tk
from tkinter import ttk
import pandas as pd
import sqlite3
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def mostrar_clustering_sabores(canvas):
    for widget in canvas.winfo_children():
        widget.destroy()

    scroll_canvas = tk.Canvas(canvas)
    scrollbar = tk.Scrollbar(canvas, orient="vertical", command=scroll_canvas.yview)
    scroll_canvas.configure(yscrollcommand=scrollbar.set)

    frame_scrollable = tk.Frame(scroll_canvas)
    scroll_canvas.create_window((0, 0), window=frame_scrollable, anchor="nw")

    scrollbar.pack(side="right", fill="y")
    scroll_canvas.pack(side="left", fill="both", expand=True)

    conexion = sqlite3.connect('ventas2.db')
    query = """
    SELECT Telefono AS ID, Nombre, Sabor, SUM(Cantidad) AS Cantidad
    FROM ventas
    GROUP BY Telefono, Nombre, Sabor
    """
    df = pd.read_sql_query(query, conexion)
    conexion.close()

    pivot = df.pivot_table(index=['ID', 'Nombre'], columns='Sabor', values='Cantidad', aggfunc='sum', fill_value=0)

    scaler = StandardScaler()
    pivot_scaled = scaler.fit_transform(pivot)

    n_clusters = 5
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    pivot['Cluster'] = kmeans.fit_predict(pivot_scaled)

    notebook = ttk.Notebook(frame_scrollable)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    for cluster in range(n_clusters):
        cluster_frame = tk.Frame(notebook, bg="white")
        notebook.add(cluster_frame, text=f'Cluster {cluster}')

        cluster_data = pivot[pivot['Cluster'] == cluster].drop('Cluster', axis=1)

        clientes_texto = ""
        for id_telefono, nombre_cliente in cluster_data.index:
            clientes_texto += f"Teléfono: {id_telefono}, Nombre: {nombre_cliente}\n"

        # Identificar el sabor más popular en el cluster
        common_flavors = cluster_data.mean().idxmax()
        clientes_texto += f"\nSabor más popular en este cluster: {common_flavors}\n"

        # Buscar clientes que no hayan comprado el sabor más popular
        non_buyers = cluster_data[cluster_data[common_flavors] == 0]
        if non_buyers.empty:
            clientes_texto += "No hay clientes que necesiten recomendaciones.\n"
            # Encontrar el segundo sabor mas popular
            other_flavors = cluster_data.mean().nlargest(2).index.tolist()
            if common_flavors in other_flavors:
                other_flavors.remove(common_flavors) 
            
            if other_flavors:
                recommended_flavor = other_flavors[0]
                clientes_texto += f"Se recomienda probar el sabor: {recommended_flavor} a todos los clientes del cluster.\n"
        else:
            clientes_texto += "Clientes a los que se les recomendaría este sabor:\n"
            for id_telefono, nombre_cliente in non_buyers.index:
                clientes_texto += f"Teléfono: {id_telefono}, Nombre: {nombre_cliente}\n"
     
        label_cluster = tk.Label(cluster_frame, text=clientes_texto, justify="left", bg="white", anchor="nw")
        label_cluster.pack(fill="both", expand=True, padx=10, pady=10)
  
    frame_scrollable.update_idletasks()
    scroll_canvas.config(scrollregion=scroll_canvas.bbox("all"))
