import pygame
import random
import math

# Incredibly powerful import, must be commented out when not in use 
#import antigravity

pygame.init()

window_size_x = 960
window_size_y = 720

window_half_x = window_size_x/2
window_half_y = window_size_y/2

window_size = (window_size_x,window_size_y)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("3d game")

clock = pygame.time.Clock()

pygame.mouse.set_visible(False)
pygame.event.set_grab(True)


tile_size_x = 16
tile_size_y = 16

world_size_x = 64
world_size_y = 64

texture_size_x = 64
texture_size_y = 64

floor_color = (158, 132, 99)
ceiling_color = (249, 244, 206)
map_color = (255,255,255)

ray_color = (255,255,255)
player_color = (255,0,0)

player_x = 1
player_y = 1

step_x = 0
step_y = 0

player_size = 4
player_speed = 50

dir_x = 1
dir_y = 0

plane_x = 0
plane_y = 1

player_equipped_gun = 0
shoot = False

click_w = False
click_s = False
click_a = False
click_d = False

click_left = False
click_right = False

mouse_down = False

tile_select = [1,1,1,1]
delete = 0

mouse_sensitivity = 0.1

mouse_view = False

hud = False

#world_data = [[2 if x == 0 or x == world_size_x-1 or y == 0 or y == world_size_y-1 else 0 for x in range(world_size_x)] for y in range(world_size_y)]
world_data = [[[9,9,10,9] if random.randint(0,10) == 4 else 0 for x in range(world_size_x)] for y in range(world_size_y)]
#world_data = [[0 for x in range(world_size_x)] for y in range(world_size_y)]

entities = [(random.randint(0,world_size_x*tile_size_x),random.randint(0,world_size_y*tile_size_y), random.randint(0,1), random.randint(0,359)) for i in range(25)]
#entities = [(100,100,1,90)]

depth_list = []

wall_image = pygame.image.load("wall.png")

entity_image = pygame.image.load("Stoic_guy.png")

gun_images = [pygame.image.load("gun1.png"),pygame.image.load("gun2.png"),pygame.image.load("shotgun1.png"),pygame.image.load("shotgun2.png")]

# Used for spritesheets and animation (Credits to Coding with Russ)
def get_image(sheet, frame_x, frame_y, width, height, scale_x, scale_y, color):
	image = pygame.Surface((width, height), pygame.SRCALPHA)
	image.blit(sheet, (0,0), ((frame_x* width),(frame_y* height), width, height))
	image = pygame.transform.scale(image, (width * scale_x, height * scale_y))
	image.set_colorkey(color)

	return image

tile_selection = []
for i in range(11):
    tile_selection.append(get_image(wall_image, i,0, 64,64,1,1, None))

