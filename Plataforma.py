#MODELO 6 PLATAFORMA
def draw_mario_platform():
    glPushMatrix()

    # plataforma cuadro aplastado
    glColor3f(1.0, 0.9, 0.2)
    glScalef(1.51, 0.2, 1.51)
    glutSolidCube(1.0)

    glPopMatrix()


    glColor3f(0.50, 0.30, 0.0)

    posiciones = [-1.50, -0.75, 0.0, 0.75, 1.50]

    # borde frontal rectangulos
    for x in posiciones:
        glPushMatrix()
        glScalef(0.40, 0.20, 1)
        glTranslatef(x, 0.08, 0.56)
        glutSolidCube(0.40)
        glPopMatrix()

    # borde trasero
    for x in posiciones:
        glPushMatrix()
        glScalef(0.40, 0.20, 1)
        glTranslatef(x, 0.08, -0.56)
        glutSolidCube(0.40)
        glPopMatrix()

    # borde derecho
    for z in posiciones:
        glPushMatrix()
        glScalef(1, 0.20, 0.40)
        glTranslatef(0.56, 0.08, z)
        glutSolidCube(0.40)
        glPopMatrix()

    # borde izquierdo
    for z in posiciones:
        glPushMatrix()
        glScalef(1, 0.20, 0.40)
        glTranslatef(-0.56, 0.08, z)
        glutSolidCube(0.40)
        glPopMatrix()
