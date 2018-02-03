# -*- coding: utf-8 -*-
import Tkinter


class Frame:
    window = Tkinter.Tk()  # Crea una ventana Tk root.
    filename = ""

    def __init__(self, ancho, alto):
        # Damos un nombre al titulo de la ventana.
        self.window.title("Optical Flow")

        # Obtenemos el ancho y alto de la pantalla.
        ancho_pant = self.window.winfo_screenwidth()  # Ancho de la pantalla.
        alto_pant = self.window.winfo_screenheight()  # Altura de la pantalla.

        # Calculamos las coordenas (x e y) para establecer la posicion de la pantalla.
        x = (ancho_pant / 2) - (ancho / 2)
        y = (alto_pant / 2) - (alto / 2)

        # Establecemos las dimensiones de la pantalla y lo colocamos.
        self.window.geometry('%dx%d+%d+%d' % (ancho, alto, x, y))

    def bucle_ventana(self):
        self.window.mainloop()
