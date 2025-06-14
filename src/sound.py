import pygame

pygame.mixer.init()

move_sound = pygame.mixer.Sound('assets/sounds/move_sound.wav')
capture_sound = pygame.mixer.Sound('assets/sounds/capture_sound.wav')
check_sound = pygame.mixer.Sound('assets/sounds/check_sound.wav')
promote_sound = pygame.mixer.Sound('assets/sounds/promote_sound.wav')
castling_sound = pygame.mixer.Sound('assets/sounds/castling_sound.wav')
horse_sound = pygame.mixer.Sound('assets/sounds/horse_sound.wav')
game_end_sound = pygame.mixer.Sound('assets/sounds/game-end_sound.wav')

sound_dict = {
    "move": move_sound,
    "capture": capture_sound,
    "check": check_sound,
    "promote": promote_sound,
    "castle": castling_sound,
    "horse": horse_sound,
    "game_end": game_end_sound
}

def play_sound(sound_type):
    sound = sound_dict.get(sound_type)
    sound.play()