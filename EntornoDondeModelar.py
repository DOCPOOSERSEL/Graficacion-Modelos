import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

# Variable global para el objeto quadric
quad = None

def init_quadric():
    global quad
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluQuadricTexture(quad, GL_TRUE)

# Variables globales para la cámara
camX, camY, camZ = 0.0, 2.0, 10.0  # posición inicial (ajustada para ver la casa mejor)
camRotX, camRotY = 0.0, 0.0  # rotación de la cámara (pitch, yaw)
camSpeed = 0.2  # velocidad de movimiento
rotSpeed = 2.0  # velocidad de rotación
zoom = 45.0  # campo de visión inicial para zoom
zoomSpeed = 2.0  # velocidad de zoom

def teclado(key, x, y):
    global camX, camY, camZ, camRotX, camRotY
    key = key.decode("utf-8").lower()  # convertir a string

    if key == 'w':  # subir en Y
        camY += camSpeed
    elif key == 's':  # bajar en Y
        camY -= camSpeed
    elif key == 'a':  # mover a la izquierda en X
        camX -= camSpeed
    elif key == 'd':  # mover a la derecha en X
        camX += camSpeed
    elif key == 'q':  # rotar cámara a la izquierda
        camRotY += rotSpeed
    elif key == 'e':  # rotar cámara a la derecha
        camRotY -= rotSpeed
    elif key == 'r':  # rotar cámara arriba
        camRotX = min(89.0, camRotX + rotSpeed)
    elif key == 'f':  # rotar cámara abajo
        camRotX = max(-89.0, camRotX - rotSpeed)
    elif key == '1':  # resetear posición
        camX, camY, camZ = 0.0, 2.0, 10.0
        camRotX, camRotY = 0.0, 0.0
        global zoom
        zoom = 45.0

    glutPostRedisplay()  # redibuja la escena

def mouse(button, state, x, y):
    global zoom
    # Rueda del mouse para zoom
    if button == 3 and state == GLUT_DOWN:  # rueda hacia arriba
        zoom = max(10.0, zoom - zoomSpeed)  # límite mínimo de zoom (más zoom in)
    elif button == 4 and state == GLUT_DOWN:  # rueda hacia abajo
        zoom = min(90.0, zoom + zoomSpeed)  # límite máximo de zoom (más zoom out)
    glutPostRedisplay()

def init():
    glClearColor(0.53, 0.81, 0.92, 1.0)  # Fondo azul cielo
    glEnable(GL_DEPTH_TEST)
    
    # Habilitar iluminación
    glEnable(GL_LIGHTING)
    
    # Configurar luces - INTENSIDAD REDUCIDA A 8/10
    # Multiplicadores de intensidad: 0.8 para todas las luces
    
    # Luz principal (LIGHT0) - luz direccional suave desde arriba
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 10.0, 0.0, 1.0])  # Luz desde arriba
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.56, 0.56, 0.56, 1.0])    # 0.7 * 0.8 = 0.56
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.24, 0.24, 0.24, 1.0])    # 0.3 * 0.8 = 0.24
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.4, 0.4, 0.4, 1.0])      # 0.5 * 0.8 = 0.4
    
    # Luz de relleno (LIGHT1) - luz ambiental desde el frente
    glEnable(GL_LIGHT1)
    glLightfv(GL_LIGHT1, GL_POSITION, [0.0, 5.0, 10.0, 1.0])  # Luz desde el frente
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.32, 0.32, 0.32, 1.0])    # 0.4 * 0.8 = 0.32
    glLightfv(GL_LIGHT1, GL_AMBIENT, [0.16, 0.16, 0.16, 1.0])    # 0.2 * 0.8 = 0.16
    glLightfv(GL_LIGHT1, GL_SPECULAR, [0.16, 0.16, 0.16, 1.0])   # 0.2 * 0.8 = 0.16
    
    # Luz lateral (LIGHT2) - para iluminar lados oscuros
    glEnable(GL_LIGHT2)
    glLightfv(GL_LIGHT2, GL_POSITION, [-10.0, 5.0, 0.0, 1.0]) # Luz desde la izquierda
    glLightfv(GL_LIGHT2, GL_DIFFUSE, [0.24, 0.24, 0.24, 1.0])    # 0.3 * 0.8 = 0.24
    glLightfv(GL_LIGHT2, GL_AMBIENT, [0.08, 0.08, 0.08, 1.0])    # 0.1 * 0.8 = 0.08
    
    # Habilitar color material
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    
    # Configurar propiedades del material (también reducidas)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.4, 0.4, 0.4, 1.0])  # Reducido
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 40.0)  # Reducido ligeramente
    
    # Suavizar normales para transiciones más suaves
    glShadeModel(GL_SMOOTH)
    
    # Normalizar normales (importante cuando escalas objetos)
    glEnable(GL_NORMALIZE)
    
    # Inicializar quadric
    init_quadric()

