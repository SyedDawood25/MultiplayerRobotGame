import pygame

pygame.init()

with open('img.txt', 'br') as f:
    img_str = f.read()

img = pygame.image.fromstring(img_str, (150, 150), 'RGB')

display = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    
    display.blit(img, (250, 250))

    pygame.display.update()
    clock.tick(30)
