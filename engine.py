#### Basicly helper stuff for rendering etc....
import pygame
import random
import json
import os
import time



class RenderManagement:
	def __init__(self,screen):
		self.camera = Camera()
		self.screen = screen
		self.font = pygame.font.SysFont(None, 24)
		self.debug = False

		#self.MoveCamera = self.camera.MoveCamera
		#self.ChangeScale = self.camera.ChangeScale
	
	def Update(self,):
		pass

	#Rendering through this handles cameralocation & Scale
	def RenderImage(self,screen,image,x,y):
		x = x*self.camera.scale
		y = y*self.camera.scale
		screen.blit(pygame.transform.scale(image, (self.camera.scale, self.camera.scale)),(x+self.camera.camera_x,y+self.camera.camera_y))

	def RenderSprite(self,sprite,x:int,y:int,width:int,height:int):
		x = (x*self.camera.scale)+self.camera.camera_x
		y = (y*self.camera.scale)+self.camera.camera_y

		sprite.Draw(
			self.screen,
			x,
			y,
			width*self.camera.scale,
			height*self.camera.scale
		)

	def RenderRect(self,x:int,y:int,width:int,height:int,color,filled=True):
		#Consider a system where when renderign a rect a unique identifier is passed.
		#all rects are then stored in RenderManagement in dict.
		#This let's us move rects by using pygames inbuilt .move-ip() function.
		#This might make fps better when rendering whole screen full of stuff.
		borderW = 2
		if filled:
			borderW = 0

		temp_rect = pygame.Rect(
			(x*self.camera.scale)+self.camera.camera_x,
			(y*self.camera.scale)+self.camera.camera_y,
			width*self.camera.scale,
			height*self.camera.scale
		)
		
		pygame.draw.rect(
			self.screen,
			color,
			temp_rect, 
			borderW
		)
		return temp_rect

		'''
		pygame.draw.rect(
			screen,
			self.colors[node.cellReference.colony],
			pygame.Rect(
				(node.x*self.cellSize+self.cellRenderOffsetX),
				(node.y*self.cellSize+self.cellRenderOffsetY),
				self.cellSize,
				self.cellSize
			)
		)
		'''


	def ShowDebug(self,):
		self.debug = True
		print("Debug: "+str(self.debug))


	def RenderText(self,text,x,y,fontsize=30,basecolor=(0, 0, 0)):
		x = (x*self.camera.scale)+self.camera.camera_x
		y = (y*self.camera.scale)+self.camera.camera_y
		fontsize = int(fontsize*self.camera.scale)
		pygame.font.init()
		font = pygame.font.SysFont('arial', fontsize)
		text = text.split('\n')

		for t in range(len(text)):
			surf = font.render(text[t], False, basecolor)
			self.screen.blit(surf,(x,y+(fontsize*t)))


	#Render string so newlines are used and implement basic color code support.
	def RenderAdvancedText(screen,text,x,y,fontsize=30,basecolor=(0, 0, 0)):

		pygame.font.init()
		font = pygame.font.SysFont('arial', fontsize)
		text = text.split('\n')

		#Loop all text cut by newlines.
		for t in range(len(text)):
			

			#loop all parts of the text by color codes.
			parts = text[t].split('$c')
			for p in range(len(parts)):
				surf = font.render(text[t], False, basecolor)
				screen.blit(surf,(x+(fontsize*p),y+(fontsize*t)))
				#print(parts[p])
				###TODO: Need get lenght of a word and use it's offset for rendering next colored work


			#print(text[t])
			#surf = font.render(text[t], False, basecolor)
			#screen.blit(surf,(x,y+(fontsize*t)))