#--------------------------------------------Poner las funciones dibujo----------------------------------------------------
def dibujar_cilindro_con_rectangulo():
    glPushMatrix()
    glScalef(1.5, 0.8, 2.0)

    alturas = [0.6, 0.6, 0.6, 0.6, 0.6] 
    colores = [
        (0.85, 0.78, 0.65),
        (0.75, 0.60, 0.40),
        (0.85, 0.78, 0.65),
        (0.75, 0.60, 0.40),
        (0.85, 0.78, 0.65),
    ]

    y_actual = 0.0

    for i in range(5):
        glPushMatrix()
        glColor3f(*colores[i])
        glRotatef(-90, 1, 0, 0)
        glTranslatef(0, 0, y_actual)
        gluCylinder(quad, 0.35, 0.35, alturas[i], 24, 1)
        glPopMatrix()
        y_actual += alturas[i]

    # Musgo fino arriba del cilindro
    glPushMatrix()
    glColor3f(0.2, 0.6, 0.2)
    glRotatef(-90, 1, 0, 0)
    glTranslatef(0, 0, 3.01)
    gluDisk(quad, 0, 0.36, 24, 1)
    glPopMatrix()

    # Franja 1 – café claro
    glPushMatrix()
    glTranslatef(1.3, 0.3, 0.0)
    glScalef(2.6, 0.6, 0.7)
    glColor3f(0.85, 0.78, 0.65)
    glutSolidCube(1.0)
    glPopMatrix()

    # Franja 2 – café medio
    glPushMatrix()
    glTranslatef(1.3, 0.9, 0.0)
    glScalef(2.6, 0.6, 0.7)
    glColor3f(0.75, 0.60, 0.40)
    glutSolidCube(1.0)
    glPopMatrix()

    # Franja 3 – café claro
    glPushMatrix()
    glTranslatef(1.3, 1.5, 0.0)
    glScalef(2.6, 0.6, 0.7)
    glColor3f(0.85, 0.78, 0.65)
    glutSolidCube(1.0)
    glPopMatrix()

    # Franja 4 – café medio
    glPushMatrix()
    glTranslatef(1.3, 2.1, 0.0)
    glScalef(2.6, 0.6, 0.7)
    glColor3f(0.75, 0.60, 0.40)
    glutSolidCube(1.0)
    glPopMatrix()

    # Franja 5 – café claro
    glPushMatrix()
    glTranslatef(1.3, 2.7, 0.0)
    glScalef(2.6, 0.6, 0.7)
    glColor3f(0.85, 0.78, 0.65)
    glutSolidCube(1.0)
    glPopMatrix()


    # Musgo ULTRA fino arriba del rectángulo
    glPushMatrix()
    glTranslatef(1.3, 3.005, 0.0)
    glScalef(2.6, 0.01, 0.71)
    glColor3f(0.2, 0.6, 0.2)
    glutSolidCube(1.0)
    glPopMatrix()

    glPopMatrix()

