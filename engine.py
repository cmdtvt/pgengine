import pygame, randon, json, os, time

#packages own import stuff
from . import render, gui, utilities

class Resource:
    def __init__(self, resource, resource_type="image"):
        self.resource_type = resource_type
        self.resource = resource

    def __repr__(self):
        has_resource = False
        if self.resource:
            has_resource = True
        return "<Resource resource_type={resource_type} has_resource={has_resource}>".format(resource_type=self.resource_type, has_resource=has_resource)


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

