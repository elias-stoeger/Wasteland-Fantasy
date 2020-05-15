from Player import Player_
from Items import *
from Commands import *
from Enemies import *
from World import *
from tkinter import Tk, Text, Button, Label, PhotoImage, INSERT, Toplevel, W, N, NORMAL, END, DISABLED, Scrollbar, \
    RIGHT, Y, BOTTOM, X, S, Entry, mainloop, NONE, E, WORD
from platform import system
from pygame import mixer, mixer_music
from sqlalchemy import Column, String, create_engine, Boolean, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from copy import deepcopy
from os import chmod
from stat import S_IREAD, S_IWUSR

# All music is royalty free and from https://www.bensound.com/royalty-free-music
# Ocean by Hazy
# https://soundcloud.com/hazy_music
# Music provided by https://www.plugnplaymusic.net
# --------------------------------------------------------
# or the youtube channels
# https://www.youtube.com/channel/UCNg336DNlXPJ4mNML9J292w
# https://www.youtube.com/channel/UCcavSftXHgxLBWwLDm_bNvA
# https://www.youtube.com/channel/UCJS15kO-_Ns3f_sGLHwzYFg

# The main background is from https://www.deviantart.com/marylise
# also free for use

# Play it on Linux for the prettiest experience

chmod("Database.db", S_IWUSR | S_IREAD)
engine = create_engine("sqlite:///Database.db", echo=False)
if not database_exists("sqlite:///Database.db"):
    create_database("sqlite:///Database.db")
DB = declarative_base()
sessionClass = sessionmaker(bind=engine)
session = sessionClass()
Meta = MetaData()

root = Tk()
root.geometry("893x664+100+100")
root.title("Wasteland Fantasy")
root.grid_propagate(False)

# since I usually work on Linux but it looks not quite the same
# I change it a little depending on the OS
OS = system()

root.grid_columnconfigure(1, weight=3)
root.grid_columnconfigure(2, weight=1)
root.grid_rowconfigure(5, weight=2)
root.grid_rowconfigure(1, weight=3)

