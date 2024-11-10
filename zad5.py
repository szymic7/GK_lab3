import sys
import random

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


# Funkcja pomocnicza do rysowania trójkąta w trójwymiarze
def draw_triangle(v1, v2, v3):
    glColor3f(random.random(), random.random(), random.random())
    glBegin(GL_TRIANGLES)
    glVertex3f(*v1)
    glVertex3f(*v2)
    glVertex3f(*v3)
    glEnd()


# Funkcja rysująca czworościan, składający się z 4 trójkątów
def draw_tetrahedron(vertices):
    draw_triangle(vertices[0], vertices[1], vertices[2])
    draw_triangle(vertices[0], vertices[1], vertices[3])
    draw_triangle(vertices[0], vertices[2], vertices[3])
    draw_triangle(vertices[1], vertices[2], vertices[3])


# Funkcja rekurencyjna do generowania trójkąta Sierpińskiego w 3D
def sierpinski_3d(vertices, depth):
    if depth == 0:
        draw_tetrahedron(vertices)
    else:
        # Wyznaczenie punktów środkowych dla każdego boku czworościanu
        midpoints = [
            (vertices[0] + vertices[1]) / 2,
            (vertices[0] + vertices[2]) / 2,
            (vertices[0] + vertices[3]) / 2,
            (vertices[1] + vertices[2]) / 2,
            (vertices[1] + vertices[3]) / 2,
            (vertices[2] + vertices[3]) / 2,
        ]

        # 4 nowe czworościany
        sierpinski_3d([vertices[0], midpoints[0], midpoints[1], midpoints[2]], depth - 1)
        sierpinski_3d([vertices[1], midpoints[0], midpoints[3], midpoints[4]], depth - 1)
        sierpinski_3d([vertices[2], midpoints[1], midpoints[3], midpoints[5]], depth - 1)
        sierpinski_3d([vertices[3], midpoints[2], midpoints[4], midpoints[5]], depth - 1)


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    spin(time * 180 / 3.1415)
    axes()

    # Wierzchołki czworościanu
    vertices = np.array([
        [-5.0, -5.0, -5.0],
        [5.0, -5.0, -5.0],
        [0.0, 5.0, -5.0],
        [0.0, 0.0, 5.0]
    ])

    sierpinski_3d(vertices, 4)

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
