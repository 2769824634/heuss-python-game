import random
from tkinter import messagebox
from unit import Attacker, Tanker
from team import Team

class Main:#主要逻辑
    def __init__(self, player_team_size=3):
        self.player_team = Team("Player")
        self.ai_team = Team("AI")
        self.create_player_team(player_team_size)
        self.create_ai_team(player_team_size)

    def create_player_team(self, size):
        for x in range(size):
            name = f"Player{x+1}"
            unit_type = random.choice([Attacker, Tanker])
            hp = random.randint(80, 120)
            atk = random.randint(8, 12)
            defense = random.randint(5, 8)
            unit = unit_type(name, hp, atk, defense)
            self.player_team.add_unit(unit)

    def create_ai_team(self, size):
        for i in range(size):
            name = f"AI{i+1}"
            unit_type = random.choice([Attacker, Tanker])
            hp = random.randint(80, 120)
            atk = random.randint(8, 12)
            defense = random.randint(5, 8)
            unit = unit_type(name, hp, atk, defense)
            self.ai_team.add_unit(unit)
    
    def player_turn(self):
        player_unit = random.choice(self.player_team.units)
        ai_unit = random.choice(self.ai_team.units)
        player_unit.attack(ai_unit)
        if self.ai_team.defeat():
            messagebox.showinfo("Game Over", "Player wins!")
            self.master.destroy()
