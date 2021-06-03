import pygame, sys
from pygame.locals import *

pygame.init()
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()

black_color = (0, 0, 0)
white_color = (255, 255, 255)
grey_color = (25, 25, 25)
red_color = (255, 100, 100)
teal_color = (100, 255, 255)
green_color = (100, 255, 100)

FPS = 12
surface_scale = 10
surface_w, surface_h = 64, 64
window_w, window_h = surface_w * surface_scale, surface_h * surface_scale
surface = pygame.Surface((surface_w, surface_h))
window = pygame.display.set_mode((window_w, window_h))

gameMatrix = [[ 0 for i in range(surface_w)] for j in range(surface_h)]
gameBuffer = [[ 0 for i in range(surface_w)] for j in range(surface_h)]

should_update = False
it = 0

def is_alive(x, y):
    alive_neighbours = 0

    # Check number of alive neighbours
    try:
        if gameMatrix[x - 1][y - 1] == 1: alive_neighbours += 1
        if gameMatrix[x][y - 1] == 1: alive_neighbours += 1
        if gameMatrix[x + 1][y - 1] == 1: alive_neighbours += 1
        if gameMatrix[x - 1][y] == 1: alive_neighbours += 1
        if gameMatrix[x + 1][y] == 1: alive_neighbours += 1
        if gameMatrix[x - 1][y + 1] == 1: alive_neighbours += 1
        if gameMatrix[x][y + 1] == 1: alive_neighbours += 1
        if gameMatrix[x + 1][y + 1] == 1: alive_neighbours += 1

    except:
        return False
        
    # Check state based on 'n' alive
    if gameMatrix[x][y] == 1:
        
        return not (alive_neighbours < 2 or alive_neighbours > 3)

    else:

        return (alive_neighbours == 3)

def reset_game():
    global gameMatrix
    gameMatrix = [[ 0 for i in range(surface_w)] for j in range(surface_h)]

def reset_buffer():
    global gameBuffer
    gameBuffer = [[ 0 for i in range(surface_w)] for j in range(surface_h)]

def update_game():
    global gameBuffer, gameMatrix
    reset_buffer()

    for row in range(len(gameMatrix)):
        for col in range(len(gameMatrix[row])):

            if is_alive(col, row):  
                gameBuffer[col][row] = 1
                
            else:                   
                gameBuffer[col][row] = 0

    gameMatrix = gameBuffer

    #global it    
    #pygame.image.save(window,"gif/" +  str(it) + "_iteration.jpeg")
    #it += 1
                

def pixel(surface, pos, color):
    surface.set_at(pos, color)

def draw_game():
    for row in range(len(gameMatrix)):
        for col in range(len(gameMatrix[row])):
            state = gameMatrix[col][row]
            if state == 1:
                  pixel(surface, (col, row), white_color)
            else: pixel(surface, (col, row), black_color)


while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if pygame.mouse.get_pressed()[0]:
            pos = (int(pygame.mouse.get_pos()[0]/surface_scale), 
                   int(pygame.mouse.get_pos()[1]/surface_scale))
            gameMatrix[pos[0]][pos[1]] = 1
        
        if pygame.mouse.get_pressed()[2]:
            pos = (int(pygame.mouse.get_pos()[0]/surface_scale), 
                   int(pygame.mouse.get_pos()[1]/surface_scale))
            gameMatrix[pos[0]][pos[1]] = 0
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                should_update = not should_update
            if event.key == pygame.K_r:
                should_update = False
                reset_game()
                

    if should_update:
        update_game()

    draw_game()
    window.blit(pygame.transform.scale(surface, window.get_rect().size), (0, 0))
    pygame.display.update()
    clock.tick(FPS)