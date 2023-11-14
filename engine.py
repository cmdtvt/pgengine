#### Basicly helper stuff for rendering etc....
import pygame
import random
import json
import os
import time
import numpy as np


class RenderManagement:
    def __init__(self, screen):
        self.camera = Camera()
        self.screen = screen
        self.font = pygame.font.SysFont(None, 24)
        self.debug = True

    # self.MoveCamera = self.camera.MoveCamera
    # self.ChangeScale = self.camera.ChangeScale

    def update(self, ):
        pass

    # Rendering through this handles cameralocation & Scale
    def render_image(self, screen, image, x: int, y: int, width: int = None, height: int = None):
        if width is None:
            width = image.get_width()
        if height is None:
            height = image.get_height()

        x = (x * self.camera.scale) + self.camera.camera_x
        y = (y * self.camera.scale) + self.camera.camera_y

        temp_img = pygame.transform.scale(image, (width * self.camera.scale, height * self.camera.scale))

        screen.blit(temp_img, (x, y))

    def render_sprite(self, sprite, x: int, y: int, width: int, height: int):
        x = (x * self.camera.scale) + self.camera.camera_x
        y = (y * self.camera.scale) + self.camera.camera_y

        sprite.Draw(
            self.screen,
            x,
            y,
            width * self.camera.scale,
            height * self.camera.scale
        )

    def render_rect(self, x: int, y: int, width: int, height: int, color, filled=True):
        # Consider a system where when renderign a rect a unique identifier is passed.
        # all rects are then stored in RenderManagement in dict.
        # This let's us move rects by using pygames inbuilt .move-ip() function.
        # This might make fps better when rendering whole screen full of stuff.
        borderW = 2
        if filled:
            borderW = 0

        temp_rect = pygame.Rect(
            (x * self.camera.scale) + self.camera.camera_x,
            (y * self.camera.scale) + self.camera.camera_y,
            width * self.camera.scale,
            height * self.camera.scale
        )

        pygame.draw.rect(
            self.screen,
            color,
            temp_rect,
            borderW
        )
        return temp_rect

    def show_debug(self, ):
        self.debug = True
        print("Debug: " + str(self.debug))

    def render_text(self, text, x, y, fontsize=30, basecolor=(0, 0, 0)):
        x = (x * self.camera.scale) + self.camera.camera_x
        y = (y * self.camera.scale) + self.camera.camera_y
        fontsize = int(fontsize * self.camera.scale)
        pygame.font.init()
        font = pygame.font.SysFont('arial', fontsize)
        text = text.split('\n')

        for t in range(len(text)):
            surf = font.render(text[t], False, basecolor)
            self.screen.blit(surf, (x, y + (fontsize * t)))

    def render_path(self, path, x: int = 0, y: int = 0):
        # x = (x*self.camera.scale)+self.camera.camera_x
        # y = (y*self.camera.scale)+self.camera.camera_y

        for p in path.points:
            self.render_rect(p.x + x, p.y + y, 10, 10, (222, 40, 173))
            if self.debug:
                self.render_text(str(p.index), p.x + x, p.y + y, 16)

    def render_animation(self, animation, x: int = 0, y: int = 0):
        self.render_sprite(
            animation.element,
            animation.element_x + x,
            animation.element_y + y,
            25,
            25
        )

        if self.debug:
            self.render_path(animation.path, x, y)

    ## For future this might be smart to move somewhere else.
    def render_world_manager(self, wm, offsetx, offsety):
        x, y = 0, 0
        for chunk in wm.chunks:
            y = 0
            for column in wm.chunks[chunk].data:  # y
                y += 1
                x = 0
                cx, cy = chunk
                cx = cx * wm.chunkSize
                cy = cy * wm.chunkSize

                for row in column:  # x
                    x += 1
                    self.render_rect((x + cx) * 30, (y + cy) * 30, 25, 25, (235, 64, 52), True)

            # if self.debug:
                # self.render_text(str(chunk), (x + cx) * wm.chunkSize, (y + cy) * wm.chunkSize)

    # BaldursGate3IsGoodGame

    # Render string so newlines are used and implement basic color code support.
    def render_advanced_text(screen, text, x, y, fontsize=30, basecolor=(0, 0, 0)):

        pygame.font.init()
        font = pygame.font.SysFont('arial', fontsize)
        text = text.split('\n')

        # Loop all text cut by newlines.
        for t in range(len(text)):

            # loop all parts of the text by color codes.
            parts = text[t].split('$c')
            for p in range(len(parts)):
                surf = font.render(text[t], False, basecolor)
                screen.blit(surf, (x + (fontsize * p), y + (fontsize * t)))

    # print(parts[p])
    ###TODO: Need get lenght of a word and use it's offset for rendering next colored work

    # print(text[t])
    # surf = font.render(text[t], False, basecolor)
    # screen.blit(surf,(x,y+(fontsize*t)))

    def render_gui(screen, gui, x: int, y: int):
        pass


