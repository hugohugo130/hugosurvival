from cryptography.fernet import Fernet
from os.path import exists
from os import makedirs as md
from tkinter import *
from random import choice as ranchoice, randint
from module.check_file_update import cfu

result = cfu()
if result == 1:
    print("已經有更新了!請打開game_file_updater_get.py更新!")
    input("點擊Enter退出")
    quit()

key = b"hhhuuugggooo111333000hugohugohugoeeeeeeeeee="
cs = Fernet(key)
filename = "game"

game = Tk(className="survival game")
game.geometry("400x300")

def readfile(cs: object, filename: str):
    if not exists(f"data\\{filename}.txt"):
        a = open(f"data\\{filename}.txt", "w")
        if filename == "hp":
            content = "100"
        elif filename == "playerinfo":
            content = "Player|.20"
        else:
            content = "0"
        a.write(cs.encrypt(content.encode()).decode())
        a.close()
    with open(f"data\\{filename}.txt", "r") as ffile:
        result = ffile.read()
    result = cs.decrypt(result.encode()).decode()
    return result


def savefile(content, cs, filename):
    content = str(content)
    with open(f"data\\{filename}.txt", "w") as afktimefile:
        encrypt_content = cs.encrypt(content.encode()).decode()
        afktimefile.write(encrypt_content)
    refresh()


def saveall():
    savefile(hp, cs, "hp")
    savefile(tick, cs, "tick")
    plrinfo = player.name + "|" + "-".join(player.backpack) + "." + str(player.hunger)
    savefile(plrinfo, cs, "playerinfo")
    savefile(coins, cs, "coins")
    savefile(add_hp_0_5, cs, "addhpcache")


def saveexit():
    saveall()
    quit("Exit")


if not exists("data"):
    md("data")


def refresh():
    global hplbl, ticklbl, player, hungerlbl, foodslbl, healthslbl, swordslbl, coinslbl
    hplbl.config(text=f"HP: {hp}")
    # mins = int((tick - (tick%20)) / 20)
    mins = int(tick * 0.06)
    hours = 0
    days = 1
    while mins >= 60:
        hours += 1
        mins -= 60
    while hours >= 24:
        days += 1
        hours -= 24
    hours = str(hours)
    mins = str(mins)
    if len(hours) == 1:
        hours = "0" + hours
    if len(mins) == 1:
        mins = "0" + mins
    foods = player.backpack.count("food")
    healths = player.backpack.count("health")
    swords = player.backpack.count("sword")
    ticklbl.config(text=f"Day {days} {hours}:{mins} ({tick} tick)")
    hungerlbl.config(text=f"Hunger: {hunger} / 20")
    foodslbl.config(text=f"Foods: {foods}")
    healthslbl.config(text=f"Healths: {healths}")
    swordslbl.config(text=f"Swords: {swords}")
    coinslbl.config(text=f"Coins: {coins}")
    player.health = hp
    player.hunger = hunger

try:
    hp = int(readfile(cs, "hp"))
    tick = int(readfile(cs, "tick"))
    coins = int(readfile(cs, "coins"))
    add_hp_0_5 = int(readfile(cs,"addhpcache"))
except Exception as err:
    if "ValueError" in err:
        quit("data數據出錯,解決辦法: 刪掉txt\n {err}")
    else:
        quit(err)
hplbl = Label(game, text="HP: Loading")
ticklbl = Label(game, text="Day -- --:-- (-- tick)")
hungerlbl = Label(game, text="Hunger: -- / 20")
foodslbl = Label(game, text="Foods: --")
healthslbl = Label(game, text="Healths: --")
swordslbl = Label(game, text="Swords: --")
coinslbl = Label(game, text="Coins: --")
hplbl.place(relx=0.5, rely=0.1, anchor="n")
ticklbl.place(relx=0.5, rely=0.175, anchor="n")
hungerlbl.place(relx=0.5, rely=0.250, anchor="n")
foodslbl.place(relx=0.5, rely=0.325, anchor="n")
healthslbl.place(relx=0.5, rely=0.4, anchor="n")
swordslbl.place(relx=0.5, rely=0.475, anchor="n")
coinslbl.place(relx=0.5, rely=0.55, anchor="n")


class monster:
    def __init__(self, name):
        self.health = 10
        self.attackage = 1
        self.name = name
        print(f"monster({self.name}) spawned!")

    def attack(self, player):
        global hp,add_hp_0_5
        if self.health <= 0 and self in zombies:
            zombies.remove(self)
            print(f"monster({self.name}) died!")
        else:
            # print(f"{self.name} want to attack {player.name}! -- monster attack function")
            mins = int(tick * 0.06)
            hours = 0
            days = 0
            while mins >= 60:
                hours += 1
                mins -= 60
            while hours >= 24:
                days += 1
                hours -= 24
            # print(f"the hour is {hours}")
            if (20 <= hours <= 24) or (0 <= hours <= 4):
                print(f"{self.name} is attacking {player.name}!")
                hp -= self.attackage
                print(f"{player.name}'s health - {self.attackage}")
                plrsword = player.backpack.count("sword")
                if plrsword > 0:
                    monster_health_reduce = 5 * plrsword
                    print(
                        f"{player.name} used {plrsword} sword to attack monster({self.name}). monster health - {monster_health_reduce}"
                    )
                    add_hp_0_5 += 1
                    print("Add player 0.5 hp cache + 1")
                    if self.health - monster_health_reduce <= 0:
                        self.health = 0
                        if self in zombies:
                            zombies.remove(self)
                            print(f"monster({self.name}) died!")
                        del self
                    else:
                        self.health -= monster_health_reduce


