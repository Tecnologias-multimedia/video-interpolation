# -*- coding: utf-8 -*-
import numpy as np
import cv2


class FlujoOptico:
    # Ruta donde se encuentra el archivo de video
    rutaOpen = ""
    # Parametros para el ShiTomasi
    feature_params = ""
    # Parametros para el optical flow
    lk_params = dict(winSize=(15, 15),
                     maxLevel=2,
                     criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
    # Captura de video original
    cap = ""
    # Captura de video de salida
    out = ""
    # Ruta del archivo de salida
    rutaSave = ""

    # Creamos unos colores aleatorios para los puntos y lineas.
    color = np.random.randint(0, 255, (100, 3))

    def __init__(self, path):
        self.rutaOpen = path

    # Metodo para empezar a capturar el video.
    def capturar(self):
        self.cap = cv2.VideoCapture(self.rutaOpen)

    # Metodo que cambia la ruta del archivo.
    def cambiar_ruta(self, path):
        self.rutaOpen = path

    # Metodo para salvar el archivo
    def ruta_guardar_archivo(self, path):
        self.rutaSave = path

    # Metodo que configura los parametros del archivo a exportar
    def parametros_exportar(self):
        # Se define el codec y se crea un objeto VideoWriter
        fourcc = cv2.VideoWriter_fourcc(*'XVID')

        # Obtenemos el ancho y alto del video original
        width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        # Abrimos un flujo donde se guardara el video
        self.out = cv2.VideoWriter(self.rutaSave, fourcc, 30, (int(width), int(height)))

    # Metodo que define los parametros necesarios para el algoritmo de detección de esquinas (ShiTomasi)
    def parametros_detector(self, max_corner, quality_level, min_distance, block_size):
        self.feature_params = dict(maxCorners=max_corner,
                                   qualityLevel=quality_level,
                                   minDistance=min_distance,
                                   blockSize=block_size)

    def aplicar_filtro(self):
        # Primero comprobamos si el cap esta abierto
        if not self.cap.isOpened():
            self.cap = cv2.VideoCapture(self.rutaOpen)

        # Tomamos el primer frame del video
        ret, old_frame = self.cap.read()

        # Convertimos el frame de RGB a blanco y negro
        old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)

        # Encontramos las esquinas del frame con el algoritmo de ShiTomasi
        p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **self.feature_params)

        # Creamos una mascara donde se dibujaran los puntos y el seguimiento de estos.
        mask = np.zeros_like(old_frame)

        # Ahora empezamos a recorrer los siguientes frames del video
        while True:
            # Capturamos un frame del video
            ret, frame = self.cap.read()

            # Si ocurre algún error al leer el frame paramos el bucle.
            if not ret:
                break

            # Convertimos el frame leido de RGB una escala de grises
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Calculamos el flujo optico entre el primer frame que hemos leido y este último
            p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **self.lk_params)

            # Seleccionamos solo los buenos puntos.
            good_new = p1[st == 1]
            good_old = p0[st == 1]

            # Dibujamos el camino que une los puntos (seguimiento del movimiento)
            for i, (new, old) in enumerate(zip(good_new, good_old)):
                a, b = new.ravel()
                c, d = old.ravel()
                mask = cv2.line(mask, (a, b), (c, d), self.color[i].tolist(), 2)
                frame = cv2.circle(frame, (a, b), 5, self.color[i].tolist(), -1)

            # Guardamos la nueva imagen generada y la mostramos
            img = cv2.add(frame, mask)
            cv2.imshow("Previsualizacion", img)

            # Guardamos el frame en el archivo
            self.out.write(img)

            # Definimos como parar el proceso.
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break

            # Por último actualizamos el frame anterior por el nuevo y los anteriores puntos por los nuevos
            old_gray = frame_gray.copy()
            p0 = good_new.reshape(-1, 1, 2)

        # Destruimos todas las ventanas
        cv2.destroyAllWindows()
        self.cap.release()
        self.out.release()
