import pygame
import math
from options import*


def drawWindow(window, distance, wallColor):
    window.fill(BLUE)
    pygame.draw.rect(window, GREEN, (0, HEIGHT/2, WIDTH, HEIGHT))
    idpx = 0
    for pixel in distance:
        height = (HEIGHT*7)/pixel        
        pygame.draw.rect(window, wallColor, (idpx*SCALE, HEIGHT/2-height+20, SCALE+1, height))
        idpx += 1
        
def drawMinimap(window, units, angle, player):
    window.fill(GREEN)
    for unit in units:
        if unit == player:
            pygame.draw.circle(window, (255, 0, 0), (unit.x+5, unit.y+5), unit.w/2)
        else:
            pygame.draw.rect(window, BRICK, unit)
    pygame.draw.arc(window, (255, 0, 170), (player.x-30, player.y-30, player.w+60, player.h+60), angle-RAD30, angle+RAD30, width=2)

pygame.init()

window = pygame.display.set_mode((WIDTH, HEIGHT))
minimap = pygame.Surface((150, 150))
clock = pygame.time.Clock()
running = True

angle = RAD90

Wall1 = pygame.Rect(110, 40, 30, 5)
Wall2 = pygame.Rect(40, 40, 40, 10)
Wall3 = pygame.Rect(120, 70, 10, 40)
playerPos = [70, 70, 10, 10]
player = pygame.Rect(playerPos)
minimapUnits = [player, Wall1, Wall2, Wall3]
render = [Wall1, Wall2, Wall3]
frame = 0
wallColor = COLORS[14]



while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #getting input
    keys = pygame.key.get_pressed()
    transform = [0, 0]
    if keys[pygame.K_w]: 
        transform[1] -= math.sin(angle)
        transform[0] += math.cos(angle)
    if keys[pygame.K_s]:
        transform[1] += math.sin(angle)
        transform[0] -= math.cos(angle)
    if keys[pygame.K_a]:
        transform[0] -= math.sin(angle)
        transform[1] -= math.cos(angle)
    if keys[pygame.K_d]:
        transform[0] += math.sin(angle)
        transform[1] += math.cos(angle)
    if keys[pygame.K_q]:
        angle += PI/180
    if keys[pygame.K_e]:
        angle -= PI/180
    if keys[pygame.K_r]:
        angle = RAD90
        player.x, player.y = 70, 70

    #Checking Collision
    collisionTop, collisionBottom, collisionLeft, collisionRight = False, False, False, False

    #Checking collision with the screen borders
    if player.x <= 0 and transform[0] < 0:
        collisionLeft = True
    if player.x + player.w >= 150 and transform[0] > 0:
        collisionRight = True
    if player.y <= 0 and transform[1] < 0:
        collisionTop = True
    if player.y + player.h >= 150 and transform[1] > 0:
        collisionBottom = True

    #Checking collision with the walls
    for wall in render:
        #Top
        if player.y == (wall.y + wall.h):
            if (player.x + player.w) > wall.x and player.x < (wall.x + wall.w) and transform[1] < 0:
                collisionTop = True
        #Bottom
        if (player.y + player.h) == wall.y:
           if (player.x + player.w) > wall.x and player.x < (wall.x + wall.w) and transform[1] > 0:
               collisionBottom = True
        #Left
        if player.x == (wall.x + wall.w):
            if(player.y + player.h) > wall.y and player.y < (wall.y + wall.h) and transform[0] < 0:
                collisionRight = True
        #Right
        if (player.x + player.h) == wall.x:
            if(player.y + player.h) > wall.y and player.y < (wall.y + wall.h) and transform[0] > 0:
                collisionRight = True

    if collisionRight or collisionLeft:
        transform[0] = 0
    if collisionTop or collisionBottom:
        transform[1] = 0
    #Transforming the player
    player.x += transform[0]
    player.y += transform[1]
    #Casting the rays
    distanceToWalls = [None]
    for angleR in range(-30, 30):
        foundWall = False
        for pixel in range(1, 215):
            working = True
            ray = pygame.Rect((math.cos(angle + (PI/180)*angleR)*pixel) + player.x, -(math.sin(angle + (PI/180)*angleR)*pixel) + player.y, 1, 1)
            for wall in render:
                if ray.colliderect(wall):
                    foundWall = True
                    dist = pixel/math.cos((angle + (PI/180)*angleR))
                    distanceToWalls.insert(0, pixel)
                    working = False
            if working == False:
                break
        if foundWall == False:
            distanceToWalls.insert(0, -1)
    del(distanceToWalls[len(distanceToWalls)-1])
    drawWindow(window, distanceToWalls, wallColor)
    drawMinimap(minimap, minimapUnits, angle, player)
    window.blit(minimap, (0, 0))
    pygame.display.update()

    clock.tick(FPS)