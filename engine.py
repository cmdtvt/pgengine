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
        self.debug_testimage = pygame.image.load("assets/gui/UiBox/box.png")

    # self.MoveCamera = self.camera.MoveCamera
    # self.ChangeScale = self.camera.ChangeScale

    def update(self, ):
        pass

    # Rendering through this handles cameralocation & Scale
    def render_image(self, image, x: int, y: int, width: int = None, height: int = None):
        if width is None:
            width = image.get_width()
        if height is None:
            height = image.get_height()

        x = (x * self.camera.scale) + self.camera.camera_x
        y = (y * self.camera.scale) + self.camera.camera_y

        temp_img = pygame.transform.scale(image, (width * self.camera.scale, height * self.camera.scale))
        self.screen.blit(temp_img, (x, y))

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
        border_width = 2
        if filled:
            border_width = 0

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
            border_width
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

    # For future this might be smart to move somewhere else.
    def render_world_manager(self, wm, offsetx, offsety):
        x, y = 0, 0
        for chunk in wm.chunks:
            y = 0
            for tiles in wm.chunks[chunk].data.values():
                x = 0
                # This is the X axcel
                for i in tiles.values():
                    # print(i)
                    cx, cy = chunk
                    cx = cx * wm.chunkSize
                    cy = cy * wm.chunkSize
                    
                    temp_holder = wm.get_holder(x, y)
                    if temp_holder is not None and temp_holder.reference is not None: #TODO: This will never be none. So this statement should be changed to check if holder has set reference to a tile or asset.
                        # self.render_image(self.debug_testimage,x,y)
                        self.render_rect((x + cx) * 30, (y + cy) * 30, 25, 25, (50, 168, 82), True)
                        
                    elif self.debug:
                        self.render_rect((x + cx) * 30, (y + cy) * 30, 25, 25, (235, 64, 52), True)
                    x += 1
                y += 1
                        
                        
                        
                        
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
        if index is None:
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
        # These are used for fixing a doubled speed if moving on x and y at the same time.
        # moving_x = False
        # moving_y = False

        point = self.path.points[self.current_index]
        delta_x = point.x - self.element_x
        delta_y = point.y - self.element_y 
        moving_x, moving_y = delta_x != 0, delta_y != 0
        self.element_x += self.speed * (delta_x / (abs(delta_x) if delta_x else 1)) / (1 + moving_y)
        self.element_y += self.speed * (delta_y / (abs(delta_y) if delta_y else 1)) / (1 + moving_x)
        if abs(delta_x) < self.speed and abs(delta_y) < self.speed:
            self.current_index = (self.current_index + 1) % len(self.path.points)
            
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

    def random_color(self, ):
        return random.choice([
            (66, 135, 245),
            (235, 64, 52),
            (50, 168, 82),
            (252, 186, 3),
            (179, 36, 176)
        ])
    
    def file_hash(self, file_path):
        # https://stackoverflow.com/questions/22058048/hashing-a-file-in-python
        # Basicly this thing can create hashes of files fast even with larger filesizes.
        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            while True:
                data = f.read(65536) # arbitrary number to reduce RAM usage
                if not data:
                    break
                sha256.update(data)
        return sha256.hexdigest()


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


class GameObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Tile(GameObject):
    def __init__(self, tile_id=0, state_id=0):
        super().__init__(None,None)
        self.size = 25
        self.tile_id = tile_id # Unique id for the tile type
        
        # State of the tile. Like rotation of the image for example.
        # Still need to consider is this a good way to implement this.
        self.state_id = state_id
        self.renderable_refrence = None

    def render(self, screen):
        # global temp_img
        # pygame.draw.rect(screen,(25, 181, 44),(self.x,self.y,self.size,self.size),0)
        # screen.blit(temp_img, (self.x, self.y))
        pass

    def __repr__(self):
        return "<Tile tile_id={tile_id}, state_id={state_id}>".format(tile_id=self.tile_id, state_id=self.state_id)

# When creating chunks thse are used in initialization.
# If we want to add an tile to the world we will set self.reference to that tile
class Holder:
    def __init__(self):
        self.reference = None
        
    def has_reference(self):
        raise NotImplementedError
    
    def __repr__(self):
        return "<Holder reference={refe}>".format(refe=self.reference)
    
        
class WorldManager:
    def __init__(self, ):
        self.chunks = {}
        self.chunkSize = 16

    def create_chunk(self, x, y):
        self.chunks[(x, y)] = Chunk(x, y, self.chunkSize)

    def generate(self, ):
        pass

    # Get tile with global x and y coordinates from a chunk
    def get_holder(self, world_x, world_y):
        
    #try:
        # TODO: WELP this mess does not work.
        # TODO: This changes behavior depending how the stored "world" looks like and i have no idea why
        # Get how many chunks from left and up
        chunk_x = int(world_x / self.chunkSize)
        chunk_y = int(world_y / self.chunkSize)
        current_chunk = self.chunks[(chunk_x, chunk_y)]
        
        #print("CHUNK: ", chunk_x, chunk_y, sep=" | ")
        
        # From current chunk get local x and y values for the wanted tile
        local_x = world_x - (chunk_x * self.chunkSize)
        local_y = world_y - (chunk_y * self.chunkSize)
        # print(local_x, local_y, sep=" | ")
        return current_chunk.data[local_y][local_x]
   # except:
        pass
        #print("Error occured while trying to fetch holder from: {x} | {y}".format(x=world_x,y=world_y))
        
    def add_tile(self, tile, x: int, y: int):
        found_tile = self.get_holder(x, y)
        if found_tile is not None:
            found_tile.reference = tile
            print("Tile added")


class Chunk:
    def __init__(self, x, y, chunk_size):
        self.chunk_size = chunk_size
        self.x = x
        self.y = y
        # self.data = np.empty(shape=(self.chunkSize, self.chunkSize))
        self.data = {}
        for y in range(self.chunk_size):
            self.data[y] = {}
            for x in range(self.chunk_size):
                self.data[y][x] = Holder()
                
    def __repr__(self):
        return "<Chunk size={size}x{size}>".format(size=self.chunk_size,has_tiles=False)
                


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
    wm.create_chunk(1, 0)
    wm.create_chunk(0, 1)
    wm.create_chunk(3, 1)
    
    temp_tile = Tile(1,0)
    print(wm.chunks)
    
    print(wm.get_holder(5, 5))
    wm.add_tile(temp_tile,5,5)
    print(wm.get_holder(5, 5))

