

class Tile:

    """
    A tile on a map. It may or may not be blocked, and may or may not block sight
    """

    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked
        self.explored = False
        #blocked meaning it can not be passed through
        #by default if a tile is blcoked, it also blocks sight
        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight
