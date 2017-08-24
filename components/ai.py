import libtcodpy as libtcod
import math as math
from random import randint

from game_messages import Message


#Generic basic monster AI
class BasicMonster:
    #We pass in the fov_map of player. If player can see monster monster can see player
    def take_turn(self, target, fov_map, game_map, entities):
        results = []
        monster = self.owner
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

            if monster.distance_to(target) >= 2:
                monster.move_astar(entities, game_map, target = target)

            elif target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)

        return results
class CowardMonster:

    def take_turn(self, target, fov_map, game_map, entities):
        results = []
        move_vector = [0,0]
        monster = self.owner
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):
            if (monster.x != target.x):
                move_vector[0] = (math.copysign(1, monster.x - target.x))
            move_vector[0] += monster.x


            if (monster.y != target.y):
                move_vector[1] = (math.copysign(1, monster.y - target.y))
            move_vector[1] += monster.y

            #should eventually make it move_astar 
            monster.move_towards(move_vector[0], move_vector[1], game_map, entities)
        return results
class ConfusedMonster:
    def __init__(self, previous_ai, number_of_turns = 10):
        self.previous_ai = previous_ai
        self.number_of_turns = number_of_turns

    def take_turn(self, target, fov_map, game_map, entities):
        results = []

        if self.number_of_turns > 0:
            random_x = self.owner.x + randint(0, 2) - 1
            random_y = self.owner.y + randint(0, 2) - 1

            if random_x != self.owner.x and random_y != self.owner.y:
                self.owner.move_towards(random_x, random_y, game_map, entities)

            self.number_of_turns -= 1
        else:
            self.owner.ai = self.previous_ai
            results.append({'message': Message('The {0} is no longer confused!'.format(self.owner.name), libtcod.red)})

        return results
