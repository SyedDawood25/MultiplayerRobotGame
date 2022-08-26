import pygame, os

pygame.init()

img = pygame.image.load(os.path.join('PythonNetworking', 'Resources', 'PlayerIdle', 'Idle (1).png'))
img = pygame.transform.scale(img, (150, 150))
img_str = pygame.image.tostring(img, 'RGB')

with open('img.txt', 'bw') as f:
    f.write(img_str)
