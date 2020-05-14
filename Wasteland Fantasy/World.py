from random import choice
from platform import system
from uuid import uuid1
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine

DB = declarative_base()
engine = create_engine("sqlite:///Database.db", echo=False)

OS = system()


class World_(DB):
    __tablename__ = "World"
    ID = Column(String, primary_key=True)
    Squares = Column(String)
    current_Square = Column(String)
    Quests = Column(String)

    def __init__(self, current_square):
        self.ID = str(uuid1())
        self.Squares = []
        self.current_Square = current_square
        self.Quests = []
        self.Squares.append(self.current_Square)

    def make_map(self):
        # ░░ ▓▓ 웃
        xcoords = []
        ycoords = []
        allcoords = []
        Map = []
        s_Map = ""
        for s in self.Squares:
            x = s.coords.__str__()
            allcoords.append(x)
            x = str(x).split(",")
            xcoords.append(int(x[0]))
            ycoords.append(int(x[1]))
        for quest in self.Quests:
            q = quest.split(",")
            xcoords.append(int(q[0]))
            ycoords.append(int(q[1]))
        if max(ycoords) <= 8:
            ycoords.append(8)
        if min(ycoords) >= -8:
            ycoords.append(-8)
        if max(xcoords) <= 8:
            xcoords.append(8)
        if min(xcoords) >= -8:
            xcoords.append(-8)
        # There's a weird thing where the map stickman goes out
        # of bound if you reach the edge so i append something
        # to keep him in
        for i in range(max(ycoords), int(min(ycoords))-1, -1):
            for j in range(min(xcoords), max(xcoords)+1):
                checker = f"{j},{i}"
                if checker == self.current_Square.coords:
                    Map.append("웃")
                elif checker in self.Quests:
                    Map.append("XX")
                elif checker in allcoords:
                    Map.append("░░")
                else:
                    # make a nice little forrest that happens to be
                    # the exact same size as all squares (͡ ° ͜ʖ ͡ °)
                    Map.append(choice(["↟ ", " ↟", "҂↟", "  ", "͡ ", " ͡"]))      # ҂ ҇ ͡
            if max(xcoords) > 13:
                Map.append(" ")
            elif min(xcoords) < -13:
                Map.append(" ")
            Map.append("\n")
        if not Map:
            Map.append("†웃")
        for e in Map:
            s_Map += e
        return s_Map

    def return_max(self):
        xcoords = []
        ycoords = []
        for s in self.Squares:
            x = s.coords.__str__()
            x = str(x).split(",")
            xcoords.append(int(x[0]))
            ycoords.append(int(x[1]))
        return [max(xcoords), max(ycoords)]

    def makestring(self):
        self.current_Square = str(self.current_Square.ID)
        World_sq = ""
        for square in self.Squares:
            World_sq += str(square.ID + ",")
        self.Squares = World_sq
        quests = ""
        for quest in self.Quests:
            quests += str(quest + ";")
        self.Quests = quests


