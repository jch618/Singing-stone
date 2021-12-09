import pygame
from PyQt5.QtCore import Qt

pygame.mixer.init()

white = {'c':'c.wav', 'd':'d.wav', 'e':'e.wav', 'f':'f.wav',
         'g':'g.wav', 'a':'a.wav', 'b':'b.wav', '_c':'_c.wav'}
for i in white:
    musicName = "./music/" + white[i]
    white[i] = pygame.mixer.Sound(musicName)


black = {'c#':'c#.wav', 'd#':'d#.wav', 'f#':'f#.wav', 'g#':'g#.wav',
         'a#':'a#.wav'}

pianoNote = {
    Qt.Key_Z:'c',
    Qt.Key_X:'d',
    Qt.Key_C:'e',
    Qt.Key_V:'f',
    Qt.Key_M:'g',
    Qt.Key_Comma:'a',
    Qt.Key_Period:'b',
    Qt.Key_Slash:'_c',

    Qt.Key_S:'c#',
    Qt.Key_D:'d#',
    Qt.Key_G:'f#',
    Qt.Key_K:'g#',
    Qt.Key_L:'a#'
}


for i in black:
    musicName = "./music/" + black[i]
    black[i] = pygame.mixer.Sound(musicName)
