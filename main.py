import pygame
from const import *
from game import *

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Chess fake 3D")



while True:
    
    drawing_chessboard(screen)
    draw_pieces(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Lewy przycisk myszy
                mouse_pos = pygame.mouse.get_pos()  # Pobiera pozycję kursora
                print(f"Lewy klik na pozycji: {mouse_pos}")
                # tutaj możesz wywołać swoją funkcję, np.:
                drawing_chessboard(screen)


    pygame.display.update()  # Update the display