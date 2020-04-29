import random


class Item:
    def __init__(self, name, boni):
        self.Name = name
        self.boni = boni  # damage, defense, evasion
        self.description = self.get_description()
        self.types = self.get_types()   # gear or potion

    def get_description(self):
        for item in descriptions:
            if self.Name == item[0]:
                return item[1]

    def get_types(self):
        if self.Name == list(potion.keys())[0]:
            return "potion"
        else:
            return "gear"


Items_tier0 = {"a sharp rock": [1, 0, 0],
               "most of a fork": [1, 0, 0],
               "grass armor": [0, 1, 0],
               "a beanie full of ants": [0, 1, 0],
               "a few extra legs": [0, 0, 1],
               "blinking sneakers": [0, 0, 1]}

Items_tier1 = {"a Knfoon": [1, 0, 1],   # Knife + Fork + Spoon
               "a hand full of razor blades": [2, 0, 0],
               "Pants with Ants": [0, 0, 2],
               "fluffy mittens": [0, 2, 0],
               "Sandpaper glove": [1, 1, 0],
               "rollerskating gear": [0, 1, 1]}

potion = {"a mysterious liquid": [0, 0, 0]}

Items_tier0_d = {"a sharp rock": "It's a rock with a pointy end\nWould be even cooler on a stick...\n",
               "most of a fork": "It is missing most of the spikes and\nthe hilt is bent. Still better than nothing...\n",
               "grass armor": "Tufts of grass glued to what used to be a shirt\n",
               "a beanie full of ants": "A little protection but at what cost...\n",
               "a few extra legs": "You can never have enough of those!\n",
               "blinking sneakers": "I am speed\n"}

Items_tier1_d = {"a Knfoon": "A knife, a fork and a spoon all in one?\nSign me the frick up!\n",
               "a hand full of razor blades": "I wonder who's hand this was\nAnd why it is holding those...\n",
               "Pants with Ants": "They *scratch scratch* make you *scratch scratch*\nsuper dodgy *scratch scratch*\n",
               "fluffy mittens": "Protect from spiky stuff and keep you warm\n",
               "Sandpaper glove": "Put the smooth side your way and the\nrough one the enemies...\n",
               "rollerskating gear": "May not look the coolest but it\nprovides some protection.\nEven when not skating!\n"}

potion_d = {"a mysterious liquid": "Could be good, could be bad...\n Only one way to find out ¯\_(ツ)_/¯\n"}

items = list(Items_tier0.items()) + list(Items_tier1.items()) + list(potion.items())
descriptions = list(Items_tier0_d.items()) + list(Items_tier1_d.items()) + list(potion_d.items())


def get_item():
    item = random.choice(items)
    return Item(item[0], item[1])