a = 0
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
            if event.key == pygame.K_ESCAPE:
                mouse_view = True

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

            if hud == True:
                if event.key == pygame.K_1:
                    tile_select[0] += 1
                if event.key == pygame.K_2:
                    tile_select[1] += 1
                if event.key == pygame.K_3:
                    tile_select[2] += 1
                if event.key == pygame.K_4:
                    tile_select[3] += 1
                if event.key == pygame.K_SPACE:
                    if delete == 0:
                        delete = 1
                    else:
                        delete = 0
            else:
                if event.key == pygame.K_1:
                    player_equipped_gun = 0
                if event.key == pygame.K_2:
                    player_equipped_gun = 1
                if event.key == pygame.K_3:
                    player_equipped_gun = 2


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

        #,tile_size_x*world_size_x,tile_size_y*world_size_y
        if event.type == pygame.MOUSEBUTTONDOWN:
            if hud == True:
                if event.button == 3:
                    mouse_view = False
            elif hud == False:
                mouse_view = False
                shoot = True
    

        if hud == True:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False

    if mouse_view == False:
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
    else:
        pygame.mouse.set_visible(True)
        pygame.event.set_grab(False)


    past_player_x = float(player_x)
    past_player_y = float(player_y)

    temp_dir_x = float(dir_x)
    temp_dir_y = float(dir_y)

    temp_plane_x = float(plane_x)
    temp_plane_y = float(plane_y)
                

    if click_w == True:
        player_x += dir_x*(player_speed*dt)
        player_y += dir_y*(player_speed*dt)

    if click_s == True:
        player_x -= dir_x*(player_speed*dt)
        player_y -= dir_y*(player_speed*dt)
                    
    if click_a == True:
        player_x += dir_y*(player_speed*dt)
        player_y -= dir_x*(player_speed*dt)

    if click_d == True:
        player_x -= dir_y*(player_speed*dt)
        player_y += dir_x*(player_speed*dt)

    if mouse_view == False:
        delta_mouse_x = pygame.mouse.get_rel()[0]
        final_mouse_change = delta_mouse_x*mouse_sensitivity
        dir_x = math.cos(math.radians(final_mouse_change))*temp_dir_x - math.sin(math.radians(final_mouse_change))*temp_dir_y
        dir_y = math.sin(math.radians(final_mouse_change))*temp_dir_x + math.cos(math.radians(final_mouse_change))*temp_dir_y

        plane_x = math.cos(math.radians(final_mouse_change))*temp_plane_x - math.sin(math.radians(final_mouse_change))*temp_plane_y
        plane_y = math.sin(math.radians(final_mouse_change))*temp_plane_x + math.cos(math.radians(final_mouse_change))*temp_plane_y


    if mouse_down == True and mouse_view == True:
        mouse_block_x = round((mouse_x-window_half_x)+player_x)//tile_size_x
        mouse_block_y = round((mouse_y-window_half_y)+player_y)//tile_size_y

        if mouse_block_y < world_size_y and mouse_block_y >= 0:
            if mouse_block_x < world_size_x and mouse_block_x >= 0:
                if delete == 0:
                    world_data[mouse_block_y][mouse_block_x] = list(tile_select)
                else:
                    world_data[mouse_block_y][mouse_block_x] = 0

    # Keeps the gun image on the shooting image until a certain number of frames have passed
    if shoot == True:
        a += 1
        if player_equipped_gun == 1:
            if a > 10:
                a = 0
                shoot = False
        elif player_equipped_gun == 2:
            if a > 15:
                a = 0
                shoot = False
 

