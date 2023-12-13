import sys
import pygame
# import random
# import json
import engine

WIDTH, HEIGHT = 1200, 800
pygame.init()
fps_clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
view = "world"

Render = engine.RenderManagement(screen)

camera_movespeed = 5
camera_scalespeed = 0.5
sprite_convayor_belt = engine.Sprite(srcDirectory="assets/sprites/convayor_belt/", secperframe=0.5)
sprite_convayor_belt.LoadAutomaticly()

image_uibox_box = pygame.image.load("assets/gui/UiBox/box.png").convert()

path = engine.Path()
path.add_point(50, 0)
path.add_point(250, 0)
path.add_point(250, 250)
path.add_point(150, 150)
path.add_point(50, 300)

animation = engine.Animation(sprite_convayor_belt, path)

wm = engine.WorldManager()

wm.create_chunk(0, 0)
wm.create_chunk(1, 0)
wm.create_chunk(0, 1)
wm.create_chunk(3, 1)

temp_tile = engine.Tile(1,0)


print(wm.get_holder(5, 5))
wm.add_tile(temp_tile,5,5)
print(wm.get_holder(5, 5))




#wm.create_chunk(0, 2)
#wm.create_chunk(1, 2)
#wm.create_chunk(2, 2)
#wm.create_chunk(0, 3)

gui = engine.Gui(Render)
temp_element = engine.UiBox()
gui.add_element(temp_element)
# print(wm.chunks[(0,0)].data)


while True:

    keys = pygame.key.get_pressed()
    screen.fill((255, 255, 255))
    sprite_convayor_belt.Update()
    animation.update()

    if view == "world":
        # gui.render(screen, )
       # Render.render_image(screen, image_uibox_box, 0, 0, 20, 20)

        #Render.render_rect(20,20,50,50,False)
        #Render.render_rect(80,20,50,50,(150,0,0),True)
        #Render.render_text("sample text",200,200,24)

        #Render.render_sprite(sprite_convayor_belt,100,250,50,50)
        #Render.render_sprite(sprite_convayor_belt,100,300,50,50)
        #Render.render_sprite(sprite_convayor_belt,100,350,50,50)

        #Render.render_animation(animation,400,300)
        #Render.render_path(path,250,50)

        Render.render_world_manager(wm,600,600)

        if keys[pygame.K_w]:
            Render.camera.MoveCamera("up", camera_movespeed)

        if keys[pygame.K_s]:
            Render.camera.MoveCamera("down", camera_movespeed)

        if keys[pygame.K_a]:
            Render.camera.MoveCamera("left", camera_movespeed)

        if keys[pygame.K_d]:
            Render.camera.MoveCamera("right", camera_movespeed)

        if keys[pygame.K_o]:
            Render.camera.ChangeScale(screen, "less", 5)

        if keys[pygame.K_p]:
            Render.camera.ChangeScale(screen, "more", 5)

        if keys[pygame.K_r]:
            Render.camera.Reset()

        if keys[pygame.K_i]:
            Render.show_debug()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEWHEEL:
            if event.y == -1:
                Render.camera.ChangeScale("less", camera_scalespeed)
            elif event.y == 1:
                Render.camera.ChangeScale("more", camera_scalespeed)

    pygame.display.flip()
    pygame.display.set_caption("Engine | " + str(int(fps_clock.get_fps())))
    fps_clock.tick(60)
