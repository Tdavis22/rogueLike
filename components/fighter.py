
#game is based in a Entity component manner
#Any thing that can 'fight' has a fighter component
class Fighter:
    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power

        
