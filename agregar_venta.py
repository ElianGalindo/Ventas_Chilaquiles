# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 21:59:13 2024

@author: elian
"""
import sqlite3
from tkinter import messagebox
import tkinter as tk
from datetime import datetime
import inventario


def conectar_db():
    return sqlite3.connect('ventas2.db')

# Función para agregar una nueva venta
def agregar_nueva_venta(contenido_frame):
    for widget in contenido_frame.winfo_children():
        widget.destroy()
    form_frame = tk.Frame(contenido_frame, width=100, bg='gold')
    form_frame.place(x=500, y=200)

    tk.Label(form_frame, text="Teléfono", font=("Arial", 12, "bold"), background='gold').grid(row=0, column=0)
    tk.Label(form_frame, text="Nombre", font=("Arial", 12, "bold"), background='gold').grid(row=1, column=0)
    telefono_entry = tk.Entry(form_frame, width=50)
    nombre_entry = tk.Entry(form_frame, width=50)
    telefono_entry.grid(row=0, column=1)
    nombre_entry.grid(row=1, column=1)

    cajas_frame = tk.Frame(form_frame, bg="gold")
    cajas_frame.grid(row=2, column=0, columnspan=2, pady=10)

    # Lista para almacenar configuraciones de cada caja
    configuraciones_cajas = []

    # Precios según el sabor
    precios = {
        'campechanos': 90,
        'bistec': 80,
        'chicharron': 80,
        'chorizo': 80,
        'pollo': 80,
        'carnitas': 80,
        'queso': 75
    }

    # Función para agregar una nueva caja con opciones de sabor y toppings
    def agregar_caja():
        caja_frame = tk.Frame(cajas_frame, bg='white', relief="ridge", bd=2)
        caja_frame.pack(fill="x", pady=5)

        # Menú desplegable para sabor
        tk.Label(caja_frame, text="Sabor:", bg="white").grid(row=0, column=0)
        sabor_var = tk.StringVar()
        sabores = ['campechanos', 'bistec', 'chicharron', 'chorizo', 'pollo', 'carnitas', 'queso']
        sabor_menu = tk.OptionMenu(caja_frame, sabor_var, *sabores)
        sabor_menu.grid(row=0, column=1)

        # Menú desplegable para salsa
        tk.Label(caja_frame, text="Salsa:", bg="white").grid(row=1, column=0)
        salsa_var = tk.StringVar()
        salsas = ['Habanero', 'Chipotle', 'Verde', 'Roja', 'Guajillo']
        salsa_menu = tk.OptionMenu(caja_frame, salsa_var, *salsas)
        salsa_menu.grid(row=1, column=1)

        # Menús desplegables para queso, crema, frijoles, y cebolla
        toppings = {
            "Queso": tk.StringVar(),
            "Crema": tk.StringVar(),
            "Frijoles": tk.StringVar(),
            "Cebolla": tk.StringVar()
        }
        opciones = ['Si', 'No']
        for i, (topping, var) in enumerate(toppings.items(), start=2):
            tk.Label(caja_frame, text=topping + ":", bg="white").grid(row=i, column=0)
            menu = tk.OptionMenu(caja_frame, var, *opciones)
            menu.grid(row=i, column=1)

        tk.Label(caja_frame, text="Cantidad:", bg="white").grid(row=6, column=0)
        cantidad_entry = tk.Entry(caja_frame, width=10)
        cantidad_entry.insert(0, "1")  # Valor predeterminado de 1
        cantidad_entry.grid(row=6, column=1)

        tk.Label(caja_frame, text="Precio:", bg="white").grid(row=7, column=0)
        precio_entry = tk.Entry(caja_frame, width=10)
        precio_entry.grid(row=7, column=1)

        # Función para actualizar el precio automáticamente según el sabor y cantidad
        def actualizar_precio(*args):
            sabor_seleccionado = sabor_var.get()
            cantidad_seleccionada = cantidad_entry.get()
            try:
                cantidad = int(cantidad_seleccionada) if cantidad_seleccionada else 1
            except ValueError:
                cantidad = 1
            if sabor_seleccionado in precios:
                precio_total = precios[sabor_seleccionado] * cantidad
                precio_entry.delete(0, tk.END)
                precio_entry.insert(0, str(precio_total))

        sabor_var.trace("w", actualizar_precio)
        cantidad_entry.bind("<KeyRelease>", actualizar_precio)

        configuraciones_cajas.append({
            "sabor": sabor_var,
            "salsa": salsa_var,
            "toppings": toppings,
            "cantidad": cantidad_entry,
            "precio": precio_entry,
            "frame": caja_frame 
        })

        # Botón para eliminar la caja
        eliminar_boton = tk.Button(caja_frame, text="Eliminar", command=lambda: eliminar_caja(caja_frame))
        eliminar_boton.grid(row=0, column=2)

    # Función para eliminar una caja
    def eliminar_caja(caja):
        caja.destroy()
        configuraciones_cajas.remove(next(config for config in configuraciones_cajas if config["frame"] == caja))

    # Botón para agregar una nueva caja
    tk.Button(form_frame, text="Agregar Caja", command=agregar_caja, bg='orange').grid(row=3, columnspan=2, pady=10)

    # Función para guardar todas las cajas en la base de datos
    def guardar_venta():
        telefono = telefono_entry.get()
        nombre = nombre_entry.get()

        if not telefono or not nombre:
            messagebox.showwarning("Advertencia", "Por favor, completa todos los campos.")
            return

        # Obtener la fecha y hora actuales
        now = datetime.now()
        fecha = now.strftime("%Y-%m-%d")
        hora = now.strftime("%H:%M:%S")
        dias_semana = {0: "lunes", 1: "martes", 2: "miércoles", 3: "jueves", 4: "viernes", 5: "sábado", 6: "domingo"}
        meses = {1: "enero", 2: "febrero", 3: "marzo", 4: "abril", 5: "mayo", 6: "junio",
                 7: "julio", 8: "agosto", 9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"}
        dia_semana = dias_semana[now.weekday()]
        mes = meses[now.month]

        # Conectar a la base de datos
        try:
            conexion = conectar_db()
            cursor = conexion.cursor()

            for config in configuraciones_cajas:
                try:
                    cantidad = int(config["cantidad"].get())
                    precio = float(config["precio"].get())
                except ValueError:
                    messagebox.showwarning("Advertencia", "Por favor, ingrese valores válidos para cantidad y precio.")
                    return

                sabor = config["sabor"].get()
                salsa = config["salsa"].get()
                queso = config["toppings"]["Queso"].get()
                crema = config["toppings"]["Crema"].get()
                frijoles = config["toppings"]["Frijoles"].get()
                cebolla = config["toppings"]["Cebolla"].get()

                if telefono and nombre and sabor and salsa and queso and crema and frijoles and cebolla and cantidad and precio:
                    print(f"Guardando venta: {telefono}, {nombre}, {sabor}, {salsa}, {queso}, {crema}, {frijoles}, {cebolla}, {cantidad}, {precio}, {fecha}, {dia_semana}, {mes}, {hora}")
    
                    cursor.execute('''INSERT INTO ventas (Telefono, Nombre, Sabor, Salsa, Queso, Crema, Frijoles, Cebolla, Cantidad, Precio, Fecha, "Dia de la semana", Mes, Hora, "Horas Redo.")
                                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                                   (telefono, nombre, sabor, salsa, queso, crema, frijoles, cebolla, cantidad, precio, fecha, dia_semana, mes, hora, None))

            conexion.commit()
            conexion.close()

            # Limpiar los campos después de guardar
            telefono_entry.delete(0, tk.END)
            nombre_entry.delete(0, tk.END)
            for config in configuraciones_cajas:
                config["sabor"].set('')
                config["salsa"].set('')
                for topping in config["toppings"].values():
                    topping.set('')
                config["cantidad"].delete(0, tk.END)
                config["cantidad"].insert(0, "1")
                config["precio"].delete(0, tk.END)

            messagebox.showinfo("Éxito", "La venta ha sido agregada con éxito.")
            for widget in cajas_frame.winfo_children():
                widget.destroy()
            configuraciones_cajas.clear()
            agregar_nueva_venta(contenido_frame)
            inventario.actualizar_inventario(sabor, salsa, frijoles, cebolla, queso, crema, cantidad)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Ocurrió un error con la base de datos: {e}")
        finally:
            if conexion:
                conexion.close()

    # Botón para guardar la venta
    tk.Button(form_frame, text="Guardar Venta", command=guardar_venta, bg='green').grid(row=8, columnspan=2, pady=10)
