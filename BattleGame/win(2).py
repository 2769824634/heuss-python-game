import tkinter as tk
import random

class Unit:
    def __init__(self, name, profession, hp, atk, defense, exp=0, rank=1):
        self.name = name
        self.profession = profession
        self.hp = hp
        self.atk = atk
        self.defense = defense
        self.exp = exp
        self.rank = rank

        self.attack_message = ""
        self.level_up_message = ""

    def attack(self, target: "Unit"):
        damage = max(0, self.atk - target.defense + random.randint(-5, 5))
        target.hp = max(0, target.hp - damage)
        self.exp += damage

        self.attack_message = f"{self.name} attacked {target.name} and caused {damage} damage."

        if target.hp == 0:
            self.attack_message += f"\n{target.name} has been defeated!"

        self.check_level_up()

    def check_level_up(self):
        if self.exp >= 100:
            self.exp -= 100
            self.rank += 1
            self.atk += random.randint(1, 5)
            self.defense += random.randint(1, 5)
            self.level_up_message = f"{self.name} leveled up! Now at rank {self.rank}."

class BattleGameUI:
    def __init__(self, root, player_units, ai_units):
        self.root = root
        self.player_units = player_units
        self.ai_units = ai_units
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Turn-Based Battle Game")
        self.root.geometry("800x600")

        self.text_log = tk.Text(self.root, height=15, state='disabled')
        self.text_log.pack(pady=10)

        # Player units on the left side
        for player_unit in self.player_units:
            self.create_unit_frame(player_unit, side='left')

        # AI units on the right side
        for ai_unit in self.ai_units:
            self.create_unit_frame(ai_unit, side='right')

        # Auto Button
        auto_button = tk.Button(self.root, text="Auto", command=self.auto_battle)
        auto_button.pack(pady=10)

    def create_unit_frame(self, unit, side):
        unit_frame = tk.Frame(self.root, padx=10, pady=5)
        unit_frame.pack(side=side, fill='y')

        label_name = tk.Label(unit_frame, text=unit.name)
        label_name.pack()

        button_attack = tk.Button(unit_frame, text="Attack", command=lambda u=unit: self.attack(u))
        button_attack.pack()

    def attack(self, player_unit):
        if self.ai_units:
            ai_unit = random.choice(self.ai_units)
            player_unit.attack(ai_unit)
            self.update_game_log(player_unit.attack_message)

            if ai_unit.hp == 0:
                self.ai_units.remove(ai_unit)
                self.update_game_log(f"{ai_unit.name} has been defeated!")

            if not self.ai_units:
                self.update_game_log("Player wins!")

            # AI turn
            if self.player_units and self.ai_units:
                ai_unit = random.choice(self.ai_units)
                player_unit = random.choice(self.player_units)
                ai_unit.attack(player_unit)
                self.update_game_log(ai_unit.attack_message)

                if player_unit.hp == 0:
                    self.player_units.remove(player_unit)
                    self.update_game_log(f"{player_unit.name} has been defeated!")

                if not self.player_units:
                    self.update_game_log("AI wins!")

    def auto_battle(self):
        while self.player_units and self.ai_units:
            player_unit = random.choice(self.player_units)
            ai_unit = random.choice(self.ai_units)

            player_unit.attack(ai_unit)
            self.update_game_log(player_unit.attack_message)

            if ai_unit.hp == 0:
                self.ai_units.remove(ai_unit)
                self.update_game_log(f"{ai_unit.name} has been defeated!")

            if self.ai_units:
                ai_unit = random.choice(self.ai_units)
                player_unit = random.choice(self.player_units)

                ai_unit.attack(player_unit)
                self.update_game_log(ai_unit.attack_message)

                if player_unit.hp == 0:
                    self.player_units.remove(player_unit)
                    self.update_game_log(f"{player_unit.name} has been defeated!")

        if not self.player_units:
            self.update_game_log("AI wins!")
        elif not self.ai_units:
            self.update_game_log("Player wins!")

    def update_game_log(self, message):
        self.text_log.config(state='normal')
        self.text_log.insert(tk.END, message + '\n')
        self.text_log.config(state='disabled')
        self.text_log.see(tk.END)

def setup_game():
    player_units = [
        Unit("Player Warrior 1", "Warrior", 100, random.randint(5, 20), random.randint(1, 10)),
        Unit("Player Warrior 2", "Warrior", 100, random.randint(5, 20), random.randint(1, 10)),
        Unit("Player Tanker", "Tanker", 100, random.randint(1, 10), random.randint(5, 15))
    ]

    ai_units = [
        Unit("AI Warrior 1", "Warrior", 100, random.randint(5, 20), random.randint(1, 10)),
        Unit("AI Warrior 2", "Warrior", 100, random.randint(5, 20), random.randint(1, 10)),
        Unit("AI Tanker", "Tanker", 100, random.randint(1, 10), random.randint(5, 15))
    ]

    return player_units, ai_units

if __name__ == "__main__":
    root = tk.Tk()
    player_units, ai_units = setup_game()
    app = BattleGameUI(root, player_units, ai_units)
    root.mainloop()