class Square(DB):
    __tablename__ = "Square"
    ID = Column(String)
    coords = Column(String)
    state = Column(String)
    type = Column(String)
    description = Column(String)
    tier = Column(Integer)
    music = Column(String)
    NPCs = Column(String)
    Floor = Column(String)
    ID2 = Column(String, primary_key=True)

    def __init__(self, coordinate):
        self.ID = str(uuid1())
        self.coords = coordinate
        self.state = None
        self.type = self.type_()
        self.description = self.get_description()
        self.tier = 0
        self.music = None
        self.NPCs = None
        self.Floor = None
        self.ID2 = str(uuid1(2))

    def type_(self):
        if self.coords == "0,0":
            self.music = "start.mp3"
            return "start"
        else:
            return None

    def get_description(self):
        if self.type == "start":
            return "You woke up here\nYou see nothing interesting, just the pond\n"
        elif self.type == "woods":
            return choice(woods)
        elif self.type == "rocky":
            return choice(rocky)
        elif self.type == "grassland":
            return choice(grassland)
        elif self.type == "snowy":
            return choice(snowy)
        elif self.type == "shore":
            return choice(shore)
        elif self.type == "river":
            return choice(river)
        elif self.type == "city":
            return choice(city)
        elif self.type == "spooky":
            return choice(spooky)
        elif self.type == "desert":
            return choice(desert)
        elif self.type == "ocean":
            return choice(ocean)
        elif self.type == "labs":
            return choice(labs)
        elif self.type == "swamp":
            return choice(swamp)
        elif self.type == "void":
            return choice(void)
        elif self.type == "ground0":
            return choice(ground0)
        elif self.type == "factory":
            return choice(factory)
        else:
            return f"{self.type}"

    def rand_type(self):
        tier = self.tier
        tier1 = ["woods", "rocky", "grassland"]
        tier2 = ["snowy", "shore", "river"]
        tier3 = ["city", "spooky", "desert"]
        tier4 = ["ocean", "labs", "swamp"]
        tier5 = ["void", "ground0", "factory"]
        if tier == 1:
            rng = choice(tier1)
            self.music = rng
            return rng
        elif tier == 2:
            rng = choice(tier2)
            self.music = rng
            return rng
        elif tier == 3:
            rng = choice(tier3)
            self.music = rng
            return rng
        elif tier == 4:
            rng = choice(tier4)
            self.music = rng
            return rng
        else:
            rng = choice(tier5)
            self.music = rng
            return rng


# Tier1
woods = ["You are surrounded by high trees and mushrooms\nThe light smell of the pines soothes you\n",
         "You struggle to walk through the dense flora\nEvery step you trip over another vine spanning\nbetween the trees.\n",
         "There is nothing like a relaxing stroll through\nthese beautiful woods\nIf only the air wasn't so toxic..\n",
         "It sure is quiet in these lush woods..\nWAIT.. nevermind, it was just another Snider\n",
         "The trees are dancing in a warm breeze...\nIt really is nice here, I wonder where i am, though..\n"]

rocky = ["\"Sharp stones all around, i really don't want\nto trip here\"\n\n",
         "Who knows what is hiding between those bolders?\nI have heard rumors of adders nesting around\nthese fields.\nBetter not find out...\n",
         "The knife-like stones cut deep into your feet.\nWhat creatures could be tough enough to\nlive here?\n",
         "You struggle to climb over the heaps of rocks\nand bolders.\nOne wrong step and you may brake more\nthan just a limb..\n",
         "OUCH!.. stubbed my toe on a rock again..\nAnother one down....\n"]

grassland = ["Ah, a nice, wide field of grass\n",
             "Who knows what is hiding in the high grass...\n",
             "Did i just hear someone call for me in the high\ngrass....\nMust have been my imagination..\n",
             "I could just lie down on a soft patch and enjoy\nthe sun!\nNo, i should get going...\n",
             "The high grass is slowly moving in a light breeze...\nwait a second..\nI don't feel any wind...\n"]


# Tier2
snowy = ["Brrr.. it really is cold up here....\n",
         "The icy wind feels like knifes cutting into\nmy face...\nAt least the view is nice...\n",
         "There is nothing quite as beautiful as a snowy\nmountain. I would love to enjoy the\nthe view a bit more but my skin is\nalready blue and brittle...\n",
         "I sure hope I don't loose another toe to frostbite\nI don't have many more to spare....\n",
         "Is it getting hot around here?\nSomething tells me I shouldn't trust my\nfeeling here...\n"]

shore = ["A salty breeze, the sound of waves...\nThis shore really is nice..\n",
         "The ocean sure is quiet since most fish\ngrew legs and went terrestrial...\n",
         "I would love to go for a swim but who knows\nwhat the radiation spawned in the waters...\n",
         "I once knew a Bathynomic that hatched in a\nsimilar area...\nThe bone fairies got him in the end\nbut it was fun while it lasted...\n",
         "I would love to float in the shallow waters\nfor a bit but you know...\nIt is really acidic...\n"]

