import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass

def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)

def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-7.5, 0.0, 0.0)
    glVertex3f(7.5, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -7.5, 0.0)
    glVertex3f(0.0, 7.5, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -7.5)
    glVertex3f(0.0, 0.0, 7.5)

    glEnd()

def generate_egg(n):
    tab = np.zeros((n, n, 3))

    # Równomierne rozłożenie wartości dla parametrów u i v
    u_values = np.linspace(0.0, 1.0, n)
    v_values = np.linspace(0.0, 1.0, n)

    # Wypełnianie tablicy współrzędnymi x, y, z dla każdej pary (u, v)
    for i, u in enumerate(u_values):
        for j, v in enumerate(v_values):
            x = (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * np.cos(np.pi * v)
            y = 160 * u ** 4 - 320 * u ** 3 + 160 * u ** 2 - 5
            z = (-90 * u ** 5 + 225 * u ** 4 - 270 * u ** 3 + 180 * u ** 2 - 45 * u) * np.sin(np.pi * v)
            tab[i, j] = [x, y, z]

    return tab

# Globalna zmienna do przechowywania liczby punktow (N x N x 3)
N = 20

def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    spin(time * 180 / 3.1415)

    axes()

    tab = generate_egg(N)

    glColor3f(1.0, 1.0, 0.0)
    glBegin(GL_LINES)

    for i in range(N - 1):
        for j in range(N - 1):

            # Linia pomiędzy (i, j) a (i+1, j)
            glVertex3f(tab[i, j, 0], tab[i, j, 1], tab[i, j, 2])
            glVertex3f(tab[i + 1, j, 0], tab[i + 1, j, 1], tab[i + 1, j, 2])

            # Linia pomiędzy (i, j) a (i, j+1)
            glVertex3f(tab[i, j, 0], tab[i, j, 1], tab[i, j, 2])
            glVertex3f(tab[i, j + 1, 0], tab[i, j + 1, 1], tab[i, j + 1, 2])

    glEnd()


    glFlush()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
