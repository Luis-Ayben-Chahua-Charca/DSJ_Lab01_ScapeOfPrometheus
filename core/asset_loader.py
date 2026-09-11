from pathlib import Path

import pygame
from pygame import mixer

BASE_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = BASE_DIR / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
SOUNDS_DIR = ASSETS_DIR / "sounds"
MUSIC_DIR = ASSETS_DIR / "music"


def load_image(filename):
    return pygame.image.load(str(IMAGES_DIR / filename))


def load_sound(filename):
    return mixer.Sound(str(SOUNDS_DIR / filename))


def music_path(filename):
    return str(MUSIC_DIR / filename)
