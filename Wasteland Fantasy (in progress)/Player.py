from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, create_engine

engine = create_engine("sqlite:///Database.db", echo=False)
DB = declarative_base()


class Player_(DB):
    __tablename__ = "Player"
    name = Column(String, primary_key=True)
    race = Column(String)
    max_hp = Column(Integer)
    current_hp = Column(Integer)
    exp = Column(Integer)
    level = Column(Integer)
    exp2lvl = Column(Integer)
    dmg = Column(Integer)
    defense = Column(Integer)
    evasion = Column(Integer)
    inventory = Column(String)
    equipped = Column(String)
    ready = Column(Boolean, unique=False, default=True)
    busy = Column(Boolean, unique=False, default=True)
    combat = Column(Boolean, unique=False, default=True)

    def __init__(self):
        self.name = None
        self.race = None
        self.max_hp = 10
        self.current_hp = self.max_hp
        self.exp = 0
        self.level = 0
        self.exp2lvl = 1
        self.dmg = 1
        self.defense = 0
        self.evasion = 1
        self.inventory = []
        self.equipped = []
        self.ready = False
        self.busy = False
        self.combat = False

    memory_items = []
    memory_equipped = []

    def pond(self):
        x = ""
        for item in self.equipped:
            x += f"You have {item.Name} equipped\n"
        return f"My Name is {self.name}\nI am {self.race} by birth\n" \
               f"I currently have {self.current_hp} of my {self.max_hp} HP\n" \
               f"I am on level {self.level} and have {self.exp} gathered experience\n" \
               f"I need {self.exp2lvl - self.exp} more experience to level up\n" \
               f"I do {self.dmg} damage with a normal hit\n" \
               f"I take {self.defense} less damage due to my defense\n" \
               f"I have a {self.evasion*10}% chance to dodge attacks\n" + x

    def get_inventory(self):
        inv = ""
        for item in self.inventory:
            inv += f"{item.Name}\n~{item.description}\n"
        return inv

    def adjust(self):
        if self.race == "Bathynomic":
            self.defense = 1
        elif self.race == "Whispling":
            self.evasion = 2
        elif self.race == "Voidspawn":
            self.dmg = 2
        elif self.race == "Ursine":
            self.max_hp = 14
            self.current_hp = 14

    def makestring(self):
        i = []
        e = []
        for item in self.equipped:
            e.append(str(item.ID))
        for item in self.inventory:
            i.append(str(item.ID))
        if not i:
            i = "empty"
        if not e:
            e = "empty"
        self.inventory = i
        self.equipped = e


# Races:
# Newtfolk -> healing
# Bathynomic -> blocking
# Whispling -> dodging
# Voidspawn -> damage
# Ursine -> health

DB.metadata.create_all(engine)
