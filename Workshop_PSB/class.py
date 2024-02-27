import random
from random import randint
import constants
from enum import Enum
import constants
from typing import TextIO
from datetime import datetime
import codecs

WarriorAttackLowerLimit: int = 5
WarriorAttackUpperLimit: int = 20
WarriorDefenceLowerLimit: int = 1
WarriorDefenceUpperLimit: int = 10
TankerAttackLowerLimit: int = 1
TankerAttackUpperLimit: int = 10
TankerDefenceLowerLimit: int = 5
TankerDefenceUpperLimit: int = 15

EXPPerLevel: int = 100
MaxLevel: int = 20

DamageRandomPartLowerLimit: int = -5
DamageRandomPartUpperLimit: int = 10

class _GameMessageHandler:
    buffer: list[str]

    def __init__(self):
        self.buffer = []

    def push(self, message: str):
        self.buffer.append(message)
        if len(self.buffer) > constants.GameMessageBufferMaxLimit:
            self.buffer = self.buffer[len(self.buffer) - constants.GameMessageBufferMaxLimit:]

    def retrieve(self) -> str:
        return self.buffer[-1]

class _EventLogHandler:
    log_file: TextIO

    def __init__(self):
        log_file_name: str = datetime.now().strftime("%m-%d-%Y-%H-%M-%S") + ".log"
        self.log_file = codecs.open(log_file_name, mode='a', encoding='utf-8')

    def __del__(self):
        if not self.log_file.closed:
            self.log_file.close()

    def push(self, message: str):
        print(message, file=self.log_file)


class LogWriter:
    game_message_handler: _GameMessageHandler
    event_log_handler: _EventLogHandler

    def __init__(self):
        self.game_message_handler = _GameMessageHandler()
        self.event_log_handler = _EventLogHandler()

    def write_player_log(self, message_name: str, *args):
        message: str = constants.PlayerVisiblePrompts[message_name].format(*args)
        self.game_message_handler.push(message)
        self.event_log_handler.push(message)

    def write_internal_log(self, message_name: str, *args):
        message: str = constants.InternalLogPrompts[message_name].format(*args)
        self.event_log_handler.push(message)

    def retrieve(self) -> str:
        return self.game_message_handler.retrieve()

class AttackFlag(Enum):
    NormalHit = 1
    CriticalHit = 2
    UselessHit = 3


HPDamageCoefficient: float = 0.05  # target HP reduced = damage * (1 - HP_DAMAGE_COEFFICIENT * target.level)
SelfEXPGainCoefficient: int = 2  # self EXP gained = damage * EXP_GAIN_COEFFICIENT
TargetEXPGainUpperLimit: int = 10  # target EXP gained = target.defence * EXP_GAIN_COEFFICIENT
CriticalHitDamage: int = 10

AppeaseExtraEXPCoefficient: float = 0.2
AwardExtraEXPCoefficient: float = 0.5

GameMessageBufferMaxLimit: int = 100

PlayerVisiblePrompts: dict[str, str] = {
    'Damage': '{} attacked {} and caused {} damage!',
    'DamageCritical': '{} attacked {} and caused {} damage! Critical hit!',
    'DamageUseless': '{} attacked {} and caused NO damage! Useless attack!',

    'Health': '{} has {} health left!',

    'LevelMaxAchieved': '{} has reached maximum level!',
    'GainEXP': '{} has gained {} EXP!',
    'LevelUp': 'Congrats! {} has leveled up to {}! Now it has {} EXP points!',
    
    'GainExtraEXP': '{} has gained {} EXP in extra!',
}

InternalLogPrompts: dict[str, str] = {
    'GainExtraEXPWithNoSpecialAttack': '{} tried to get extra EXP but its previous attack is normal.',
}


def _get_damage_flag(damage: int) -> constants.AttackFlag:
    damage_flag: constants.AttackFlag

    if damage > constants.CriticalHitDamage:
        damage_flag = constants.AttackFlag.CriticalHit
    elif damage <= 0:
        damage_flag = constants.AttackFlag.UselessHit
    else:
        damage_flag = constants.AttackFlag.NormalHit

    return damage_flag