class Camera:
    def __init__(self, ):
        self.camera_x = 0
        self.camera_y = 0
        self.scale = 1

    def MoveCamera(self, direction: str, speed: int = 1):
        speed = speed + self.scale  # Makes moving camera faster depending on current size.
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

    def ChangeScale(self, direction: str, speed: int = 1):
        speed = speed + self.scale / 10  # Makes scaling faster depending on current size.
        match direction:
            case "more":
                self.scale += speed
            # self.camera_x += self.scale
            # self.camera_y += self.scale

            case "less":
                self.scale -= speed
            # self.camera_x -= self.scale
            # self.camera_y -= self.scale

            case _:
                return False

        if self.scale < 0.1:
            self.scale = 0.1
        return True

    def Reset(self, ):
        self.camera_x = 0
        self.camera_y = 0
        self.scale = 1
        print("Render location & Scale reset")


class Point:
    def __init__(self, x: int = 0, y: int = 0, index: int = None):
        self.x = x
        self.y = y
        self.index = index


class Path:
    def __init__(self, ):
        self.points = []
        self.index = 0

    def add_point(self, x: int = 0, y: int = 0, index: int = None):
        if index == None:
            index = self.index
            self.index += 1

        self.points.append(Point(x, y, index))


class Animation:
    def __init__(self, element, path):
        self.element = element
        self.path = path
        self.speed = 1
        self.current_index = 0

        self.element_x = self.path.points[0].x
        self.element_y = self.path.points[0].y

    def update(self, ):

        ## These are used for fixing a doubled speed if moving on x and y at the same time.
        moving_x = False
        moving_y = False

        for point in self.path.points:
            if point.index == self.current_index:
                # print(self.element_x)
                # print(self.element_y)
                if self.element_x > point.x:
                    moving_x = True
                    if moving_x and moving_y:
                        self.element_x -= self.speed / 2
                    else:
                        self.element_x -= self.speed

                if self.element_x < point.x:
                    moving_x = True
                    if moving_x and moving_y:
                        self.element_x += self.speed / 2
                    else:
                        self.element_x += self.speed

                if self.element_y > point.y:
                    moving_y = True
                    if moving_x and moving_y:
                        self.element_y -= self.speed / 2
                    else:
                        self.element_y -= self.speed

                if self.element_y < point.y:
                    moving_y = True
                    if moving_x and moving_y:
                        self.element_y += self.speed / 2
                    else:
                        self.element_y += self.speed

                # If element has arrived to a point.
                # if self.element_x > point.x - 1 and self.element_x < point.x + self.speed + 1:
                if self.element_x > point.x - 1 and self.element_x < point.x + self.speed + 1:
                    if self.element_y > point.y - 1 and self.element_y < point.y + self.speed + 1:

                        self.current_index += 1
                        if self.current_index + 1 > len(self.path.points):
                            self.current_index = 0

        # print("Swiched to index "+str(self.current_index))


