import random
import platform


OS = platform.system()


class World:
    def __init__(self, current_square):
        self.Squares = []
        self.bioms = []
        self.current_Square = current_square
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
        if max(ycoords) <= 8:
            for x in range(8, max(ycoords), -1):
                Map.append("\n")
        # There's a weird thing where the map stickman goes out
        # of bound if you reach the edge so i append something
        # to keep him in
        for i in range(max(ycoords), int(min(ycoords))-1, -1):
            if max(xcoords) > 13:
                if OS == "Windows":
                    Map.append(" ↟")
                else:
                    Map.append("   ↟")
            elif min(xcoords) < -13:
                if OS == "Windows":
                    Map.append(" ↟")
                else:
                    Map.append("   ↟")
            if max(xcoords) > 14:
                for x in range(max(xcoords), 13, -1):
                    if OS == "Windows":
                        Map.append("  ")
                    else:
                        Map.append("      ")
            if min(xcoords) < -14:
                for x in range(min(xcoords), -13, 1):
                    if OS == "Windows":
                        Map.append("  ")
                    else:
                        Map.append("      ")
            for j in range(min(xcoords), max(xcoords)+1):
                checker = f"{j},{i}"
                if checker == self.current_Square.coords:
                    Map.append("†웃")
                elif checker in allcoords:
                    Map.append("░░")
                else:
                    # make a nice little forrest that happens to be
                    # the exact same size as all squares (͡ ° ͜ʖ ͡ °)
                    if OS == "Windows":
                        Map.append(random.choice(["↟ ", "↟ ", " ↟", "↟↟", " ."]))
                    else:
                        Map.append(random.choice([" ↟ ", "↟  ", "  ↟"]))
            if max(xcoords) > 13:
                Map.append(" ")
            elif min(xcoords) < -13:
                Map.append(" ")
            Map.append("\n")
        if Map == []:
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


class Square:
    def __init__(self, coordinate):
        self.coords = coordinate
        self.state = None
        self.inhab = self.inhabs()
        self.type = self.type_()
        self.description = self.get_description()
        self.tier = 0
        self.music = None
        self.NPCs = None

    def inhabs(self):
        return "todo"

    def type_(self):
        if self.coords == "0,0":
            self.music = "start.mp3"
            return "start"
        else:
            return None

    def get_description(self):
        if self.type == "start":
            return "You woke up here\nYou see nothing interesting, just the pond"
        elif self.type == "woods":
            return random.choice(woods)
        elif self.type == "rocky":
            return random.choice(rocky)
        elif self.type == "grassland":
            return random.choice(grassland)
        else:
            return f"{self.type}"

    def rand_type(self):
        tier = self.tier
        tier1 = ["woods", "rocky", "grassland"]
        if tier == 1:
            rng = random.choice(tier1)
            self.music = rng
            return rng
        else:
            return "What is you doing??"


woods = ["You are surrounded by high trees and mushrooms\nThe light smell of the pines soothes you\n",
         "You struggle to walk through the dense flora\nEvery step you trip over another vine spanning\nbetween the trees.\n",
         "There is nothing like a relaxing stroll through\nthese beautiful woods\nIf only the air wasn't so toxic..\n",
         "It sure is quiet in these lush woods..\nWAIT.. nevermind, it was just another Snider\n",
         "The trees are dancing in a warm breeze...\nIt really is nice here, I wonder where i am, though..\n"]


rocky = ["\"Sharp stones all around, i really don't want\nto trip here\"\n",
         "Who knows what is hiding between those bolders?\nI have heard rumors of adders nesting around\nthese field.\nBetter not find out...\n",
         "The knife-like stones cut deep into your feet.\nWhat creatures could be tough enough to\nlive here?",
         "You struggle to climb over the heaps of rocks\nand bolders.\nOne wrong step and you may brake more\nthan just a limb..\n"]


grassland = ["Ah, a nice, wide field of grass\n",
             "Who knows what is hiding in the high grass...\n",
             "Did i just hear someone call for me in the high\ngrass....\nMust have been my imagination..\n",
             "I could just lie down on a soft patch and enjoy\nthe sun!\nNo, i should get going...\n"]
