import pygame
import random

pygame.mixer.init()

move_sound = pygame.mixer.Sound('assets/sounds/move_sound.wav')
capture_sound = pygame.mixer.Sound('assets/sounds/capture_sound.wav')
check_sound = pygame.mixer.Sound('assets/sounds/check_sound.wav')
promote_sound = pygame.mixer.Sound('assets/sounds/promote_sound.wav')
castling_sound = pygame.mixer.Sound('assets/sounds/castling_sound.wav')
horse_sound = pygame.mixer.Sound('assets/sounds/horse_sound.wav')
king_sound = pygame.mixer.Sound('assets/sounds/king_sound.wav')
game_end_sound = pygame.mixer.Sound('assets/sounds/game-end_sound.wav')
stalemate_sound = pygame.mixer.Sound('assets/sounds/stalemate_sound.wav')
bishop_sound1 = pygame.mixer.Sound('assets/sounds/bishop_sound1.wav')
bishop_sound2 = pygame.mixer.Sound('assets/sounds/bishop_sound2.wav')

sound_dict = {
    "move": move_sound,
    "capture": capture_sound,
    "check": check_sound,
    "promote": promote_sound,
    "castle": castling_sound,
    "horse": horse_sound,
    "king": king_sound,
    "game_end": game_end_sound,
    "stalemate": stalemate_sound,
    "bishop": [bishop_sound1, bishop_sound2]
}

def play_sound(sound_type):
    sound = sound_dict.get(sound_type)
    if sound_type == "bishop":
        sound = random.choice(sound)
    sound.play()