background_image = PhotoImage(file="Background.png")
background_label = Label(root, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Noone's messing with my window
root.resizable(0, 0)

if OS == "Windows":
    from ctypes import windll

    # The failed abortion of an OS that is Windows
    # messes up the font, displaying it blurry so
    # I use this line to fix that complete bs
    windll.shcore.SetProcessDpiAwareness(2)
    # Thanks for nothing, Bill


# That's for getting rid of that nasty border of the window
# root.overrideredirect(True)


foundS = False
while foundS is False:
    fileName = "scores.txt"
    try:
        with open(fileName, "r") as file:
            Score = file.read().split(",")
            if Score == [""] or Score == []:
                Score = None
        foundS = True
    except:
        with open(fileName, "w+") as file:
            test = file.read()

# We don't want you falsifying your best scores :)
chmod("scores.txt", S_IREAD)
# I know it's not hard to get around it, it's more
# of a discouragement...


class Everything_(DB):
    __tablename__ = "Everything"
    pnd = Column(String(20))
    doneCombat = Column(Boolean, default=False)
    foundItem = Column(Boolean, default=False)
    alive = Column(Boolean, default=True, primary_key=True)
    trading = Column(Boolean, default=False)
    gambling = Column(Boolean, default=False)

    def __init__(self):
        self.pnd = "False"
        self.doneCombat = False
        self.foundItem = False
        self.alive = True
        self.trading = False
        self.gambling = False
        self.Trade = None
        self.roll = None
        self.map_uptodate = True
        self.inventory_uptodate = True
        self.character_uptodate = True


Everything = Everything_()

Player = Player_()
mixer.init()
DB_player = session.query(World_).first()
logs_ = []
logs = Table(
    "logs", Meta,
    Column("ID", String, primary_key=True),
    Column("entries", String),
)


def load():
    chmod("Database.db", S_IWUSR | S_IREAD)
    DB_P = session.query(Player_).first()
    DB_W = session.query(World_).first()
    DB_L = engine.connect().execute(logs.select())
    DB_E = session.query(Everything_).first()
    DB_S = session.query(Square).all()
    DB_I = session.query(Item).all()
    DB_N = session.query(Enemy).all()

    # Items
    DB_Items = []
    for item in DB_I:
        item.boni = item.boni.split(",")
        item.boni[0] = int(item.boni[0])
        item.boni[1] = int(item.boni[1])
        item.boni[2] = int(item.boni[2])
        i = Item(item.Name, item.boni, item.tier)
        i.ID = item.ID
        DB_Items.append(deepcopy(i))
    Item_Dict = {}
    for item in DB_Items:
        Item_Dict[item.ID] = item

    # Player
    Player.name = DB_P.name
    Player.race = DB_P.race
    Player.max_hp = DB_P.max_hp
    Player.current_hp = DB_P.current_hp
    Player.exp = DB_P.exp
    Player.level = DB_P.level
    Player.exp2lvl = DB_P.exp2lvl
    Player.dmg = DB_P.dmg
    Player.defense = DB_P.defense
    Player.evasion = DB_P.evasion
    DB_P.inventory = DB_P.inventory.split(",")
    DB_P.equipped = DB_P.equipped.split(",")
    loaded_inv = []
    for item in DB_P.inventory:
        # for no god-damned reason whatsoever, some of the
        # items have a space between the inner and outer "..
        # TOOK ME A WHILE TO REALIZE WHY THE ITEMS WERE DISAPPEARING
        # but now it should work
        item = item.strip()
        if item[1:-1] in Item_Dict:
            loaded_inv.append(Item_Dict[item[1:-1]])
    loaded_equ = []
    for item in DB_P.equipped:
        item = item.strip()
        if item[1:-1] in Item_Dict:
            loaded_equ.append(Item_Dict[item[1:-1]])
    Player.inventory = loaded_inv
    Player.equipped = loaded_equ
    Player.ready = DB_P.ready
    Player.busy = DB_P.busy
    Player.combat = DB_P.combat

    # Enemies
    Enemy_Dict = {}
    DB_Enemies = []
    for enemy in DB_N:
        e = Enemy(enemy.tier)
        e.ID = enemy.ID
        e.name = enemy.name
        DB_Enemies.append(deepcopy(e))
        Enemy_Dict[e.ID] = e

    # Squares
    DB_Squares = []
    for square in DB_S:
        if square.NPCs in Enemy_Dict:
            square.NPCs = Enemy_Dict[square.NPCs]
        else:
            square.NPCs = None
        if square.Floor == "empty":
            square.Floor = None
        if square.Floor is not None:
            for i in range(len(DB_Items)):
                if square.Floor == DB_Items[i].ID:
                    square.Floor = DB_Items[i]
                else:
                    square.Floor = None
        f = Square(square.coords)
        f.ID = square.ID
        f.state = square.state
        f.type = square.type
        f.description = square.description
        f.tier = square.tier
        f.music = square.music
        f.NPCs = square.NPCs
        f.Floor = square.Floor
        DB_Squares.append(deepcopy(f))

    # Logs
    for log in DB_L:
        logs_.append(log.entries)

    # World
    DB_W.Squares = []
    for piece in DB_Squares:
        DB_W.Squares.append(deepcopy(piece))
    for i in DB_Squares:
        if DB_W.current_Square == i.ID:
            DB_W.current_Square = deepcopy(i)
    global World
    World = World_(DB_W.current_Square)
    World.Squares = DB_W.Squares
    World.Quests = DB_W.Quests.split(";")
    if World.Quests == ['']:
        World.Quests = []
    if "" in World.Quests:
        World.Quests.remove("")

    # Everything
    Everything.doneCombat = DB_E.doneCombat
    Everything.foundItem = DB_E.foundItem
    Everything.alive = DB_E.alive
    Everything.trading = DB_E.trading
    Everything.gambling = DB_E.gambling
    Screen.config(state=NORMAL)
    Screen.see("end")
    Log.see("end")
    Screen.config(state=DISABLED)
    chmod("Database.db", S_IREAD)


def help_():
    help_pop = Toplevel()
    if OS == "Windows":
        help_pop.geometry("400x370")
    else:
        help_pop.geometry("400x330")
    help_pop.title("Help")
    Text_ = Label(help_pop, anchor=W, justify="left",
                  text="Here is how this game is played:\n\n"
                       "There are 3 buttons and a command line\n"
                       "\"Inventory\" opens a window with all your items\n"
                       "\"Map\" shows a map of all places you have visited\n"
                       "\"Character\" shows information about your Character,\n"
                       "things like your level, your race and your stats.\n\n"
                       "The white line at the bottom is your command line\n"
                       "You can just type what you want to do but keep it crisp!\n"
                       "Something like \"hit the goblin\" or \"take the ring\" + Enter\n\n"
                       "You can see your personal best by writing \"score\"\n\n"
                       "You move by giving your direction in cardinal directions:\n"
                       "\"go north\", \"go south\" and stuff like that.\n"
                       "I am sure you will figure the rest out yourself...\n"
                       "If not you can write \"help\" in the command line.\n"
                       "I hope you enjoy :)")
    Text_.grid(row=0, column=0)
    if OS == "Windows":
        Text_.config(font=("Times", 12))
    Text_.grab_set()
    help_pop.transient()


def start():
    if DB_player is None:
        mixer_music.load("Music/start.mp3")
        mixer_music.play(-1)
        mixer.music.set_volume(0.4)
        Screen.insert(INSERT, "You wake up in a forest glade,\nthe morning sun blinding you,\n"
                              "the sounds of birds and critters around you.\n"
                              "They are so loud your head hurts\n\"Am I hungover?\", you think..."
                              "\n\nSome water would do wonders.\n"
                              "You look around and spot a pond at the edge\nof the glade...\n")

        Log.insert(INSERT, "Log:\n"
                           "You woke up\n")
        logs_.append("Log:\nYou woke up\n")
    else:
        mixer_music.load(f"Music/{World.current_Square.music}.mp3")
        mixer_music.play(-1)
        mixer.music.set_volume(0.4)
        Screen.insert(INSERT, World.current_Square.description)
        for element in logs_:
            Log.insert(INSERT, element)
        Screen.config(state=NORMAL)
        Screen.insert(INSERT, "You wake up from your nap...\n\n")
        Screen.insert(INSERT, World.current_Square.description)
        if World.current_Square.Floor is not None:
            Screen.insert(INSERT, f"\n{World.current_Square.Floor.Name} is sitting on the floor...\n")
        if World.current_Square.state != "clear":
            Screen.insert(INSERT, "\nThe enemy got bored of waiting and went away...\n")
            Player.combat = False
            Player.busy = False
            World.current_Square.NPCs = None
            World.current_Square.Floor = None
        elif Everything.trading is True or Everything.gambling is True:
            Screen.insert(INSERT, "\n The figure is gone...\nI guess they had better things to do than wait...\n")
            Everything.trading = False
            Everything.gambling = False
        Screen.config(state=DISABLED)
        Log.see("end")


def clear_db():
    chmod("Database.db", S_IREAD | S_IWUSR)
    it = session.query(Player_).all()
    for x in it:
        session.delete(x)
    it = session.query(Item).all()
    for x in it:
        session.delete(x)
    it = session.query(World_).all()
    for x in it:
        session.delete(x)
    it = session.query(Square).all()
    for x in it:
        session.delete(x)
    it = session.query(Everything_).all()
    for x in it:
        session.delete(x)
    it = session.query(Enemy).all()
    for x in it:
        session.delete(x)
    session.commit()
    conn = engine.connect()
    conn.execute(logs.delete())
    chmod("Database.db", S_IREAD)


def enter(event=None):
    x = Input.get()
    Input.delete(0, "end")
    com = commands(x)
    Screen.config(state=NORMAL)
    Log.config(state=NORMAL)
    last_square = World.current_Square
    coords = []
    if Everything.alive is False:
        clear_db()
        chmod("scores.txt", S_IWUSR | S_IREAD)
        if Score is not None:
            if Player.level > int(Score[2]):
                with open(fileName, "w+") as savedScores:
                    savedScores.write(f"{Player.name},{Player.race},{Player.level},{int(Score[3]) + 1}")
            else:
                with open(fileName, "w+") as savedScores:
                    savedScores.write(f"{Score[0]},{Score[1]},{Score[2]},{int(Score[3]) + 1}")
        else:
            with open(fileName, "w+") as savedScores:
                savedScores.write(f"{Player.name},{Player.race},{Player.level},1")
        Screen.delete("1.0", END)
        Everything.alive = True
        for entry in logs_:
            logs_.remove(entry)
        Log.delete("1.0", END)
        Player.inventory = []
        Player.equipped = []
        Player.ready = False
        World.current_Square = Square("0,0")
        World.Squares = [World.current_Square]
        World.Quests = []
        Everything.inventory_uptodate = False
        Everything.map_uptodate = False
        Everything.character_uptodate = False
        World.current_Square.music = "start"
        start()
        chmod("scores.txt", S_IREAD)
    elif com == "suicide":
        if Player.ready is True:
            Everything.alive = False
            Screen.insert(INSERT, "\nYou decide to end it all...\n"
                                  "You take a shard of glass from the ground and...\n"
                                  "You commit Sudoku...")
        else:
            Screen.insert(INSERT, "\nYou don't even know who you are yet, chill...\n")
    elif Everything.gambling:
        if x in ["yes", "Yes"] and Everything.roll is None:
            Everything.roll = randint(1, 6)
            Screen.insert(INSERT, "\"Very well, here's how we do it:\n"
                                  "I will roll a die and show the number..\n"
                                  "Then it is your turn, if you roll higher\n"
                                  "than me, I will give you an Item...\n"
                                  "If you roll lower, I will take one of\n"
                                  "your precious items...\n And if we roll the same I will take\n"
                                  "half of your current HP...\"\n\n"
                                  "The gambler takes out a worn out wooden die and...\n\n"
                                  f"He rolls a {Everything.roll}\n")
        elif x in ["no", "No"] and Everything.roll is None:
            Screen.insert(INSERT, f"\"Pff.. I expected nothing different from\na {Player.race}...\n")
            Everything.gambling = False
        elif com == "roll":
            roll = randint(1, 6)
            Screen.insert(INSERT, f"\nYou roll a {roll}\n\n")
            if roll > Everything.roll:
                item = get_item(World.current_Square.tier)
                Screen.insert(INSERT, f"\n\"Hmpf, very well...\"\n"
                                      f"The gambler hands you {item.Name}\n\n")
                Player.inventory.append(item)
                Log.insert(INSERT, f"You won\n{item.Name}\n\n")
                logs_.append(f"You won\n{item.Name}\n\n")
            elif roll < Everything.roll:
                stuff = []
                for item in Player.inventory + Player.equipped:
                    stuff.append(item)
                loss = choice(stuff)
                if loss in Player.inventory:
                    Player.inventory.remove(loss)
                else:
                    loose_stats(loss.boni)
                    Player.equipped.remove(loss)
                Screen.insert(INSERT, f"Harharhar.. your {loss.Name}\nwill look good in my collection..\n")
                Log.insert(INSERT, f"You lost {loss.Name}\nto a gambler...\n\n")
                logs_.append(f"You lost {loss.Name}\nto a gambler...\n\n")
            else:
                Screen.insert(INSERT, f"The figure takes out a small knife and with\na swift cut...\n"
                                      f"You loose {(Player.current_hp + 1) // 2} HP..\n")
                Player.current_hp -= (Player.current_hp + 1) // 2
                if Player.current_hp <= 0:
                    Everything.alive = False
                    Screen.insert(INSERT, "\nYou die a fools death...")
                    save()
            Everything.gambling = False
            Everything.roll = None
            Everything.inventory_uptodate = False
            Everything.character_uptodate = False
        else:
            Screen.insert(INSERT, "Come on, kid.. roll the die...\n")
    elif Everything.trading:
        if x in ["yes", "Yes"]:
            Screen.insert(INSERT, "\n\"Hehehe...\"\n")
            Log.insert(INSERT, f"You traded\n"
                               f"{Everything.Trade[1].Name} for\n{Everything.Trade[0].Name}\n\n")
            logs_.append(f"You traded\n{Everything.Trade[1].Name} for\n{Everything.Trade[0].Name}\n\n")
            found = 0
            while found != -1 and found <= len(Player.inventory) - 1:
                if Player.inventory[found] == Everything.Trade[1]:
                    Player.inventory.remove(Player.inventory[found])
                    Player.inventory.append(Everything.Trade[0])
                    Player.current_hp -= Player.current_hp // 4
                    Everything.trading = False
                    found = -1
                else:
                    found += 1
            if Everything.trading:
                found -= found
                while found != -1 and found <= len(Player.equipped) - 1:
                    if Player.equipped[found] == Everything.Trade[1]:
                        Player.equipped.remove(Player.equipped[found])
                        Player.inventory.append(Everything.Trade[0])
                        Player.current_hp -= Player.current_hp // 4
                        Everything.trading = False
                        found = -1
                    else:
                        found += 1
            Everything.inventory_uptodate = False
            Everything.character_uptodate = False
        elif x in ["no", "No"]:
            Everything.trading = False
            Screen.insert(INSERT, "\n\"Get lost then....\"")
        else:
            Screen.insert(INSERT, "\nDefinitively honest trader:\n\"What was that?\"\n")
    elif x == "help":
        Screen.delete("1.0", END)
        Screen.insert(INSERT, "Here's a few commands and what they do:\n"
                              "\"pond\" will start the character creation\n"
                              "\"attack\" makes you attack an enemy\n"
                              "\"north\", \"east\", \"south\" and \"west\" make you\n"
                              "go that direction\n"
                              "\"take\" for picking up stuff\n"
                              "\"read ITEM\" for reading texts and books\n"
                              "\"equip ITEM\" to equip items\n"
                              "\"unequip ITEM\" to, well, unequip items\n"
                              "\"drink ITEM\" to drink items that are potions\n"
                              "\"flee\" to flee from combat\n"
                              "\nThose are not the only way you can call them\n"
                              "but I don't want to spoil all the fun\n"
                              "If you still struggle, look inwards :^)")
    elif com == "pond" or Everything.pnd is True:
        if Everything.pnd is True and Player.name is None:
            Player.name = x
            Screen.delete('1.0', END)
            Screen.insert(INSERT, f"My name is {Player.name}\nI am of ... descent\n\n"
                                  f"Newtfolk\nBathynomic\nWhispling\nVoidspawn\nUrsine\n"
                                  f"\n\n\nFor information about the races  type \"info race\"\n\n"
                                  f"replace \"race\" with the race you want to know more about")
        elif Everything.pnd is True and Player.name is not None and com in ["newt", "bathy", "whisp", "void", "ursine"]:
            Screen.delete('1.0', END)
            Screen.insert(INSERT, infos(com))
        elif Everything.pnd is True and com in ["Newtfolk", "Bathynomic", "Whispling", "Voidspawn", "Ursine"]:
            Player.race = com
            Player.adjust()
            Player.ready = True
            World.current_Square.state = "clear"
            Screen.delete('1.0', END)
            Screen.insert(INSERT, f"You gaze into the water and see your reflection:\n\n{Player.pond()}\n\n\n"
                                  f"Use the cardinal directions (North, East, South and West)\nto move around")
            Log.insert(INSERT, "\nYou remembered who \nyou are\n\n")
            logs_.append("\nYou remembered who \nyou are\n\n")
            Everything.pnd = False
            Everything.character_uptodate = False
        elif World.current_Square.type == "start" and World.current_Square.state is None and Everything.pnd == "False":
            Everything.pnd = True
            Screen.delete('1.0', END)
            if Player.name is None:
                Screen.insert(INSERT, f"You gaze into the water and see your reflection:\nMy name is....")
        elif World.current_Square.type == "start" and Player.ready is True:
            Screen.delete('1.0', END)
            Screen.insert(INSERT, f"You gaze into the water and see your reflection:\n\n{Player.pond()}")
        elif Player.ready is True:
            Screen.delete('1.0', END)
            Screen.insert(INSERT, "There is no pond to gaze into here...")
    elif com == "pond" and Player.ready is True and World.current_Square.type == "start":
        Screen.delete('1.0', END)
        Screen.insert(INSERT, f"You gaze into the water and see your reflection:\n\n{Player.pond()}")
    elif com in ["w", "n", "e", "s"] and Player.ready is True and Player.busy is False and Player.combat is False:
        x = World.current_Square.coords.split(",")[0]
        y = World.current_Square.coords.split(",")[1]
        if com == "w":
            newSquare = f"{int(x) - 1},{int(y)}"
        elif com == "n":
            newSquare = f"{int(x)},{int(y) + 1}"
        elif com == "e":
            newSquare = f"{int(x) + 1},{int(y)}"
        else:
            newSquare = f"{int(x)},{int(y) - 1}"
        for s in World.Squares:
            coords.append(s.coords)
        if newSquare in coords:
            for t in World.Squares:
                if t.coords == newSquare:
                    World.current_Square = t
        else:
            World.current_Square = Square(newSquare)
            World.Squares.append(World.current_Square)
        prep_square(last_square)
    elif com == "attack":
        if Player.combat is False:
            Screen.insert(INSERT, "\nThere is nothing to attack here..\nYou decide to punch the ground instead\n")
        else:
            combat()
    elif com == "flee":
        if Player.combat is False:
            Screen.insert(INSERT, "\nYou start running in circles in panic!\nBut wait.. where is the threat?\n")
        else:
            rng = randint(0, 9)
            if rng > 4:
                x = World.current_Square.coords.split(",")[0]
                y = World.current_Square.coords.split(",")[1]
                newSquare = choice([f"{int(x)},{int(y) - 1}", f"{int(x)},{int(y) + 1}",
                                    f"{int(x) - 1},{int(y)}", f"{int(x) + 1},{int(y)}"])
                for s in World.Squares:
                    coords.append(s.coords)
                if newSquare in coords:
                    for t in World.Squares:
                        if t.coords == newSquare:
                            World.current_Square = t
                else:
                    World.current_Square = Square(newSquare)
                    World.Squares.append(World.current_Square)
                Player.combat = False
                prep_square(last_square)
            else:
                Screen.insert(INSERT, "\nYou try to run but your trip over your legs while turning...\n\n")
                enemy_turn()
            Everything.character_uptodate = False
    elif com == "take":
        if World.current_Square.Floor is not None:
            Screen.insert(INSERT, f"\nYou pick up {World.current_Square.Floor.Name} and\nstuff it in your backpack.\n")
            Player.inventory.append(World.current_Square.Floor)
            Log.insert(INSERT, f"You found\n{World.current_Square.Floor.Name}\n\n")
            logs_.append(f"You found\n{World.current_Square.Floor.Name}\n\n")
            World.current_Square.Floor = None
            Everything.inventory_uptodate = False
        else:
            Screen.insert(INSERT, "\nYou pick a flower and stick it behind your ear...\n"
                                  "There is nothing else to pick up here...\n")
    elif com[0] == "equip":
        equipped = []
        for item in Player.equipped:
            equipped.append(item)
        if len(equipped) > 1:
            Screen.insert(INSERT, "You can't equip more items, unequip some first...\n")
        elif com[1] not in synonyms["a mysterious liquid"] + synonyms["a faded letter"] + synonyms["a charred diary"] + synonyms["a humanoid-ish skull"] + synonyms["a talking book"] + synonyms["broken electronics"]:
            for item in Player.inventory:
                if com[1] == item.Name:
                    Player.equipped.append(item)
                    Player.inventory.remove(item)
                    Screen.insert(INSERT, f"\nYou equipped {item.Name}\n\n")
                    get_stats(item.boni)
            if Player.equipped == equipped:
                Screen.insert(INSERT, f"\nYou don't have {com[1]} in your inventory...\n")
        else:
            Screen.insert(INSERT, "\nMan, how do you image that working?\n\n")
        Everything.character_uptodate = False
        Everything.inventory_uptodate = False
    elif com[0] == "drink" or com[0] == "use":
        if com[1] in synonyms["a mysterious liquid"]:
            found = False
            for item in Player.inventory:
                if item.Name == com[1] and found is False:
                    found = True
                    drink_potion()
                    Player.inventory.remove(item)
            if found is False:
                Screen.insert(INSERT, f"You don't have {com[1]} in\nyour backpack.\n")
            Everything.character_uptodate = False
            Everything.inventory_uptodate = False
        else:
            Screen.insert(INSERT, f"\nYou can't {com[0]} {com[1]}...\n")
    elif com[0] == "unequip":
        unequipped = False
        for item in Player.equipped:
            if item.Name == com[1]:
                loose_stats(item.boni)
                Screen.insert(INSERT, f"You take off {com[1]}\n")
                Player.equipped.remove(item)
                Player.inventory.append(item)
                unequipped = True
        if unequipped is False:
            Screen.insert(INSERT, f"You don't seem to be wearing {com[1]}\n")
        Everything.character_uptodate = False
        Everything.inventory_uptodate = False
    elif com == "score":
        if Score is not None:
            Screen.delete("0.1", END)
            Screen.insert(INSERT, f"Best run:\n{Score[0]}, a vagabond of {Score[1]} descent...\n"
                                  f"reached level {Score[2]}\n\n"
                                  f"You lived and died a total of {Score[3]} times...\n\n")
        else:
            Screen.insert(INSERT, "\nNo scores saved...\n\n")
    elif com == "read_w":
        Screen.insert(INSERT, "\nYou start to read your hand\nyou read your tea leaves\nyou read in the essence of time...\n"
                              "How about you tell me what exactly you\nwant to read....\n\n")
    elif com[0] == "read":
        found = False
        for item in Player.inventory:
            if com[1] == item.Name and com[1] in list(quests_item.keys()):
                Player.inventory.remove(item)
                Screen.insert(INSERT, choice(quests))
                x = World.current_Square.coords.split(",")[0]
                y = World.current_Square.coords.split(",")[1]
                QuestSquare = f"{int(x) + randint(-15, 15)},{int(y) + randint(-15, 15)}"
                World.Quests.append(QuestSquare)
                found = True
                Everything.inventory_uptodate = False
                Everything.map_uptodate = False
        if found is False:
            Screen.insert(INSERT, f"\nYou can't read {com[1]}\n\n")
    elif com == "look":
        if World.current_Square.coords in World.Quests:
            item = get_item(Player.level // 5 + 1)
            Screen.insert(INSERT, f"\nYou look around and... OH! What's that?\nYou find {item.Name}!\nYou put it in your backpack.\n\n")
            Player.inventory.append(item)
            Log.insert(INSERT, f"You found\n{item.Name}")
            logs_.append(f"You found\n{item.Name}")
            World.Quests.remove(World.current_Square.coords)
            Everything.map_uptodate = False
            Everything.inventory_uptodate = False
        else:
            Screen.insert(INSERT, "\nYou look around and see...\nSome corpses..\nA few sludge pools..\nMost of what used to be a car..\nNothing of value to loot\n\n")
    elif com == "nothing":
        Screen.insert(INSERT, f"\nYou don't know how to {x}...\n")
    Screen.see("end")
    Log.see("end")
    Screen.config(state=DISABLED)
    Log.config(state=DISABLED)


def get_stats(boni):
    Player.dmg += boni[0]
    Player.defense += boni[1]
    Player.evasion += boni[2]


def loose_stats(boni):
    Player.dmg -= boni[0]
    Player.defense -= boni[1]
    Player.evasion -= boni[2]


def drink_potion():
    rng = randint(0, 9)
    if rng > 3:
        Screen.insert(INSERT, "Your health has been restored!\n")
        Player.current_hp = Player.max_hp
    else:
        if Player.current_hp >= 1:
            Screen.insert(INSERT, f"Yuck, that wasn't good...\nYou loose {Player.current_hp // 2} health...\n")
            Player.current_hp -= Player.current_hp // 2
        else:
            Screen.insert(INSERT, "Eww.. You puke a little but you will hang on for now...\n")


def prep_square(last_square):
    World.current_Square.tier = Player.level // 5 + 1
    rng = randint(0, 9)
    if World.current_Square.type is None:
        if rng > 1 and last_square.type != "start":
            World.current_Square.type = last_square.type
            World.current_Square.music = last_square.music
        else:
            World.current_Square.type = World.current_Square.rand_type()
    World.current_Square.description = World.current_Square.get_description()
    Screen.delete("0.1", END)
    Screen.insert(INSERT, f"{World.current_Square.description}")
    if World.current_Square.Floor is not None:
        Screen.insert(INSERT, f"\n{World.current_Square.Floor.Name} is sitting on the floor...\n")
    if World.current_Square.NPCs is None and World.current_Square.state != "clear":
        World.current_Square.NPCs = Enemy(World.current_Square.tier - 1)
        if World.current_Square.NPCs.name in Enemies[World.current_Square.tier - 1]:
            Screen.insert(INSERT, appear(World.current_Square.NPCs.name))
            Player.combat = True
            if Everything.doneCombat is False:
                intro_combat()
                Everything.doneCombat = True
        elif World.current_Square.NPCs.name in NPC:
            World.current_Square.state = "clear"
            if World.current_Square.NPCs.name is None:
                pass
            else:
                if appear_npc(World.current_Square.NPCs.name) not in ["gamble", "trade"]:
                    Screen.insert(INSERT, appear_npc(World.current_Square.NPCs.name))
                elif appear_npc(World.current_Square.NPCs.name) == "gamble":
                    gamble()
                elif appear_npc(World.current_Square.NPCs.name) == "trade":
                    x = trade()
                    Everything.Trade = x
        else:
            World.current_Square.state = "clear"
    elif World.current_Square.NPCs is not None and World.current_Square.state != "clear":
        Screen.insert(INSERT, appear(World.current_Square.NPCs.name))
        Player.combat = True
    elif World.current_Square.NPCs is not None and World.current_Square.state == "clear":
        if World.current_Square.NPCs.name is None:
            pass
        else:
            if appear_npc(World.current_Square.NPCs.name) not in ["gamble", "trade"]:
                Screen.insert(INSERT, appear_npc(World.current_Square.NPCs.name))
            elif appear_npc(World.current_Square.NPCs.name) == "gamble":
                Screen.insert(INSERT, "You see a gambler but he seems busy...\n")
            elif appear_npc(World.current_Square.NPCs.name) == "trade":
                Screen.insert(INSERT, "You see a trader but he seems busy...\n")
    if last_square.music != World.current_Square.music:
        mixer_music.fadeout(500)
        mixer_music.load(f"Music/{World.current_Square.music}.mp3")
        mixer_music.play(-1)
    Everything.map_uptodate = False
    save()


def enemy_turn():
    e_rng = randint(0, 9)
    damage = World.current_Square.NPCs.dmg
    if e_rng < Player.evasion:
        Screen.insert(INSERT, f"The clumsy attack from {World.current_Square.NPCs.name}\n"
                              f"misses by a hairs breath...\n")
    elif e_rng == 9:
        if damage * 2 - Player.defense <= 0:
            damage = 0
        else:
            damage = damage * 2 - Player.defense
        Screen.insert(INSERT, f"A critical hit! You take {damage} damage.\n")
        Player.current_hp -= damage
    else:
        if damage - Player.defense <= 0:
            damage = 0
        else:
            damage = damage - Player.defense
        Player.current_hp -= damage
        Screen.insert(INSERT, f"You take {damage} damage...\n")
    if Player.current_hp <= 0:
        Screen.insert(INSERT, "You succumb to your injuries...")
        Everything.alive = False
        save()


def combat():
    rng = randint(0, 9)
    if rng == 0:
        Screen.insert(INSERT, "You missed! That sucks..\n")
        enemy_turn()
    elif rng == 9:
        Screen.insert(INSERT, "A devastating hit!\n")
        World.current_Square.NPCs.hp -= Player.dmg * 2
        if World.current_Square.NPCs.hp <= 0:
            Screen.insert(INSERT, f"\nYou defeated {World.current_Square.NPCs.name}.\n")
            Player.combat = False
            World.current_Square.state = "clear"
            Log.insert(INSERT, f"you have slain\n{World.current_Square.NPCs.name}\n\n")
            logs_.append(f"you have slain\n{World.current_Square.NPCs.name}\n\n")
            reward()
            World.current_Square.NPCs = None
        else:
            Screen.insert(INSERT, f"It sure is hard to kill {World.current_Square.NPCs.name}\n"
                                  f"It has {World.current_Square.NPCs.hp} HP left.\n")
            enemy_turn()
    else:
        World.current_Square.NPCs.hp -= Player.dmg
        if World.current_Square.NPCs.hp <= 0:
            Screen.insert(INSERT, f"You hit doing {Player.dmg} damage\n"
                                  f"You defeated {World.current_Square.NPCs.name}.\n")
            Player.combat = False
            World.current_Square.state = "clear"
            Log.insert(INSERT, f"you have slain\n{World.current_Square.NPCs.name}\n\n")
            logs_.append(f"you have slain\n{World.current_Square.NPCs.name}\n\n")
            reward()
            World.current_Square.NPCs = None
        else:
            Screen.insert(INSERT, f"You hit doing {Player.dmg} damage\n"
                                  f"The foe still has {World.current_Square.NPCs.hp} HP left\n")
            enemy_turn()
    Everything.character_uptodate = False


def reward():
    if Player.race == "Newtfolk":
        if Player.current_hp < Player.max_hp:
            Player.current_hp += 1
            Screen.insert(INSERT, "\nYou regrow a toe or two\n")
    Player.exp += World.current_Square.NPCs.tier + 1
    if Player.exp >= Player.exp2lvl:
        Player.exp -= Player.exp2lvl
        Player.level += 1
        Player.current_hp += 1
        Player.max_hp += 1
        Player.exp2lvl = Player.level * 2 + 2
        Screen.insert(INSERT, f"You reached the next level! Level {Player.level}\n")
    rng = randint(0, 9)
    if rng < 6:
        pass
    else:
        if Everything.foundItem is False:
            intro_items()
            Everything.foundItem = True
        item = get_item(World.current_Square.tier)
        Screen.insert(INSERT, f"\nYou see something drop from the corpse..\n"
                              f"Where did {World.current_Square.NPCs.name} get {item.Name}???\n")
        World.current_Square.Floor = item
    Everything.character_uptodate = False
    save()


def gamble():
    stuff = []
    for item in Player.inventory + Player.equipped:
        stuff.append(item)
    if stuff:
        Everything.gambling = True
        Screen.insert(INSERT, f"\nShoddy figure:\n"
                              f"Hey there, hero! Can I interest you in...\n"
                              f"a little game?\n\n")
    else:
        Screen.insert(INSERT, "\nShoddy figure:\n"
                              "Talk to me when you have some items...\n")


def trade():
    Player_items = []
    for item in Player.inventory + Player.equipped:
        Player_items.append(item)
    if Player_items:
        offer = get_item(World.current_Square.tier)
        price = choice(Player_items)
        Screen.insert(INSERT, f"\nTotally not shady trader:\n"
                              f"\"Hey handsome, can I interest you in...\n"
                              f"a little deal?...\n"
                              f"I am willing to give you {offer.Name} but you have to give\n"
                              f"me {price.Name}.. and also...\n{Player.current_hp // 4} health points.\n"
                              f"What do you say?\"\n")
        Everything.trading = True
        return offer, price
    else:
        Screen.insert(INSERT, "\nVery honest and well-meaning trader:\n"
                              "\"You have nothing I want, kid...\"\n")


def intro_combat():
    help_pop = Toplevel()
    if OS == "Windows":
        help_pop.geometry("350x300")
    else:
        help_pop.geometry("350x258")
    help_pop.title("Combat")
    Text_ = Label(help_pop, anchor=W, justify="left",
                  text="It seems like this is your first time fighting\n"
                       "in Wasteland Fantasy so let me give you a quick\n"
                       "Introduction:\n"
                       "Most of it is luck-based, you have 3 options\n"
                       "You either attack the enemy doing your damage\n"
                       "and seeing if he dies, if not, he will attack...\n\n"
                       "You can use an item from your inventory...\n\n"
                       "Or you flee, this has a 60% chance of working\n"
                       "and will place you on a random square around\n"
                       "the enemy, if it fails it's the enemies turn.\n"
                       "All clear?\n\nWaidmanns Heil, adventurer!")
    Text_.grid(row=0, column=0)
    if OS == "Windows":
        Text_.config(font=("Times", 12))
    Text_.grab_set()
    help_pop.transient()


def intro_items():
    help_pop = Toplevel()
    if OS == "Windows":
        help_pop.geometry("350x350")
    else:
        help_pop.geometry("350x308")
    help_pop.title("Items")
    Text_ = Label(help_pop, anchor=W, justify="left",
                  text="Hey there, champ!\n"
                       "Looks like you just found your first item.\n"
                       "I may know a thing or two about those..\n"
                       "Want me to tell you?\n"
                       "\nNo? Well, it's not your decision anyways:\n"
                       "There are three kinds of items, quests, gear and\n"
                       "potions. You can read quests to get marks on your\n"
                       "map. If you are in a marked square you can look for\n"
                       "stuff and see what you find :)\n"
                       "You can equip gear to get some boni to your stats\n"
                       "damage, defense and evasion but only two at a time\n"
                       "\nThen there are potions, they are tricky:\n"
                       "They can either be good or bad but you can only\n"
                       "know if you drink them.\n\nProst, adventurer!")
    Text_.grid(row=0, column=0)
    if OS == "Windows":
        Text_.config(font=("Times", 12))
    Text_.grab_set()
    help_pop.transient()


def inventory():
    inv_pop = Toplevel()
    inv_pop.geometry("400x300")
    inv_pop.title("Your Backpack")
    scroll = Scrollbar(inv_pop)
    scroll.pack(side=RIGHT, fill=Y)
    if not Player.inventory:
        Text_ = Text(inv_pop, bg="#837373", fg="#d9d9d9", yscrollcommand=scroll.set, relief="flat")
        Text_.insert(INSERT, "Nothing in here yet...")
    else:
        Text_ = Text(inv_pop, bg="#837373", fg="#d9d9d9", yscrollcommand=scroll.set, relief="flat")
        Text_.insert(INSERT, Player.get_inventory())
    Text_.pack(expand=True)
    if OS == "Windows":
        Text_.config(font=("Times", 12))
    scroll.config(command=Text_.yview)
    Text_.config(state=DISABLED)

    def update():
        if Everything.inventory_uptodate is False:
            Text_.config(state=NORMAL)
            Text_.delete("1.0", END)
            if Player.get_inventory():
                Text_.insert(INSERT, Player.get_inventory())
            else:
                Text_.insert(INSERT, "Nothing in here yet...")
            Text_.config(state=DISABLED)
            Everything.inventory_uptodate = True
            Text_.see("end")
        inv_pop.after(500, update)

    inv_pop.after(1000, update)


def map_():
    Map_pop = Toplevel()
    Map_pop.geometry("400x400")
    Map_pop.title("Your Map")
    Map_pop.config(bg="#CABB92")
    m = World.make_map()
    yscroll = Scrollbar(Map_pop)
    xscroll = Scrollbar(Map_pop, orient="horizontal")
    yscroll.pack(side=RIGHT, fill=Y)
    xscroll.pack(side=BOTTOM, fill=X)
    Text_ = Text(Map_pop, bg="#CABB92", fg="black", relief="flat", highlightbackground="#CABB92",
                 font=("DejaVu Sans Mono", 14), yscrollcommand=yscroll.set, xscrollcommand=xscroll.set, wrap=NONE)
    Text_.tag_configure("center", justify='center')
    Text_.insert("1.0", m)
    Text_.pack(expand=False)
    yscroll.config(command=Text_.yview)
    xscroll.config(command=Text_.xview)
    Text_.config(state=DISABLED)

    def update():
        if Everything.map_uptodate is False:
            scrollposx = Text_.xview()
            scrollposy = Text_.yview()
            scrollposx = str(scrollposx)[1:-1].split(", ")
            scrollposy = str(scrollposy)[1:-1].split(", ")
            Text_.config(state=NORMAL)
            x = World.make_map()
            Text_.delete("1.0", END)
            Text_.insert("1.0", x)
            # the code below is for keeping the map
            # focus to where you scrolled it
            Text_.yview_moveto(float(scrollposy[0]))
            Text_.xview_moveto(float(scrollposx[0]))
            Text_.config(state=DISABLED)
            Everything.map_uptodate = True
        Map_pop.after(500, update)
    Map_pop.after(100, update)


def character():
    char_pop = Toplevel()
    char_pop.geometry("400x200")
    char_pop.title("You")
    if Player.ready is False:
        Text_ = Label(char_pop, anchor=W, justify="left", text="All so blurry...\n"
                                                               "Who.. am I?...\n"
                                                               "I need some water...")
    else:
        Text_ = Label(char_pop, anchor=W, justify="left", text=Player.pond())
    Text_.grid(row=0, column=0)
    if OS == "Windows":
        Text_.config(font=("Times", 12))

    def update():
        if Player.ready is False:
            Text_.config(text="All so blurry...\nWho.. am I?...\nI need some water...")
        elif Everything.character_uptodate is False:
            Text_.config(text=Player.pond())
            Everything.character_uptodate = True
        char_pop.after(500, update)

    char_pop.after(1000, update)


def save():
    # After long consideration, a save button
    # is way easier to do than just saving everything
    # real time and the exit button was redundant anyways

    # After even longer consideration, a save button is stupid,
    # the game saves every time you move now

    chmod("Database.db", S_IWUSR | S_IREAD)

    if Player.ready is False:
        Screen.config(state=NORMAL)
        Screen.insert(INSERT, "\nDon't you wanna create a character first?\n")
        Screen.config(state=DISABLED)
        Screen.see("end")
        return None

    clear_db()

    chmod("Database.db", S_IREAD | S_IWUSR)

    # Database stuff
    E_ = deepcopy(Everything)
    P_ = deepcopy(Player)
    W_ = deepcopy(World)
    I_ = deepcopy(Player.inventory + Player.equipped)
    S_ = deepcopy(World.Squares)
    Floor_Item = deepcopy(World.current_Square.Floor)

    # Player
    r = []
    for item in I_:
        if item != "empty":
            r.append(item)
    z = deepcopy(r)
    P_.makestring()
    session.add(P_)

    # World
    if W_.current_Square.Floor is not None:
        W_.current_Square.Floor = W_.current_Square.Floor.ID
    if W_.current_Square.NPCs is not None:
        W_.current_Square.NPCs = W_.current_Square.NPCs.ID
    W_.current_Square.ID2 = str(uuid1(2))
    session.add(W_.current_Square)
    y = W_.Squares
    W_.makestring()
    session.add(W_)

    # Squares
    floor_items = []
    for square in S_:
        if square.NPCs is not None and not isinstance(square.NPCs, str):
            square.NPCs = square.NPCs.ID
        else:
            square.NPCs = "empty"
        if square.Floor is not None:
            floor_items.append(deepcopy(square.Floor))
            square.Floor = square.Floor.ID
        else:
            square.Floor = "empty"
        session.add(square)

    # Enemies
    for square in y:
        if square.NPCs is not None and not isinstance(square.NPCs, str):
            square.NPCs.extraUniqueID = str(uuid1(3))
            session.add(square.NPCs)

    # Items
    if z or Floor_Item is not None:
        all_items = []
        for item in floor_items:
            all_items.append(item)
        for item in z:
            all_items.append(item)
        for item in all_items:
            if not isinstance(item, str):
                item.boni = str(item.boni)[1:-1]
                session.add(item)

    # logs
    for item in logs_:
        session.execute(logs.insert().values(ID=str(uuid1()), entries=item))

    # Everything
    session.add(E_)
    session.commit()
    Screen.see("end")

    chmod("Database.db", S_IREAD)


Input = Entry(root, text="Write a command...")
Input.grid(row=4, column=1, columnspan=4, sticky=E + W + N, pady=10, padx=100)
Inventory = Button(root, text="Inventory", bg="#837373", fg="white", command=inventory, font=("Times", 12),
                   relief="solid", highlightbackground="darkgreen", highlightthickness="2")
Inventory.grid(row=3, column=1, sticky=S + W + N, padx=100)
Map = Button(root, text="Map", command=map_, font=("Times", 12), relief="solid", fg="white", bg="#837373",
             highlightbackground="darkgreen", highlightthickness="2")
Map.grid(row=3, column=2, sticky=S + W + N, padx=60)
Character_b = Button(root, text="Character", command=character, font=("Times", 12), relief="solid", fg="white",
                     bg="#837373", highlightbackground="darkgreen", highlightthickness="2")
Character_b.grid(row=3, column=3, sticky=S + W, padx=100)
Screen = Text(root, bg="#d9d9d9", relief="flat", font=("Times", 12, "italic"), height=15, width=40)
if OS == "Windows":
    Screen = Text(root, bg="#d9d9d9", relief="flat", font=("Times", 12, "italic"), wrap=WORD, height=15, width=50)
    Log = Text(root, bg="#d9d9d9", height=15, width=20, relief="groove", font=("Times", 12), wrap=WORD)
else:
    Screen = Text(root, bg="#d9d9d9", relief="flat", font=("Times", 12, "italic"), wrap=WORD, height=15, width=50)
    Log = Text(root, bg="#d9d9d9", height=15, width=25, relief="ridge", font=("Times", 12), wrap=WORD)
Screen.grid(row=0, column=2, rowspan=3, columnspan=3, sticky=W + S, pady=40)
Log.grid(row=0, column=1, rowspan=3, padx=60, pady=40, sticky=S)
Close = Button(root, text="Close", command=root.destroy, bg="#430C0C", fg="white", font=("Times", 12), relief="solid",
               highlightbackground="black", highlightthickness="3")
Close.grid(row=5, column=5, sticky=S)
Help = Button(root, text="Help", bg="#430C0C", fg="white", command=help_, font=("Times", 12), relief="solid",
              highlightbackground="black", highlightthickness="3")
Help.grid(row=5, column=0, sticky=S)


if not DB_player:
    Current_Square = Square("0,0")
    Current_Square.music = "start"
    World = World_(Current_Square)
else:
    load()

start()
Input.bind("<Return>", enter)
Screen.config(state=DISABLED)
Log.config(state=DISABLED)
Meta.create_all(engine)
DB.metadata.create_all(engine)
chmod("Database.db", S_IREAD)
session.close()
mainloop()