def dibujar_cilindro_con_rectangulo_cruzado():
    glPushMatrix()

    # Misma posición y rotación
    glTranslatef(2.5, 0.0, -1.5)
    glRotatef(270, 0, 1, 0)

    # Módulo base
    dibujar_cilindro_con_rectangulo()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(2.5, 0.0, -1.5)
    glRotatef(270, 0, 1, 0)
    glScalef(1.5, 0.9, 2.0)

    # Gris claro
    glPushMatrix()
    glColor3f(0.85, 0.85, 0.85)
    glRotatef(-90, 1, 0, 0)
    glTranslatef(0, 0, 2.4)
    gluCylinder(quad, 0.35, 0.35, 0.6, 24, 1)
    glPopMatrix()

    # Gris un poco más oscuro
    glPushMatrix()
    glColor3f(0.75, 0.75, 0.75)
    glRotatef(-90, 1, 0, 0)
    glTranslatef(0, 0, 3.0)
    gluCylinder(quad, 0.35, 0.35, 0.6, 24, 1)
    glPopMatrix()

    # Musgo fino encima del cilindro
    glPushMatrix()
    glColor3f(0.2, 0.6, 0.2)
    glRotatef(-90, 1, 0, 0)
    glTranslatef(0, 0, 3.6)
    gluDisk(quad, 0, 0.36, 24, 1)
    glPopMatrix()


    # Gris claro
    glPushMatrix()
    glTranslatef(1.3, 2.7, 0.0)
    glScalef(2.6, 0.6, 0.71)
    glColor3f(0.85, 0.85, 0.85)
    glutSolidCube(1.0)
    glPopMatrix()

    # Gris un poco más oscuro
    glPushMatrix()
    glTranslatef(1.3, 3.3, 0.0)
    glScalef(2.6, 0.6, 0.71)
    glColor3f(0.75, 0.75, 0.75)
    glutSolidCube(1.0)
    glPopMatrix()

    # Musgo fino arriba del rectángulo
    glPushMatrix()
    glTranslatef(1.3, 3.6, 0.0)
    glScalef(2.6, 0.01, 0.72)
    glColor3f(0.2, 0.6, 0.2)
    glutSolidCube(1.0)
    glPopMatrix()

    glPopMatrix()

def dibujar_escaleras_desde_cubo():
    glPushMatrix()
    glTranslatef(1.7,2.4,-0.5)
    glRotatef(180, 0, 1, 0)
    glScalef(0.4,0.7,0.3)
    # =========================
    # CUBO / PLATAFORMA PRINCIPAL
    # =========================
    glPushMatrix()
    glTranslatef(0.0, 0.6, 0.0)
    glScalef(1.6, 1.2, 1.6)
    glColor3f(0.75, 0.75, 0.75)
    glutSolidCube(1.0)
    glPopMatrix()

    # =========================
    # LÁMINA DE MUSGO (ENCIMA)
    # =========================
    glPushMatrix()
    glTranslatef(0.0, 1.2, 0.0)   # justo arriba de la cara superior
    glScalef(1.62, 0.01, 1.62)     # mismo tamaño en X y Z
    glColor3f(0.2, 0.6, 0.2)
    glutSolidCube(1.0)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.091,0.15,0)
    # =========================
    # ESCALÓN 1 (NO SE TOCA)
    # =========================
    glPushMatrix()
    glTranslatef(0.0, 0.9, -1)
    glScalef(1.4, 0.3, 0.8)
    glColor3f(0.70, 0.70, 0.70)
    glutSolidCube(1.0)
    glPopMatrix()

    # ESCALÓN 2 (más largo y metido en el cubo)
    glPushMatrix()
    glTranslatef(0.0, 0.6, -1.4)
    glScalef(1.4, 0.3, 1.2)
    glColor3f(0.68, 0.68, 0.68)
    glutSolidCube(1.0)
    glPopMatrix()

    # ESCALÓN 3
    glPushMatrix()
    glTranslatef(0.0, 0.3, -1.5)
    glScalef(1.4, 0.3, 1.6)
    glColor3f(0.66, 0.66, 0.66)
    glutSolidCube(1.0)
    glPopMatrix()

    # ESCALÓN 4
    glPushMatrix()
    glTranslatef(0.0, 0.0, -1.8)
    glScalef(1.4, 0.3, 2.0)
    glColor3f(0.64, 0.64, 0.64)
    glutSolidCube(1.0)
    glPopMatrix()

    glPopMatrix()

    glPopMatrix()

