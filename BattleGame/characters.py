import random

class Character:
    level_experience = 100  # 每级所需的经验

    def __init__(self, name, health=100, level=1):
        self.name = name
        self.health = health
        self.level = level
        self.experience = 0

    def attack(self, target):
        damage_dealt = random.randint(self.attack_min, self.attack_max) - target.defense
        if damage_dealt > 0:
            target.health -= damage_dealt
            self.gain_experience(10)
        return damage_dealt

    def gain_experience(self, exp):
        self.experience += exp
        while self.experience >= Character.level_experience:
            self.experience -= Character.level_experience
            self.level_up()

    def level_up(self):
        self.level += 1
        self.attack_min += 1
        self.attack_max += 1
        self.defense += 1

    def is_alive(self):
        return self.health > 0

class Warrior(Character):
    def __init__(self, name):
        super().__init__(name)
        self.attack_min = 10
        self.attack_max = 20
        self.defense = 5
        self.rage = 0  # 可能在特殊攻击中使用

    # (如果需要的话，Warrior 类的特殊攻击和其他方法可以在这里添加)

class Tanker(Character):
    def __init__(self, name):
        super().__init__(name)
        self.attack_min = 5
        self.attack_max = 15
        self.defense = 10
        self.armor = 0  # 可能在特殊防御中使用

    # (如果需要的话，Tanker 类的特殊防御和其他方法可以在这里添加)

# 示例用法
if __name__ == "__main__":
    warrior = Warrior("Warrior")
    tanker = Tanker("Tanker")

    print(f"{warrior.name} attacks {tanker.name}!")
    damage = warrior.attack(tanker)
    print(f"{warrior.name} dealt {damage} damage to {tanker.name}.")
    print(f"{warrior.name} now has {warrior.experience} experience and is level {warrior.level}.")
    print(f"{tanker.name} has {tanker.health} health remaining.")