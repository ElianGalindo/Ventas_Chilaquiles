# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 16:37:36 2024

@author: elian
"""

import sqlite3
import pandas as pd
from tkinter import ttk
from tkinter import messagebox
import tkinter as tk
from tkinter.ttk import Progressbar
from tkinter import Frame

# Actualizar el inventario al realizar una venta
def actualizar_inventario(sabor, salsa, frijoles, cebolla, queso, crema, cantidad):
    conexion = sqlite3.connect("ventas2.db")
    cursor = conexion.cursor()

    try:
        
        # Actualizar la salsa
        salsa_por_caja = 5 / 200  # 5 litros para 200 cajas
        cursor.execute(
            "UPDATE inventario SET cantidad = cantidad - ? WHERE nombre = ?",
            (salsa_por_caja * cantidad, 'Salsa ' + salsa)
        )

        # Actualizar las bolsas de chilaquiles
        bolsas_por_caja = 1 / 7  # 1 bolsa para 7 cajas
        cursor.execute(
            "UPDATE inventario SET cantidad = cantidad - ? WHERE nombre = ?",
            (bolsas_por_caja * cantidad, 'Bolsas de ' + sabor)
        )
        if frijoles == "Si":
           frijoles_por_caja = 0.1  #0.1 litros de frijoles por caja
           cursor.execute(
               "UPDATE inventario SET cantidad = cantidad - ? WHERE nombre = ?",
               (frijoles_por_caja * cantidad, "Frijoles")
           )

        if cebolla == "Si":
            cebolla_por_caja = 0.03  #0.02 kilos de cebolla por caja
            cursor.execute(
               "UPDATE inventario SET cantidad = cantidad - ? WHERE nombre = ?",
               (cebolla_por_caja * cantidad, "Cebolla")
           )

        if queso == "Si":
            queso_por_caja = 0.03  #0.03 kilos de queso por caja
            cursor.execute(
                "UPDATE inventario SET cantidad = cantidad - ? WHERE nombre = ?",
                (queso_por_caja * cantidad, "Queso")
         )
            
        if crema == "Si":
            queso_por_caja = 0.03  #0.03 kilos de queso por caja
            cursor.execute(
                "UPDATE inventario SET cantidad = cantidad - ? WHERE nombre = ?",
                (queso_por_caja * cantidad, "Queso")
         )
            

        conexion.commit()
    except Exception as e:
        print("Error al actualizar el inventario:", e)
    finally:
        conexion.close()
        
def limpiar_frame(contenido_frame):
    for widget in contenido_frame.winfo_children():
        widget.destroy()

def mostrar_inventario(contenido_frame):
    limpiar_frame(contenido_frame)

    notebook = ttk.Notebook(contenido_frame)
    notebook.place(x=100, y=10, width=1300, height=925)
    
    listado_frame = tk.Frame(notebook, bg="white smoke")
    progreso_frame = tk.Frame(notebook, bg="white smoke")
    actualizar_frame = tk.Frame(notebook, bg="white smoke")

    notebook.add(listado_frame, text='Listado de Productos')
    notebook.add(progreso_frame, text='Cantidad Restante')
    notebook.add(actualizar_frame, text='Actualizar Inventario')
    
    def actualizar_pestana(event):
        pestaña_seleccionada = notebook.index(notebook.select())
        if pestaña_seleccionada == 0:
            limpiar_frame(listado_frame)
            mostrar_listado_productos(listado_frame)
        elif pestaña_seleccionada == 1: 
            limpiar_frame(progreso_frame)
            mostrar_barras_progreso(progreso_frame)
        elif pestaña_seleccionada == 2:
            limpiar_frame(actualizar_frame)
            formulario_actualizar_inventario(actualizar_frame)

    notebook.bind("<<NotebookTabChanged>>", actualizar_pestana)
    
    mostrar_listado_productos(listado_frame)
    mostrar_barras_progreso(progreso_frame)
    formulario_actualizar_inventario(actualizar_frame)


# Función para mostrar el listado de productos en un Treeview
def mostrar_listado_productos(frame):
    conexion = sqlite3.connect("ventas2.db")
    df_inventario = pd.read_sql_query(
        "SELECT nombre AS 'Producto', unidad AS 'Unidad', cantidad AS 'Cantidad Disponible' FROM inventario",
        conexion
    )
    conexion.close()

    tree_frame = Frame(frame)
    tree_frame.pack(fill="both", expand=True)

    columns = df_inventario.columns.tolist()
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
   
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")

    for _, row in df_inventario.iterrows():
        cantidad_disponible = row['Cantidad Disponible']
        cantidad_total = 20
        porcentaje = (cantidad_disponible/cantidad_total)*100
        tree.insert("", "end", values=(row['Producto'], row['Unidad'], f'{porcentaje:.2f}%'))
        
    tree.pack(fill="both", expand=True)
    def eliminar_producto():
        try:
            # Obtener el producto seleccionado
            selected_item = tree.selection()[0]
            producto = tree.item(selected_item)["values"][0] 

            # Confirmar la eliminación
            confirmar = messagebox.askyesno("Confirmar eliminación", f"¿Seguro que quieres eliminar el producto {producto}?")
            if confirmar:
                conexion = sqlite3.connect("ventas2.db")
                cursor = conexion.cursor()
                cursor.execute("DELETE FROM inventario WHERE nombre = ?", (producto,))
                conexion.commit()
                conexion.close()

                tree.delete(selected_item)
                messagebox.showinfo("Producto eliminado", f"El producto {producto} ha sido eliminado del inventario.")

        except IndexError:
            messagebox.showerror("Error", "Por favor, selecciona un producto para eliminar.")

    # Botón para eliminar producto
    eliminar_button = tk.Button(frame, text="Eliminar Producto", command=eliminar_producto, font=("Arial", 12), relief="raised")
    eliminar_button.pack(pady=20)

# Función para mostrar barras de progreso
def mostrar_barras_progreso(frame):
    canvas = tk.Canvas(frame)
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)
    frame_scrollable = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame_scrollable, anchor="nw")
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)


    conexion = sqlite3.connect("ventas2.db")
    df_inventario = pd.read_sql_query(
        "SELECT nombre AS 'Producto', cantidad AS 'Cantidad Disponible' FROM inventario",
        conexion
    )
    conexion.close()

    # Crear barras de progreso para cada producto
    column = 0
    row_num = 0
    for idx, row in df_inventario.iterrows(): 
        producto = row['Producto']  
        cantidad_disponible = row['Cantidad Disponible']
        max_cantidad = 20  # Cantidad en litros, kilos y bolsas
        
        # Etiqueta del producto
        label = tk.Label(frame_scrollable, text=producto, font=("Arial", 12))
        label.grid(row=row_num, column=column, padx=10, pady=40)
        
        # Barra de progreso
        progreso = Progressbar(frame_scrollable, orient="horizontal", length=300, mode="determinate")
        progreso["maximum"] = max_cantidad
        progreso["value"] = cantidad_disponible  
        progreso.grid(row=row_num + 1, column=column, padx=45, pady=2) 
        
        porcentaje = (cantidad_disponible/max_cantidad)*100
        # Etiqueta con la cantidad restante
        cantidad_label = tk.Label(frame_scrollable, text=f"Cantidad restante: {porcentaje:.2f}%", font=("Arial", 10))
        cantidad_label.grid(row=row_num + 2, column=column, padx=10, pady=5)
        
        column += 1
        if column > 2:
            column = 0
            row_num += 4

    frame_scrollable.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def formulario_actualizar_inventario(frame):
    def obtener_productos():
        conexion = sqlite3.connect("ventas2.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre FROM inventario")
        productos = [row[0] for row in cursor.fetchall()]
        conexion.close()
        return productos

    
    def actualizar_menu():
        productos = obtener_productos()
        menu = producto_var_menu['menu']
        menu.delete(0, 'end')
        for producto in productos:
            menu.add_command(label=producto, command=lambda value=producto: producto_var.set(value))
        producto_var.set(productos[0] if productos else "No hay productos")
    
    
    # Formulario para actualizar inventario
    actualizar_label = tk.Label(frame, text="Actualizar Inventario", font=("Arial", 14, "bold"),background='white smoke')
    actualizar_label.pack(pady=20)
    cantidad_mensaje_label = tk.Label(frame, text="Rellenar producto para completar stock (20 litros, bolsas, kilos, botellas)", font=("Arial", 12), background='white smoke')
    cantidad_mensaje_label.pack(pady=5)
    producto_label = tk.Label(frame, text="Producto:", font=("Arial", 12), background='white smoke')
    producto_label.pack(pady=5)
    
    producto_var = tk.StringVar(frame)
    productos = obtener_productos()
    producto_var.set(productos[0] if productos else "No hay productos")
    producto_var_menu = tk.OptionMenu(frame, producto_var, *productos)
    producto_var_menu.config(font=("Arial", 12))
    producto_var_menu.pack(pady=5)

   
    

    # Formulario para agregar nuevo producto
    agregar_label = tk.Label(frame, text="Agregar producto", font=("Arial", 14, "bold"),background='white smoke')
    agregar_label.pack(pady=20)

    nuevo_producto_label = tk.Label(frame, text="Producto:", font=("Arial", 12), background='white smoke')
    nuevo_producto_label.pack(pady=5)
    nuevo_producto_entry = tk.Entry(frame, font=("Arial", 12))
    nuevo_producto_entry.pack(pady=5)

    unidad_label = tk.Label(frame, text="Unidad:", font=("Arial", 12), background='white smoke')
    unidad_label.pack(pady=5)
    unidad_entry = tk.Entry(frame, font=("Arial", 12))
    unidad_entry.pack(pady=5)    
    
    
    def rellenar_inventario():
        producto = producto_var.get()
        cantidad = 20
    
        if producto and cantidad:
            conexion = sqlite3.connect("ventas2.db")
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM inventario WHERE nombre = ?", (producto,))
            producto_existente = cursor.fetchone()
    
            if producto_existente:
                cursor.execute("UPDATE inventario SET cantidad = ? WHERE nombre = ?", (cantidad, producto))
                messagebox.showinfo("Actualización exitosa", f"Se ha rellenado el producto {producto}.")
            
            conexion.commit()
            conexion.close()
            producto_var.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Por favor, ingrese un valor válido.")

    # Botón para actualizar el inventario
    actualizar_button = tk.Button(frame, text="Rellenar Producto", command=rellenar_inventario, font=("Arial", 12), relief="raised")
    actualizar_button.pack(pady=20)
    
    
    def agregar_producto():
        nuevo_producto = nuevo_producto_entry.get()
        unidad = unidad_entry.get()
        cantidad = "20"
    
        if nuevo_producto and unidad and cantidad.isdigit():
            cantidad = int(cantidad)
            conexion = sqlite3.connect("ventas2.db")
            cursor = conexion.cursor()
            cursor.execute("INSERT INTO inventario (nombre, unidad, cantidad) VALUES (?, ?, ?)", (nuevo_producto, unidad, cantidad))
            messagebox.showinfo("Producto agregado", f"{nuevo_producto} ha sido añadido al inventario.")
            conexion.commit()
            conexion.close()
            nuevo_producto_entry.delete(0, tk.END)
            unidad_entry.delete(0, tk.END)
            actualizar_menu()
    
    # Botón para agregar producto
    agregar_button = tk.Button(frame, text="Agregar Producto", command=agregar_producto, font=("Arial", 12), relief="raised")
    agregar_button.pack(pady=20)
    
    
