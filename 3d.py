import pygame
import random
import math

pygame.init()

window_size_x = 960
window_size_y = 720

window_half_x = window_size_x/2
window_half_y = window_size_y/2

window_size = (window_size_x,window_size_y)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("3d game")

clock = pygame.time.Clock()

tile_size_x = 16
tile_size_y = 16

world_size_x = 128
world_size_y = 128

texture_size_x = 64
texture_size_y = 64

tile_colors = [(255,0,0), (0,0,225),(228,230,168)]
floor_color = (158, 132, 99)
ceiling_color = (249, 244, 206)
map_color = (255,255,255)

ray_color = (255,255,255)
player_color = (255,0,0)

player_x = 1
player_y = 1


step_x = 0
step_y = 0

player_size = 2

dir = 0
player_dir = 0
player_speed = 50

click_w = False
click_s = False
click_a = False
click_d = False


click_left = False
click_right = False

mouse_down = False

tile_select = 0

hud = False

#world_data = [[2 if x == 0 or x == world_size_x-1 or y == 0 or y == world_size_y-1 else 0 for x in range(world_size_x)] for y in range(world_size_y)]
world_data = [[3 if random.randint(0,4) == 4 else 0 for x in range(world_size_x)] for y in range(world_size_y)]

depth_list = []

# Makes the floor and ceiling textures
"""
celing_surf = pygame.Surface((1,3))
floor_surf = pygame.Surface((1,3))

celing_surf.set_at((0,0), ceiling_color)
celing_surf.set_at((0,1), (ceiling_color[0]/2, ceiling_color[1]/2, ceiling_color[2]/2))
celing_surf.set_at((0,2), (0,0,0))

floor_surf.set_at((0,0), (0,0,0))
floor_surf.set_at((0,1), (floor_color[0]/2, floor_color[1]/2, floor_color[2]/2))
floor_surf.set_at((0,2), floor_color)

gradient_celing_surf = pygame.transform.smoothscale(celing_surf, (window_size_x, window_half_y))
gradient_floor_surf = pygame.transform.smoothscale(floor_surf, (window_size_x, window_half_y))
"""

wall_image = pygame.image.load("wall.png")

# Used for spritesheets and animation (Credits to Coding with Russ)
def get_image(sheet, frame, width, height, scale_x, scale_y, color):
	image = pygame.Surface((width, height))
	image.blit(sheet, (0,0), ((frame* width),0, width, height))
	image = pygame.transform.scale(image, (width * scale_x, height * scale_y))
	image.set_colorkey(color)

	return image.convert_alpha()