def dibujar_campanita_mario():
    glPushMatrix()
    glTranslatef(0,2.5,0)
    glScalef(0.2,0.2,0.2)
    # =========================
    # CUERPO DE LA CAMPANA
    # =========================
    glPushMatrix()
    glTranslatef(0.0, 0.6, 0.0)
    glScalef(1.3, 1.7, 1.3)
    glColor3f(0.95, 0.85, 0.2)
    glutSolidSphere(0.6, 24, 24)
    glPopMatrix()

    # =========================
    # BOCA
    # =========================
    glPushMatrix()
    glTranslatef(0.0, 0.22, 0.0)
    glScalef(1.6, 1.0, 1.6)
    glRotatef(90, 1, 0, 0)
    glColor3f(0.9, 0.75, 0.15)
    glutSolidTorus(0.3, 0.4, 5, 30)
    glPopMatrix()

    # =========================
    # ARO SUPERIOR
    # =========================
    glPushMatrix()
    glTranslatef(0.0, 1.6, 0.0)
    glScalef(0.7, 1.0, 0.7)
    glColor3f(0.85, 0.65, 0.1)
    glutSolidTorus(0.06, 0.18, 20, 30)
    glPopMatrix()

    # =========================
    # Bola Blanca inferior
    # =========================
    glPushMatrix()
    glTranslatef(0.0, 0.05, 0.0)
    glColor3f(1, 1, 1)
    glutSolidSphere(0.58, 24, 24)
    glPopMatrix()

    # =========================
    # OJOS (al frente)
    # =========================

    # Ojo izquierdo
    glPushMatrix()
    glTranslatef(-0.18, 0.75, 0.85)   # X, Y, Z (frente)
    glScalef(0.15, 0.35, 0.15)        # alargado en Y
    glColor3f(0, 0, 0)
    glutSolidSphere(1.0, 16, 16)
    glPopMatrix()

    # Ojo derecho
    glPushMatrix()
    glTranslatef(0.18, 0.75, 0.85)
    glScalef(0.15, 0.35, 0.15)
    glColor3f(0, 0, 0)
    glutSolidSphere(1.0, 16, 16)
    glPopMatrix()

    glPopMatrix()

def dibujar_arbol_campana():
    glPushMatrix()
    glTranslatef(2.5,4.1,-1.2)
    glScalef(0.4,0.4,0.4)
    # =========================
    # CUERPO DE LA CAMPANA
    # =========================
    glPushMatrix()
    glTranslatef(0.0, 0.6, 0.0)
    glScalef(1.3, 1.7, 1.3)
    glColor3f(0.6, 0.4, 0.2)
    glutSolidSphere(0.6, 24, 24)
    glPopMatrix()

    # =========================
    # BOCA (COLORES INTERCALADOS)
    # =========================
    distancia = 0.3
    for i in range(6):
        glPushMatrix()
        glTranslatef(0.0, 0.8 - distancia, 0.0)
        glScalef(1.6, 1.0, 1.6)
        glRotatef(90, 1, 0, 0)

        # 🔑 Color intercalado
        if i % 2 == 0:
            glColor3f(0.9, 0.75, 0.15)   # dorado
        else:
            glColor3f(0.6, 0.4, 0.2)     # café medio

        glutSolidTorus(0.3, 0.3, 8, 30)
        glPopMatrix()
        distancia += 0.3

    # =========================
    # Bola Blanca inferior
    # =========================
    glPushMatrix()
    glTranslatef(0.0, -1.4, 0.0)
    glScalef(0.5, 5, 0.5)
    glColor3f(1, 1, 1)
    glutSolidSphere(0.58, 24, 24)
    glPopMatrix()

    glPopMatrix()