# Player collsion 

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
                if not world_data[player_tile_y-1][player_tile_x] == 0 and player_local_tile_pos_y < player_size:
                    player_y += (player_size-player_local_tile_pos_y)

            if not player_tile_y == world_size_y-1:
                if not world_data[player_tile_y+1][player_tile_x] == 0 and player_local_tile_pos_y > tile_size_y-player_size: 
                    player_y -= (player_size-(tile_size_y-player_local_tile_pos_y))
        

            if not player_tile_x == 0:
                if not world_data[player_tile_y][player_tile_x-1] == 0 and player_local_tile_pos_x < player_size:
                    player_x += (player_size-player_local_tile_pos_x)


            if not player_tile_x == world_size_x-1:
                if not world_data[player_tile_y][player_tile_x+1] == 0 and player_local_tile_pos_x > tile_size_x-player_size:
                    player_x -= (player_size-(tile_size_x-player_local_tile_pos_x))
    print("no")
    # Limits the player's selection to the avalable tiles
    for i in range(4):
        if tile_select[i] > 10:
            tile_select[i] = 1
        if tile_select[i] < 1:
            tile_select[i] = 10


    
    screen.fill((0,0,0))
    
    # Blits the happy background
    pygame.draw.rect(screen, (0,0,255), (0,0,window_size_x,window_half_y))
    pygame.draw.rect(screen, (0,220,30), (0,window_half_y,window_size_x,window_half_y))


    # Raycaster
    lines = []
    ray_lines = []

    depth_list = []

    circles = []
    for x in range(240):
        # Position of the ray initally
        ray_x = 0
        ray_y = 0

        # A value from -1 to 1 which determines the direction the ray will be heading
        camera_x = (x/120) -1

        # The ray vector
        ray_dir_x = dir_x + (plane_x * camera_x)
        ray_dir_y = dir_y + (plane_y * camera_x)

        side_hit = 0

        if ray_dir_x > 0:
            step_x = 1
        else:
            step_x = -1

        if ray_dir_y > 0:
            step_y = -1
        else:
            step_y = 1

        if ray_dir_y == 0:
            delta_y = 10**21
        else:
            delta_y = abs(tile_size_y/ray_dir_y)

        if ray_dir_x == 0:
            delta_x = 10**21
        else:
            delta_x = abs(tile_size_x/ray_dir_x)


        if step_x == -1:
            side_x = delta_x*((player_x-((player_tile_x)*tile_size_x))/tile_size_x)
        else:
            side_x = delta_x*(1-((player_x-((player_tile_x)*tile_size_x))/tile_size_x))

        if step_y == -1:
            side_y = delta_y*(1-(player_y-((player_tile_y)*tile_size_y))/tile_size_y)
        else:
            side_y = delta_y*(((player_y-((player_tile_y)*tile_size_y))/tile_size_y))

        
        tile_x = int(player_tile_x)
        tile_y = int(player_tile_y)


        while True:

            if side_y < side_x:
                ray_x = ray_dir_x*side_y
                ray_y = ray_dir_y*side_y

                tile_y -= step_y

                side_y += delta_y
                side_hit = 1
            else:
                ray_x = ray_dir_x*side_x
                ray_y = ray_dir_y*side_x

                tile_x += step_x

                side_x += delta_x
                side_hit = 0
            
            circles.append((ray_x,ray_y))

            tile_x = int(tile_x)
            tile_y = int(tile_y)

            side = None
            # math.sqrt(((ray_x)**2)+((ray_y)**2))*math.cos(d-player_dir) < 128 and
            if tile_x >= 0 and tile_x < world_size_x and tile_y >= 0 and tile_y < world_size_y:
                
                final_tex_dif = 0
                if not world_data[tile_y][tile_x] == 0:
                    
                    texture_x = ((((ray_x+player_x) - (tile_x*tile_size_x)) % tile_size_x)/tile_size_x)*texture_size_x
                    texture_y = ((((ray_y+player_y) - (tile_y*tile_size_y)) % tile_size_y)/tile_size_y)*texture_size_y

    
                    if side_hit == 1:
                        if round(((ray_y+player_y) - (tile_y*tile_size_y))) == 0:
                            final_tex_dif = texture_size_x-texture_x
                            side = 0
                        else:
                            final_tex_dif = texture_x
                            side = 2

                        perp_wall = side_y - delta_y
                        
                    elif side_hit == 0:
                        
                        if round(((ray_x+player_x) - (tile_x*tile_size_x))) == 0:
                            final_tex_dif = texture_y
                            side = 3
                        else:
                            final_tex_dif = texture_size_y-texture_y
                            side = 1
                        
                        perp_wall = side_x - delta_x


                    depth_list.append(perp_wall)
                    lines.append((perp_wall, final_tex_dif, world_data[tile_y][tile_x], side))
                    break


                elif math.sqrt(((tile_x-player_tile_x)**2)+((tile_y-player_tile_y)**2)) > 25:
                    depth_list.append(10**21)
                    lines.append(None)
                    break

            else:
                depth_list.append(10**21)
                lines.append(None)
                break
            
        ray_lines.append((ray_x,ray_y))

    # Sorts entities from furthest to closest
    entities.sort(reverse=True, key=lambda entity: math.sqrt((entity[0]-player_x)**2 + (entity[1]-player_y)**2))
    
    # Draws the 3D world
    for i in range(240):
        line = lines[i]
        if line != None:
            line_distance = line[0]
            slice_index = line[1]
            tile = line[2]
            side = line[3]

            line_height = (window_size_y/line_distance)*10
            #(sheet, frame, width, height, scale_x, scale_y, color):

            # In order to avoid errors related to getting too close to a wall or other various scaling issues.
            if line_height/64 < 200 and line_height/64 > 0:
                img = get_image(wall_image, slice_index+((tile[side])*64),0, 1, 64, 4, line_height/64, None)

            # Darkens the north and south side of a wall
            if side == 0 or side == 2:
                img.fill((25,25,25),special_flags=pygame.BLEND_RGB_SUB)

            screen.blit(img, (i*4, window_half_y-(line_height/2)))

    
    """
    Entity code. A lot of it was based of Lodev's tutorial so a lot of credit goes to him.
    Also searched up some formulas for the inverse camera matrix and also the formula for 
    transform x and y.
    """
    inverse = 1/(plane_x*dir_y - dir_x * plane_y)

    for entity in entities:
        relative_x = entity[0] - player_x
        relative_y = entity[1] - player_y

        transform_x = inverse * (dir_y*relative_x -dir_x*relative_y)
        transform_y = inverse *(-plane_y*relative_x+plane_x*relative_y)

        screen_x = (window_half_x * (1+ transform_x/transform_y))

        entity_size = abs(int(window_size_y/transform_y))*10

        # Useless since we are bliting an image at a certain (x,y) coordinate with the origin of the drawing in the corner of the slice
        #draw_start_y = (-entity_size/2 + window_size_y/2)//4
        #draw_end_y = (entity_size/2 + window_size_y/2)//4

        draw_start_x = (-entity_size / 2 + screen_x) //4
        draw_end_x = (entity_size / 2 + screen_x) //4

        angle = (entity[3] - math.degrees(math.atan2(dir_y,dir_x)))+22.5

        angle = (angle//45) % 8

        for i in range(int(draw_start_x), int(draw_end_x), 1):

            entity_texture_x = int(256 * (i - draw_start_x) * texture_size_x / entity_size) / 256
            
            if transform_y > 0 and i >= 0 and i < window_size_x//4 and not depth_list[i] < transform_y:
                if entity_size/64 < 200 and entity_size/64 > 0:
                    img = get_image(entity_image, (entity_texture_x*4)+(entity[2]*64),angle, 1, 64, 4, entity_size/64, None).convert_alpha()
                    screen.blit(img, ((i*4), window_half_y-((entity_size/2)*1)))

    # Draws the player's firearm
    if player_equipped_gun == 1:
        if shoot == True:
            gun = gun_images[1]
        else:
            gun = gun_images[0]
    elif player_equipped_gun == 2:
        if shoot == True:
            gun = gun_images[3]
        else:
            gun = gun_images[2]

    if player_equipped_gun != 0:
        screen.blit(gun, (window_half_x-(gun.get_width()/2),window_size_y-(gun.get_height())))

    # Draws the map if the hud is enabled
    if hud == True:
        for y in range(world_size_y):
            for x in range(world_size_x):
                if world_data[y][x] != 0:
                    pygame.draw.rect(screen,(0,0,0), (((tile_size_x*x)-player_x)+window_half_x,((tile_size_y*y)-player_y)+window_half_y,tile_size_x,tile_size_y))


        for ray in ray_lines:
            pygame.draw.line(screen, (ray_color), (window_half_x,window_half_y), (ray[0]+window_half_x, ray[1]+window_half_y), 1)

        for entity in entities:
             pygame.draw.circle(screen, player_color, ((entity[0]+window_half_x)-player_x, (entity[1]+window_half_y)-player_y), 2)
             pygame.draw.line(screen, player_color, ((entity[0]+window_half_x)-player_x,(entity[1]+window_half_y)-player_y), ((math.cos(math.radians(entity[3]))*20)+((entity[0]+window_half_x)-player_x),((entity[1]+window_half_y)-player_y)+(math.sin(math.radians(entity[3]))*20)))

        """
        for circle in circles:
            pygame.draw.circle(screen, player_color, (circle[0]+window_half_x, circle[1]+window_half_y), 1)
        """

        pygame.draw.circle(screen, player_color, (window_half_x,window_half_y), player_size)
        pygame.draw.line(screen, player_color, (window_half_x,window_half_y), ((dir_x*20)+window_half_x,(dir_y*20)+window_half_y))

        pygame.draw.rect(screen, map_color, ((-player_x)+window_half_x,(-player_y)+window_half_y,tile_size_x*world_size_x,tile_size_y*world_size_y), 4)

        for index, tile in enumerate(tile_select):
            screen.blit(tile_selection[tile_select[index]], (index*texture_size_x,0,tile_size_x,tile_size_y))
    
    pygame.display.flip()