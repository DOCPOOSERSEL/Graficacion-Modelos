import math

import cv2
import glfw
from assets import Assets
from config import *
from controlador import HandController
from niveles import NivelMundo
from OpenGL.GL import *
from OpenGL.GLU import *

# Estado Global
window = None
controlador = None
niveles = []
nivel_actual = None
indice_nivel = 0
tiempo = 0.0

# Estado Cámara (Suavizado)
cam_radio = 24.0
cam_angulo = 0.0
cam_altura = 16.0


def input_callback(window, key, scancode, action, mods):
    """Manejador de eventos de teclado."""
    global indice_nivel, nivel_actual

    # Selector de Niveles
    if action == glfw.PRESS:
        if len(niveles) > 1:
            if key == glfw.KEY_1:
                indice_nivel = 0
            elif key == glfw.KEY_2 and len(niveles) > 1:
                indice_nivel = 1
            elif key == glfw.KEY_3 and len(niveles) > 2:
                indice_nivel = 2
            nivel_actual = niveles[indice_nivel]

    # Delegar input al nivel activo
    if nivel_actual:
        nivel_actual.input_teclado(key, action)


def mouse_button_callback(window, button, action, mods):
    """Manejador de eventos de mouse."""
    if action == glfw.PRESS and button == glfw.MOUSE_BUTTON_LEFT:
        if hasattr(nivel_actual, "click_mouse"):
            nivel_actual.click_mouse()


def resize(window, width, height):
    """Callback de redimensionado de ventana."""
    if height == 0:
        height = 1
    glViewport(0, 0, width, height)
    if nivel_actual:
        nivel_actual.configurar_camara()


def init_sistema():
    """Inicialización de GLFW, Ventana y OpenGL."""
    global window
    if not glfw.init():
        return False
    glfw.window_hint(glfw.SAMPLES, 4)
    window = glfw.create_window(WIDTH, HEIGHT, WINDOW_TITLE, None, None)
    if not window:
        glfw.terminate()
        return False
    glfw.make_context_current(window)
    glfw.set_key_callback(window, input_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_window_size_callback(window, resize)

    # Configuración OpenGL (Luces, Niebla, Depth)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_NORMALIZE)
    glLightfv(GL_LIGHT0, GL_POSITION, (10, 40, 10, 0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.6, 0.6, 0.6, 1.0))
    glEnable(GL_FOG)
    glFogi(GL_FOG_MODE, GL_LINEAR)
    glFogfv(GL_FOG_COLOR, C_CIELO)
    glFogf(GL_FOG_START, 30.0)
    glFogf(GL_FOG_END, 90.0)
    glClearColor(*C_CIELO)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Carga de recursos (Inicializar Assets (Quadrics, Agua))
    Assets.init_opengl()

    return True


def main():
    global tiempo, cam_radio, cam_angulo, cam_altura, niveles, nivel_actual, controlador

    if not init_sistema():
        return

    # Setup inicial de componentes
    controlador = HandController()
    niveles = [NivelMundo()]
    nivel_actual = niveles[0]
    resize(window, WIDTH, HEIGHT)

    # Bucle Principal
    while not glfw.window_should_close(window):
        # Lógica de Control (Manos)
        frame_debug = controlador.procesar()

        target_r = controlador.target_radio
        target_a = controlador.target_angulo
        target_h = controlador.target_altura

        # Interpolación de cámara (Smooth movement)
        tiempo += 0.03
        cam_radio += (target_r - cam_radio) * 0.1
        cam_angulo += (target_a - cam_angulo) * 0.1
        cam_altura += (target_h - cam_altura) * 0.1

        # Renderizado (OpenGL)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        nivel_actual.configurar_camara()

        # Posicionamiento de cámara orbital
        if isinstance(nivel_actual, NivelMundo):
            camX = math.sin(cam_angulo) * cam_radio
            camZ = math.cos(cam_angulo) * cam_radio
            gluLookAt(camX, cam_altura, camZ, 0, 2, 0, 0, 1, 0)

        nivel_actual.dibujar(tiempo)

        glfw.swap_buffers(window)
        glfw.poll_events()

        # Interfaz de Depuración (OpenCV)
        if frame_debug is not None:
            cv2.imshow("Control Manos", frame_debug)
            if cv2.waitKey(1) & 0xFF == 27:
                break

    controlador.cerrar()
    cv2.destroyAllWindows()
    glfw.terminate()


if __name__ == "__main__":
    main()
