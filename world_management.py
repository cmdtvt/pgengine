from . import structure

class Tile(structure.GameObject):
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

    def set_reference(self, res: structure.Resource):
        self.renderable_refrence = res

    # def render(self, render_management: RenderManagement, x:int, y:int):
        # return
        #render_management.render_image()

    def __repr__(self):
        return "<Tile tile_id={tile_id}, state_id={state_id}>".format(tile_id=self.tile_id, state_id=self.state_id)

        
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

        found_tile = self.get_holder(x, y)
        if found_tile is not None:
            found_tile.reference = tile
    #TODO: Figure out the difference using this and using get_holder
    def get_tile(self,x:int,y:int):
        chunk_x, chunk_y = self.get_chunk_coordinates(x, y)
        if self.chunk_exsists(chunk_x, chunk_y):
            found_tile = self.get_holder(x, y)
            if found_tile is not None:
                return found_tile.reference



    def move_tile_location(self):
        pass

    def move_tile_location_relative(self):
        pass

    def swap_tile_location(self):
        pass

    def destroy_tile(self,x:int,y:int):
        #TODO: Make this also return the deleted tile so it might be used elsewhere.

        temp_deleted = None

        chunk_x, chunk_y = self.get_chunk_coordinates(x, y)
        if self.chunk_exsists(chunk_x, chunk_y):
            found_tile = self.get_holder(x, y)
            if found_tile is not None:
                temp_deleted = found_tile
                found_tile.reference = None
        return temp_deleted




class WorldManipulationTools:
        def __init__(self,wm:WorldManager):
            self.wm:WorldManager = wm
            self.add_tile = wm.add_tile
            self.blueprints = {}

        def add_blueprint(self):
            pass

        def create_blueprint(self,sx:int,sy:int,ex:int,ey:int,name:str):
            blueprint = {}
            for y in range(sy,ey+1):
                for x in range(sx,ex+1):
                    self.wm.get_tile(sx,sy)
                    self.wm.destroy_tile(x,y)

            self.blueprints[name] = {}

        def fill_area(self):
            pass

        def delete_area(self,sx:int,sy:int,ex:int,ey:int):
            for y in range(sy,ey+1):
                for x in range(sx,ex+1):
                    self.wm.destroy_tile(x,y)

        #Delete whole chunk
        def delete_chunk_tiles(self,x:int,y:int):
            pass

        def fill_chunk_tiles(self):
            pass
