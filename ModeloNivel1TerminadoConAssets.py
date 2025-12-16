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