class Camera():
	def __init__(self,):
		self.camera_x = 0
		self.camera_y = 0
		self.scale = 1

	def MoveCamera(self,direction:str,speed:int=1):
		speed = speed + self.scale #Makes moving camera faster depending on current size.
		match direction:
			case "up":
				self.camera_y += speed

			case "down":
				self.camera_y -= speed

			case "left":
				self.camera_x += speed

			case "right":
				self.camera_x -= speed

			case _:
				return False
		return True

	def ChangeScale(self,direction:str,speed:int=1):
		speed = speed + self.scale/10 #Makes scaling faster depending on current size.
		match direction:
			case "more":
				self.scale += speed

			case "less":
				self.scale -= speed

			case _:
				return False

		if self.scale < 0.1:
			self.scale = 0.1
		return True

	def Reset(self,):
		self.camera_x = 0
		self.camera_y = 0
		self.scale = 1
		print("Render location & Scale reset")
		

class UtilityTools():
	def __init__(self,):
		pass

	def randomChance(self,chance):
		chance = 100 - chance
		temp = random.randrange(0,100)

		if temp >= chance:
			return True
		return False

	def procTest(self,amount):
		proc = 0
		for i in range(amount):
			if self.randomChance(1):
				proc += 1

		print("hit "+str(proc)+" times")
		return proc

	def ReadFile(self,filename):
		with open(filename, 'r') as file:
			data = json.load(file)
		return data

	def WriteFile(self,filename:str,data:any):
		data = json.dumps(data,indent=4)
		with open(filename, 'w') as file:
			file.write(data)




class GameObject():
	def __init__(self,x,y):
		self.x = x
		self.y = y

class Tile(GameObject):
	def __init__(self,x,y,id=0):
		super().__init__(x,y)
		self.size = 25
		self.id = id

	def Render(self,screen):
		global temp_img
		#pygame.draw.rect(screen,(25, 181, 44),(self.x,self.y,self.size,self.size),0)
		screen.blit(temp_img,(self.x,self.y))

	def __repr__(self):
		return "<Tile x={x}, y={y}>".format(x=self.x,y=self.y)

class WorldManager():
	def __init__(self,):
		self.world = {}
		self.size_x = 20
		self.size_y = 20

	def Generate(self,):
		pass
			

class Sprite:
	def __init__(self,size_x:int=0,size_y:int=0,srcDirectory:str="",secperframe=2):
		self.frames = []
		self.currentFrameIndex = 0
		self.currentFrame = None
		self.seconds_per_frame = secperframe
		self.frameTimer = 0

		self.position_x = 0
		self.position_y = 0

		self.srcDirectory = srcDirectory
		self.isPlaying = True

	def LoadManualy(self,srcFiles:list):
		self.frames = srcFiles
		print("Loaded: "+str(len(self.frames))+" files to sprite")


	def LoadAutomaticly(self,):
		for frame in os.listdir(self.srcDirectory):
			self.frames.append(pygame.image.load(self.srcDirectory+frame).convert())
		self.currentFrame = self.frames[0]
		print("Loaded: "+str(len(self.frames))+" files to sprite")

	#Find all possible numbers from the filenames and sort frames
	#With those
	def SmartSortFrames(self,):
		raise NotImplementedError
		
	def resetFrameTimer(self,):
		self.frameTimer = time.time()

	#This should be ran in the programs main loop
	def Update(self,):
		if self.isPlaying:
			timer_current = time.time()
			if (timer_current-self.frameTimer) > self.seconds_per_frame:




				self.resetFrameTimer()
				if self.currentFrameIndex < len(self.frames)-1:
					self.setCurrentFrame()
					self.currentFrameIndex += 1
				else:
					self.setCurrentFrame()
					self.currentFrameIndex = 0


	def Draw(self,screen,x,y,width,height):
		self.position_x = x
		self.position_y = y
		screen.blit(pygame.transform.scale(self.currentFrame, (width, height)),(self.position_x,self.position_y))


	def Play(self,):
		self.isPlaying = True

	def Stop(self,):
		self.isPlaying = False


	def setCurrentFrame(self,index=None):
		if index == None:
			#print("INDEX: "+str(self.currentFrameIndex))
			self.currentFrame = self.frames[self.currentFrameIndex]
		else:
			self.currentFrame = self.frames[index]

	def setMaxFrameTime(self,time):
		self.seconds_per_frame = time

	def getCurrentFrame(self,):
		return self.currentFrame


	def getFrames(self,):
		return self.frames