def dibujar_rampa_cafe_3d():
    glPushMatrix()

    glBegin(GL_TRIANGLES)

    # =========================
    # CARA SUPERIOR INCLINADA (CAFÉ MEDIO)
    # =========================
    glColor3f(0.6, 0.4, 0.2)
    glVertex3f(-1.0, 1.0, 0.0)
    glVertex3f( 1.0, 1.0, 0.0)
    glVertex3f( 1.0, 0.0, -2.0)

    glVertex3f(-1.0, 1.0, 0.0)
    glVertex3f( 1.0, 0.0, -2.0)
    glVertex3f(-1.0, 0.0, -2.0)

    # =========================
    # CARA INFERIOR (CAFÉ CLARO)
    # =========================
    glColor3f(0.75, 0.6, 0.4)
    glVertex3f(-1.0, 0.0, 0.0)
    glVertex3f( 1.0, 0.0, 0.0)
    glVertex3f( 1.0, 0.0, -2.0)

    glVertex3f(-1.0, 0.0, 0.0)
    glVertex3f( 1.0, 0.0, -2.0)
    glVertex3f(-1.0, 0.0, -2.0)

    # =========================
    # CARA FRONTAL
    # =========================
    glColor3f(0.75, 0.6, 0.4)
    glVertex3f(-1.0, 0.0, 0.0)
    glVertex3f( 1.0, 0.0, 0.0)
    glVertex3f( 1.0, 1.0, 0.0)

    glVertex3f(-1.0, 0.0, 0.0)
    glVertex3f( 1.0, 1.0, 0.0)
    glVertex3f(-1.0, 1.0, 0.0)

    # =========================
    # CARA TRASERA
    # =========================
    glColor3f(0.75, 0.6, 0.4)
    glVertex3f(-1.0, 0.0, -2.0)
    glVertex3f( 1.0, 0.0, -2.0)
    glVertex3f( 1.0, 0.0, -2.0)  # base

    glVertex3f(-1.0, 0.0, -2.0)
    glVertex3f( 1.0, 0.0, -2.0)
    glVertex3f(-1.0, 0.0, -2.0)

    # =========================
    # LADO IZQUIERDO
    # =========================
    glColor3f(0.75, 0.6, 0.4)
    glVertex3f(-1.0, 0.0, 0.0)
    glVertex3f(-1.0, 1.0, 0.0)
    glVertex3f(-1.0, 0.0, -2.0)

    # =========================
    # LADO DERECHO
    # =========================
    glVertex3f(1.0, 0.0, 0.0)
    glVertex3f(1.0, 1.0, 0.0)
    glVertex3f(1.0, 0.0, -2.0)

    glEnd()
    glPopMatrix()
    

def dibujar_moneda_mario():
    glPushMatrix()
    glTranslatef(0.2,3.5,-0.5)
    # =========================
    # CUERPO DE LA MONEDA
    # =========================
    glPushMatrix()
    glScalef(1.0, 1.0, 0.2)     # delgada
    glColor3f(1.0, 0.85, 0.2)  # dorado Mario
    glutSolidCylinder(0.6, 0.2, 32, 1)
    glPopMatrix()

    # =========================
    # BORDE (RELIEVE)
    # =========================
    glPushMatrix()
    glTranslatef(0.0, 0.0, 0.0)
    glColor3f(0.9, 0.75, 0.15)
    glutSolidTorus(0.03, 0.6, 20, 40)
    glPopMatrix()

    # =========================
    # CENTRO (RELIEVE SIMPLE)
    # =========================
    glPushMatrix()
    glTranslatef(0.0, 0.0, 0.12)
    glScalef(0.6, 0.6, 0.1)
    glColor3f(0.95, 0.8, 0.2)
    glutSolidSphere(0.4, 20, 20)
    glPopMatrix()

    glPopMatrix()



