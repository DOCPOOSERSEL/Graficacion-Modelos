import math
from OpenGL.GL import *
from OpenGL.GLU import *
from config import *


class Assets:
    quad = None
    CACHE_AGUA_VERTS = []

    @classmethod
    def init_opengl(cls):
        """Inicializa Quadrics y datos precalculados"""
        cls.quad = gluNewQuadric()

        # Pre-calculo agua
        GRID_SIZE = 60
        WORLD_SIZE = 120
        step = WORLD_SIZE / GRID_SIZE
        cls.CACHE_AGUA_VERTS = []
        for i in range(GRID_SIZE):
            z = -WORLD_SIZE / 2 + i * step
            row = []
            for j in range(GRID_SIZE):
                x = -WORLD_SIZE / 2 + j * step
                row.append((x, z))
            cls.CACHE_AGUA_VERTS.append(row)

    # ==========================================
    # PRIMITIVAS BÁSICAS
    # ==========================================
    @staticmethod
    def dibujar_cubo_solido():
        """Dibuja un cubo unitario (1x1x1) centrado en el origen."""
        glBegin(GL_QUADS)
        glNormal3f(0, 0, 1)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(-0.5, -0.5, 0.5)
        glVertex3f(0.5, -0.5, 0.5)
        glNormal3f(0, 0, -1)
        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(0.5, 0.5, -0.5)
        glNormal3f(1, 0, 0)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(0.5, -0.5, 0.5)
        glVertex3f(0.5, -0.5, -0.5)
        glVertex3f(0.5, 0.5, -0.5)
        glNormal3f(-1, 0, 0)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(-0.5, -0.5, -0.5)
        glVertex3f(-0.5, -0.5, 0.5)
        glNormal3f(0, 1, 0)
        glVertex3f(0.5, 0.5, 0.5)
        glVertex3f(0.5, 0.5, -0.5)
        glVertex3f(-0.5, 0.5, -0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glEnd()

    @classmethod
    def dibujar_cilindro_quadric(cls, radio, altura, slices=32, stacks=8):
        """Cilindro cerrado con tapas."""
        glPushMatrix()
        glRotatef(-90, 1, 0, 0)
        gluCylinder(cls.quad, radio, radio, altura, slices, stacks)
        glPushMatrix()
        glRotatef(180, 1, 0, 0)
        gluDisk(cls.quad, 0, radio, slices, 1)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0, 0, altura)
        gluDisk(cls.quad, 0, radio, slices, 1)
        glPopMatrix()
        glPopMatrix()

    @staticmethod
    def dibujar_toroide(radio_interno, radio_externo, lados_seccion, anillos):
        for i in range(anillos):
            theta = 2.0 * math.pi * i / anillos
            theta_next = 2.0 * math.pi * (i + 1) / anillos
            glBegin(GL_QUAD_STRIP)
            for j in range(lados_seccion + 1):
                phi = 2.0 * math.pi * j / lados_seccion
                cos_phi = math.cos(phi)
                sin_phi = math.sin(phi)
                dist = radio_externo + radio_interno * cos_phi
                glNormal3f(
                    cos_phi * math.cos(theta), cos_phi * math.sin(theta), sin_phi
                )
                glVertex3f(
                    dist * math.cos(theta),
                    dist * math.sin(theta),
                    radio_interno * sin_phi,
                )
                glNormal3f(
                    cos_phi * math.cos(theta_next),
                    cos_phi * math.sin(theta_next),
                    sin_phi,
                )
                glVertex3f(
                    dist * math.cos(theta_next),
                    dist * math.sin(theta_next),
                    radio_interno * sin_phi,
                )
            glEnd()

    # ==========================================
    # ENTORNO Y TERRENO
    # ==========================================
    @classmethod
    def dibujar_mar_abierto(cls, tiempo):
        glPushMatrix()
        glTranslatef(0, NIVEL_MAR, 0)
        glMaterialfv(GL_FRONT, GL_SPECULAR, (0.8, 0.8, 0.8, 1))
        glMaterialf(GL_FRONT, GL_SHININESS, 60)
        glBegin(GL_QUADS)
        glNormal3f(0, 1, 0)
        dir_x, dir_z = 0.7, 0.4
        freq, speed = 0.45, 1.5
        GRID_SIZE = 60
        for i in range(GRID_SIZE - 1):
            for j in range(GRID_SIZE - 1):
                p1, p2 = cls.CACHE_AGUA_VERTS[i][j], cls.CACHE_AGUA_VERTS[i][j + 1]
                p3, p4 = (
                    cls.CACHE_AGUA_VERTS[i + 1][j + 1],
                    cls.CACHE_AGUA_VERTS[i + 1][j],
                )
                cx, cz = (p1[0] + p3[0]) * 0.5, (p1[1] + p3[1]) * 0.5
                onda = math.sin((cx * dir_x + cz * dir_z) * freq + tiempo * speed)
                mascara = math.sin(cx * 0.15 - cz * 0.2 + tiempo * 0.3)
                glColor3fv(
                    C_OLAS_MAR if onda > 0.92 and mascara > -0.2 else C_MAR_PROFUNDO
                )
                glVertex3f(p1[0], 0, p1[1])
                glVertex3f(p2[0], 0, p2[1])
                glVertex3f(p3[0], 0, p3[1])
                glVertex3f(p4[0], 0, p4[1])
        glEnd()
        glPopMatrix()

    @staticmethod
    def dibujar_placa_espuma(w, d, radio):
        iw = w - 2 * radio
        id_ = d - 2 * radio
        glNormal3f(0, 1, 0)
        glBegin(GL_QUADS)
        glVertex3f(-w / 2, 0, -id_ / 2)
        glVertex3f(w / 2, 0, -id_ / 2)
        glVertex3f(w / 2, 0, id_ / 2)
        glVertex3f(-w / 2, 0, id_ / 2)
        glVertex3f(-iw / 2, 0, -d / 2)
        glVertex3f(iw / 2, 0, -d / 2)
        glVertex3f(iw / 2, 0, -id_ / 2)
        glVertex3f(-iw / 2, 0, -id_ / 2)
        glVertex3f(-iw / 2, 0, id_ / 2)
        glVertex3f(iw / 2, 0, id_ / 2)
        glVertex3f(iw / 2, 0, d / 2)
        glVertex3f(-iw / 2, 0, d / 2)
        glEnd()
        corners = [
            (iw / 2, id_ / 2),
            (iw / 2, -id_ / 2),
            (-iw / 2, id_ / 2),
            (-iw / 2, -id_ / 2),
        ]
        for i_c, (cx, cz) in enumerate(corners):
            glBegin(GL_TRIANGLE_FAN)
            glVertex3f(cx, 0, cz)
            for i in range(17):
                theta = math.radians([0, 270, 90, 180][i_c] + (i * 90.0 / 16))
                glVertex3f(
                    cx + math.cos(theta) * radio, 0, cz + math.sin(theta) * radio
                )
            glEnd()

    @staticmethod
    def dibujar_alfombra_pasto(w, d):
        divs_x, divs_z = int(w * 5.0), int(d * 5.0)
        sx, sz = w / max(1, divs_x), d / max(1, divs_z)
        ox, oz = -w / 2, -d / 2
        glBegin(GL_QUADS)
        glNormal3f(0, 1, 0)
        for i in range(divs_x):
            for j in range(divs_z):
                glColor3fv(C_PASTO_A if (i + j) % 2 == 0 else C_PASTO_B)
                glVertex3f(ox + i * sx, 0, oz + j * sz)
                glVertex3f(ox + (i + 1) * sx, 0, oz + j * sz)
                glVertex3f(ox + (i + 1) * sx, 0, oz + (j + 1) * sz)
                glVertex3f(ox + i * sx, 0, oz + (j + 1) * sz)
        glEnd()

    @classmethod
    def dibujar_isla_avanzada(cls, w, h, d, r=RADIO_BORDE):
        glMaterialfv(GL_FRONT, GL_SPECULAR, (0.2, 0.2, 0.2, 1))
        glMaterialf(GL_FRONT, GL_SHININESS, 10)
        iw, ih, id_ = w - 2 * r, h - 2 * r, d - 2 * r
        glColor3fv(C_ARENA)
        for px, pz, sx, sz in [(0, 0, iw, id_), (0, 0, w, id_), (0, 0, iw, d)]:
            glPushMatrix()
            glTranslatef(px, -r / 2, pz)
            glScalef(sx, h - r, sz)
            cls.dibujar_cubo_solido()
            glPopMatrix()
        esquinas = [
            (iw / 2, id_ / 2),
            (iw / 2, -id_ / 2),
            (-iw / 2, id_ / 2),
            (-iw / 2, -id_ / 2),
        ]
        for ex, ez in esquinas:
            glPushMatrix()
            glTranslatef(ex, -h / 2, ez)
            glRotatef(-90, 1, 0, 0)
            gluCylinder(cls.quad, r, r, h - r, 12, 1)
            glPopMatrix()
        glColor3fv(C_PASTO_A)
        top_y = h / 2 - r
        glPushMatrix()
        glTranslatef(0, h / 2, 0)
        cls.dibujar_alfombra_pasto(iw, id_)
        glPopMatrix()
        for z_pos in [id_ / 2, -id_ / 2]:
            glPushMatrix()
            glTranslatef(-iw / 2, top_y, z_pos)
            glRotatef(90, 0, 1, 0)
            gluCylinder(cls.quad, r, r, iw, 12, 1)
            glPopMatrix()
        for x_pos in [iw / 2, -iw / 2]:
            glPushMatrix()
            glTranslatef(x_pos, top_y, -id_ / 2)
            gluCylinder(cls.quad, r, r, id_, 12, 1)
            glPopMatrix()
        for ex, ez in esquinas:
            glPushMatrix()
            glTranslatef(ex, top_y, ez)
            gluSphere(cls.quad, r, 12, 12)
            glPopMatrix()

    # ==========================================
    # OBJETOS ESPECÍFICOS Y DECORACIÓN
    # ==========================================
    @classmethod
    def dibujar_casa_toad(cls):
        glPushMatrix()
        glScalef(ESCALA_CASA, ESCALA_CASA, ESCALA_CASA)
        glMaterialfv(GL_FRONT, GL_SPECULAR, (0.0, 0.0, 0.0, 1))
        glMaterialf(GL_FRONT, GL_SHININESS, 0)
        glColor3f(0.85, 0.75, 0.6)
        cls.dibujar_cilindro_quadric(2.0, 3.0)
        # Puerta
        glPushMatrix()
        glTranslatef(0, 0.5, 2.02)
        glScalef(1.0, 1.5, 1.0)
        glColor3f(0.45, 0.22, 0.08)
        gluDisk(cls.quad, 0.0, 0.75, 32, 1)
        glTranslatef(0, 0, 0.01)
        glColor3f(0.65, 0.35, 0.15)
        gluDisk(cls.quad, 0.0, 0.6, 32, 1)
        glPopMatrix()
        # Techo
        glPushMatrix()
        glTranslatef(0, 3.0, 0)
        glColor3f(1.0, 0.0, 0.0)
        gluSphere(cls.quad, 2.3, 32, 32)
        glTranslatef(0, -0.7, 0)
        glColor3f(0.95, 0.95, 0.95)
        gluCylinder(cls.quad, 1.7, 1.7, 0.5, 32, 1)
        glPopMatrix()
        # Manchas
        glPushMatrix()
        glTranslatef(0, 3.0, 0)
        glColor3f(1.0, 1.0, 1.0)
        for x, y, z in [
            (0.0, 0.6, 1.4),
            (0.0, 0.6, -1.4),
            (1.4, 0.6, 0.0),
            (-1.4, 0.6, 0.0),
        ]:
            glPushMatrix()
            glTranslatef(x, y, z)
            gluSphere(cls.quad, 1.0, 16, 16)
            glPopMatrix()
        glPushMatrix()
        glTranslatef(0, 1.6, 0)
        gluSphere(cls.quad, 1, 16, 16)
        glPopMatrix()
        glPopMatrix()
        # Chimenea
        glPushMatrix()
        glTranslatef(1.4, 3.8, -0.8)
        glColor3f(0.6, 0.6, 0.6)
        glRotatef(-90, 1, 0, 0)
        gluCylinder(cls.quad, 0.25, 0.25, 1.5, 4, 1)
        glTranslatef(0, 0, 1.5)
        gluDisk(cls.quad, 0, 0.3, 4, 1)
        glPopMatrix()
        glPopMatrix()

    @classmethod
    def dibujar_cilindro_con_rectangulo(cls):
        glPushMatrix()
        glScalef(1.5, 0.8, 2.0)
        alturas = [0.6] * 5
        colores = [(0.55, 0.45, 0.35), (0.35, 0.25, 0.15)] * 3
        y_actual = 0.0
        for i in range(5):
            glPushMatrix()
            glColor3f(*colores[i])
            glRotatef(-90, 1, 0, 0)
            glTranslatef(0, 0, y_actual)
            gluCylinder(cls.quad, 0.35, 0.35, alturas[i], 24, 1)
            glPopMatrix()
            y_actual += alturas[i]
        glPushMatrix()
        glColor3fv(C_PASTO_OSCURO)
        glRotatef(-90, 1, 0, 0)
        glTranslatef(0, 0, 3.01)
        gluDisk(cls.quad, 0, 0.36, 24, 1)
        glPopMatrix()
        for i, offset_y in enumerate([0.3, 0.9, 1.5, 2.1, 2.7]):
            glPushMatrix()
            glTranslatef(1.3, offset_y, 0.0)
            glScalef(2.6, 0.6, 0.7)
            glColor3f(*(colores[i]))
            cls.dibujar_cubo_solido()
            glPopMatrix()
        glPushMatrix()
        glTranslatef(1.3, 3.005, 0.0)
        glScalef(2.6, 0.01, 0.71)
        glColor3fv(C_PASTO_OSCURO)
        cls.dibujar_cubo_solido()
        glPopMatrix()
        glPopMatrix()

    @classmethod
    def dibujar_cilindro_con_rectangulo_cruzado(cls):
        glPushMatrix()
        glTranslatef(2.5, 0.0, -1.5)
        glRotatef(270, 0, 1, 0)
        cls.dibujar_cilindro_con_rectangulo()
        glPopMatrix()

        # CORRECCION: Se eliminó el último glPopMatrix() que sobraba
        glPushMatrix()
        glTranslatef(2.5, 0.0, -1.5)
        glRotatef(270, 0, 1, 0)
        glScalef(1.5, 0.9, 2.0)
        glPushMatrix()
        glColor3f(0.6, 0.6, 0.6)
        glRotatef(-90, 1, 0, 0)
        glTranslatef(0, 0, 2.4)
        gluCylinder(cls.quad, 0.35, 0.35, 0.6, 24, 1)
        glPopMatrix()
        glPushMatrix()
        glColor3f(0.4, 0.4, 0.4)
        glRotatef(-90, 1, 0, 0)
        glTranslatef(0, 0, 3.0)
        gluCylinder(cls.quad, 0.35, 0.35, 0.6, 24, 1)
        glPopMatrix()
        glPushMatrix()
        glColor3fv(C_PASTO_OSCURO)
        glRotatef(-90, 1, 0, 0)
        glTranslatef(0, 0, 3.6)
        gluDisk(cls.quad, 0, 0.36, 24, 1)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(1.3, 2.7, 0.0)
        glScalef(2.6, 0.6, 0.71)
        glColor3f(0.6, 0.6, 0.6)
        cls.dibujar_cubo_solido()
        glPopMatrix()
        glPushMatrix()
        glTranslatef(1.3, 3.3, 0.0)
        glScalef(2.6, 0.6, 0.71)
        glColor3f(0.4, 0.4, 0.4)
        cls.dibujar_cubo_solido()
        glPopMatrix()
        glPushMatrix()
        glTranslatef(1.3, 3.6, 0.0)
        glScalef(2.6, 0.01, 0.72)
        glColor3fv(C_PASTO_OSCURO)
        cls.dibujar_cubo_solido()
        glPopMatrix()
        glPopMatrix()

    @classmethod
    def dibujar_escaleras_desde_cubo(cls):
        glPushMatrix()
        glTranslatef(1.7, 2.4, -0.5)
        glRotatef(180, 0, 1, 0)
        glScalef(0.4, 0.7, 0.3)
        glPushMatrix()
        glTranslatef(0.0, 0.6, 0.0)
        glScalef(1.6, 1.2, 1.6)
        glColor3f(0.5, 0.5, 0.5)
        cls.dibujar_cubo_solido()
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0.0, 1.2, 0.0)
        glScalef(1.62, 0.01, 1.62)
        glColor3fv(C_PASTO_OSCURO)
        cls.dibujar_cubo_solido()
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0.091, 0.15, 0)
        offs = [0.9, 0.6, 0.3, 0.0]
        deeps = [-1, -1.4, -1.5, -1.8]
        scales = [0.8, 1.2, 1.6, 2.0]
        for k in range(4):
            glPushMatrix()
            glTranslatef(0.0, offs[k], deeps[k])
            glScalef(1.4, 0.3, scales[k])
            glColor3f(0.45 - k * 0.02, 0.45 - k * 0.02, 0.45 - k * 0.02)
            cls.dibujar_cubo_solido()
            glPopMatrix()
        glPopMatrix()
        glPopMatrix()

    @classmethod
    def dibujar_campanita_mario(cls):
        glPushMatrix()
        glTranslatef(0, 2.5, 0)
        glScalef(0.2, 0.2, 0.2)
        glPushMatrix()
        glTranslatef(0.0, 0.6, 0.0)
        glScalef(1.3, 1.7, 1.3)
        glColor3f(0.95, 0.85, 0.2)
        gluSphere(cls.quad, 0.6, 24, 24)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0.0, 0.22, 0.0)
        glScalef(1.6, 1.0, 1.6)
        glRotatef(90, 1, 0, 0)
        glColor3f(0.9, 0.75, 0.15)
        cls.dibujar_toroide(0.3, 0.4, 30, 30)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0.0, 1.6, 0.0)
        glScalef(0.7, 1.0, 0.7)
        glColor3f(0.85, 0.65, 0.1)
        cls.dibujar_toroide(0.06, 0.18, 20, 30)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0.0, 0.05, 0.0)
        glColor3f(1, 1, 1)
        gluSphere(cls.quad, 0.58, 24, 24)
        glPopMatrix()
        for x_eye in [-0.18, 0.18]:
            glPushMatrix()
            glTranslatef(x_eye, 0.75, 0.85)
            glScalef(0.15, 0.35, 0.15)
            glColor3f(0, 0, 0)
            gluSphere(cls.quad, 1.0, 16, 16)
            glPopMatrix()
        glPopMatrix()

    @classmethod
    def dibujar_arbol_campana(cls):
        glPushMatrix()
        glTranslatef(2.5, 4.1, -1.2)
        glScalef(0.4, 0.4, 0.4)
        glPushMatrix()
        glTranslatef(0.0, 0.6, 0.0)
        glScalef(1.3, 1.7, 1.3)
        glColor3f(0.6, 0.4, 0.2)
        gluSphere(cls.quad, 0.6, 24, 24)
        glPopMatrix()
        distancia = 0.3
        for i in range(6):
            glPushMatrix()
            glTranslatef(0.0, 0.8 - distancia, 0.0)
            glScalef(1.6, 1.0, 1.6)
            glRotatef(90, 1, 0, 0)
            glColor3f(0.9, 0.75, 0.15) if i % 2 == 0 else glColor3f(0.6, 0.4, 0.2)
            cls.dibujar_toroide(0.3, 0.3, 30, 8)
            glPopMatrix()
            distancia += 0.3
        glPushMatrix()
        glTranslatef(0.0, -1.4, 0.0)
        glScalef(0.5, 5, 0.5)
        glColor3f(1, 1, 1)
        gluSphere(cls.quad, 0.58, 24, 24)
        glPopMatrix()
        glPopMatrix()

    @staticmethod
    def dibujar_rampa_cafe_3d():
        glPushMatrix()
        glBegin(GL_TRIANGLES)
        glColor3f(0.4, 0.3, 0.2)
        glVertex3f(-1.0, 1.0, 0.0)
        glVertex3f(1.0, 1.0, 0.0)
        glVertex3f(1.0, 0.0, -2.0)
        glVertex3f(-1.0, 1.0, 0.0)
        glVertex3f(1.0, 0.0, -2.0)
        glVertex3f(-1.0, 0.0, -2.0)
        glColor3f(0.5, 0.4, 0.3)
        glVertex3f(-1.0, 0.0, 0.0)
        glVertex3f(1.0, 0.0, 0.0)
        glVertex3f(1.0, 0.0, -2.0)
        glVertex3f(-1.0, 0.0, 0.0)
        glVertex3f(1.0, 0.0, -2.0)
        glVertex3f(-1.0, 0.0, -2.0)
        glColor3f(0.5, 0.4, 0.3)
        glVertex3f(-1.0, 0.0, 0.0)
        glVertex3f(1.0, 0.0, 0.0)
        glVertex3f(1.0, 1.0, 0.0)
        glVertex3f(-1.0, 0.0, 0.0)
        glVertex3f(1.0, 1.0, 0.0)
        glVertex3f(-1.0, 1.0, 0.0)
        glColor3f(0.5, 0.4, 0.3)
        glVertex3f(-1.0, 0.0, 0.0)
        glVertex3f(-1.0, 1.0, 0.0)
        glVertex3f(-1.0, 0.0, -2.0)
        glVertex3f(1.0, 0.0, 0.0)
        glVertex3f(1.0, 1.0, 0.0)
        glVertex3f(1.0, 0.0, -2.0)
        glEnd()
        glPopMatrix()

    @classmethod
    def dibujar_moneda_mario(cls):
        glPushMatrix()
        glTranslatef(0.2, 3.5, -0.5)
        glPushMatrix()
        glScalef(1.0, 1.0, 0.2)
        glColor3f(1.0, 0.85, 0.2)
        cls.dibujar_cilindro_quadric(0.6, 1.0)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0.0, 0.0, 0.0)
        glColor3f(0.9, 0.75, 0.15)
        cls.dibujar_toroide(0.03, 0.6, 20, 40)
        glPopMatrix()

        # CORRECCION: Se eliminó un glPopMatrix() extra en la siguiente línea
        glPushMatrix()
        glTranslatef(0.0, 0.0, 0.12)
        glScalef(0.6, 0.6, 0.1)
        glColor3f(0.95, 0.8, 0.2)
        gluSphere(cls.quad, 0.4, 20, 20)
        glPopMatrix()

        glPopMatrix()

    @classmethod
    def dibujar_sombra_redonda(cls, radio):
        glDisable(GL_LIGHTING)
        glPushMatrix()
        glTranslatef(0, 0.02, 0)
        glRotatef(-90, 1, 0, 0)
        glColor4f(0.0, 0.0, 0.0, 0.7)
        gluDisk(cls.quad, 0, radio, 32, 1)
        glPopMatrix()
        glEnable(GL_LIGHTING)

    @classmethod
    def dibujar_signo_interrogacion(cls):
        glPushMatrix()
        glColor3f(1.0, 1.0, 1.0)
        glTranslatef(0, 0.1, 0)
        glScalef(0.15, 0.15, 0.1)
        cls.dibujar_toroide(0.2, 0.5, 8, 16)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0, -0.25, 0)
        glScalef(0.1, 0.1, 0.1)
        glColor3f(1.0, 1.0, 1.0)
        cls.dibujar_cubo_solido()
        glPopMatrix()

    @classmethod
    def dibujar_cubo_pregunta(cls):
        glPushMatrix()
        tamano = 0.8
        color_cubo = (0.9, 0.75, 0.2)
        glPushMatrix()
        glScalef(tamano, tamano, tamano)
        glColor3f(*color_cubo)
        cls.dibujar_cubo_solido()
        glPopMatrix()
        distancia = tamano / 2 + 0.01
        glPushMatrix()
        glTranslatef(0, 0, distancia)
        cls.dibujar_signo_interrogacion()
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0, 0, -distancia)
        glRotatef(180, 0, 1, 0)
        cls.dibujar_signo_interrogacion()
        glPopMatrix()
        glPushMatrix()
        glTranslatef(distancia, 0, 0)
        glRotatef(90, 0, 1, 0)
        cls.dibujar_signo_interrogacion()
        glPopMatrix()
        glPushMatrix()
        glTranslatef(-distancia, 0, 0)
        glRotatef(-90, 0, 1, 0)
        cls.dibujar_signo_interrogacion()
        glPopMatrix()
        glPopMatrix()

    @staticmethod
    def dibujar_estrella():
        glPushMatrix()
        num_puntas = 5
        radio_ext = 0.5
        radio_int = 0.2
        profundidad = 0.1
        glColor3f(1.0, 0.84, 0.0)
        vertices_front = []
        vertices_back = []
        for i in range(num_puntas * 2):
            angulo = (math.pi * 2 * i) / (num_puntas * 2) - math.pi / 2
            radio = radio_ext if i % 2 == 0 else radio_int
            x = radio * math.cos(angulo)
            y = radio * math.sin(angulo)
            vertices_front.append([x, y, profundidad])
            vertices_back.append([x, y, -profundidad])
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0, 0, profundidad)
        for v in vertices_front:
            glVertex3f(v[0], v[1], v[2])
        glVertex3f(vertices_front[0][0], vertices_front[0][1], vertices_front[0][2])
        glEnd()
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0, 0, -profundidad)
        for v in reversed(vertices_back):
            glVertex3f(v[0], v[1], v[2])
        glVertex3f(vertices_back[-1][0], vertices_back[-1][1], vertices_back[-1][2])
        glEnd()
        glBegin(GL_QUAD_STRIP)
        for i in range(len(vertices_front)):
            glVertex3f(vertices_front[i][0], vertices_front[i][1], vertices_front[i][2])
            glVertex3f(vertices_back[i][0], vertices_back[i][1], vertices_back[i][2])
        glVertex3f(vertices_front[0][0], vertices_front[0][1], vertices_front[0][2])
        glVertex3f(vertices_back[0][0], vertices_back[0][1], vertices_back[0][2])
        glEnd()
        glPopMatrix()

    @classmethod
    def dibujar_mario(cls):
        C_PIEL = (0.96, 0.8, 0.68)
        C_ROJO = (0.85, 0.1, 0.1)
        C_AZUL = (0.1, 0.2, 0.8)
        C_CAFE = (0.4, 0.2, 0.1)
        C_BLANCO = (1.0, 1.0, 1.0)
        C_NEGRO = (0.1, 0.1, 0.1)
        glPushMatrix()
        glScalef(0.7, 0.7, 0.7)
        for lado in [-1, 1]:
            glPushMatrix()
            glTranslatef(0.25 * lado, 0.15, 0)
            glPushMatrix()
            glColor3fv(C_CAFE)
            glScalef(0.3, 0.3, 0.4)
            cls.dibujar_cubo_solido()
            glPopMatrix()
            glPushMatrix()
            glTranslatef(0, 0.15, 0)
            glColor3fv(C_AZUL)
            glRotatef(-90, 1, 0, 0)
            gluCylinder(cls.quad, 0.12, 0.12, 0.4, 12, 1)
            glPopMatrix()
            glPopMatrix()
        glPushMatrix()
        glTranslatef(0, 0.7, 0)
        glColor3fv(C_AZUL)
        glPushMatrix()
        glScalef(1.0, 0.8, 1.0)
        gluSphere(cls.quad, 0.45, 16, 16)
        glPopMatrix()
        glTranslatef(0, 0.3, 0)
        glColor3fv(C_ROJO)
        glPushMatrix()
        glScalef(1.0, 0.7, 1.0)
        gluSphere(cls.quad, 0.42, 16, 16)
        glPopMatrix()
        glColor3f(1.0, 0.8, 0.0)
        for lado in [-1, 1]:
            glPushMatrix()
            glTranslatef(0.2 * lado, 0.0, 0.38)
            gluSphere(cls.quad, 0.08, 8, 8)
            glPopMatrix()
        for lado in [-1, 1]:
            glPushMatrix()
            glTranslatef(0.45 * lado, 0.1, 0)
            glRotatef(20 * lado, 0, 0, 1)
            glColor3fv(C_ROJO)
            glPushMatrix()
            glScalef(0.8, 1.0, 0.8)
            gluSphere(cls.quad, 0.18, 12, 12)
            glTranslatef(0, -0.15, 0)
            glRotatef(90, 1, 0, 0)
            gluCylinder(cls.quad, 0.15, 0.12, 0.35, 12, 1)
            glPopMatrix()
            glTranslatef(0, -0.65, 0)
            glColor3fv(C_BLANCO)
            gluSphere(cls.quad, 0.2, 12, 12)
            glPopMatrix()
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0, 1.55, 0)
        glColor3fv(C_PIEL)
        glPushMatrix()
        glScalef(1.0, 0.9, 1.0)
        gluSphere(cls.quad, 0.5, 20, 20)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0, 0, 0.5)
        gluSphere(cls.quad, 0.15, 12, 12)
        glPopMatrix()
        glColor3fv(C_NEGRO)
        glPushMatrix()
        glTranslatef(0, -0.15, 0.45)
        glScalef(0.4, 0.1, 0.15)
        cls.dibujar_cubo_solido()
        glPopMatrix()
        for lado in [-1, 1]:
            glPushMatrix()
            glTranslatef(0.18 * lado, 0.15, 0.42)
            glScalef(0.08, 0.15, 0.05)
            cls.dibujar_cubo_solido()
            glPopMatrix()
        glTranslatef(0, 0.35, 0)
        glColor3fv(C_ROJO)
        glPushMatrix()
        glRotatef(90, 1, 0, 0)
        glTranslatef(0, 0.1, 0)
        gluDisk(cls.quad, 0, 0.55, 20, 1)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0, 0.1, -0.1)
        glScalef(1.0, 0.7, 1.0)
        gluSphere(cls.quad, 0.4, 20, 20)
        glPopMatrix()
        glPopMatrix()
        glPopMatrix()

    @classmethod
    def dibujo_nivel_1(cls):
        glPushMatrix()
        glTranslatef(-1.5, 0, 0)
        cls.dibujar_cilindro_con_rectangulo()
        cls.dibujar_cilindro_con_rectangulo_cruzado()
        cls.dibujar_escaleras_desde_cubo()
        cls.dibujar_campanita_mario()
        cls.dibujar_arbol_campana()
        glPushMatrix()
        glTranslatef(3, 3, 2)
        glScalef(0.2, 0.8, 0.8)
        cls.dibujar_rampa_cafe_3d()
        glPopMatrix()
        glPushMatrix()
        glScalef(1, 0.3, 1)
        cls.dibujar_moneda_mario()
        glPopMatrix()
        glPopMatrix()

    @classmethod
    def dibujar_arbol_generico(cls):
        glPushMatrix()
        glScalef(0.8, 0.8, 0.8)
        glPushMatrix()
        glColor3f(0.0, 0.5, 0.0)
        glTranslatef(0.0, 0.5, 0.0)
        gluSphere(cls.quad, 0.6, 16, 16)
        glPopMatrix()
        glPushMatrix()
        glColor3f(0.0, 0.6, 0.0)
        glTranslatef(-0.4, 0.4, 0.2)
        gluSphere(cls.quad, 0.5, 16, 16)
        glPopMatrix()
        glPushMatrix()
        glColor3f(0.0, 0.6, 0.0)
        glTranslatef(0.4, 0.4, -0.2)
        gluSphere(cls.quad, 0.5, 16, 16)
        glPopMatrix()
        glPushMatrix()
        glColor3f(0.2, 0.7, 0.2)
        glTranslatef(0.1, 0.9, -0.1)
        gluSphere(cls.quad, 0.45, 16, 16)
        glPopMatrix()
        glPushMatrix()
        glColor3f(0.3, 0.8, 0.3)
        glTranslatef(-0.1, 0.3, 0.5)
        gluSphere(cls.quad, 0.4, 16, 16)
        glPopMatrix()
        glPushMatrix()
        glColor3f(0.0, 0.5, 0.0)
        glTranslatef(0.2, 0.35, -0.5)
        gluSphere(cls.quad, 0.4, 16, 16)
        glPopMatrix()
        glPushMatrix()
        glColor3f(0.55, 0.27, 0.07)
        glTranslatef(0.0, -0.3, 0.0)
        glRotatef(-90, 1, 0, 0)
        gluCylinder(cls.quad, 0.15, 0.15, 0.8, 20, 1)
        glPopMatrix()
        glPopMatrix()

    @classmethod
    def dibujar_nube(cls, scale=1.0):
        glPushMatrix()
        glScalef(scale, scale, scale)
        glColor3f(1.0, 1.0, 1.0)
        glPushMatrix()
        glTranslatef(0, 0.1, 0)
        gluSphere(cls.quad, 0.45, 24, 24)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(-0.42, 0, 0)
        gluSphere(cls.quad, 0.35, 24, 24)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0.42, 0, 0)
        gluSphere(cls.quad, 0.35, 24, 24)
        glPopMatrix()
        glColor3f(0, 0, 0)
        glPushMatrix()
        glTranslatef(-0.15, 0.1, 0.35)
        glScalef(0.05, 0.15, 0.05)
        cls.dibujar_cubo_solido()
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0.15, 0.1, 0.35)
        glScalef(0.05, 0.15, 0.05)
        cls.dibujar_cubo_solido()
        glPopMatrix()
        glPopMatrix()

    @classmethod
    def dibujar_arbusto(cls):
        glPushMatrix()
        glColor3f(0.2, 0.7, 0.2)
        glPushMatrix()
        glTranslatef(-0.40, 0, 0)
        glScalef(1, 2.30, 1)
        gluSphere(cls.quad, 0.4, 24, 24)
        glPopMatrix()
        glColor3f(0.2, 0.7, 0.2)
        glPushMatrix()
        glTranslatef(0.15, -0.30, 0)
        glScalef(1, 1.50, 1)
        gluSphere(cls.quad, 0.4, 24, 24)
        glPopMatrix()
        glColor3f(0, 0, 0)
        glPushMatrix()
        glTranslatef(0.10, -0.10, 0.32)
        glScalef(1, 2.40, 1)
        gluSphere(cls.quad, 0.1, 16, 16)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0.35, -0.10, 0.25)
        glScalef(1, 2.40, 1)
        gluSphere(cls.quad, 0.1, 16, 16)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(-0.50, 0.20, 0.32)
        glScalef(1, 2.40, 1)
        gluSphere(cls.quad, 0.1, 16, 16)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(-0.30, 0.20, 0.32)
        glScalef(1, 2.40, 1)
        gluSphere(cls.quad, 0.1, 16, 16)
        glPopMatrix()
        glPopMatrix()

    @classmethod
    def dibujar_plataforma_mario(cls, size=1.0, thickness=0.1):
        glPushMatrix()
        glColor3f(1.0, 0.9, 0.2)
        glPushMatrix()
        glScalef(size, thickness, size)
        cls.dibujar_cubo_solido()
        glPopMatrix()
        glColor3f(0.50, 0.30, 0.0)
        posiciones = [-1.50, -0.75, 0.0, 0.75, 1.50]
        s_borde = 0.40
        for x in posiciones:
            glPushMatrix()
            glScalef(s_borde, 0.20, 1)
            glTranslatef(x / s_borde, 0.4, 0.56)
            cls.dibujar_cubo_solido()
            glPopMatrix()
            glPushMatrix()
            glScalef(s_borde, 0.20, 1)
            glTranslatef(x / s_borde, 0.4, -0.56)
            cls.dibujar_cubo_solido()
            glPopMatrix()
        for z in posiciones:
            glPushMatrix()
            glScalef(1, 0.20, s_borde)
            glTranslatef(0.56, 0.4, z / s_borde)
            cls.dibujar_cubo_solido()
            glPopMatrix()
            glPushMatrix()
            glScalef(1, 0.20, s_borde)
            glTranslatef(-0.56, 0.4, z / s_borde)
            cls.dibujar_cubo_solido()
            glPopMatrix()
        glPopMatrix()

    @classmethod
    def dibujar_bloque_random(cls):
        glPushMatrix()
        glColor3f(1.0, 0.9, 0.2)
        glPushMatrix()
        cls.dibujar_cubo_solido()
        glPopMatrix()
        glColor3f(1.0, 0.9, 0.2)
        glPushMatrix()
        glScalef(1, 1, 0.50)
        glScalef(0.9, 0.9, 0.9)
        cls.dibujar_cubo_solido()
        glPopMatrix()
        glColor3f(1.0, 0.9, 0.2)
        glPushMatrix()
        glScalef(1.14, 1, 1.30)
        glScalef(0.9, 0.9, 0.9)
        cls.dibujar_cubo_solido()
        glPopMatrix()
        glColor3f(1, 1, 1)
        glPushMatrix()
        glTranslatef(0, 0.35, 0.41)
        glScalef(1.60, 0.50, 2)
        glScalef(0.2, 0.2, 0.2)
        cls.dibujar_cubo_solido()
        glPopMatrix()
        glPushMatrix()
        glTranslatef(-0.20, 0.15, 0.41)
        glScalef(0.50, 1.40, 2)
        glScalef(0.2, 0.2, 0.2)
        cls.dibujar_cubo_solido()
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0.20, 0.15, 0.41)
        glScalef(0.50, 1.40, 2)
        glScalef(0.2, 0.2, 0.2)
        cls.dibujar_cubo_solido()
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0.10, -0.03, 0.41)
        glScalef(1, 0.50, 2)
        glScalef(0.2, 0.2, 0.2)
        cls.dibujar_cubo_solido()
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0, -0.16, 0.41)
        glScalef(0.50, 1.33, 2)
        glScalef(0.2, 0.2, 0.2)
        cls.dibujar_cubo_solido()
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0, -0.40, 0.41)
        glScalef(0.50, 0.50, 2)
        glScalef(0.2, 0.2, 0.2)
        cls.dibujar_cubo_solido()
        glPopMatrix()
        glPopMatrix()

    @classmethod
    def dibujar_tuberia(cls, height=2.5, radius=0.6, radius2=0.4):
        glPushMatrix()
        glColor3f(0.0, 0.7, 0.0)
        glPushMatrix()
        glRotatef(-90, 1, 0, 0)
        gluCylinder(cls.quad, radius, radius, height, 32, 1)
        glPopMatrix()
        glColor3f(0.0, 0.85, 0.0)
        glPushMatrix()
        glTranslatef(0, height, 0)
        glRotatef(-90, 1, 0, 0)
        gluCylinder(cls.quad, radius * 1.15, radius * 1.15, 0.25, 32, 1)
        glTranslatef(0, 0, 0.25)
        gluDisk(cls.quad, 0.0, radius * 1.15, 32, 1)
        glPopMatrix()
        glColor3f(0.0, 0.0, 0.0)
        glPushMatrix()
        glTranslatef(0, height + 0.26, 0)
        glRotatef(-90, 1, 0, 0)
        gluDisk(cls.quad, 0.0, radius2 * 1.15, 32, 1)
        glPopMatrix()
        glPopMatrix()

    @classmethod
    def dibujar_bandera_triangular(cls, width=1.3, height=0.5, depth=0.04):
        w = width / 2
        h = height / 2
        d = depth / 2
        glBegin(GL_TRIANGLES)
        glNormal3f(1, 1, 1)
        glVertex3f(0, h, d)
        glVertex3f(w, 0, d)
        glVertex3f(0, -h, d)
        glNormal3f(1, 1, 1)
        glVertex3f(0, h, -d)
        glVertex3f(0, -h, -d)
        glVertex3f(w, 0, -d)
        glEnd()

    @classmethod
    def dibujar_asta_bandera(cls):
        glPushMatrix()
        glColor3f(0, 1, 0)
        glPushMatrix()
        glRotatef(-90, 1, 0, 0)
        gluCylinder(cls.quad, 0.08, 0.08, 4.0, 24, 1)
        glPopMatrix()
        glColor3f(0, 1, 0)
        glPushMatrix()
        glTranslatef(0, 4.0, 0)
        gluSphere(cls.quad, 0.15, 24, 24)
        glPopMatrix()
        glColor3f(1, 1, 1)
        glPushMatrix()
        glTranslatef(0, 3.6, 0)
        cls.dibujar_bandera_triangular()
        glPopMatrix()
        glColor3f(0.70, 0.45, 0.20)
        glPushMatrix()
        glTranslatef(0, 0.2, 0)
        glScalef(0.6, 0.4, 0.6)
        glScalef(1.2, 1.2, 1.2)
        cls.dibujar_cubo_solido()
        glPopMatrix()
        glPopMatrix()

    @staticmethod
    def dibujar_moneda_pixel(scale=1.0):
        glPushMatrix()
        glScalef(scale, scale, scale)
        glColor3f(0.85, 0.75, 0.1)
        glPushMatrix()
        glScalef(0.5, 0.8, 0.1)
        Assets.dibujar_cubo_solido()
        glPopMatrix()
        glColor3f(1.0, 0.9, 0.2)
        glPushMatrix()
        glScalef(0.3, 0.6, 0.12)
        Assets.dibujar_cubo_solido()
        glPopMatrix()
        glPopMatrix()
