import pygame

pygame.mixer.init()

move_sound = pygame.mixer.Sound('assets/sounds/move_sound.wav')
capture_sound = pygame.mixer.Sound('assets/sounds/capture_sound.wav')
check_sound = pygame.mixer.Sound('assets/sounds/check_sound.wav')
promote_sound = pygame.mixer.Sound('assets/sounds/promote_sound.wav')
castling_sound = pygame.mixer.Sound('assets/sounds/castling_sound.wav')
horse_sound = pygame.mixer.Sound('assets/sounds/horse_sound.wav')
king_sound = pygame.mixer.Sound('assets/sounds/king_sound.wav')

def play_sound(sound_type):
    if sound_type == "move":
        move_sound.play()
    elif sound_type == "capture":
        capture_sound.play()
    elif sound_type == "check":
        check_sound.play()
    elif sound_type == "promote":
        promote_sound.play()
    elif sound_type == "castle":
        castling_sound.play()
    elif sound_type == "horse":
        horse_sound.play()
    elif sound_type == "king":
        king_sound.play()
        
