import libtcodpy as libtcod

from game_messages import Message
#game is based in a Entity component manner
#Any thing that can 'fight' has a fighter component
#All fighting ends up with a list describing some of the effects of what has happened
class Fighter:
    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power

    def take_damage(self, amount):
        #A list describing what happened
        results = []

        self.hp -= amount

        if self.hp <= 0:
            results.append({'dead': self.owner})

        return results

    def heal(self, amount):
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def attack(self, target):
        results = []
        damage = self.power - target.fighter.defense

        if damage > 0:
            target.fighter.take_damage(damage)
            results.append({'message': Message('{0} attacks {1} for {2} hit points.'.format(
                           self.owner.name.capitalize(), target.name, str(damage)), libtcod.white)})

            #extend keeps our list flat and avoids it from becoming 2d
            results.extend(target.fighter.take_damage(damage))

        else:
            results.append({'message': Message('{0} attacks {1} but does no damage.'.format(
                           self.owner.name.capitalize(), target.name), libtcod.white)})
        return results
