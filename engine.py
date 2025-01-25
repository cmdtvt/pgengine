#### Basicly helper stuff for rendering etc....
import pygame
import random
import json
import os
import time


#from . import gui

# import utilities
class Resource:
    def __init__(self, resource, resource_type="image"):
        self.resource_type = resource_type
        self.resource = resource

    def __repr__(self):
        has_resource = False
        if self.resource:
            has_resource = True
        return "<Resource resource_type={resource_type} has_resource={has_resource}>".format(resource_type=self.resource_type, has_resource=has_resource)


class Chunk:
    #TODO: Add a way for chunk to store "compiled" image of all tiles in chunk
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

    def get_renderable_reference(self):
        #TODO return list of all holders in chunk or return only the "compiled" image
        pass

    def __repr__(self):
        return "<Chunk size={size}x{size}>".format(size=self.chunk_size,has_tiles=False)

class RenderingIsometric:
    def __init__(self,screen):
        pass

class RenderManagement:
    # https://stackoverflow.com/questions/29112003/saving-pygame-display-as-pygame-subsurface
    def __init__(self, screen):
        self.camera = Camera()
        self.screen: pygame.Surface = screen
        self.font = pygame.font.SysFont(None, 24)
        self.debug = False
        self.debug_testimage = None#pygame.image.load("assets/debug.png")



    def update(self, ):
        pass

    # passed image can be pygame's image or Resource class.
    def render_image(self, image, x: int, y: int, width: int = None, height: int = None):
        #TODO: Make a system where tiles outside of cameras view are not actually moved or rendered.
        #TODO: When chunk becomes visible fix coordinates of all tiles to it.
        source_image = image
        if isinstance(image, Resource):
            source_image = image.resource

        if width is None:
            width = source_image.get_width()
        if height is None:
            height = source_image.get_height()

        x = (x * self.camera.scale) + self.camera.camera_x
        y = (y * self.camera.scale) + self.camera.camera_y

        temp_img = pygame.transform.scale(source_image, (width * self.camera.scale, height * self.camera.scale))
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

    def render_resource(self, res: Resource, resource_type: str = "image", x: int = 0, y: int = 0, width: int = 0, height: int = 0):
        if resource_type == "image":
            self.render_image(res, x, y, width, height)
        elif resource_type == "sprite":
            self.render_sprite(res.resource, x, y, width, height)

    # Turns all tiles of a chunk to single image to reduce redering load.
    def compile_chunk(self, chunk: Chunk):
        #TODO: The problem with rendering this directly is that all offset calculations are doen two times
        #TODO: This is because subsurface is just an "window" to the parent surface. So when we change the location of items in the parent they also change in child.
        #TODO: Theen the "window" gets moved seperatly so all offsets come as 2x
        # print(chunk)
        tile_size = 16
        x = chunk.x
        y = chunk.y

        # This is stupid but easiest way to make it work. This can be maybe done better with image.get_buffer
        subsurf = self.screen.subsurface([x, y, 25*tile_size, 25*tile_size])
        pygame.image.save(subsurf, "cache/rendering/chunk_{x}_{y}.png".format(x=x, y=y))
        return pygame.image.load("cache/rendering/chunk_{x}_{y}.png".format(x=x, y=y)).convert()


    def compile_all_chunks(self, wm):
        compiled = {}
        for c in wm.chunks.values():
            compiled[(c.x, c.y)] = self.compile_chunk(c)

        return compiled

    # For future this might be smart to move somewhere else.
    def render_world_manager(self, wm, offsetx, offsety):
        #TODO: Add a way to control the size of tile. Currently all tiles are scaled to 25x25px
        for chunk, chunk_data in wm.chunks.items():
            cx, cy = chunk  # Coordinates of the current chunk
            for y, tiles in enumerate(chunk_data.data.values()):
                for x, tile in enumerate(tiles.values()):

                    temp_cx = cx * wm.chunkSize
                    temp_cy = cy * wm.chunkSize
                    temp_holder = wm.get_holder(temp_cx+x, temp_cy+y)

                    if temp_holder is not None and temp_holder.reference is not None:
                        if isinstance(temp_holder.reference, Tile):

                            self.render_resource(
                                temp_holder.reference.renderable_refrence,
                                "image",
                                x=(x+temp_cx)*25,
                                y=(y+temp_cy)*25,
                                width=25,
                                height=25
                            )

                    #TODO: This is broken. +1 is added to each offset so if we want to render to 5,5 it gets rendered to 6,6
                    elif self.debug:
                        self.render_rect((x + temp_cx) * 25, (y + temp_cy) * 25, 25, 25, (235, 64, 52), False)

            if self.debug:
                self.render_rect((cx*wm.chunkSize)*25, (cy*wm.chunkSize)*25, wm.chunkSize*25, wm.chunkSize*25, (66, 135, 245), False)




    def render_advanced_text(self,screen, x, y, fontsize=30, basecolor=(0, 0, 0)):
        """
        Renders text with support for newline and inline coloring using
        '$c(R,G,B)' to change the color and '$n' to reset to the base color.
        """
        pygame.font.init()
        font = pygame.font.SysFont('arial', fontsize)

        text = "Hello $c(255,0,0)Red Text$n back to black.\nAnother $c(0,255,0)Green Line!"
           # Split text by newlines
        lines = text.split('\n')

        y_offset = 0  # Track vertical position for new lines
        for line in lines:
            x_offset = 0  # Track horizontal position for each line
            parts = line.split('$c')  # Split by color codes
            
            current_color = basecolor
            for part in parts:
                if part.startswith('('):
                    # Check if a color code exists at the start of the part
                    try:
                        color_end = part.index(')')
                        color_code = part[1:color_end]  # Extract RGB from inside parentheses
                        r, g, b = map(int, color_code.split(','))
                        current_color = (r, g, b)
                        part = part[color_end + 1:]  # Remove the color code from the part
                    except ValueError:
                        pass  # Invalid color code, continue with the part as-is

                if '$n' in part:
                    # Reset to the base color if $n is found
                    part, reset_part = part.split('$n', 1)
                    if part:  # Render text before reset only if not empty
                        surf = font.render(part, True, current_color)
                        self.render_image(surf, x + x_offset, y + y_offset)
                        x_offset += surf.get_width()

                    # Render the reset part in base color
                    current_color = basecolor
                    if reset_part:  # Render reset text only if not empty
                        surf = font.render(reset_part, True, current_color)
                        self.render_image(surf, x + x_offset, y + y_offset)
                        x_offset += surf.get_width()
                else:
                    # Render the part in the current color
                    if part:  # Avoid rendering empty strings
                        surf = font.render(part, True, current_color)
                        self.render_image(surf, x + x_offset, y + y_offset)
                        x_offset += surf.get_width()

            y_offset += fontsize  # Move to the next line vertically

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

