from Player import *
from Items import *
from Commands import *
from Enemies import *
from World import *
from tkinter import *
import platform
from pygame import mixer, mixer_music


# All music is royalty free and from https://www.bensound.com/royalty-free-music
# or the youtube channel https://www.youtube.com/channel/UCNg336DNlXPJ4mNML9J292w

root = Tk()
root.geometry("893x664+100+100")
root.title("Wasteland Fantasy")
root.grid_propagate(False)

# since I usually work on Linux but it looks not quite the same
# i change it a little depending on the OS
OS = platform.system()

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
    windll.shcore.SetProcessDpiAwareness(1)
    # Thanks for nothing, Bill


# That's for getting rid of that nasty border of the window
# root.overrideredirect(True)

class Everything:
    def __init__(self):
        self.pnd = "False"


Everything = Everything()

Player = Player()
DB = None
mixer.init()


if DB is None:
    Current_Square = Square("0,0")
    Current_Square.music = "start"
    World = World(Current_Square)
else:
    print("Well that's awkward")


def help_():
    help_pop = Toplevel()
    help_pop.geometry("400x300")
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
                       "You move by giving your direction in cardinal directions:\n"
                       "\"go north\", \"go south\" and stuff like that.\n"
                       "I am sure you will figure the rest out yourself...\n\n"
                       "I hope you enjoy :)")
    Text_.grid(row=0, column=0)
    Text_.grab_set()
    help_pop.transient()


def start():
    if DB is None:
        mixer_music.load("Music/start.mp3")
        mixer_music.play(-1)
        mixer.music.set_volume(0.4)
        Screen.insert(INSERT, "You wake up in a forest glade,\nthe morning sun blinding you,\n"
                              "the sounds of birds and critters around you.\n"
                              "They are so loud your head hurts\n\"Am i hungover?\", you think..."
                              "\n\nSome water would do wonders.\n"
                              "You look around and spot a pond at the edge\nof the glade...")

        Log.insert(INSERT, "Log:\n"
                           "You woke up\n")


def enter(event=None):
    x = Input.get()
    Input.delete(0, "end")
    com = commands(x)
    Screen.config(state=NORMAL)
    last_square = World.current_Square
    if com == "pond" or Everything.pnd is True:
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
            Log.config(state=NORMAL)
            Log.insert(INSERT, "\nYou remembered who \nyou are\n\n")
            Everything.pnd = False
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
    elif com in ["w", "n", "e", "s"] and Player.ready is True and Player.busy is False:
        x = World.current_Square.coords.split(",")[0]
        y = World.current_Square.coords.split(",")[1]
        if com == "w":
            newSquare = f"{int(x) -1},{int(y)}"
        elif com == "n":
            newSquare = f"{int(x)},{int(y) + 1}"
        elif com == "e":
            newSquare = f"{int(x) + 1},{int(y)}"
        else:
            newSquare = f"{int(x)},{int(y) - 1}"
        coords = []
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
    Screen.config(state=DISABLED)
    Log.config(state=DISABLED)


def prep_square(last_square):
    World.current_Square.tier = Player.level // 5 + 1
    rng = random.randint(0, 9)
    if World.current_Square.tier == 1 and World.current_Square.type is None:
        if rng > 1 and last_square.type != "start":
            World.current_Square.type = last_square.type
            World.current_Square.music = last_square.music
        else:
            World.current_Square.type = World.current_Square.rand_type()
    World.current_Square.description = World.current_Square.get_description()
    Screen.delete("0.1", END)
    Screen.insert(INSERT, f"{World.current_Square.description}")
    if World.current_Square.NPCs is None and World.current_Square.state != "clear":
        World.current_Square.NPCs = Enemy(World.current_Square.tier - 1)
        print(World.current_Square.NPCs.name)
        if World.current_Square.NPCs.name in Enemies[World.current_Square.tier - 1]:
            Screen.insert(INSERT, appear(World.current_Square.NPCs.name))
        elif World.current_Square.NPCs.name in NPC:
            print(appear_npc(World.current_Square.NPCs.name))
            Screen.insert(INSERT, appear_npc(World.current_Square.NPCs.name))
    if last_square.music is not World.current_Square.music:
        mixer_music.fadeout(500)
        mixer_music.load(f"Music/{World.current_Square.music}.mp3")
        mixer_music.play(-1)


