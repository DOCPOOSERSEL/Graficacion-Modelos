def dibujar_cilindro_quadric(radio, altura, slices=32, stacks=8):
    glPushMatrix()
    glRotatef(-90, 1, 0, 0)

    gluCylinder(quad, radio, radio, altura, slices, stacks)

    # Tapa inferior
    glPushMatrix()
    glRotatef(180, 1, 0, 0)
    gluDisk(quad, 0, radio, slices, 1)
    glPopMatrix()

    # Tapa superior
    glPushMatrix()
    glTranslatef(0, 0, altura)
    gluDisk(quad, 0, radio, slices, 1)
    glPopMatrix()

    glPopMatrix()


def dibujar_puerta_u():
    glPushMatrix()

    glTranslatef(0, 0.5, 2.02)
    glScalef(1.0, 1.5, 1.0)

    glColor3f(0.45, 0.22, 0.08)
    gluDisk(quad, 0.0, 0.75, 32, 1)

    glTranslatef(0, 0, 0.01)
    glColor3f(0.65, 0.35, 0.15)
    gluDisk(quad, 0.0, 0.6, 32, 1)

    glPopMatrix()




def dibujar_techo_champinon():
    glPushMatrix()
    glTranslatef(0, 3.0, 0)

    glColor3f(1.0, 0.0, 0.0)
    gluSphere(quad, 2.3, 32, 32)

    glTranslatef(0, -0.7, 0)
    glColor3f(0.95, 0.95, 0.95)
    gluCylinder(quad, 1.7, 1.7, 0.5, 32, 1)

    glPopMatrix()


def dibujar_manchas_techo():
    glPushMatrix()
    glTranslatef(0, 3.0, 0)  # misma base del techo

    glColor3f(1.0, 1.0, 1.0)

    radio_techo = 2.3
    radio_mancha = 1.0

    # 4 manchas alrededor (ligeramente enterradas)
    manchas = [
        (0.0, 0.6,  radio_techo - 0.9),   # frente
        (0.0, 0.6, -radio_techo + 0.9),   # atrás
        ( radio_techo - 0.9, 0.6, 0.0),   # derecha
        (-radio_techo + 0.9, 0.6, 0.0),   # izquierda
    ]

    for x, y, z in manchas:
        glPushMatrix()
        glTranslatef(x, y, z)
        gluSphere(quad, radio_mancha, 16, 16)
        glPopMatrix()

    glPushMatrix()
    glTranslatef(0, radio_techo - 0.7, 0)
    gluSphere(quad, 1, 16, 16)
    glPopMatrix()

    glPopMatrix()


def dibujar_chimenea():
    glPushMatrix()
    glTranslatef(1.4, 3.8, -0.8)

    glColor3f(0.6, 0.6, 0.6)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(quad, 0.25, 0.25, 1.5, 4, 1)

    glTranslatef(0, 0, 1.5)
    gluDisk(quad, 0, 0.3, 4, 1)

    glPopMatrix()



def dibujar_casa_toad():
    # Cuerpo
    glColor3f(0.85, 0.75, 0.6)
    dibujar_cilindro_quadric(2.0, 3.0)

    # Detalles
    dibujar_puerta_u()
    dibujar_techo_champinon()
    dibujar_manchas_techo()
    dibujar_chimenea()