class Unit:
    name: str
    health: int
    level: int
    exp: int
    attack: int
    defence: int

    log_writer: LogWriter

    def __init__(self, name: str, attack: int, defence: int, health: int = 100, exp: int = 0, level: int = 1):
        self.name = name
        self.health = health
        self.level = level
        self.exp = exp
        self.attack = attack
        self.defence = defence

        self.log_writer = LogWriter()

    def attack(self, target: "Unit"):
        damage: int = self.attack - target.defence + randint(
            constants.DamageRandomPartLowerLimit,
            constants.DamageRandomPartUpperLimit,
        )
        damage_flag = _get_damage_flag(damage)

        if damage_flag == constants.AttackFlag.CriticalHit:
            self.log_writer.write_player_log("DamageCritical", self.name, target.name, damage)
        elif damage_flag == constants.AttackFlag.UselessHit:
            self.log_writer.write_player_log("DamageUseless", self.name, target.name)
        else:
            self.log_writer.write_player_log("Damage", self.name, target.name, damage)

        if damage_flag != constants.AttackFlag.UselessHit:
            target.health -= int(damage * (1 - constants.HPDamageCoefficient * target.level))
            self.log_writer.write_player_log("Health", self.name, target.health)

            self.gain_normal_exp(damage * constants.SelfEXPGainCoefficient)

        target_gained_exp: int = min(damage, constants.TargetEXPGainUpperLimit)
        target.gain_normal_exp(target_gained_exp)
        if damage_flag != constants.AttackFlag.NormalHit:
            target.gain_extra_exp(target_gained_exp, damage_flag)

    def _gain_exp(self, diff_exp: int):
        self.exp += diff_exp

        if self.exp > constants.EXPPerLevel:
            self.level_up()

    def gain_normal_exp(self, diff_exp: int):
        self._gain_exp(diff_exp)
        self.log_writer.write_player_log('GainEXP', self.name, diff_exp)

    def gain_extra_exp(self, diff_exp: int, attack_flag: constants.AttackFlag):
        if attack_flag == constants.AttackFlag.NormalHit:
            self.log_writer.write_internal_log('GainExtraEXPWithNoSpecialAttack', self.name)
            return

        extra_exp = int(constants.AppeaseExtraEXPCoefficient * diff_exp) \
            if attack_flag == constants.AttackFlag.UselessHit \
            else int(constants.AwardExtraEXPCoefficient * diff_exp)

        self._gain_exp(extra_exp)
        self.log_writer.write_player_log('GainExtraEXP', self.name, extra_exp)

    def level_up(self):
        self.level += self.exp // constants.EXPPerLevel

        if self.level >= constants.MaxLevel:
            self.level = constants.MaxLevel
            self.exp = constants.EXPPerLevel
            self.log_writer.write_player_log("LevelMaxAchieved", self.name)
        else:
            self.exp %= constants.EXPPerLevel
            self.log_writer.write_player_log("LevelUp", self.name, self.level, self.exp)

    def is_alive(self):
        return self.health > 0


class Warrior(Unit):
    def __init__(self, name: str, attack: int = 0, defence: int = 0):
        attack = random.randint(constants.WarriorAttackLowerLimit, constants.WarriorAttackUpperLimit) \
            if not (constants.WarriorAttackLowerLimit <= attack <= constants.WarriorAttackUpperLimit) \
            else attack
        defence = random.randint(constants.WarriorDefenceLowerLimit, constants.WarriorDefenceUpperLimit) \
            if not (constants.WarriorDefenceLowerLimit <= defence <= constants.WarriorDefenceUpperLimit) \
            else defence
        super().__init__(name, attack, defence)


class Tanker(Unit):
    def __init__(self, name, attack: int, defence: int):
        attack = random.randint(constants.TankerAttackLowerLimit, constants.TankerAttackUpperLimit) \
            if not (constants.TankerAttackLowerLimit <= attack <= constants.TankerAttackUpperLimit) \
            else attack
        defence = random.randint(constants.TankerDefenceLowerLimit, constants.TankerDefenceUpperLimit) \
            if not (constants.TankerDefenceLowerLimit <= defence <= constants.TankerDefenceUpperLimit) \
            else defence
        super().__init__(name, attack, defence)




    
import tkinter as tk
from tkinter import ttk

# Assume the Unit, Warrior, Tanker, and LogWriter classes are defined elsewhere
# as well as the constants and other related code.

class BattleGameUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Battle Game")
        self.geometry("800x600")
        self.create_units()
        self.create_widgets()
        self.log_writer = LogWriter()

    def create_units(self):
        # Initialize player and AI units here
        self.player_characters = [Warrior("Player Warrior"), Tanker("Player Tanker")]
        self.ai_characters = [Warrior("AI Warrior"), Tanker("AI Tanker")]

    def create_widgets(self):
        # Create UI widgets for character information and logs
        self.player_frame = ttk.LabelFrame(self, text="Player Characters")
        self.player_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.ai_frame = ttk.LabelFrame(self, text="AI Characters")
        self.ai_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.log_frame = ttk.LabelFrame(self, text="Battle Log")
        self.log_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        self.log_text = tk.Text(self.log_frame, state='disabled', height=10)
        self.log_text.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(self.log_frame, orient="vertical", command=self.log_text.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.log_text.config(yscrollcommand=self.scrollbar.set)

        # Populate player and AI frames with character info
        for player in self.player_characters:
            ttk.Label(self.player_frame, text=str(player)).pack()

        for ai in self.ai_characters:
            ttk.Label(self.ai_frame, text=str(ai)).pack()

        # Attack button (example for player attacking AI)
        self.attack_button = ttk.Button(self, text="Attack", command=self.attack)
        self.attack_button.pack(side="top", pady=10)

    def add_log(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.config(state='disabled')
        self.log_text.see(tk.END)

    def attack(self):
        # Example attack logic: Player's first character attacks AI's first character
        player = self.player_characters[0]
        ai = self.ai_characters[0]
        player.attack(ai)
        # Retrieve and display the log message
        log_message = self.log_writer.retrieve()
        self.add_log(log_message)
        # Update the UI to reflect the new health status
        self.update_character_info()

    def update_character_info(self):
        # Clear existing character info
        for widget in self.player_frame.winfo_children():
            widget.destroy()
        for widget in self.ai_frame.winfo_children():
            widget.destroy()
        # Repopulate character info
        for player in self.player_characters:
            ttk.Label(self.player_frame, text=str(player)).pack()
        for ai in self.ai_characters:
            ttk.Label(self.ai_frame, text=str(ai)).pack()

if __name__ == "__main__":
    app = BattleGameUI()
    app.mainloop()