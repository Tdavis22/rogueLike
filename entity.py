import math
import libtcodpy as libtcod
from render_functions import RenderOrder

class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    Possible component:Fighter/AI
    """
    def __init__(self, x, y, char, color, name, blocks = False, render_order = RenderOrder.CORPSE, fighter = None, ai = None,
                 item = None, inventory = None, stairs = None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.render_order = render_order
        self.fighter = fighter
        self.ai = ai
        self.item = item
        self.inventory = inventory
        self.stairs = stairs

        #We want to be able to reference the owner from inside the component
        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

        if self.item:
            self.item.owner = self

        if self.inventory:
            self.inventory.owner = self

        if self.stairs:
            self.stairs.owner = self
    def move(self, dx, dy):
        #move by the given amount
        self.x += dx
        self.y += dy

    def move_towards(self, target_x, target_y, game_map, entities):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if(distance != 0):
            dx = int(round(dx / distance))
            dy = int(round(dy / distance))

            if not (game_map.is_blocked(self.x + dx, self.y + dy ) or
                        get_blocking_entities_at_location(entities, self.x + dx, self.y + dy)):
                        self.move(dx, dy)

    def distance(self, x, y):
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)
    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def move_astar(self, entities, game_map, target = None, target_x = -1, target_y = -1):
        if target != None:
            target_x = target.x
            target_y = target.y
        #create a fov map that has the dimensions of the map
        fov = libtcod.map_new(game_map.width, game_map.height)

        #scan the current map each turn and set all the walls as unwalkable
        #TO DO implement A* for creatures that can move through special terrain
        for y1 in range(game_map.height):
            for x1 in range(game_map.width):
                libtcod.map_set_properties(fov, x1, y1, not game_map.tiles[x1][y1].block_sight,
                                           not game_map.tiles[x1][y1].blocked)

        #Scan all the objects to see if there are objects that must be navigated around
        #Check also that the object isn't self or the target(So that the start and the end points are free)
        #The Ai class handles the situation if self is next to the target so it will not use A*(may need refactor)
        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                #set the tile as a wall to be navigated around
                libtcod.map_set_properties(fov, entity.x, entity.y, True, False)

        #Allocate the A* path
        #The 1.41 is the normal diagonal cost of moving, it can be set as 0.0 if diagonal move are proibited
        my_path = libtcod.path_new_using_map(fov, 1.41)

        libtcod.path_compute(my_path, self.x, self.y, target_x, target_y)
        #Check if the path exists, and in this case, also the path is shorter than 25 tiles
        #The path size matters if you want the monster to use alternative longer paths (for example through other rooms) if for example the player is in a corridor
        #keeping the path size low keeps the monster from running a long alternative route
        if not libtcod.path_is_empty(my_path) and libtcod.path_size(my_path) < 25:
            #find the next coordinates in the computed full path
            x, y = libtcod.path_walk(my_path, True)
            if x or y:
                #set self's coordinates to the next path tile
                #May not work for fast moving, May have to loop through AStar
                self.x = x
                self.y = y
        else:
            #Keep the old move function as a backup so that if there are no paths
            #It will still try to move towards the player
            self.move_towards(target_x, target_y, game_map, entities)

        #We recreate the path every
        libtcod.path_delete(my_path)




def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity
    return None
