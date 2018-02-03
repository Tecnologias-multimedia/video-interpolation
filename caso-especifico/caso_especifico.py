# -*- coding: utf-8 -*-
import numpy as np
import cv2


# Metodo que calcula las coordenadas del rectangulo intermedio.
def calcular_intermedio(before, after):
    p3 = np.zeros_like(before)  # Se crea un matriz igual al parametro
    i = 0
    j = 0
    k = 0

    while k < len(before):
        while i < len(before[0]):
            while j < len(before[0][0]):
                num_after = int(round(after[k][i][j]))
                num_before = int(round(before[k][i][j]))

                p3[k][i][j] = ((num_after - num_before) / 2) + num_before

                j = j + 1
            i = i + 1
            j = 0
        k = k + 1
        i = 0

    return p3


# Metodo que se encarga de pintar el frame nuevo.
def pintar_nuevo_frame(before_frame, after_frame, p0, p1, p3):
    i = 0
    k = 0
    frame_nuevo = np.zeros_like(before_frame)
    ptoArrIzqX = p3[3][0][0]
    ptoArrIzqY = p3[3][0][1]
    ptoArrDerX = p3[2][0][0]
    ptoAbjDerY = p3[0][0][1]

    while k < len(before_frame):
        while i < len(before_frame[0]):
            if i >= ptoArrIzqX and k >= ptoArrIzqY and i < ptoArrDerX and k < ptoAbjDerY:
                frame_nuevo[k][i] = [255,0,0]
            else:
                frame_nuevo[k][i] = [0,0,255]

            i = i + 1
        k = k + 1
        i = 0

    return frame_nuevo


# Parametros para la detección de esquinas (ShiTomasi)
feature_params = dict( maxCorners = 100,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 3 )

# Parametros para el Lucas Kanade optical Flow
lk_params = dict( winSize  = (15,15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Creamos unos cuantos colores de forma aleatoria
color = np.random.randint(0,255,(100,3))

# Toma el primer frame y encuentra las esquinas.
old_frame = cv2.imread("1.png")
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)

# Crea una mascara donde se dibujara los vectores
mask = np.zeros_like(old_frame)
cont = 2
while cont<8:
    nom = str(cont)+".png"

    frame = cv2.imread(nom)
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # calculate optical flow
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

    # Calculamos la posicion del rectangulo intermedio
    pi = calcular_intermedio(p0, p1)

    # Pintamos el nuevo frame
    frame_int = pintar_nuevo_frame(old_frame, frame, p0, p1, pi)

    # Seleccionamos solo los puntos que no tengan error.
    good_new = p1[st == 1]
    good_old = p0[st == 1]

    cv2.imwrite("Imagenes-intermedias/resInt"+nom, frame_int)
    cont = cont + 1

    # Por último actualizamos el anterior frame y los anteriores puntos
    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1, 1, 2)
    old_frame = frame.copy()
