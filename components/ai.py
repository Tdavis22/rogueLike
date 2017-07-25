import libtcodpy as libtcod
#Generic basic monster AI
class BasicMonster:
    #We pass in the fov_map of player. If player can see monster monster can see player
    def take_turn(self, target, fov_map, game_map, entities):
        monster = self.owner
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

            if monster.distance_to(target) >= 2:
                monster.move_astar(target, entities, game_map)

            elif target.fighter.hp > 0:
                monster.fighter.attack(target)
