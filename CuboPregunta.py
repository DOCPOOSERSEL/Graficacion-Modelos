def dibujar_cubo_pregunta():
    
    glPushMatrix()
    
    tamano = 1.0
    medio = tamano / 2.0
    
    # Color amarillo dorado del cubo
    color_cubo = (0.9, 0.75, 0.2)
    
    # Desplazamiento para el signo de interrogación
    profundidad_signo = medio + 0.02
    
    # ==========================================
    # CARA FRONTAL (Z+)
    # ==========================================
    glBegin(GL_QUADS)
    glColor3f(*color_cubo)
    glNormal3f(0, 0, 1)
    glVertex3f(-medio, -medio, medio)
    glVertex3f(medio, -medio, medio)
    glVertex3f(medio, medio, medio)
    glVertex3f(-medio, medio, medio)
    glEnd()
    
    glPushMatrix()
    glTranslatef(0, 0, profundidad_signo)
    dibujar_signo_interrogacion()
    glPopMatrix()
    
    # ==========================================
    # CARA TRASERA (Z-)
    # ==========================================
    glBegin(GL_QUADS)
    glColor3f(*color_cubo)
    glNormal3f(0, 0, -1)
    glVertex3f(-medio, -medio, -medio)
    glVertex3f(-medio, medio, -medio)
    glVertex3f(medio, medio, -medio)
    glVertex3f(medio, -medio, -medio)
    glEnd()
    
    glPushMatrix()
    glTranslatef(0, 0, -profundidad_signo)
    glRotatef(180, 0, 1, 0)
    dibujar_signo_interrogacion()
    glPopMatrix()
    
    # ==========================================
    # CARA SUPERIOR (Y+)
    # ==========================================
    glBegin(GL_QUADS)
    glColor3f(*color_cubo)
    glNormal3f(0, 1, 0)
    glVertex3f(-medio, medio, -medio)
    glVertex3f(-medio, medio, medio)
    glVertex3f(medio, medio, medio)
    glVertex3f(medio, medio, -medio)
    glEnd()
    
    # ==========================================
    # CARA INFERIOR (Y-)
    # ==========================================
    glBegin(GL_QUADS)
    glColor3f(*color_cubo)
    glNormal3f(0, -1, 0)
    glVertex3f(-medio, -medio, -medio)
    glVertex3f(medio, -medio, -medio)
    glVertex3f(medio, -medio, medio)
    glVertex3f(-medio, -medio, medio)
    glEnd()
    
    # ==========================================
    # CARA DERECHA (X+)
    # ==========================================
    glBegin(GL_QUADS)
    glColor3f(*color_cubo)
    glNormal3f(1, 0, 0)
    glVertex3f(medio, -medio, -medio)
    glVertex3f(medio, medio, -medio)
    glVertex3f(medio, medio, medio)
    glVertex3f(medio, -medio, medio)
    glEnd()
    
    glPushMatrix()
    glTranslatef(profundidad_signo, 0, 0)
    glRotatef(90, 0, 1, 0)
    dibujar_signo_interrogacion()
    glPopMatrix()
    
    # ==========================================
    # CARA IZQUIERDA (X-)
    # ==========================================
    glBegin(GL_QUADS)
    glColor3f(*color_cubo)
    glNormal3f(-1, 0, 0)
    glVertex3f(-medio, -medio, -medio)
    glVertex3f(-medio, -medio, medio)
    glVertex3f(-medio, medio, medio)
    glVertex3f(-medio, medio, -medio)
    glEnd()
    
    glPushMatrix()
    glTranslatef(-profundidad_signo, 0, 0)
    glRotatef(-90, 0, 1, 0)
    dibujar_signo_interrogacion()
    glPopMatrix()
    
    glPopMatrix()
