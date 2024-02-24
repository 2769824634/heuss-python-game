import random

class Unit:#属性管理
    def __init__(self, name, hp, atk, defense, exp=0, rank=1):
        self.name = name
        self.hp = hp
        self.atk = atk
        self.defense = defense
        self.exp = exp
        self.rank = rank

    def alive(self):
        return self.hp > 0
    
    def attack(self, enemy_unit):
        damage = max(0, self.atk - enemy_unit.defense)
        enemy_unit.hp -= damage
        print(f"{self.name} attacks {enemy_unit.name} for {damage} damage.")
        if not enemy_unit.alive():
            print(f"{enemy_unit.name} has been defeated!")
        
    def __str__(self):
        return f"{self.name} (HP: {self.hp}, ATK: {self.atk}, DEF: {self.defense}, EXP: {self.exp}, Rank: {self.rank})"

class Attacker(Unit):
    def __init__(self, name, hp, atk, defense, exp=0, rank=1):
        super().__init__(name, hp, atk, defense, exp, rank)

class Tanker(Unit):
    def __init__(self, name, hp, atk, defense, exp=0, rank=1):
        super().__init__(name, hp, atk, defense, exp, rank)