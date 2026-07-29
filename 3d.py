import pygame
import random
import math

pygame.init()

window_size = (960,720)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("3d game")

clock = pygame.time.Clock()

tile_size_x = 16
tile_size_y = 16

world_size_x = 32
world_size_y = 32

tile_color = (228,230,168)
floor_color = (168, 142, 109)
ceiling_color = (229, 224, 206)

ray_color = (255,255,255)
player_color = (255,0,0)

player_x = 0
player_y = 0

player_size = 2

dir = 0
player_dir = 0
player_speed = 2

click_w = False
click_s = False

click_left = False
click_right = False

mouse_down = False

tile_select = 0
hud = False

#world_data = [[1 if random.randint(0,5) == 0 else 0 for x in range(world_size_x)] for y in range(world_size_y)]
world_data = [[0 for x in range(world_size_x)] for y in range(world_size_y)]

while True:
    mouse = pygame.mouse.get_pos()
    mouse_x, mouse_y = mouse[0], mouse[1]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                click_w = True
            if event.key == pygame.K_s:
                click_s = True
            if event.key == pygame.K_LEFT:
                click_left = True
            if event.key == pygame.K_RIGHT:
                click_right = True
            if event.key == pygame.K_SPACE:
                tile_select += 1
            if event.key == pygame.K_h:
                if hud ==  True:
                    hud = False
                else:
                    hud = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                click_w = False
            if event.key == pygame.K_s:
                click_s = False
            if event.key == pygame.K_LEFT:
                click_left = False
            if event.key == pygame.K_RIGHT:
                click_right = False

        if hud == True:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
                

    player_dir = dir*(math.pi/180)

    if click_w == True:
        player_x += math.cos(player_dir)*player_speed
        player_y += math.sin(player_dir)*player_speed
    if click_s == True:
        player_x -= math.cos(player_dir)*player_speed
        player_y -= math.sin(player_dir)*player_speed
    if click_left == True:
        dir -= 2
    if click_right == True:
        dir += 2

    if mouse_down == True:
        try:
            world_data[mouse_y//tile_size_y][mouse_x//tile_size_x] = tile_select
        except:
            pass

    if player_dir > 360:
        dir = 0
    if player_dir < 0:
        dir = 360

    if tile_select > 1:
        tile_select = 0
    if tile_select < 0:
        tile_select = 1

    # Draws the floor and ceiling gradients
    screen.fill((0,0,0))
    celing_surf = pygame.Surface((1,3))
    floor_surf = pygame.Surface((1,3))

    celing_surf.set_at((0,0), ceiling_color)
    celing_surf.set_at((0,1), (ceiling_color[0]/2, ceiling_color[1]/2, ceiling_color[2]/2))
    celing_surf.set_at((0,2), (0,0,0))

    floor_surf.set_at((0,0), (0,0,0))
    floor_surf.set_at((0,1), (floor_color[0]/2, floor_color[1]/2, floor_color[2]/2))
    floor_surf.set_at((0,2), floor_color)

    gradient_celing_surf = pygame.transform.smoothscale(celing_surf, (window_size[0], window_size[1]/2))
    gradient_floor_surf = pygame.transform.smoothscale(floor_surf, (window_size[0], window_size[1]/2))

    screen.blit(gradient_celing_surf, (0,0))
    screen.blit(gradient_floor_surf, (0,window_size[1]/2))


    # Raycaster
    lines = []
    ray_lines = []
    for x in range(240):
        ray_x = player_x
        ray_y = player_y
        d = (dir+((x*0.375)-45))*(math.pi/180)

        while True:
            ray_x += (math.cos(d)*1)
            ray_y += (math.sin(d)*1)

            world_ray_x = round(ray_x//tile_size_x)
            world_ray_y = round(ray_y//tile_size_y)

            if world_ray_x >= 0 and world_ray_x < world_size_x and world_ray_y >= 0 and world_ray_y < world_size_y:
                if world_data[world_ray_y][world_ray_x] == 1:
                    lines.append(math.sqrt(((ray_x-player_x)**2)+((ray_y-player_y)**2))* math.cos(d-player_dir))
                    break

            else:
                lines.append(-1)
                break

        ray_lines.append((ray_x, ray_y))

    # Draws the 3D world
    for i in range(len(lines)):
        if lines[i] != -1:
            line_height = ((960/lines[i])*10)

            line_color = [tile_color[0]-round(lines[i]*1.5), tile_color[1]-round(lines[i]*1.5), tile_color[2]-round(lines[i]*1.5)]

            for e in range(3):
                if line_color[e] > 255:
                    line_color[e] = 255
                elif line_color[e] < 0:
                    line_color[e] = 0

            pygame.draw.line(screen, line_color, (i*4, (-line_height/2) + 360), (i*4, (line_height/2) + 360), 4)

    # Draws the map if the Hud is enabled
    if hud == True:
        for y in range(world_size_y):
            for x in range(world_size_x):
                if world_data[y][x] == 1:
                    pygame.draw.rect(screen, tile_color, (tile_size_x*x,tile_size_y*y,tile_size_x,tile_size_y))

        for ray in ray_lines:
            pygame.draw.line(screen, ray_color, (player_x,player_y), (ray[0], ray[1]), 1)

        pygame.draw.circle(screen, player_color, (player_x, player_y), player_size)
        pygame.draw.line(screen, player_color, (player_x, player_y), (player_x + (math.cos(player_dir)*20),player_y+(math.sin(player_dir)*20)))

    pygame.display.flip()

    clock.tick(60)

