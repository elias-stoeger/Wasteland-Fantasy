import random


class Enemy:
    def __init__(self, tier):
        self.tier = tier
        self.name = self.enemy()
        self.hp = random.choice([tier + 1, tier + 2, tier + 3])
        self.dmg = random.choice([tier + 1, tier + 2])

    def enemy(self):
        rng = random.randint(0, 9)
        if rng < 5:
            return None
        elif rng > 5:
            return random.choice(Enemies[self.tier])
        else:
            return random.choice(NPC)


# List of Enemies sorted by tier
Enemies = [["a Ratling", "a Snider", "like 12 or 13 ants", "a Dust Golem", "a Sproutling", "3/4 of an adder"],
           ["an Adder", "an Ent", "a briddle Ghule", "25 to 30 ants", "a Fish with legs", "a bubbling pile of goo"],
           ["a Jackalope", "at least a basket of ants", "a DogCat", "a murdering mantis", "a Whispling", "a Treant"],
           ["a Skin fairy", "hundreds of ants", "a Chimera", "a Skunk with 3 butts", "a Shark with legs", "a Reverse Centaur"],
           ["a Bone Fairy", "a hulking Ant Golem", "a rabid Ursine", "a Voidcrawler", "the Left Arm of the Forbidden One", "Steve"]]

# Gambler NPC -> Sphinx
NPC = ["Gambler", "Trader", "Guide"]


def appear(enemy):
    Appearances_Enemy = [f"\nWatch out!\nYou see {enemy} charging at you\n",
                         f"\nYou just barely manage to dodge the mighty first\nsweep of {enemy}\n"]
    return random.choice(Appearances_Enemy)


def appear_npc(npc):
    if npc == "Guide":
        return random.choice(guide_facts)
    elif npc == "Trader":
        return "trade"
    elif npc == "Gambler":
        return "gamble"


guide_facts = ["\nGuide:\n\"Hey there, sports!\nDid you know that the common Snider once was\ntwo separate animals that merged into\none when they came into contact with a radstone?\nNow isn't that interesting?\"\n",
               "\nGuide:\n\"Oh hey there, champ!\nDid you know that Sproutlings grow up to\nbecome Ents?\nAnd Ents then grow up to be Treants?\nI bet you didn't.. haha...\"\n",
               "\nGuide:\n\"What's up, fella?\nDid you know that, since the bombs fell\nants have stopped being settlers and started\nroaming around in swarms?\nIt's true and the swarms can get exceedingly big!\nLuckily i have never met more then a basket full\nof them...\n",
               "\nGuide:\n\"What's up you goofball?\nDid you know that fairies are compulsive\ncollectors? So much so that we started\nnaming them after what they collect! I sure\nwon't forget the time i ran into that\nBone Fairy...\n"]
