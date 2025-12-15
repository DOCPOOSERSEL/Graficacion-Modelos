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

    # =========================
    # ➕ CAPAS EXTRA CILINDRO
    # =========================

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


    # =========================
    # ➕ CAPAS EXTRA RECTÁNGULO
    # =========================

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
    glScalef(0.3,0.7,0.3)
    # =========================
    # CUBO / PLATAFORMA PRINCIPAL
    # =========================
    glPushMatrix()
    glTranslatef(0.0, 0.6, 0.0)
    glScalef(1.6, 1.2, 1.6)
    glColor3f(0.75, 0.75, 0.75)
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


def dibujo_nivel_1():
    glPushMatrix()
    # Módulo original
    dibujar_cilindro_con_rectangulo()
    # Módulo cruzado (forma X)
    dibujar_cilindro_con_rectangulo_cruzado()
    #Escaleras
    dibujar_escaleras_desde_cubo()
    glPopMatrix()
