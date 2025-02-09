import pygame, random, json, os, time

#packages own import stuff
from . import structure
from . import utilities

class EngineSetup:
    def __init__(self,):
        pass

    def setup(self,):
        #Generate cache folders
        pass

class SpritesheetManager:
    def __init__(self,):
        self.data = {}
        self.cols_in_set = 0
        self.rows_in_set = 0
        self.sprite_width = 0
        self.sprite_height = 0

    #Each Spritesheet should have config file accosiated with them.
    #From this file we can parse the tileset from one image
    def load(self,filename:str,name:str=None,sprite_width:int=16,sprite_height:int=16,sprite_margin:int=1,cols_in_set:int=16,rows_in_set:int=16):

        if cols_in_set >= 1:
            cols_in_set -= 1
        self.cols_in_set = cols_in_set

        if rows_in_set >= 1:
            rows_in_set -= 1
        self.rows_in_set = rows_in_set
        self.sprite_height = sprite_height
        self.sprite_width = sprite_width

        ut = utilities.UtilityTools()
        folder_location = "data/tilesets/"
        if not name:
            name = filename

        # If spritesheet does not have generated configuration let's add it.
        if not ut.check_file_exsist(folder_location,f"tileset_{name}.json"):
            template_config = {
                "settings": {
                    "sprite_width" : sprite_width,
                    "sprite_height" : sprite_height,
                    "sprite_margin" : sprite_margin,
                    "cols_in_set" : cols_in_set,
                    "rows_in_set" : rows_in_set,
                    "finalrow_sprites_removed" : 0
                },
                "sprites" : {},
                "version" : 1
            }

            for row in range(template_config["settings"]["rows_in_set"]):
                for column in range(template_config["settings"]["cols_in_set"]):


                    tc_settings = template_config["settings"]

                    sx = column * (tc_settings["sprite_width"] + tc_settings["sprite_margin"])
                    sy = row * (tc_settings["sprite_height"] + tc_settings["sprite_margin"])
                    ex = tc_settings["sprite_width"]
                    ey = tc_settings["sprite_height"]

                    template_config["sprites"][f"sprite_{row}_{column}"] = {
                        "id": int(f"{row}{column}"), 
                        "location": {
                            "sx": sx,
                            "sy": sy,
                            "ex": ex,
                            "ey": ey
                        },
                        "colorMode": "rgba",
                    }
            ut.write_file(f"{folder_location}/tileset_{name}.json",template_config)

        # Let's parse the spritesheet
        sprites = {}
        spritesheet = pygame.image.load(filename).convert_alpha()
        spritesheet_config = ut.read_file(f"{folder_location}/tileset_{name}.json")

        for key,config in spritesheet_config["sprites"].items():
            sprites[key] = structure.Resource(spritesheet.subsurface([config["location"]["sx"], config["location"]["sy"], config["location"]["ex"], config["location"]["ey"]]))
        self.data[name] = sprites
        return sprites

        # Should be implemented in render. Not here.
        def autocreate_animation():
            pass

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
    def __init__(self, element: structure.Resource, path):
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


if __name__ == "__main__":
    pass


