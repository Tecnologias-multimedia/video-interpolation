# -*- coding: utf-8 -*-
import tkFileDialog
import ttk
from Ventana import Frame
from OpticalFlow import FlujoOptico
from Tkinter import PhotoImage


# Metodo que permite abrir un fichero.
def abrir_fichero():
    ventana.filename = tkFileDialog.askopenfilename(title="Seleccione un video",
                                                    filetypes=(("Archivos avi", "*.avi"), ("Todos", "*.*")))

    flujo.cambiar_ruta(ventana.filename)
    flujo.capturar()


# Metodo que permite guardar un fichero.
def guardar_fichero():
    ventana.filename = tkFileDialog.asksaveasfilename(title="Seleccione ubicación",
                                                      filetypes=(("Archivo avi", "avi"), ("Todos", "*.*")))

    btnProcesar['state'] = 'normal'
    flujo.ruta_guardar_archivo(ventana.filename)


# Metodo que procesa el video
def procesar_fichero():
    # Parametros para la deteccion de esquinas
    flujo.parametros_detector(100, 0.3, 7, 7)
    flujo.parametros_exportar()
    flujo.aplicar_filtro()


# Se crea un objeto de tipo Frame la cual contiene la ventana principal
ventana = Frame(800, 400)
flujo = FlujoOptico("")
cont = 0

# Creamos los label como titulo de la aplicacion y los autores.
titulo = ttk.Label(ventana.window, text="Interpolación de imágenes en video")
titulo.config(font=("Calibri", 25))  # Se ajusta el tipo de fuente y el tamaño de fuente.
autores = ttk.Label(ventana.window, text="Antonio Navarro Duarte | Jesús Pérez Escámez | Juan José Camacho Hidalgo")

# Logo de la ual.
img = PhotoImage(file='static/logo.gif')
logo = ttk.Label(ventana.window, image=img)
logo.place(x=20, y=240)

# Creamos los botones
btnLoad = ttk.Button(ventana.window, text="Cargar archivo", command=abrir_fichero)
btnExp = ttk.Button(ventana.window, text="Exportar archivo", command=guardar_fichero)
btnProcesar = ttk.Button(ventana.window, text="Procesar video", command=procesar_fichero)
btnProcesar['state'] = 'disabled'  # Primero estara desactivado hasta que el usuario escoja donde exportarlo


# Le damos una posición a los botones en la ventana.
btnLoad.place(x=73, y=60, width=120, height=25)
btnProcesar.place(x=339, y=60, width=120, height=25)
btnExp.place(x=605, y=60, width=120, height=25)

# Añadimos los label a la ventana
titulo.pack()
autores.place(x=330, y=375)

ventana.bucle_ventana()  # Se mantiene en bucle hasta que el usuario cierre la ventana.
