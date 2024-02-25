import random
from random import randint
import constants
from logger import LogWriter


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
