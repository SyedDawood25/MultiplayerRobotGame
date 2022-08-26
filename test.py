import pygame, os, time

pygame.init()

class Player(pygame.sprite.Sprite):

    def __init__(self, state, posX, posY) -> None:

        super().__init__()

        self.state = state
        self.anim_stage = 0
        self.player_size = 150
        self.posX = posX
        self.posY = posY

        self.idle = []
        self.run = []
        self.slide = []
        self.jump = []
        self.shoot = []
        self.melee = []
        self.dead = []

        for i in range(10):
            self.image = pygame.image.load(os.path.join('PythonNetworking', 'Resources', 'PlayerIdle', f'Idle ({i+1}).png'))
            self.image = pygame.transform.scale(self.image, (self.player_size, self.player_size))
            self.idle.append(self.image)
        for i in range(8):
            self.image = pygame.image.load(os.path.join('PythonNetworking', 'Resources', 'PlayerRun', f'Run ({i+1}).png'))
            self.image = pygame.transform.scale(self.image, (self.player_size, self.player_size))
            self.run.append(self.image)
        for i in range(10):
            self.image = pygame.image.load(os.path.join('PythonNetworking', 'Resources', 'PlayerSlide', f'Slide ({i+1}).png'))
            self.image = pygame.transform.scale(self.image, (self.player_size, self.player_size))
            self.slide.append(self.image)
        for i in range(10):
            self.image = pygame.image.load(os.path.join('PythonNetworking', 'Resources', 'PlayerJump', f'Jump ({i+1}).png'))
            self.image = pygame.transform.scale(self.image, (self.player_size, self.player_size))
            self.jump.append(self.image)
        for i in range(4):
            self.image = pygame.image.load(os.path.join('PythonNetworking', 'Resources', 'PlayerShoot', f'Shoot ({i+1}).png'))
            self.image = pygame.transform.scale(self.image, (self.player_size, self.player_size))
            self.shoot.append(self.image)
        for i in range(8):
            self.image = pygame.image.load(os.path.join('PythonNetworking', 'Resources', 'PlayerMelee', f'Melee ({i+1}).png'))
            self.image = pygame.transform.scale(self.image, (self.player_size, self.player_size))
            self.melee.append(self.image)
        for i in range(10):
            self.image = pygame.image.load(os.path.join('PythonNetworking', 'Resources', 'PlayerDead', f'Dead ({i+1}).png'))
            self.image = pygame.transform.scale(self.image, (self.player_size, self.player_size))
            self.dead.append(self.image)
        
        self.states = {
            'Idle':self.idle, 
            'Run':self.run, 
            'Slide':self.slide, 
            'Jump':self.jump, 
            'Shoot':self.shoot, 
            'Melee':self.melee, 
            'Dead':self.dead
            }
        
        self.current_state = self.states[state]
        self.image = self.current_state[self.anim_stage]

        self.rect = self.image.get_rect()
        self.rect.topleft = [self.posX, self.posY]
    
    def update_image(self):
        self.anim_stage += 1

        if self.anim_stage >= len(self.current_state):
            if self.state == 'Jump':
                self.set_state('Idle')
            self.anim_stage = 0
        
        self.image = self.current_state[self.anim_stage]
    
    def set_state(self, state):
        self.anim_stage = 0
        self.state = state
        self.current_state = self.states[state]
        self.image = self.current_state[self.anim_stage]

        self.rect = self.image.get_rect()
        self.rect.topleft = [self.posX, self.posY]

    def get_state(self) -> str:
        return self.state
    
    def get_image(self) -> object:
        return self.image

DISPLAY = pygame.display
WINDOW = DISPLAY.set_mode((800, 600))
DISPLAY.set_caption('TEST GAME')
CLOCK = pygame.time.Clock()
FPS = 60
WAIT_FOR_SECONDS = 0.05

# Variables
player_sprites = pygame.sprite.Group()
white = (255, 255, 255)
posX = 150
posY = 80
start_time = 0

player = Player('Idle', posX, posY)
player_sprites.add(player)
testing = True


while testing:

    WINDOW.fill(white)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            testing = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                player.set_state('Run')
            if event.key == pygame.K_a:
                player.set_state('Run')
            if event.key == pygame.K_s:
                player.set_state('Run')
            if event.key == pygame.K_w:
                player.set_state('Run')
            if event.key == pygame.K_SPACE:
                player.set_state('Jump')
        elif event.type == pygame.KEYUP:
            if player.get_state() != 'Jump':
                player.set_state('Idle')

    player_sprites.draw(WINDOW)

    if start_time < time.time():
        player.update_image()
        start_time = (time.time() + WAIT_FOR_SECONDS)

    DISPLAY.update()
    CLOCK.tick(FPS)
    

pygame.quit()