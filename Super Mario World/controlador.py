import cv2
import mediapipe as mp
import math
import numpy as np


class HandController:
    def __init__(self):
        # Inicialización de MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5,
        )
        self.cap = cv2.VideoCapture(0)
        self.drawing_utils = mp.solutions.drawing_utils

        # Zonas de botones (áreas de interacción en pantalla (0.0 a 1.0))
        self.btn_left_area = (0.0, 0.15)
        self.btn_right_area = (0.85, 1.0)

        # Variables de control de cámara (Estado interno)
        self.target_radio = 24.0
        self.target_angulo = 0.0
        self.target_altura = 16.0
        self.last_zoom_dist = -1

    def dibujar_ui(self, frame, active_left, active_right, mode_text):
        """Dibuja la interfaz superpuesta (HUD) en el feed de la cámara."""
        h, w, _ = frame.shape
        overlay = frame.copy()
        color_ok = (0, 255, 0)
        color_act = (0, 0, 255)

        # UI Visual
        cv2.rectangle(
            overlay,
            (0, 0),
            (int(w * 0.15), h),
            color_act if active_left else color_ok,
            -1 if active_left else 2,
        )
        cv2.rectangle(
            overlay,
            (int(w * 0.85), 0),
            (w, h),
            color_act if active_right else color_ok,
            -1 if active_right else 2,
        )

        # Etiquetas de texto
        cv2.putText(
            overlay,
            "< GIRAR",
            (10, h // 2),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 0),
            2,
        )
        cv2.putText(
            overlay,
            "GIRAR >",
            (w - 110, h // 2),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 0),
            2,
        )
        cv2.putText(
            overlay,
            mode_text,
            (w // 2 - 100, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            # Cyan color
            (255, 255, 0),
            2,
        )

        # Mezcla alfa para transparencia
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        return frame

    def procesar(self):
        """Procesa un frame de video, detecta manos y actualiza variables de control."""
        ret, frame = self.cap.read()
        if not ret:
            return None

        # Preprocesamiento de imagen
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)

        mode_text = "ESPERANDO..."
        active_left = False
        active_right = False

        if results.multi_hand_landmarks:
            for hl in results.multi_hand_landmarks:
                self.drawing_utils.draw_landmarks(
                    frame, hl, self.mp_hands.HAND_CONNECTIONS
                )

            # Lógica: Zoom (Dos manos detectadas)
            if len(results.multi_hand_landmarks) == 2:
                mode_text = "MODO: ZOOM"
                h1 = results.multi_hand_landmarks[0].landmark[8]
                h2 = results.multi_hand_landmarks[1].landmark[8]
                dist = math.sqrt((h1.x - h2.x) ** 2 + (h1.y - h2.y) ** 2)

                if self.last_zoom_dist != -1:
                    delta = abs(dist - self.last_zoom_dist)
                    if delta < 0.15:
                        # Actualizamos el estado interno
                        self.target_radio = 1.0 + (dist * 45.0)
                self.last_zoom_dist = dist

            # Lógica: Rotación y Altura (Una mano detectada)
            elif len(results.multi_hand_landmarks) == 1:
                mode_text = "MODO: ROTAR"
                self.last_zoom_dist = -1
                dedo = results.multi_hand_landmarks[0].landmark[8]

                # Control horizontal (Rotación)
                if dedo.x < self.btn_left_area[1]:
                    active_left = True
                    self.target_angulo -= 0.05
                elif dedo.x > self.btn_right_area[0]:
                    active_right = True
                    self.target_angulo += 0.05

                # Control vertical (Altura)
                if 0.2 < dedo.x < 0.8:
                    self.target_altura = 5.0 + ((1.0 - dedo.y) * 20.0)
        else:
            self.last_zoom_dist = -1

        frame = self.dibujar_ui(frame, active_left, active_right, mode_text)
        return frame

    def cerrar(self):
        self.cap.release()