#TODO: Fix this. Make it use the stuff from Resource class.
class Animation:
    def __init__(self, element: Resource, path):
        self.element = element
        self.path = path
        self.speed = 1
        self.current_index = 0

        self.element_x = self.path.points[0].x
        self.element_y = self.path.points[0].y

    def update(self, ):
        point = self.path.points[self.current_index]
        delta_x = point.x - self.element_x
        delta_y = point.y - self.element_y
        moving_x, moving_y = delta_x != 0, delta_y != 0
        self.element_x += self.speed * (delta_x / (abs(delta_x) if delta_x else 1)) / (1 + moving_y)
        self.element_y += self.speed * (delta_y / (abs(delta_y) if delta_y else 1)) / (1 + moving_x)
        if abs(delta_x) < self.speed and abs(delta_y) < self.speed:
            self.current_index = (self.current_index + 1) % len(self.path.points)

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

        #TODO: This should basicly be a Resource i think.
        #TODO: Currently WM stores holders which have refrence to a tile and tile should then have a resource that can be rendered.
        self.renderable_refrence: Resource|None = None

    def set_reference(self, res: Resource):
        self.renderable_refrence = res

    # def render(self, render_management: RenderManagement, x:int, y:int):
        # return
        #render_management.render_image()

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

    def chunk_exsists(self, chunk_x, chunk_y):
        temp_coords = (chunk_x, chunk_y)
        if temp_coords in self.chunks:
            return True
        return False

    def chunk_remove_unused(self):
        raise NotImplementedError
        for c in self.chunks:
            if c.data:
                pass

    # Get tile with global x and y coordinates from a chunk
    def get_holder(self, world_x, world_y):
        chunk_x, chunk_y = self.get_chunk_coordinates(world_x, world_y)
        current_chunk = self.chunks[(chunk_x, chunk_y)]

        # From current chunk get local x and y values for the wanted tile
        local_x = world_x - (chunk_x * self.chunkSize)
        local_y = world_y - (chunk_y * self.chunkSize)
        # print(local_x, local_y, sep=" | ")
        return current_chunk.data[local_y][local_x]

    # Get chunk coordinates from global tile coordinates.
    def get_chunk_coordinates(self, world_x, world_y):
        chunk_x = int(world_x / self.chunkSize)
        chunk_y = int(world_y / self.chunkSize)

        return chunk_x, chunk_y

    def add_tile(self, tile: Tile, x: int, y: int):
        chunk_x, chunk_y = self.get_chunk_coordinates(x, y)
        if self.chunk_exsists(chunk_x, chunk_y) == False:
            self.create_chunk(chunk_x, chunk_y)
            # print("Chunk created to: {x} | {y}".format(x=chunk_x, y=chunk_y))
        found_tile = self.get_holder(x, y)
        if found_tile is not None:
            found_tile.reference = tile

        #TODO: If chunk does not exsists where we want to add an tile create it.
        #TODO: Add a way to remove unused chunks

    def move_tile_location(self):
        pass

    def move_tile_location_relative(self):
        pass

    def swap_tile_location(self):
        pass

    def destroy_tile(self):
        #TODO: Make this also return the deleted tile so it might be used elsewhere.
        pass

class WorldManipulationTools:
        def __init__(self,wm:WorldManager):
            self.wm:WorldManager = wm
            self.add_tile = wm.add_tile

        def add_blueprint(self):
            pass

        def create_blueprint(self):
            pass

        def fill_area(self):
            pass

        def delete_area(self):
            pass

        def delete_chunk_tiles(self):
            pass

        def fill_chunk_tiles(self):
            pass



if __name__ == "__main__":
    wm = WorldManager()
    wm.create_chunk(0, 0)
    wm.create_chunk(1, 0)
    wm.create_chunk(0, 1)
    wm.create_chunk(3, 1)

    temp_tile = Tile(1,0)
    print(wm.chunks)

    print("gang gang")
    print(gui)

    print(wm.get_holder(5, 5))
    wm.add_tile(temp_tile,5,5)
    print(wm.get_holder(5, 5))

