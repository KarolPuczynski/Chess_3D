from OpenGL.GLUT import *
from camera import Camera
from inputhandler import InputHandler
from chesslogic import ChessLogic
from render import Render
from scenesetup import setup_scene

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BACKGROUND_COLOR = (0.1, 0.3, 0.1, 1.0)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b"Chess Board 3D")
    
    models = setup_scene()
    camera = Camera()
    chess_logic = ChessLogic(models)
    render = Render(models, camera)
    input_handler = InputHandler(camera, chess_logic)
    
    render.init_gl(BACKGROUND_COLOR)
    
    glutDisplayFunc(render.display)
    glutReshapeFunc(camera.setup_projection)
    glutMouseFunc(input_handler.mouse)
    glutMotionFunc(input_handler.motion)
    glutKeyboardFunc(input_handler.keyboard)
    
    glutMainLoop()

if __name__ == "__main__":
    main()