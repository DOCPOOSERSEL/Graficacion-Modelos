def dibujar_campanita_mario():
    glPushMatrix()

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