class UtilityTools():
    def __init__(self, ):
        pass

    def randomChance(self, chance):
        chance = 100 - chance
        temp = random.randrange(0, 100)

        if temp >= chance:
            return True
        return False

    def procTest(self, amount):
        proc = 0
        for i in range(amount):
            if self.randomChance(1):
                proc += 1

        print("hit " + str(proc) + " times")
        return proc

    def read_file(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
        return data

    def write_file(self, filename: str, data: any):
        data = json.dumps(data, indent=4)
        with open(filename, 'w') as file:
            file.write(data)
            
    def random_color(self,):
        return random.choice([
            (66, 135, 245),
            (235, 64, 52),
            (50, 168, 82),
            (252, 186, 3),
            (179, 36, 176)
        ])


class Sprite:
    def __init__(self, size_x: int = 0, size_y: int = 0, srcDirectory: str = "", secperframe=2):
        self.frames = []
        self.currentFrameIndex = 0
        self.currentFrame = None
        self.seconds_per_frame = secperframe
        self.frameTimer = 0

        self.position_x = 0
        self.position_y = 0

        self.srcDirectory = srcDirectory
        self.isPlaying = True

    def LoadManualy(self, srcFiles: list):
        self.frames = srcFiles
        print("Loaded: " + str(len(self.frames)) + " files to sprite")

    def LoadAutomaticly(self, ):
        for frame in os.listdir(self.srcDirectory):
            self.frames.append(pygame.image.load(self.srcDirectory + frame).convert())
        self.currentFrame = self.frames[0]
        print("Loaded: " + str(len(self.frames)) + " files to sprite")

    # Find all possible numbers from the filenames and sort frames
    # With those
    def SmartSortFrames(self, ):
        raise NotImplementedError

    def resetFrameTimer(self, ):
        self.frameTimer = time.time()

    # This should be ran in the programs main loop
    def Update(self, ):
        if self.isPlaying:
            timer_current = time.time()
            if (timer_current - self.frameTimer) > self.seconds_per_frame:

                self.resetFrameTimer()
                if self.currentFrameIndex < len(self.frames) - 1:
                    self.setCurrentFrame()
                    self.currentFrameIndex += 1
                else:
                    self.setCurrentFrame()
                    self.currentFrameIndex = 0

    def Draw(self, screen, x, y, width, height):
        self.position_x = x
        self.position_y = y
        screen.blit(pygame.transform.scale(self.currentFrame, (width, height)), (self.position_x, self.position_y))

    def Play(self, ):
        self.isPlaying = True

    def Stop(self, ):
        self.isPlaying = False

    def setCurrentFrame(self, index=None):
        if index == None:
            # print("INDEX: "+str(self.currentFrameIndex))
            self.currentFrame = self.frames[self.currentFrameIndex]
        else:
            self.currentFrame = self.frames[index]

    def setMaxFrameTime(self, time):
        self.seconds_per_frame = time

    def getCurrentFrame(self, ):
        return self.currentFrame

    def getFrames(self, ):
        return self.frames


class GameObject():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Tile(GameObject):
    def __init__(self, x, y, id=0):
        super().__init__(x, y)
        self.size = 25
        self.id = id

    def render(self, screen):
        global temp_img
        # pygame.draw.rect(screen,(25, 181, 44),(self.x,self.y,self.size,self.size),0)
        screen.blit(temp_img, (self.x, self.y))

    def __repr__(self):
        return "<Tile x={x}, y={y}>".format(x=self.x, y=self.y)


class WorldManager:
    def __init__(self, ):
        self.chunks = {}
        self.chunkSize = 16

    def create_chunk(self, x, y):
        self.chunks[(x, y)] = Chunk(x, y, self.chunkSize)

    def generate(self, ):
        pass
    
    def get_tile(self, world_x, world_y):
        pass


class Chunk:
    def __init__(self, x, y, chunkSize):
        self.chunkSize = chunkSize
        self.x = x
        self.y = y
        self.data = np.empty(shape=(self.chunkSize, self.chunkSize))


class Element:
    def __init__(self, name="unnamed-element"):
        self.name = name


class UiBox(Element):
    def __init__(self, ):
        super().__init__("UiBox")
        self.width = 2
        self.height = 2


class Gui:
    def __init__(self, RenderManagement):
        self.elements = []
        self.RenderManagement = RenderManagement

    def add_element(self, element: Element):
        self.elements.append(element)
        print(self.elements)

    def render(self, screen):
        for e in self.elements:
            # e.Render(screen,self.RenderManagement)
            pass


if __name__ == "__main__":
    wm = WorldManager()
    wm.create_chunk(0, 0)
    print(wm.chunks[(0, 0)].data)
