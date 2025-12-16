def dibujar_estrella():
    """chupala sergio"""
    glPushMatrix()
    
    # Parámetros de la estrella (igual que el original)
    num_puntas = 5
    radio_ext = 1.0
    radio_int = 0.4
    profundidad = 0.15
    
    # Calcular todos los vértices (alternando externos e internos)
    vertices_front = []
    vertices_back = []
    
    for i in range(num_puntas * 2):
        angulo = (math.pi * 2 * i) / (num_puntas * 2) - math.pi / 2
        if i % 2 == 0:
            radio = radio_ext
        else:
            radio = radio_int
        
        x = radio * math.cos(angulo)
        y = radio * math.sin(angulo)
        vertices_front.append([x, y, profundidad])
        vertices_back.append([x, y, -profundidad])
    
    # Color dorado
    glColor3f(1.0, 0.84, 0.0)
    
    # Dibujar cara frontal usando triangulación en abanico desde el centro
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0, 0, profundidad)  # Centro
    for v in vertices_front:
        glVertex3f(v[0], v[1], v[2])
    glVertex3f(vertices_front[0][0], vertices_front[0][1], vertices_front[0][2])  # Cerrar
    glEnd()
    
    # Dibujar cara trasera
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0, 0, -profundidad)  # Centro
    for v in reversed(vertices_back):
        glVertex3f(v[0], v[1], v[2])
    glVertex3f(vertices_back[-1][0], vertices_back[-1][1], vertices_back[-1][2])  # Cerrar
    glEnd()
    
    # Dibujar lados (conectar frente con atrás)
    glBegin(GL_QUAD_STRIP)
    for i in range(len(vertices_front)):
        glVertex3f(vertices_front[i][0], vertices_front[i][1], vertices_front[i][2])
        glVertex3f(vertices_back[i][0], vertices_back[i][1], vertices_back[i][2])
    # Cerrar el strip
    glVertex3f(vertices_front[0][0], vertices_front[0][1], vertices_front[0][2])
    glVertex3f(vertices_back[0][0], vertices_back[0][1], vertices_back[0][2])
    glEnd()
    
    # Ojos (esferas negras) - AHORA USANDO glutSolidSphere
    glColor3f(0.0, 0.0, 0.0)
    
    # Ojo izquierdo
    glPushMatrix()
    glTranslatef(-0.2, -0.1, profundidad + 0.05)
    glutSolidSphere(0.08, 16, 16)
    glPopMatrix()
    
    # Ojo derecho
    glPushMatrix()
    glTranslatef(0.2, -0.1, profundidad + 0.05)
    glutSolidSphere(0.08, 16, 16)
    glPopMatrix()
    
    glPopMatrix()
