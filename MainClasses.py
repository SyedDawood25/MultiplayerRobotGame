import pygame, os

# Initialize pygame
pygame.init()

# Main Player Class
class MainPlayer(pygame.sprite.Sprite):

    def __init__(self, state, posX, posY, rotation) -> None:

        super().__init__()

        self.state = state
        self.anim_stage = 0
        self.player_size = 150
        self.posX = posX
        self.posY = posY
        self.rotation = rotation
        self.current_rotation = self.rotation

        self.idle = []
        self.run = []
        self.slide = []
        self.jump = []
        self.shoot = []
        self.melee = []
        self.dead = []

        for i in range(10):
            try:
                self.image = pygame.image.load(os.path.join('PythonNetworking', 'Resources', 'PlayerIdle', f'Idle ({i+1}).png'))
                self.image = pygame.transform.scale(self.image, (self.player_size, self.player_size))
                if(self.rotation == 'left'):
                    self.image = pygame.transform.flip(self.image, True, False)
                self.idle.append(self.image)
            except:
                self.image = pygame.image.load(os.path.join('Resources', 'PlayerIdle', f'Idle ({i+1}).png'))
                self.image = pygame.transform.scale(self.image, (self.player_size, self.player_size))
                if(self.rotation == 'left'):
                    self.image = pygame.transform.flip(self.image, True, False)
                self.idle.append(self.image)
        for i in range(8):
            try:
                self.image = pygame.image.load(os.path.join('PythonNetworking', 'Resources', 'PlayerRun', f'Run ({i+1}).png'))
                self.image = pygame.transform.scale(self.image, (self.player_size, self.player_size))
                if(self.rotation == 'left'):
                    self.image = pygame.transform.flip(self.image, True, False)
                self.run.append(self.image)
            except:
                self.image = pygame.image.load(os.path.join('Resources', 'PlayerRun', f'Run ({i+1}).png'))
                self.image = pygame.transform.scale(self.image, (self.player_size, self.player_size))
                if(self.rotation == 'left'):
                    self.image = pygame.transform.flip(self.image, True, False)
                self.run.append(self.image)
        for i in range(10):
            try:
                self.image = pygame.image.load(os.path.join('PythonNetworking', 'Resources', 'PlayerSlide', f'Slide ({i+1}).png'))
                self.image = pygame.transform.scale(self.image, (self.player_size, self.player_size))
                if(self.rotation == 'left'):
                    self.image = pygame.transform.flip(self.image, True, False)
                self.slide.append(self.image)
            except:
                self.image = pygame.image.load(os.path.join('Resources', 'PlayerSlide', f'Slide ({i+1}).png'))
                self.image = pygame.transform.scale(self.image, (self.player_size, self.player_size))
                if(self.rotation == 'left'):
                    self.image = pygame.transform.flip(self.image, True, False)
                self.slide.append(self.image)
        for i in range(10):
            try:
                self.image = pygame.image.load(os.path.join('PythonNetworking', 'Resources', 'PlayerJump', f'Jump ({i+1}).png'))
                self.image = pygame.transform.scale(self.image, (self.player_size, self.player_size))
                if(self.rotation == 'left'):
                    self.image = pygame.transform.flip(self.image, True, False)
                self.jump.append(self.image)
            except:
                self.image = pygame.image.load(os.path.join('Resources', 'PlayerJump', f'Jump ({i+1}).png'))
                self.image = pygame.transform.scale(self.image, (self.player_size, self.player_size))
                if(self.rotation == 'left'):
                    self.image = pygame.transform.flip(self.image, True, False)
                self.jump.append(self.image)
        for i in range(4):
            try:
                self.image = pygame.image.load(os.path.join('PythonNetworking', 'Resources', 'PlayerShoot', f'Shoot ({i+1}).png'))
                self.image = pygame.transform.scale(self.image, (self.player_size, self.player_size))
                if(self.rotation == 'left'):
                    self.image = pygame.transform.flip(self.image, True, False)
                self.shoot.append(self.image)
            except:
                self.image = pygame.image.load(os.path.join('Resources', 'PlayerShoot', f'Shoot ({i+1}).png'))
                self.image = pygame.transform.scale(self.image, (self.player_size, self.player_size))
                if(self.rotation == 'left'):
                    self.image = pygame.transform.flip(self.image, True, False)
                self.shoot.append(self.image)
        for i in range(8):
            try:
                self.image = pygame.image.load(os.path.join('PythonNetworking', 'Resources', 'PlayerMelee', f'Melee ({i+1}).png'))
                self.image = pygame.transform.scale(self.image, (self.player_size, self.player_size))
                if(self.rotation == 'left'):
                    self.image = pygame.transform.flip(self.image, True, False)
                self.melee.append(self.image)
            except:
                self.image = pygame.image.load(os.path.join('Resources', 'PlayerMelee', f'Melee ({i+1}).png'))
                self.image = pygame.transform.scale(self.image, (self.player_size, self.player_size))
                if(self.rotation == 'left'):
                    self.image = pygame.transform.flip(self.image, True, False)
                self.melee.append(self.image)
        for i in range(10):
            try:
                self.image = pygame.image.load(os.path.join('PythonNetworking', 'Resources', 'PlayerDead', f'Dead ({i+1}).png'))
                self.image = pygame.transform.scale(self.image, (self.player_size, self.player_size))
                if(self.rotation == 'left'):
                    self.image = pygame.transform.flip(self.image, True, False)
                self.dead.append(self.image)
            except:
                self.image = pygame.image.load(os.path.join('Resources', 'PlayerDead', f'Dead ({i+1}).png'))
                self.image = pygame.transform.scale(self.image, (self.player_size, self.player_size))
                if(self.rotation == 'left'):
                    self.image = pygame.transform.flip(self.image, True, False)
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

    def update_position(self, posX, posY):
        self.posX = posX
        self.posY = posY
        self.rect.topleft = [self.posX, self.posY]

    def update_rotation(self, rotation):
        if rotation != self.current_rotation:
            self.rotation = rotation
            self.current_rotation = self.rotation
            for state in self.states:
                for i in range(len(self.states[state])):
                    image = self.states[state][i]
                    image = pygame.transform.flip(image, True, False)
                    self.states[state][i] = image

    def get_rotation(self) -> str:
        return self.rotation

    def get_position(self) -> list:
        return [self.posX, self.posY]

    def get_state(self) -> str:
        return self.state

    def Move(self, right, left, up, down, posX, posY, moveSpeed, offset):
        if right and not (up or down):
            return (posX + moveSpeed), posY
        elif right and up:
            return (posX + (moveSpeed - offset)), (posY - (moveSpeed - offset))
        elif right and down:
            return (posX + (moveSpeed - offset)), (posY + (moveSpeed - offset))
        elif left and not (up or down):
            return (posX - moveSpeed), posY
        elif left and up:
            return (posX - (moveSpeed - offset)), (posY - (moveSpeed - offset))
        elif left and down:
            return (posX - (moveSpeed - offset)), (posY + (moveSpeed - offset))
        elif up and not (left or right):
            return posX, (posY - moveSpeed)
        elif down and not (left or right):
            return posX, (posY + moveSpeed)
        else:
            return posX, posY

# Buttons Class
class Button:

    def __init__(self, height, width, button_color, posX, posY, text = 'Button', font = 'Arial', font_color = (0, 0, 0), bold = False, italic = False, antialiasing = False) -> None:
        self.height = height
        self.width = width
        if (self.width - self.height) >= 150:
            self.font_size = int((self.width/1.5 - self.height)/3)
            self.divide_width = 4
            self.divide_height = 4.5
        else:
            self.font_size = int((self.width - self.height)/3)
            self.divide_width = 6
            self.divide_height = 3.5
        self.button_color = button_color
        self.text = text
        self.font_color = font_color
        self.text_AA = antialiasing
        self.posX = posX
        self.posY = posY
        self.rect = [posX, posY, self.width, self.height]
        self.font = pygame.font.SysFont(font, self.font_size, bold, italic)

    def instantiate_button(self, display):
        button = pygame.draw.rect(display, self.button_color, self.rect)
        text = self.font.render(self.text, self.text_AA, self.font_color)
        display.blit(text, [self.posX + self.width/self.divide_width, self.posY + self.height/self.divide_height])