river = ["The first thing to do when trying to survive\nin a foreign place is finding a river!...\nWas it Bear Grylls that said that?...\n",
         "Feel free to take a sip but watch out for\nsharks! They are a real pain since\nthey grew legs...\n",
         "I remember fishing in a river like this\nwhen i was younger but the fish have grown\na lot more confrontative since then...\n",
         "You feel watched... As if something was\nlingering in the muddy water...\n",
         "Most cities are built near rivers...\nShould I follow it?..\n"]


# Tier3
city = ["You stand amidst the ruins of a once great\ncivilization...\n",
        "So many ruins...\nThe few humans that survived soon fell\nvictim to the radiation...\n",
        "All those empty buildings are now nothing but\nmonuments of humanities hubris...\n",
        "Oh how the mighty have fallen...\n",
        "All that's left of this city is ruins and\nghules... Both not so nice...\n"]

spooky = ["I thought I saw a figure...\nBut now there is only fog...\n",
          "I thought I heard someone call my name...\nI need to get out of that fog...\n",
          "I can barely see my own limbs in this fog...\n",
          "Something about this place makes me really\nuncomfortable...\n",
          "All those shadowy figures in the corners\nof my eyes...\nI shouldn't be here...\n"]

desert = ["It's so hot...\nReally makes you miss the mountains\n",
          "NOPE, not drinking that cactus juice!\nNot again...\n",
          "The sun is boiling my skin...\nHow did people live around here?\n",
          "Where did that river go??\nI saw it just behind the dune...\n",
          "I lost a friend to quicksand once...\nBetter watch my steps\n"]


# Tier4
ocean = ["*blub*\n",
         "*blub* *blub* *bliblub*\n",
         "You feel something staring at you from\nfrom the black abyss beneath you...\n",
         "The oceans house some crazy creatures\nOnly the most malformed mutants manage\nto survive in these toxic waters...\n",
         "Just what I needed! A nice swim in\nthe toxic oceans...\n"]

labs = ["I heard stories about experiments done\nin such laboratories...\nSpooky stuff, I tell you...\n",
        "Blinking machines all around you...\nIf only you knew how to use them...\n",
        "I once got a shock while looting\nbewtween such cables...\nBetter stay safe...\n",
        "There are tubes with body parts around\nhere... Just keep going...\n",
        "I remember meeting meeting a living\nmachine a while back.\nIt told me about this place...\n"]

swamp = ["A prime breeding ground for Newtfolk!\n",
         "The smell is disgusting, the water is\nmuddy, the mosquitoes are everywhere...\n",
         "Watch were you tread, the whaligators\nlike to lurk in those areas...\n",
         "Newtfolk have their caves near swamps\nlike this one.\nGetting jumped by a pack of them\nis no joke...\n",
         "The vegetation around those swamps\n tends to be a tad...\nlively...\n"]


# Tier5
void = ["Dang it, slid into the void again!\n",
        "There is no up\nThere is no down\nOnly blackness...\n",
        "I have seen Voidspawn before...\nLet's hope we don't meet any...\n",
        "How can nothing be so big?\n",
        "If this real is truly empty then\nwhat is spawning the voidlings?\n"]

ground0 = ["This is the place where the\nbomb dropped...\n",
           "Life around here is broken\nMutations happen in seconds...\n",
           "This place is crawling with ghules...\n"
           "You feel your skin melting off\nyour body just to regrow in\nmere second...\n",
           "You can feel fingers and toes\ngrowing all over your body...\n"]

factory = ["So this is where they made\nthe bombs...\n",
           "\"Опасность: радиоактивный\"\nI wonder what it means...\n",
           "There are tanks and other military\nvehicles everywhere...\n",
           "There are skeletons sitting\nagainst the wall...\nGuess they didn't want to wait\nfor the radiation to kill them...\n",
           "To think they struggle of three\nnations doomed them all...\n"]


DB.metadata.create_all(engine)
