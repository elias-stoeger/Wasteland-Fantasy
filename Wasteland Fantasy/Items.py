from random import choice
from uuid import uuid1
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

DB = declarative_base()
engine = create_engine("sqlite:///Database.db", echo=False)


class Item(DB):
    __tablename__ = "items"
    ID = Column(String, primary_key=True)
    Name = Column(String)
    boni = Column(String)
    description = Column(String)
    type = Column(String)
    tier = Column(Integer)

    def __init__(self, name, boni, tier):
        self.ID = str(uuid1())
        self.Name = name
        self.boni = boni  # damage, defense, evasion
        self.description = self.get_description()
        self.types = self.get_types()   # gear or potion
        self.tier = tier

    def get_description(self):
        for item in descriptions:
            if self.Name == item[0]:
                return item[1]

    def get_types(self):
        if self.Name == list(potion.keys())[0]:
            return "potion"
        elif self.Name in list(quests_item.keys()):
            return "quest"
        else:
            return "gear"


Items_tier1 = {"a sharp rock": [1, 0, 0],
               "most of a fork": [1, 0, 0],
               "grass armor": [0, 1, 0],
               "a beanie full of ants": [0, 1, 0],
               "a few extra legs": [0, 0, 1],
               "blinking sneakers": [0, 0, 1]}

Items_tier2 = {"a Knfoon": [1, 0, 1],   # Knife + Fork + Spoon
               "a hand full of razor blades": [2, 0, 0],
               "Pants with Ants": [0, 0, 2],
               "fluffy mittens": [0, 2, 0],
               "sandpaper glove": [1, 1, 0],
               "rollerskating gear": [0, 1, 1]}

potion = {"a mysterious liquid": [0, 0, 0]}

quests_item = {"a faded letter": [0, 0, 0],
               "a charred diary": [0, 0, 0],
               "a humanoid-ish skull": [0, 0, 0],
               "a talking book": [0, 0, 0],
               "broken electronics": [0, 0, 0]}

quests_d = {"a faded letter": "A letter... looks old, maybe I\n~should read it?...\n",
            "a charred diary": "The charred remains of a book\n~You can decipher the word \"DIARY\"\n~on its front..\n",
            "a humanoid-ish skull": "The skull of what most likely used\n~to be a humanoid...\n~On the inside you see text\n",
            "a talking book": "\"Hey big boy, wanna know a quest?\n",
            "broken electronics": "There is a fruit on the back, maybe\n~it was used to make food?\n~There is something scratched into\n~the glass part...\n"}

quests = ["\nIt's hard to read...\nSomething about a hidden stash...\nYou mark the place mentioned on your map\n\n",
          "\n\"Note to self: Hide treasure under\nthe fancy stone, make sure noone\nfinds out about it!\"\n"
          "You mark the place on your map\n\n",
          "\nIt looks like a classic treasure map\ndots and a cross and all...\nYou compare it to your map...\n"
          "Yeah, that checks out! You mark the place\non your map\n\n"]

Items_tier1_d = {"a sharp rock": "It's a rock with a pointy end\n~Would be even cooler on a stick...\n",
                 "most of a fork": "It is missing most of the spikes and\n~the hilt is bent. Still better than nothing...\n",
                 "grass armor": "Tufts of grass glued to what\n~used to be a shirt\n",
                 "a beanie full of ants": "A little protection but at what cost...\n",
                 "a few extra legs": "You can never have enough of those!\n",
                 "blinking sneakers": "I am speed\n"}

Items_tier2_d = {"a Knfoon": "A knife, a fork and a spoon all in one?\n~Sign me the frick up!\n",
                 "a hand full of razor blades": "I wonder who's hand this was\n~And why it is holding those...\n",
                 "Pants with Ants": "They *scratch scratch* make you *scratch*\n~super dodgy *scratch scratch*\n",
                 "fluffy mittens": "Protect from spiky stuff and keep you warm\n",
                 "sandpaper glove": "Put the smooth side your way and the\n~rough one the enemies...\n",
                 "rollerskating gear": "May not look the coolest but it\nprovides some protection.\n~Even when not skating!\n"}

potion_d = {"a mysterious liquid": "Could be good, could be bad...\n~Only one way to find out ¯\\_(ツ)_/¯\n"}

# Potions are added multiple times to increase the drop chance since they are pretty essential
items1 = list(Items_tier1.items()) + list(potion.items()) + list(quests_item.items()) + list(potion_d.items()) + list(potion_d.items())
items2 = list(Items_tier2.items()) + list(potion.items()) + list(quests_item.items()) + list(potion_d.items()) + list(potion_d.items())
descriptions = list(Items_tier1_d.items()) + list(Items_tier2_d.items()) + list(potion_d.items()) + list(quests_d.items())


def get_item(tier):
    if tier == 1:
        item = choice(items1)
    else:
        item = choice(items2)
    return Item(item[0], item[1], tier)


synonyms = {"a sharp rock": ["a sharp rock", "sharp rock", "rock", "the sharp rock"],
            "most of a fork": ["most of a fork", "fork", "Fork", "most of fork"],
            "grass armor": ["grass armor", "Grass Armor", "a grass armor", "armor", "Armor"],
            "a beanie full of ants": ["a beanie full of ants", "beanie full of ants", "Beanie", "beanie", "a beanie"],
            "a few extra legs": ["a few extra legs", "extra legs", "legs", "few extra legs", "Legs"],
            "blinking sneakers": ["blinking sneakers", "sneakers", "Blinking Sneakers", "Sneakers"],
            "a Knfoon": ["a Knfoon", "Knfoon", "knfoon", "the knfoon", "a knfoon"],
            "a hand full of razor blades": ["a hand full of razor blades", "hand full of razor blades", "razor blades"],
            "Pants with Ants": ["Pants with Ants", "pants with ants", "pants", "Pants"],
            "fluffy mittens": ["fluffy mittens", "Fluffy mittens", "Fluffy Mittens", "fluffy Mittens", "mittens", "Mittens"],
            "sandpaper glove": ["sandpaper glove", "Sandpaper glove", "Sandpaper Glove", "sandpaper", "glove"],
            "rollerskating gear": ["rollerskating gear", "skating gear", "gear", "Gear"],
            "a mysterious liquid": ["a mysterious liquid", "potion", "Potion", "liquid", "Liquid", "mysterious liquid"],
            "a faded letter": ["letter", "Letter", "faded letter", "Faded letter", "Faded Letter", "a faded letter", "the letter"],
            "a charred diary": ["charred diary", "a charred diary", "Charred diary", "Charred Diary", "diary", "Diary", "the diary"],
            "a humanoid-ish skull": ["a humanoid-ish skull", "humanoid-ish skull", "Skull", "skull", "Humanoid-ish skull"],
            "a talking book": ["a talking book", "talking book", "book", "Book", "Talking book", "the talking book"],
            "broken electronics": ["broken electronics", "Broken electronics", "Broken Electronics", "electronics", "Electronics"]}

DB.metadata.create_all(engine)