while True:
    dt = clock.tick(60)/1000

    mouse = pygame.mouse.get_pos()
    mouse_x, mouse_y = mouse[0], mouse[1]

    player_tile_x = math.floor(player_x)//tile_size_x
    player_tile_y = math.floor(player_y)//tile_size_y


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                click_w = True
            if event.key == pygame.K_s:
                click_s = True
            if event.key == pygame.K_a:
                click_a = True
            if event.key == pygame.K_d:
                click_d = True
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
            if event.key == pygame.K_a:
                click_a = False
            if event.key == pygame.K_d:
                click_d = False
            if event.key == pygame.K_LEFT:
                click_left = False
            if event.key == pygame.K_RIGHT:
                click_right = False

        if hud == True:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False

    past_player_x = float(player_x)
    past_player_y = float(player_y)
                
    player_dir = dir*(math.pi/180)

    if click_w == True:
        player_x += math.cos(player_dir)*(player_speed*dt)
        player_y += math.sin(player_dir)*(player_speed*dt)
    if click_s == True:
        player_x -= math.cos(player_dir)*(player_speed*dt)
        player_y -= math.sin(player_dir)*(player_speed*dt)
    if click_a == True:
        player_x += math.cos(player_dir-(math.pi/2))*(player_speed*dt)
        player_y += math.sin(player_dir-(math.pi/2))*(player_speed*dt)
    if click_d == True:
        player_x += math.cos(player_dir+(math.pi/2))*(player_speed*dt)
        player_y += math.sin(player_dir+(math.pi/2))*(player_speed*dt)



    if click_left == True:
        dir -= 2
    if click_right == True:
        dir += 2

    if mouse_down == True:
        mouse_block_x = round((mouse_x-window_half_x)+player_x)//tile_size_x
        mouse_block_y = round((mouse_y-window_half_y)+player_y)//tile_size_y

        if mouse_block_y < world_size_y and mouse_block_y >= 0:
            if mouse_block_x < world_size_x and mouse_block_x >= 0:
                world_data[mouse_block_y][mouse_block_x] = tile_select
 

    if dir > 360:
        dir = 0
    if dir < 0:
        dir = 360

    if player_tile_x < world_size_y and player_tile_y >= 0:
        if player_tile_x < world_size_x and player_tile_x >= 0:


            # The position of the player in a tile from 0 - 16
            player_local_tile_pos_x = player_x-(player_tile_x*tile_size_x)
            player_local_tile_pos_y = player_y-(player_tile_y*tile_size_y)

            # Checks if the player goes out of the bounds of the world and fixes their position
            if player_tile_y == 0 and player_local_tile_pos_y < 1:
                player_y = float(past_player_y)
            if player_tile_y == world_size_y-1 and player_local_tile_pos_y > tile_size_y-1:
                player_y = float(past_player_y)

            if player_tile_x == 0 and player_local_tile_pos_x < 1:
                player_x = float(past_player_x)
            if player_tile_x == world_size_x-1 and player_local_tile_pos_x > tile_size_x-1:
                player_x = float(past_player_x)

            # Checks if a player has hit the side of a block and fixes their position
            if not player_tile_y == 0:
                if not world_data[player_tile_y-1][player_tile_x] == 0 and player_local_tile_pos_y < 1:
                    player_y = float(past_player_y)

            if not player_tile_y == world_size_y-1:
                if not world_data[player_tile_y+1][player_tile_x] == 0 and player_local_tile_pos_y > tile_size_y-1:
                    player_y = float(past_player_y)

            if not player_tile_x == 0:
                if not world_data[player_tile_y][player_tile_x-1] == 0 and player_local_tile_pos_x < 1:
                    player_x = float(past_player_x)

            if not player_tile_x == world_size_x-1:
                if not world_data[player_tile_y][player_tile_x+1] == 0 and player_local_tile_pos_x > tile_size_x-1:
                    player_x = float(past_player_x)

                
    if tile_select > 3:
        tile_select = 0
    if tile_select < 0:
        tile_select = 3

    # Draws the floor and ceiling gradients
    screen.fill((0,0,0))

    # Blits the happy background
    #pygame.draw.rect(screen, (0,0,255), (0,0,window_size_x,window_half_y))
    #pygame.draw.rect(screen, (0,255,0), (0,window_half_y,window_size_x,window_size_y))

    # Blits the gradient background
    """
    screen.blit(gradient_celing_surf, (0,0))
    screen.blit(gradient_floor_surf, (0,window_half_y))
    """
    # Blits the backrooms background
    pygame.draw.rect(screen, ceiling_color, (0,0,window_size_x,window_half_y))
    pygame.draw.rect(screen, floor_color, (0,window_half_y,window_size_x,window_size_y))
    

    # Raycaster
    lines = []
    ray_lines = []
    circles = []
    for x in range(240):
        ray_x = 0
        ray_y = 0

        side_hit = 0

        d = math.radians(dir+((x*0.375)-45))

        
        if math.cos(d) > 0:
            step_x = 1
        else:
            step_x = -1

        if math.sin(d) > 0:
            step_y = -1
        else:
            step_y = 1

        if math.sin(d) == 0:
            delta_y = 10**21
        else:
            delta_y = abs(tile_size_y/math.sin(d))

        if math.cos(d) == 0:
            delta_x = 10**21
        else:
            delta_x = abs(tile_size_x/math.cos(d))

        if step_x == -1:
            side_x = delta_x*((player_x-((player_tile_x)*tile_size_x))/tile_size_x)
        else:
            side_x = delta_x*(1-((player_x-((player_tile_x)*tile_size_x))/tile_size_x))

        if step_y == -1:
            side_y = delta_y*(1-(player_y-((player_tile_y)*tile_size_y))/tile_size_y)
        else:
            side_y = delta_y*(((player_y-((player_tile_y)*tile_size_y))/tile_size_y))
        #print(side_x, side_y)
        
        tile_x = int(player_tile_x)
        tile_y = int(player_tile_y)

        #print(delta_x, delta_y)
        b = 0
        while True:

            if side_y < side_x:
                ray_x = math.cos(d)*side_y
                ray_y = math.sin(d)*side_y

                tile_y -= step_y

                side_y += delta_y
                side_hit = 1
            else:
                ray_x = math.cos(d)*side_x
                ray_y = math.sin(d)*side_x

                tile_x += step_x

                side_x += delta_x
                side_hit = 0
            
            #circles.append((ray_x,ray_y))

            world_ray_x = int(tile_x)
            world_ray_y = int(tile_y)

            
            # math.sqrt(((ray_x)**2)+((ray_y)**2))*math.cos(d-player_dir) < 128 and
            if world_ray_x >= 0 and world_ray_x < world_size_x and world_ray_y >= 0 and world_ray_y < world_size_y:
                final_dif = 0
                if not world_data[world_ray_y][world_ray_x] == 0:

                    texture_x = ((((ray_x+player_x) - (tile_x*tile_size_x)) % tile_size_x)/tile_size_x)*texture_size_x
                    texture_y = ((((ray_y+player_y) - (tile_y*tile_size_y)) % tile_size_y)/tile_size_y)*texture_size_y

                    if side_hit == 1:
                        final_dif = texture_x
                    elif side_hit == 0:
                        final_dif = texture_y

            
                    lines.append((math.sqrt(((ray_x)**2)+((ray_y)**2))*math.cos(d-player_dir), final_dif, world_data[world_ray_y][world_ray_x]))
                    break
            else:
                lines.append((-1,0,0))
                break
            
            if b == 40:
                lines.append((-1,0,0))
                break

            b += 1

        ray_lines.append((ray_x,ray_y))
        

    # Draws the 3D world
    for i in range(len(lines)):
        line_distance = lines[i][0]
        slice_index = lines[i][1]
        tile = lines[i][2]
        if line_distance != -1 and line_distance != 0:
            
            line_height = ((window_size_y/line_distance)*10)

            # For when we used to draw plain colors
            """
            line_color = [tile_color[0]-round(lines[i]*2), tile_color[1]-round(lines[i]*2), tile_color[2]-round(lines[i]*2)]

            for e in range(3):
                if line_color[e] > 255:
                    line_color[e] = 255
                elif line_color[e] < 0:
                    line_color[e] = 0
            """

            #if line_height < 1200:
            img = get_image(wall_image, slice_index+((tile)*64), 1, 64, 4, line_height/64, None)
            screen.blit(img, (i*4, (((-line_height))/2) + window_half_y))


            # For when we used to draw plain colors
            #pygame.draw.line(screen, line_color, (i*4, (-line_height/2) + window_half_y), (i*4, (line_height/2) + window_half_y), 4)

    # Draws the map if the hud is enabled
    if hud == True:
        for y in range(world_size_y):
            for x in range(world_size_x):
                if world_data[y][x] != 0:
                    pygame.draw.rect(screen, tile_colors[world_data[y][x]-1], (((tile_size_x*x)-player_x)+window_half_x,((tile_size_y*y)-player_y)+window_half_y,tile_size_x,tile_size_y))

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
        for ray in ray_lines:
            pygame.draw.line(screen, (ray_color), (window_half_x,window_half_y), (ray[0]+window_half_x, ray[1]+window_half_y), 1)

        """
        for circle in circles:
            pygame.draw.circle(screen, player_color, (circle[0]+window_half_x, circle[1]+window_half_y), 1)
        """

        pygame.draw.circle(screen, player_color, (window_half_x,window_half_y), player_size)
        pygame.draw.line(screen, player_color, (window_half_x,window_half_y), ((math.cos(player_dir)*20)+window_half_x,(math.sin(player_dir)*20)+window_half_y))

        pygame.draw.rect(screen, map_color, ((-player_x)+window_half_x,(-player_y)+window_half_y,tile_size_x*world_size_x,tile_size_y*world_size_y), 4)

    pygame.display.flip()