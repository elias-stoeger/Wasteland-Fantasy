from re import search
from Items import synonyms


def commands(command):
    x = r"[w|W]est$|[n|N]orth$|[s|S]outh$|[e|E]ast$"
    pond = r"[p|P]ond$|[w|W]ater$"
    info_newtfolk = r"[i|I]nfo\s[n|N]ewtfolk"
    info_bathy = r"[i|I]nfo\s[b|B]athynomic"
    info_whisp = r"[i|I]nfo\s[w|W]hispling"
    info_void = r"[i|I]nfo\s[v|V]oidspawn"
    info_ursine = r"[i|I]nfo\s[u|U]rsine"
    newtfolk = r"[n|N]ewtfolk"
    bathy = r"[b|B]athynomic"
    whisp = r"[w|W]hispling"
    void = r"[v|V]oidspawn"
    ursine = r"[u|U]rsine"
    attack = r"^[a|A]ttack|^[h|H]it|^[s|S]trike|^[s|S]ma[sh|ck]"
    flee = r"^[r|R]un\s?|^[f|F]lee\s?"
    take = r"^[t|T]ake|^[p|P]ick\sup|^[g|G]et"
    equip = r"^[e|E]quip\s|^[p|P]ut\son"
    drink = r"^[d|D]rink\s"
    use = r"^[u|U]se\s"
    unequip = r"^[u|U]nequip\s|^[t|T]ake\soff|^[l|L]oose"
    roll = r"^[r|R]oll"
    score = r"^[s|S]core$"
    suicide = r"^[s|S]uicide$|^[k|K]ill\s[s|S]elf$"
    read_w = r"^[r|R]ead$"
    read = r"^[r|R]ead\s"
    look = r"^[s|S]earch|^[l|L]ook\sfor|^[c|C]heck\sfor|^[i|I]nspect|^[c|C]heck|^[l|L]ook"
    check = search(x, command)
    check_pond = search(pond, command)
    check_newt = search(info_newtfolk, command)
    check_bathy = search(info_bathy, command)
    check_whisp = search(info_whisp, command)
    check_void = search(info_void, command)
    check_ursine = search(info_ursine, command)
    check_newt_ = search(newtfolk, command)
    check_bathy_ = search(bathy, command)
    check_whisp_ = search(whisp, command)
    check_void_ = search(void, command)
    check_ursine_ = search(ursine, command)
    check_attack = search(attack, command)
    check_flee = search(flee, command)
    check_take = search(take, command)
    check_equip = search(equip, command)
    check_drink = search(drink, command)
    check_unequip = search(unequip, command)
    check_roll = search(roll, command)
    check_use = search(use, command)
    check_score = search(score, command)
    check_suicide = search(suicide, command)
    check_read = search(read, command)
    check_read_w = search(read_w, command)
    check_look = search(look, command)
    if check:
        return move(check.group(0))
    elif check_pond:
        return "pond"
    elif check_newt:
        return "newt"
    elif check_bathy:
        return "bathy"
    elif check_whisp:
        return "whisp"
    elif check_void:
        return "void"
    elif check_ursine:
        return "ursine"
    elif check_newt_:
        return "Newtfolk"
    elif check_bathy_:
        return "Bathynomic"
    elif check_whisp_:
        return "Whispling"
    elif check_void_:
        return "Voidspawn"
    elif check_ursine_:
        return "Ursine"
    elif check_attack:
        return "attack"
    elif check_flee:
        return "flee"
    elif check_take:
        return "take"
    elif check_equip:
        x = item_synonyms(command[6:])
        if x:
            return "equip", x
        else:
            return "equip", command[6:]
    elif check_drink:
        x = item_synonyms(command[6:])
        if x:
            return "drink", x
        else:
            return "drink", command[6:]
    elif check_use:
        x = item_synonyms(command[4:])
        if x:
            return "use", x
        else:
            return "use", command[4:]
    elif check_unequip:
        x = item_synonyms(command[8:])
        if x:
            return "unequip", x
        else:
            return "unequip", command[8:]
    elif check_roll:
        return "roll"
    elif check_score:
        return "score"
    elif check_suicide:
        return "suicide"
    elif check_read_w:
        return "read_w"
    elif check_read:
        x = item_synonyms(command[5:])
        if x:
            return "read", x
        else:
            return "read", command[5:]
    elif check_look:
        return "look"
    else:
        return "nothing"


def infos(race):
    if race == "newt":
        return "Newtfolk\n" \
               "A race of small, goblin like people inhabiting\n" \
               "the swamps around one of the biggest bombsights.\n" \
               "Often dismissed for their size and look\n" \
               "these creatures regenerative abilities make\n" \
               "them excellent survivalists\n\n" \
               "Bathynomic\nWhispling\nVoidspawn\nUrsine"
    if race == "bathy":
        return "Newtfolk\n\n" \
               "Bathynomic\n" \
               "Originally inhabiting the oceans, the radiation\n" \
               "turned those crab-like creatures terrestrial.\n" \
               "Their thick plates shrug off any attack coming their way\n\n" \
               "Whispling\n" \
               "Voidspawn\n" \
               "Ursine"
    if race == "whisp":
        return "Newtfolk\n" \
               "Bathynomic\n\n" \
               "Whispling\n" \
               "Not much is know about this silent folk\n" \
               "Some say they came from soldiers caught in the center\nof the blast " \
               "but we only know that they glow so bright it is\nhard to look at them\n\n" \
               "Voidspawn\n" \
               "Ursine"
    if race == "void":
        return "Newtfolk\n" \
               "Bathynomic\n" \
               "Whispling\n\n" \
               "Voidspawn\n" \
               "Beings of darkness spawned from an empty realm\n" \
               "the Voidspawn are mindless murder machines killing\n" \
               "all and every life they come across.\n" \
               "or so they say...\n\n" \
               "Ursine"
    if race == "ursine":
        return "Newtfolk\n" \
               "Bathynomic\n" \
               "Whispling\n" \
               "Voidspawn\n\n" \
               "Ursine\n" \
               "This hulking race of mutated wolverine have little\n" \
               "regard for mutant life. Due to their size, thick fur\n" \
               "and loose skin there are few beings with enough power\n" \
               "to seriously wound these goliaths"


def move(passed):
    passed = str(passed)
    if passed == "West" or passed == "west":
        return "w"
    elif passed == "North" or passed == "north":
        return "n"
    elif passed == "East" or passed == "east":
        return "e"
    else:
        return "s"


def interact():
    return "hi"


def item_synonyms(b):
    for item in synonyms:
        if b in synonyms[item]:
            return item
