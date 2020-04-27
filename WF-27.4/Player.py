class Player:
    def __init__(self):
        self.name = None
        self.race = None
        self.max_hp = 10
        self.current_hp = self.max_hp
        self.exp = 0
        self.exp2lvl = 1  # Maybe do (level +1)^2
        self.dmg = 1
        self.level = 0
        self.defense = 0
        self.evasion = 1
        self.inventory = []
        self.equipped = []
        self.ready = False
        self.busy = False

    def pond(self):
        return f"My Name is {self.name}\nI am {self.race} by birth\n" \
               f"I currently have {self.current_hp} of my {self.max_hp} HP\n" \
               f"I am on level {self.level} and have {self.exp} gathered experience\n" \
               f"I need {self.exp2lvl - self.exp} more experience to level up\n" \
               f"I do {self.dmg} damage with a normal hit\n" \
               f"I take {self.defense} less damage due to my defense\n" \
               f"I have a {self.evasion*10}% chance to dodge attacks"

    def adjust(self):
        if self.race == "Bathynomic":
            self.defense = 1
        elif self.race == "Whispling":
            self.evasion = 2
        elif self.race == "Voidspawn":
            self.dmg = 3
        elif self.race == "Ursine":
            self.max_hp = 14
            self.current_hp = 14


# Races:
# Newtfolk -> healing
# Bathynomic -> blocking
# Whispling -> dodging
# Voidspawn -> damage
# Ursine -> health
