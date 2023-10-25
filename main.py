import sys
import pygame
import random
import json
import engine


WIDTH, HEIGHT = 1200, 800
pygame.init()
fps_clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Factory")
view = "world"

Render = engine.RenderManagement(screen)

camera_movespeed = 5
camera_scalespeed = 0.5
sprite_convayor_belt = engine.Sprite(srcDirectory="assets/sprites/convayor_belt/",secperframe=0.5)
sprite_convayor_belt.LoadAutomaticly()

while True:

	keys = pygame.key.get_pressed()
	screen.fill((255,255,255))
	sprite_convayor_belt.Update()

	if view == "world":
		Render.RenderRect(20,20,50,50,False)
		Render.RenderRect(80,20,50,50,(150,0,0),True)
		Render.RenderText("sample text",200,200,24)

		Render.RenderSprite(sprite_convayor_belt,100,250,50,50)
		Render.RenderSprite(sprite_convayor_belt,100,300,50,50)
		Render.RenderSprite(sprite_convayor_belt,100,350,50,50)

		if keys[pygame.K_w]:
			Render.camera.MoveCamera("up",camera_movespeed)

		if keys[pygame.K_s]:
			Render.camera.MoveCamera("down",camera_movespeed)

		if keys[pygame.K_a]:
			Render.camera.MoveCamera("left",camera_movespeed)

		if keys[pygame.K_d]:
			Render.camera.MoveCamera("right",camera_movespeed)

		if keys[pygame.K_o]:
			Render.camera.ChangeScale(screen,"less",5)
		
		if keys[pygame.K_p]:
			Render.camera.ChangeScale(screen,"more",5)

		if keys[pygame.K_r]:
			Render.camera.Reset()

		if keys[pygame.K_i]:
			Render.ShowDebug()


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
			
		if event.type == pygame.MOUSEWHEEL:
			if event.y == -1:
				Render.camera.ChangeScale("less",camera_scalespeed)
			elif event.y == 1:
				Render.camera.ChangeScale("more",camera_scalespeed)


	pygame.display.flip()
	fps_clock.tick(60)
