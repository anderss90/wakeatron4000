import pygame
import pygame.mixer
import os
pygame.mixer.init()

name = os.path.join('music','gladiator.mp3')
print name

pygame.mixer.music.load(name)

pygame.mixer.music.play()
while True:
     a = 1
