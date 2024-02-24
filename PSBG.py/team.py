class Team:#队伍系统
    def __init__(self, name, units=None):
        self.name = name
        self.units = units or []

    def add_unit(self, unit):
        self.units.append(unit)

    def remove_unit(self, unit):
        self.units.remove(unit)

    def defeat(self):
        return all(not unit.alive() for unit in self.units)