def dibujo_nivel_1():
    glPushMatrix()
    # Módulo original
    dibujar_cilindro_con_rectangulo()
    # Módulo cruzado (forma X)
    dibujar_cilindro_con_rectangulo_cruzado()
    # Escaleras
    dibujar_escaleras_desde_cubo()
    # Campanita de mario lista
    dibujar_campanita_mario()
    # Arbol que parece campana
    dibujar_arbol_campana()
    #Rampa cafe
    glPushMatrix
    glTranslatef(3,3,2)
    glScalef(0.2,0.8,0.8)
    dibujar_rampa_cafe_3d()
    glPopMatrix
    #Moneda sobre la rampa
    glPushMatrix()
    glScalef(1,0.3,1)
    dibujar_moneda_mario()
    glPopMatrix()

    glPopMatrix()


#--------------------------------------------------- configuracion -----------------------------------------
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(zoom, 800/600, 0.1, 100.0)  # Usar zoom variable
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    # Calcular dirección de la cámara basada en rotaciones
    rad_y = math.radians(camRotY)
    rad_x = math.radians(camRotX)
    
    # Calcular punto al que mira la cámara
    look_x = camX + math.sin(rad_y) * math.cos(rad_x)
    look_y = camY + math.sin(rad_x)
    look_z = camZ - math.cos(rad_y) * math.cos(rad_x)
    
    # Configurar la vista de la cámara
    gluLookAt(camX, camY, camZ,  # Posición de la cámara
              look_x, look_y, look_z,  # Punto al que mira
              0.0, 1.0, 0.0)      # Vector "arriba"
    
    # Actualizar posición de las luces en relación con la cámara
    glLightfv(GL_LIGHT0, GL_POSITION, [camX, camY + 10.0, camZ, 1.0])  # Luz sigue a la cámara desde arriba
    glLightfv(GL_LIGHT1, GL_POSITION, [camX, camY + 5.0, camZ + 10.0, 1.0])  # Luz frontal relativa
    
    # Dibujar ejes de referencia
    glDisable(GL_LIGHTING)
    glLineWidth(2.0)
    
    glBegin(GL_LINES)
    # Eje X (rojo)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(3.0, 0.0, 0.0)
    
    # Eje Y (verde)
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 3.0, 0.0)
    
    # Eje Z (azul)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, 3.0)
    glEnd()
    
    glEnable(GL_LIGHTING)
    
    # -----------------------------Aqui va para que dibuje-----------------------------------
    dibujo_nivel_1()
    
    # ---------------------------------------------------------------------------------------
    # Mostrar información en pantalla
    glDisable(GL_LIGHTING)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 600)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glColor3f(1.0, 1.0, 1.0)  # Texto blanco para mejor visibilidad
    glRasterPos2f(10, 580)
    
    info = f"Pos: ({camX:.1f}, {camY:.1f}, {camZ:.1f}) Zoom: {zoom:.1f}° Rot: ({camRotX:.1f}, {camRotY:.1f})"
    for char in info:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(char))
    
    # Instrucciones
    instructions = [
        "CASA DE TOAD - Super Mario",
        "Controles Movimiento:",
        "W: Subir (Y+)  S: Bajar (Y-)",
        "A: Izquierda (X-)  D: Derecha (X+)",
        "Controles Rotacion:",
        "Q: Rotar Izq  E: Rotar Der",
        "R: Mirar Arriba  F: Mirar Abajo",
        "Rueda: Zoom In/Out  1: Reset"
    ]
    
    for i, line in enumerate(instructions):
        glRasterPos2f(10, 550 - i * 20)
        for char in line:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(char))
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_LIGHTING)

    glutSwapBuffers()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b'Casa de Toad - Super Mario')
    
    init()
    glutDisplayFunc(display)
    glutKeyboardFunc(teclado)
    glutMouseFunc(mouse)  # Registrar función del mouse
    glutIdleFunc(display)  # Para actualizar continuamente
    
    glutMainLoop()

if __name__ == "__main__":
    main()