def inventory():
    inv_pop = Toplevel()
    inv_pop.geometry("400x300")
    inv_pop.title("Your Backpack")
    if DB is None:
        Text_ = Label(inv_pop, anchor=W, justify="left", text="Nothing in here yet...")
    else:
        Text_ = Label(inv_pop, anchor=W, justify="left", text="Implement once you have a DB")
    Text_.grid(row=0, column=0)


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
    if OS == "Windows":
        Text_ = Text(Map_pop, bg="#CABB92", fg="black", relief="flat", highlightbackground="#CABB92",
                     font=("DejaVu Sans Mono", 14), yscrollcommand=yscroll.set, xscrollcommand=xscroll.set, wrap=NONE)
    else:
        Text_ = Text(Map_pop, bg="#CABB92", fg="black", relief="flat", highlightbackground="#CABB92",
                     font=("Times", 14), yscrollcommand=yscroll.set, xscrollcommand=xscroll.set, wrap=NONE)
    Text_.tag_configure("center", justify='center')
    Text_.insert("1.0", m)
    Text_.tag_add("center", "1.0", "end")
    Text_.pack(expand=True)
    yscroll.config(command=Text_.yview)
    xscroll.config(command=Text_.xview)
    Text_.config(state=DISABLED)
    # To force you to close the map if you want to play
    # again because i don't want to rewrite it to use
    # threading:
    Map_pop.focus_force()
    Map_pop.focus_set()
    Map_pop.grab_set()
    Map_pop.attributes("-topmost", True)


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


Input = Entry(root, text="Write a command...")
Input.grid(row=4, column=1, columnspan=4, sticky=EW+N, pady=10, padx=100)
Inventory = Button(root, text="Inventory", bg="#837373", fg="white", command=inventory, font=("Times", 12),
                   relief="solid", highlightbackground="darkgreen", highlightthickness="2")
Inventory.grid(row=3, column=1, sticky=SW+N, padx=100)
Map = Button(root, text="Map", command=map_, font=("Times", 12), relief="solid", fg="white", bg="#837373",
             highlightbackground="darkgreen", highlightthickness="2")
Map.grid(row=3, column=2, sticky=SW + N, padx=60)
Character_b = Button(root, text="Character", command=character, font=("Times", 12), relief="solid", fg="white",
                     bg="#837373", highlightbackground="darkgreen", highlightthickness="2")
Character_b.grid(row=3, column=3, sticky=SW, padx=100)
Screen = Text(root, bg="#d9d9d9", relief="flat", font=("Times", 12, "italic"), height=15, width=40)
if OS == "Windows":
    Screen = Text(root, bg="#d9d9d9", relief="flat", font=("Times", 12, "italic"), height=15, width=50)
    Log = Text(root, bg="#d9d9d9", height=15, width=20, relief="ridge", font=("Times", 12))
else:
    Screen = Text(root, bg="#d9d9d9", relief="flat", font=("Times", 12, "italic"), height=15, width=50)
    Log = Text(root, bg="#d9d9d9", height=15, width=25, relief="ridge", font=("Times", 12))
Screen.grid(row=0, column=2, rowspan=3, columnspan=3, sticky=W+S, pady=40)
Log.grid(row=0, column=1, rowspan=3, padx=60, pady=40, sticky=S)
Exit = Button(root, text="Close", command=root.destroy, bg="#430C0C", fg="white", font=("Times", 12), relief="solid",
              highlightbackground="black", highlightthickness="3")
Exit.grid(row=5, column=5, sticky=S)
Help = Button(root, text="Help", bg="#430C0C", fg="white", command=help_, font=("Times", 12), relief="solid",
              highlightbackground="black", highlightthickness="3")
Help.grid(row=5, column=0, sticky=S)

start()
Input.bind("<Return>", enter)
Screen.config(state=DISABLED)
Log.config(state=DISABLED)


mainloop()
