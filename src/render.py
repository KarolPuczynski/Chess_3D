from OpenGL.GL import *
from OpenGL.GLUT import glutSwapBuffers

class Render:
    def __init__(self, models, camera):
        self.models = models
        self.camera = camera

    def init_gl(self, background_color):
        glClearColor(*background_color)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, [0, 1, 1, 0])

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.camera.update_view()
        
        for model in self.models:
            glPushMatrix()
            glTranslatef(*model.position)
            glCallList(model.obj_model.gl_list)
            glPopMatrix()
        
        glutSwapBuffers()