from enum import Enum

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