zombies = []


class Player:
    def __init__(self, hp, hunger, foods=5, backpack=None, name="Player"):
        if backpack is None:
            self.backpack = []
        else:
            self.backpack = backpack
        self.health = hp
        self.name = name
        if hunger is None:
            self.hunger = 20
        else:
            self.hunger = hunger
        self.foods = foods


player = Player(hp, None)
playerinfo = readfile(cs, "playerinfo")
player.name = playerinfo.split("|")[0]
if len(playerinfo) > 1:
    player.backpack = playerinfo.split("|")[1].split(".")[0].split("-")
hunger = int(playerinfo.split(".")[1])
print(f"player({player.name}) spawned!")
print(f"{player.name}'s backpack : {player.backpack}")
print(f"{player.name}'s health: {player.health}")
print(f"{player.name}'s hunger: {player.hunger}")

add_hp_0_5 = 0

def refresh_():
    global tick, hp, zombies, player, hunger,add_hp_0_5
    tick += 1
    if add_hp_0_5 >= 2:
        add_hp_0_5 -= 2
        hp += 1
        print(f"{player.name}'s health + 1")
    refresh()
    mins = int(tick * 0.06)
    hours = 0
    days = 0
    while mins >= 60:
        hours += 1
        mins -= 60
    while hours >= 24:
        days += 1
        hours -= 24
    if tick % 100 == 0:
        saveall()
    if tick % 500 == 0:
        try:
            randomonezombie = ranchoice(zombies)
        except IndexError:
            pass
        else:
            # print(f"{randomonezombie.name} want to attack {player.name}!")
            randomonezombie.attack(player)
    if player.health == 0:
        print("Ah! You're Died!")
        hp = 100
        print("You've revived!")
    if len(zombies) == 0 and not (4 <= hours < 20):
        for i in range(3):
            exec(f"zombie{i} = monster('zombie{i}')")
            exec(f"zombies.append(zombie{i})")
    if tick % 100 == 0:
        if 4 < hours < 20 and hp < 100:
            a = player.backpack.count("health")
            addhp = 1
            if a > 0:
                addhp *= a + 1
            if hunger > 16:
                hunger -= 1
                addhp += 1
            hp += addhp
            print(f"{player.name}'s health + {addhp}")
    if hp > 100:
        print(f"{player.name} too many hp ({hp}), set to max (100)")
        hp = 100
    game.after(50, refresh_)


def get_food():
    global player
    player.backpack.append("food")
    plrfoodcount = player.backpack.count("food")
    print(f"{player.name} got 1 food. Now he has {plrfoodcount} food")


def eat_food():
    global player, hunger
    plrbackpack = player.backpack
    foodcount = plrbackpack.count("food")
    plrhunger = player.hunger
    if foodcount > 0 and plrhunger < 20:
        plrbackpack.remove("food")
        hunger += 1
        plrfoodcount = player.backpack.count("food")
        print(
            f"{player.name} ate 1 food. Now he has {plrfoodcount} food. His hunger: {player.hunger}"
        )


def skip_night():
    global tick,hunger
    mins = int(tick * 0.06)
    hours = 0
    days = 0
    while mins >= 60:
        hours += 1
        mins -= 60
    while hours >= 24:
        days += 1
        hours -= 24
    if (18 <= hours <= 24) or (0 <= hours <= 4):
        _tick = tick
        _tick -= days * 24000
        addtick = 24000 - _tick
        skipto_hour = 5
        addtick += skipto_hour * 1000  # skip to next day 05:00
        tick += addtick
        reducehunger = randint(1, 5)
        hunger -= reducehunger
        print(f"skipped night, hunger - {reducehunger}")


def get_coin():
    global coins
    coins += 1
    print(f"coins + 1 (now coins: {coins})")


def buy(obj):
    global coins
    if obj == "h":
        if coins >= 5:
            player.backpack.append("health")
            coins -= 5
        else:
            print("5 coins = 1 health")
    elif obj == "s":
        if coins >= 5:
            player.backpack.append("sword")
            coins -= 5
        else:
            print("5 coins = 1 sword")


def buy_():
    buy("h")


def buy__():
    buy("s")


eat_food_btn = Button(game, text="eat food", command=eat_food)
get_food_btn = Button(game, text="get food", command=get_food)
skip_night_btn = Button(game, text="skip night", command=skip_night)
buy_health_btn = Button(game, text="buy health", command=buy_)
buy_sword_btn = Button(game, text="buy sword", command=buy__)
get_coin_btn = Button(game, text="get coin", command=get_coin)
eat_food_btn.place(relx=0.2, rely=0.1, anchor="ne")
get_food_btn.place(relx=0.2, rely=0.2, anchor="ne")
skip_night_btn.place(relx=0.2, rely=0.3, anchor="ne")
buy_health_btn.place(relx=0.2, rely=0.4, anchor="ne")
buy_sword_btn.place(relx=0.2, rely=0.5, anchor="ne")
get_coin_btn.place(relx=0.2, rely=0.6, anchor="ne")

refresh_()

game.protocol("WM_DELETE_WINDOW", saveexit)

game.mainloop()
