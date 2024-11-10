import sys
import random

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np

def startup():
    update_viewport(None, 600, 600)
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
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(*v1)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(*v2)
    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(*v3)
    glEnd()


# Funkcja rysująca ostrosłup kwadratowy
def draw_pyramid(vertices):
    # Podstawa - dwa dopełniające się trójkąty
    draw_triangle(vertices[0], vertices[1], vertices[2])
    draw_triangle(vertices[0], vertices[2], vertices[3])

    # Ściany boczne ostrosłupa
    draw_triangle(vertices[0], vertices[1], vertices[4])
    draw_triangle(vertices[1], vertices[2], vertices[4])
    draw_triangle(vertices[2], vertices[3], vertices[4])
    draw_triangle(vertices[3], vertices[0], vertices[4])


# Funkcja rekurencyjna do generowania ostrosłupa Sierpińskiego
def sierpinski_3d(vertices, level):
    if level == 0:
        draw_pyramid(vertices)
    else:
        # Punkty środkowe dla krawędzi podstawy kwadratu
        midpoints_base = [
            (vertices[0] + vertices[1]) / 2,
            (vertices[1] + vertices[2]) / 2,
            (vertices[2] + vertices[3]) / 2,
            (vertices[3] + vertices[0]) / 2
        ]

        # Środek podstawy
        center_base = (vertices[0] + vertices[1] + vertices[2] + vertices[3]) / 4

        # Punkty środkowe - leżące w połowie wysokościc ostrosłupa
        top_0 = (vertices[0] + vertices[4]) / 2
        top_1 = (vertices[1] + vertices[4]) / 2
        top_2 = (vertices[2] + vertices[4]) / 2
        top_3 = (vertices[3] + vertices[4]) / 2

        # Cztery narożne ostrosłupy
        sierpinski_3d([vertices[0], midpoints_base[0], center_base, midpoints_base[3], top_0], level - 1)
        sierpinski_3d([midpoints_base[0], vertices[1], midpoints_base[1], center_base, top_1], level - 1)
        sierpinski_3d([center_base, midpoints_base[1], vertices[2], midpoints_base[2], top_2], level - 1)
        sierpinski_3d([midpoints_base[3], center_base, midpoints_base[2], vertices[3], top_3], level - 1)

        # Centralny ostrosłup
        sierpinski_3d([top_0, top_1, top_2, top_3, vertices[4]], level - 1)


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    spin(time * 180 / 3.1415)
    axes()

    vertices = np.array([
        [-3.0, -3.0, -2.5],
        [3.0, -3.0, -2.5],
        [3.0, 3.0, -2.5],
        [-3.0, 3.0, -2.5],
        [0.0, 0.0, 6.0*np.sqrt(2)-2.5]
    ])
    sierpinski_3d(vertices, 3)

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
