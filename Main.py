import Client
from MainClasses import *
import time
import pygame
import math

# Constants/Initializations
RESOLUTION = (800, 600)
SCREEN = pygame.display
DRAW = pygame.draw
CLOCK = pygame.time.Clock()
FPS = 60
WAIT_FOR_SECONDS = 0.05
MAX_PLAYERS = 2

# Variables
start_game = False
playerSize = 50
positionX, positionY = Client.player.getPosition()
position = [positionX, positionY]
remote_pos_x, remote_pos_y = Client.player.getPosition()
previousPosition = []
local_rotation = Client.player.get_rotation()
remote_rotation = Client.player.get_rotation()
moveSpeed = 7
moveRight = False
moveLeft = False
moveUp = False
moveDown = False
playedIdle = True
playedRun = False
sent_state = False
update_rotation = False
previous_state = ''
players_in_game = 0
wait = 0
start_time = 0

# Movement Normalizing
offset = math.sqrt((moveSpeed * moveSpeed) * 2) - moveSpeed

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
sky_blue = (134, 236, 255)
colors = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (0, 0, 0)
]

# Client Connection
Client.connect_to_server()
if(Client.player.getPlayableState()):
    start_game = True

# Display Settings
display = SCREEN.set_mode(RESOLUTION)
SCREEN.set_caption('Multiplayer Game')

# Player (Robot)
local_renderer = pygame.sprite.Group()
remote_renderer = pygame.sprite.Group()
localPlayer = MainPlayer('Idle', positionX, positionY, local_rotation)
remotePlayer = MainPlayer('Idle', remote_pos_x, remote_pos_y, remote_rotation)
local_renderer.add(localPlayer)
remote_renderer.add(remotePlayer)

# Buttons
server_start = Button(50, 100, white, 10, 10, 'Start Server', antialiasing=True)
server_end = Button(100, 200, white, 50, 50, 'End Server', antialiasing=True)
welcome = Button(50, 200, white, 500, 500, 'Welcome', antialiasing=True)

# Game Loop
while(start_game):

    players_in_game = Client.count[0]

    display.fill(sky_blue)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start_game = False
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                if local_rotation != 'right':
                    local_rotation = 'right'
                    update_rotation = True
                playedRun = True
                sent_state = False
                moveRight = True
                playedIdle = False
            elif event.key == pygame.K_d and event.key == pygame.K_w:
                sent_state = False
                playedRun = True
                update_rotation = False
                moveRight = True
                moveUp = True
                playedIdle = False
            elif event.key == pygame.K_d and event.key == pygame.K_s:
                sent_state = False
                moveRight = True
                playedRun = True
                update_rotation = False
                moveDown = True
                playedIdle = False
            elif event.key == pygame.K_a:
                if local_rotation != 'left':
                    local_rotation = 'left'
                    update_rotation = True
                sent_state = False
                playedRun = True
                moveLeft = True
                playedIdle = False
            elif event.key == pygame.K_a and event.key == pygame.K_w:
                sent_state = False
                moveLeft = True
                playedRun = True
                update_rotation = False
                moveUp = True
                playedIdle = False
            elif event.key == pygame.K_a and event.key == pygame.K_s:
                sent_state = False
                moveLeft = True
                update_rotation = False
                moveDown = True
                playedRun = True
                playedIdle = False
            elif event.key == pygame.K_w:
                sent_state = False
                moveUp = True
                update_rotation = False
                playedRun = True
                playedIdle = False
            elif event.key == pygame.K_s:
                sent_state = False
                update_rotation = False
                moveDown = True
                playedRun = True
                playedIdle = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                moveRight = False
            elif event.key == pygame.K_a:
                moveLeft = False
            elif event.key == pygame.K_w:
                moveUp = False
            elif event.key == pygame.K_s:
                moveDown = False

    if(not moveRight and not moveLeft and not moveDown and not moveUp and not playedIdle):
        localPlayer.update_rotation(local_rotation)
        localPlayer.set_state('Idle')
        sent_state = False
        playedIdle = True
    elif (moveRight or moveDown or moveLeft or moveUp):
        if update_rotation:
            localPlayer.update_rotation(local_rotation)
        if playedRun:
            localPlayer.set_state('Run')
            playedRun = False
        update_rotation = False
    
    if(not sent_state):
        current_state = localPlayer.get_state()
        if current_state != previous_state:
            Client.send_msg(f'#{current_state}')
            previous_state = current_state
        sent_state = True


    positionX, positionY = localPlayer.Move(moveRight, moveLeft, moveUp, moveDown, positionX, positionY, moveSpeed, offset)

    position = [positionX, positionY]

    if(position != previousPosition and players_in_game > 1):
        previousPosition = position
        Client.send_pos(position)

    if(players_in_game == MAX_PLAYERS):
        remote_pos_x, remote_pos_y = Client.player.getPosition()
        if(Client.player.get_animPlayable()):
            remotePlayer.set_state(Client.player.get_state())
            Client.player.set_animPlayable(False)
        remotePlayer.update_position(remote_pos_x, remote_pos_y)
        remote_renderer.draw(display)

    localPlayer.update_position(positionX, positionY)
    
    if start_time < time.time():
        localPlayer.update_image()
        remotePlayer.update_image()
        start_time = (time.time() + WAIT_FOR_SECONDS)

    local_renderer.draw(display)

    CLOCK.tick(FPS)
    SCREEN.update()

pygame.quit()
Client.close_connection()