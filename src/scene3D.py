import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from const import *

def scene_lightning():
    pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
    pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 16)
    glEnable(GL_MULTISAMPLE)

    glClearColor(*BACKGROUND_COLOR_3D)

    glLightfv(GL_LIGHT0, GL_POSITION, (-40, 200, 100, 0.0))     # GL_Light 0
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.4, 0.4, 0.4, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, (0.1, 0.1, 0.1, 1.0))

    glMaterialfv(GL_FRONT, GL_SPECULAR, (0.6, 0.6, 0.6, 1.0))
    glMaterialfv(GL_FRONT, GL_SHININESS, 70)

    glLightfv(GL_LIGHT1, GL_POSITION, (0, 50, 0, 1.0))          # GL_Light1
    glLightfv(GL_LIGHT1, GL_AMBIENT, (0.15, 0.15, 0.15, 1.0))
    glLightfv(GL_LIGHT1, GL_DIFFUSE, (0.1, 0.1, 0.1, 1.0))
    glLightfv(GL_LIGHT1, GL_SPECULAR, (0, 0, 0, 1.0))

    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_NORMALIZE)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, WINDOW_WIDTH_3D / float(WINDOW_HEIGHT_3D), 3.0, 100.0)
    glMatrixMode(GL_MODELVIEW)

def rotate(tx, ty, rx, ry, rz, zpos):
    glTranslate(tx / 20., ty / 20., -zpos)
    glRotate(ry, 1, 0, 0)
    glRotate(rx, 0, 1, 0)
    glRotate(rz, 0, 0, 1)

    
