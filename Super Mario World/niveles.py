# niveles.py
import math
import random

import glfw
from assets import Assets
from config import *
from OpenGL.GL import *
from OpenGL.GLU import *


class Nivel:
    def configurar_camara(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, (WIDTH / HEIGHT), 0.1, 200.0)
        glMatrixMode(GL_MODELVIEW)

    def dibujar(self, tiempo):
        pass

    def input_teclado(self, key, action):
        pass


class NivelMundo(Nivel):
    def __init__(self):
        # Generamos posiciones estáticas para las nubes una sola vez
        self.nubes_pos = []
        for x in range(-60, 60, 15):
            for z in range(-60, 60, 15):
                # Variación aleatoria para que no se vea cuadriculado
                ox = random.uniform(-5, 5)
                oz = random.uniform(-5, 5)
                h = random.uniform(12, 18)  # Altura variada
                s = random.uniform(1.0, 2.0)  # Tamaño variado
                self.nubes_pos.append((x + ox, h, z + oz, s))

    def dibujar_cielo(self, tiempo):
        """Dibuja un campo de nubes distribuidas como el mar"""
        for x, y, z, s in self.nubes_pos:
            glPushMatrix()
            # Movimiento del viento constante
            desplazamiento = (tiempo * 1.0) % 120
            # Si se sale del mapa, vuelve al inicio (efecto infinito)
            pos_x = x + desplazamiento
            if pos_x > 60:
                pos_x -= 120

            glTranslatef(pos_x, y, z)
            Assets.dibujar_nube(scale=s)
            glPopMatrix()

    def dibujar_bandera_animada(self, x, y, z, tiempo):
        """Asta bandera con animación de subida/bajada"""
        glPushMatrix()
        glTranslatef(x, y, z)

        # 1. Base y Poste (Estáticos)
        glPushMatrix()
        glColor3f(0.70, 0.45, 0.20)  # Base Café
        glTranslatef(0, 0.2, 0)
        glScalef(0.6, 0.4, 0.6)
        glScalef(1.2, 1.2, 1.2)
        Assets.dibujar_cubo_solido()
        glPopMatrix()

        glPushMatrix()
        glColor3f(0, 1, 0)  # Poste Verde
        glRotatef(-90, 1, 0, 0)
        gluCylinder(Assets.quad, 0.08, 0.08, 4.0, 24, 1)
        glPopMatrix()

        glPushMatrix()
        glColor3f(0, 1, 0)  # Bola Top
        glTranslatef(0, 4.0, 0)
        gluSphere(Assets.quad, 0.15, 24, 24)
        glPopMatrix()

        # 2. Bandera Blanca (Animada)
        # Sube y baja suavemente entre altura 1.0 y 2.5
        altura_flag = 1.0 + (math.sin(tiempo * 1.5) + 1.0) * 1.3

        glPushMatrix()
        glColor3f(1, 1, 1)
        glTranslatef(0, altura_flag, 0)
        Assets.dibujar_bandera_triangular()
        glPopMatrix()

        glPopMatrix()

    def dibujar(self, tiempo):
        # 1. Mar y Cielo
        Assets.dibujar_mar_abierto(tiempo)
        self.dibujar_cielo(tiempo)

        # 2. Islas
        for i, isla in enumerate(DATA_ISLAS):
            w, d = isla["w"], isla["d"]
            y_suelo = NIVEL_MAR + isla["h_rel"]
            pos_y_isla = y_suelo - (20.0 / 2.0)

            # Espuma
            glPushMatrix()
            glTranslatef(isla["x"], NIVEL_MAR + 0.03, isla["z"])
            drift_x = 0.25 * math.sin(tiempo * 1.1 + isla["x"] * 0.5)
            drift_z = 0.25 * math.cos(tiempo * 1.3 + isla["z"] * 0.5)
            glTranslatef(drift_x, 0, drift_z)
            margen_dinamico = 1.3 + 0.35 * math.sin(tiempo * 2.5)
            glDisable(GL_LIGHTING)
            glColor3fv(C_ESPUMA_COSTA)
            Assets.dibujar_placa_espuma(
                w + margen_dinamico, d + margen_dinamico, RADIO_BORDE + 0.2
            )
            glEnable(GL_LIGHTING)
            glPopMatrix()

            # Cuerpo de la Isla
            glPushMatrix()
            glTranslatef(isla["x"], pos_y_isla, isla["z"])
            Assets.dibujar_isla_avanzada(w, 20.0, d)
            glPopMatrix()

            # =========================================================
            # ISLA 0: MARIO, TUBERIA, PLATAFORMA Y META
            # =========================================================
            if i == 0:
                # --- VARIABLES DE ANIMACIÓN ---
                walk_z = math.sin(tiempo * 2.5) * 1.5
                jump_cycle = math.sin(tiempo * 5.0)
                jump_y = 0.0
                if jump_cycle > 0.5:
                    jump_y = (jump_cycle - 0.5) * 2.0

                # Sombra Mario
                glPushMatrix()
                glTranslatef(isla["x"], y_suelo + 0.02, isla["z"] + walk_z)
                s_scale = 1.0 - (jump_y * 0.5)
                glScalef(s_scale, 1.0, s_scale)
                Assets.dibujar_sombra_redonda(0.6)
                glPopMatrix()

                # Mario
                glPushMatrix()
                glTranslatef(isla["x"], y_suelo + jump_y, isla["z"] + walk_z)
                if math.cos(tiempo * 2.5) > 0:
                    glRotatef(0, 0, 1, 0)
                else:
                    glRotatef(180, 0, 1, 0)
                Assets.dibujar_mario()
                glPopMatrix()

                # Tuberia
                glPushMatrix()
                glTranslatef(isla["x"], y_suelo, isla["z"] - 1.6)
                Assets.dibujar_sombra_redonda(0.8)
                Assets.dibujar_tuberia(height=1.0)
                glPopMatrix()

                # Plataforma
                glPushMatrix()
                glTranslatef(isla["x"], y_suelo + 0.1, isla["z"] + 1.5)
                Assets.dibujar_sombra_redonda(0.5)
                glScalef(0.3, 0.3, 0.3)
                Assets.dibujar_plataforma_mario()
                glPopMatrix()

                # Bloque Random (Donde Mario salta)
                glPushMatrix()
                flote_cubo = math.sin(tiempo * 3) * 0.2
                glTranslatef(isla["x"], y_suelo + 2.0 + flote_cubo, isla["z"])
                glRotatef(tiempo * 100, 0, 1, 0)  # Girando

                # Sombra proyectada
                glPushMatrix()
                glTranslatef(0, -(2.0 + flote_cubo) + 0.02, 0)
                Assets.dibujar_sombra_redonda(0.5)
                glPopMatrix()

                Assets.dibujar_bloque_random()
                glPopMatrix()

                # Estrella
                glPushMatrix()
                glTranslatef(isla["x"] + 2.0, y_suelo + 1.0, isla["z"] - 1.0)
                glRotatef(tiempo * 120, 0, 1, 0)
                Assets.dibujar_estrella()
                glPopMatrix()

                # Meta (Asta con Bandera)
                self.dibujar_bandera_animada(
                    isla["x"] + 2.5, y_suelo, isla["z"] - 1.5, tiempo
                )

                # Arbusto
                glPushMatrix()
                glTranslatef(-4, y_suelo, 1.3)
                Assets.dibujar_sombra_redonda(0.7)
                glScalef(0.8, 0.8, 0.8)
                Assets.dibujar_arbusto()
                glPopMatrix()

                # Arbol
                glPushMatrix()
                glTranslatef(-2.5, y_suelo, -0.4)
                Assets.dibujar_sombra_redonda(0.5)
                glScalef(0.9, 0.9, 0.9)
                Assets.dibujar_arbol_generico()
                glPopMatrix()

                # Moneda
                glPushMatrix()
                glTranslatef(-4.2, y_suelo + 0.7 + math.sin(tiempo * 2) * 0.1, -0.2)
                glRotatef(tiempo * 150, 0, 1, 0)
                Assets.dibujar_moneda_pixel(scale=1.5)
                glPopMatrix()

            # =========================================================
            # ISLA 1: MAQUETA
            # =========================================================
            if i == 1:
                # --- VARIABLES ---
                ESCALA_MAQUETA = 0.55
                oscilacion = math.sin(tiempo * 1.5)
                # Altura base (0.5) + Lo que flota
                altura_flotante = 0.2 + oscilacion * 0.2
                rotacion = tiempo * 20.0

                # Sombra Maqueta
                glPushMatrix()
                glTranslatef(isla["x"], y_suelo + 0.02, isla["z"])  # Pegada al suelo
                glRotatef(315, 0, 1, 0)  # Misma orientación base

                # FÓRMULA DE SOMBRA:
                # Tamaño base * (1.0 - (altura extra * sensibilidad))
                # Usamos 'oscilacion' porque es la variación de altura
                s_scale = ESCALA_MAQUETA * (1.0 - (oscilacion * 0.2))

                glScalef(s_scale, 1.0, s_scale)
                Assets.dibujar_sombra_redonda(2.5)  # Radio base
                glPopMatrix()

                # Maqueta
                glPushMatrix()
                glTranslatef(isla["x"], y_suelo, isla["z"])
                glRotatef(315, 0, 1, 0)

                glTranslatef(0, altura_flotante, 0)
                glRotatef(rotacion, 0, 1, 0)
                glScalef(ESCALA_MAQUETA, ESCALA_MAQUETA, ESCALA_MAQUETA)

                Assets.dibujo_nivel_1()
                glPopMatrix()

            # =========================================================
            # ISLA 2: CASA TOAD
            # =========================================================
            if i == 2:
                # --- VARIABLES ---
                ESCALA_CASA = 0.8
                oscilacion = math.sin(tiempo * 2.0)
                altura_flotante = oscilacion * 0.2

                # Sombra Casa Toad
                glPushMatrix()
                glTranslatef(isla["x"], y_suelo + 0.02, isla["z"])
                glRotatef(45, 0, 1, 0)

                s_scale = ESCALA_CASA * (1.0 - (oscilacion * 0.1))

                glScalef(s_scale, 1.0, s_scale)
                Assets.dibujar_sombra_redonda(1.2)
                glPopMatrix()

                # Casa Toad
                glPushMatrix()
                glTranslatef(isla["x"], y_suelo, isla["z"])
                glRotatef(45, 0, 1, 0)

                # Aplicar altura
                glTranslatef(0, altura_flotante, 0)
                # Aplicar escala
                glScalef(ESCALA_CASA, ESCALA_CASA, ESCALA_CASA)

                Assets.dibujar_casa_toad()
                glPopMatrix()
