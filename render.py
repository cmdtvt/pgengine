import pygame
from . import structure
from . import world_management
from . import camera

class RenderingIsometric:
    def __init__(self,screen):
        pass

class RenderManagement:
    # https://stackoverflow.com/questions/29112003/saving-pygame-display-as-pygame-subsurface
    def __init__(self, screen):
        self.camera = camera.Camera()
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
        if isinstance(image, structure.Resource):
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

    def render_resource(self, res: structure.Resource, resource_type: str = "image", x: int = 0, y: int = 0, width: int = 0, height: int = 0):
        if resource_type == "image":
            self.render_image(res, x, y, width, height)
        elif resource_type == "sprite":
            self.render_sprite(res.resource, x, y, width, height)

    # Turns all tiles of a chunk to single image to reduce redering load.
    def compile_chunk(self, chunk: world_management.Chunk):
        #TODO: The problem with rendering this directly is that all offset calculations are doen two times
        #TODO: This is because subsurface is just an "window" to the parent surface. So when we change the location of items in the parent they also change in child.
        #TODO: Then the "window" gets moved seperatly so all offsets come as 2x



        #ch = chunk.data[0][0].reference.renderable_refrence

        tile_size = 16

        surface_chunk = pygame.Surface((chunk.chunk_size*tile_size,chunk.chunk_size*tile_size))
        #surface_chunk.fill((245, 200, 66))
        for y in range(chunk.chunk_size):
            for x in range(chunk.chunk_size):
                chunk_ref = chunk.data[y][x].reference
                if chunk_ref != None:
                    surface_chunk.blit(chunk_ref.renderable_refrence.resource,(x*tile_size,y*tile_size))
        #pygame.image.save(surface_chunk, "subsurf_test.png")



        # This is stupid but easiest way to make it work. This can be maybe done better with image.get_buffer
        #subsurf = self.screen.subsurface([x, y, 25*tile_size, 25*tile_size])
        pygame.image.save(surface_chunk, "cache/rendering/chunk_{x}_{y}.png".format(x=chunk.x, y=chunk.y))
        return pygame.image.load("cache/rendering/chunk_{x}_{y}.png".format(x=chunk.x, y=chunk.y)).convert()


    def compile_all_chunks(self, wm):
        compiled = {}
        for c in wm.chunks.values():
            compiled[(c.x, c.y)] = self.compile_chunk(c)

        return compiled

    def render_compiled_chunks(self,wm):
        pass

    # Renders all tiles one by one from the chunks
    def render_world_manager(self, wm):
        #TODO: Add a way to control the size of tile. Currently all tiles are scaled to 25x25px
        for chunk, chunk_data in wm.chunks.items():
            cx, cy = chunk  # Coordinates of the current chunk
            for y, tiles in enumerate(chunk_data.data.values()):
                for x, tile in enumerate(tiles.values()):

                    temp_cx = cx * wm.chunkSize
                    temp_cy = cy * wm.chunkSize
                    temp_holder = wm.get_holder(temp_cx+x, temp_cy+y)

                    if temp_holder is not None and temp_holder.reference is not None:
                        if isinstance(temp_holder.reference, world_management.Tile):

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
