from cryptography.fernet import Fernet
from os.path import exists
from os import makedirs as md, system as cmd, kill
from tkinter import *
from random import choice as ranchoice, randint
from time import sleep as slp
from signal import CTRL_C_EVENT as k
import psutil
from module.check_file_update import cfu
import module.check_all_requirements as car
import configparser

if not exists("config.ini"):
    while True:
        user_checkupdate = input("是否檢查遊戲更新?\n是否检查游戏更新?\n(1 = 是, 0 = 否)\n")
        if any(user_checkupdate in i for i in ["1","0"]):
            break
        else:
            print("請輸入 请输入 1或0!")
    while True:
        user_cuosf = input("此環境是否可以使用os.system功能?\n此环境是否可以使用os.system功能?\n(1 = 是, 0 = 否)\n")
        if any(user_cuosf in i for i in ["1","0"]):
            break
        else:
            print("請輸入 请输入 1或0!")
    while True:
        user_lang = input("請選擇語言\n请选择语言\ntc = 繁體中文\nsc = 简体中文\n")
        if any(user_lang in i for i in["tc","sc"]):
            break
        else:
            print("請輸入 请输入 tc或sc!")
    gameconfig = configparser.ConfigParser()
    gameconfig["CONFIG"] = {}
    gameconfig["CONFIG"]["checkupdate"] = user_checkupdate
    gameconfig["CONFIG"]["cuosf"] = user_cuosf
    gameconfig["CONFIG"]["lang"] = user_lang
    with open("config.ini", "w") as cf:
        gameconfig.write(cf)

config = configparser.ConfigParser()
config.read("config.ini")
cu = config["CONFIG"]["checkupdate"]
cuosf = config["CONFIG"]["cuosf"]
langchoose = config["CONFIG"]["lang"]
if cu == "1":
    checkupdate = True
else:
    checkupdate = False
if cuosf == "1":
    can_use_os_system_function = True
else:
    can_use_os_system_function = False
if langchoose == "sc":
    import lang.sc as lang
else:
    import lang.tc as lang

# checkupdate = True

# can_use_os_system_function = True

car.run()

result = cfu()
if result == 1 and checkupdate:
    print(lang.cfu1)
    input(lang.pressentertoquit)
    quit()

key = b"hhhuuugggooo111333000hugohugohugoeeeeeeeeee="
cs = Fernet(key)
filename = "game"


def readfile(cs: object, filename: str):
    if not exists(f"data\\{filename}.txt"):
        a = open(f"data\\{filename}.txt", "w")
        if filename == "hp":
            content = "100"
        elif filename == "playerinfo":
            content = "Player|.20"
        elif filename == "password":
            content = ""
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


def restart():
    saveall()
    if not can_use_os_system_function:
        print(f"{lang.cannotusecmd},{lang.plsrestartself}!!")
        return
    cmd(f"start {filename}.py")
    quit()


def saveexit():
    saveall()
    quit("Exit")


if not exists("data"):
    md("data")

password = readfile(cs, "password")
pwwrongtime = 0
maxwrongtime = 5
while True:
    if password == "":
        break
    if pwwrongtime >= maxwrongtime:
        print({lang.errtoomanydestroyingpc})
        slp(1)
        print(f"noooooooooooo{lang.destoryfailed}")
        input(lang.okpressenterexit)
        quit()
    else:
        user_entry = input(lang.pleaseenterpw)
        if user_entry == password:
            print(lang.pwcorrect)
            break
        else:
            pwwrongtime += 1
            print(
                f"{lang.pwerr}{pwwrongtime}, {lang.remain} {maxwrongtime - pwwrongtime} {lang.times}"
            )

game = Tk(className=lang.survivalgame)
game.geometry("400x300")


def refresh():
    global hplbl, ticklbl, player, hungerlbl, foodslbl, healthslbl, swordslbl, coinslbl
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
    hplbl.config(text=f"{lang.shealth[1:]}: {hp}")
    ticklbl.config(text=f"{lang.day1} {days} {lang.day2} {hours}:{mins} ({tick} tick)")
    hungerlbl.config(text=f"{lang.shunger[1:]}: {hunger} / 20")
    foodslbl.config(text=f"{lang.food}: {foods}")
    healthslbl.config(text=f"{lang.healthup}: {healths}")
    swordslbl.config(text=f"{lang.attackup}: {swords}")
    coinslbl.config(text=f"{lang.coins}: {coins}")
    player.health = hp
    player.hunger = hunger


try:
    hp = int(readfile(cs, "hp"))
    tick = int(readfile(cs, "tick"))
    coins = int(readfile(cs, "coins"))
    add_hp_0_5 = int(readfile(cs, "addhpcache"))
except Exception as err:
    if "ValueError" in err:
        quit(f"{lang.dataerr}\n {err}")
    else:
        quit(err)

hplbl = Label(game, text=f"生命值: Loading")
ticklbl = Label(game, text=f"第 -- 天 --:-- (-- tick)")
hungerlbl = Label(game, text=f"飢餓值: -- / 20")
foodslbl = Label(game, text=f"食物: --")
healthslbl = Label(game, text=f"{lang.healthup}: --")
swordslbl = Label(game, text=f"{lang.attackup}: --")
coinslbl = Label(game, text=f"{lang.coins}: --")
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
        print(f"{lang.zombie}{self.name} {lang.spawned}!")

    def attack(self, player):
        global hp, add_hp_0_5
        if self.health <= 0 and self in zombies:
            zombies.remove(self)
            print(f"{lang.zombie}{self.name} {lang.udied[1:]}!")
        else:
            # print(f"{self.name} want to attack {player.name}! -- monster attack function")
            if randint(1, 2) == 1:
                print(f"{player.name}{lang.evade}{lang.zombie}{self.name}{lang.success}!")
            else:
                print(
                    f"{player.name}{lang.evade}{lang.zombie}{self.name}{lang.failed}，{lang.zombie}{self.name}{lang.attacking[2:]}!"
                )
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
                    print(f"{self.name} {lang.attacking} {player.name}!")
                    hp -= self.attackage
                    print(f"{player.name}{lang.shealth} - {self.attackage}")
                    plrsword = player.backpack.count("sword")
                    if plrsword > 0:
                        monster_health_reduce = 5 * plrsword
                        print(
                            f"{player.name} {lang.used} {plrsword} {lang.swordtoattack}{lang.zombie}{self.name}. {lang.zombie}{lang.health} - {monster_health_reduce}"
                        )
                        add_hp_0_5 += 1
                        print(f"{player.name}{lang.s} 0.5 hp + 1 ({lang.two0_5hpto1hp})")
                        if self.health - monster_health_reduce <= 0:
                            self.health = 0
                            if self in zombies:
                                zombies.remove(self)
                                print(f"{lang.zombie}{self.name} {lang.udied[1:]}!")
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
print(f"{lang.player} {player.name} {lang.spawned}!")
print(f"{player.name}{lang.sbackpack} : {player.backpack}")
print(f"{player.name}{lang.shealth}: {player.health}")
print(f"{player.name}{lang.shunger}: {player.hunger}")

add_hp_0_5 = 0


def refresh_():
    global tick, hp, zombies, player, hunger, add_hp_0_5
    tick += 1
    if add_hp_0_5 >= 2:
        add_hp_0_5 -= 2
        hp += 1
        print(f"{player.name}{lang.shealth} + 1")
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
        print(lang.udied)
        hp = 100
        print(lang.urevive)
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
            print(f"{player.name} {lang.shealth} + {addhp}")
    if hp > 100:
        print(f"{player.name}{lang.toomanyhealth}({hp}), {lang.settomax} (100)")
        hp = 100
    game.after(50, refresh_)


def get_food():
    global player
    player.backpack.append("food")
    plrfoodcount = player.backpack.count("food")
    print(f"{player.name}{lang.gotfood1}{plrfoodcount}{lang.gotfood2}")


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
            f"{player.name}{lang.atefood1}{plrfoodcount}{lang.atefood2}{player.hunger}"
        )


def skip_night():
    global tick, hunger
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
        print(f"{lang.skippednight}{reducehunger}")


def get_coin():
    global coins
    coins += 1
    print(f"{lang.coinsget}{coins})")


def buy(obj):
    global coins
    if obj == "h":
        if coins >= 5:
            player.backpack.append("health")
            coins -= 5
        else:
            print(lang.e5ceq1h)
    elif obj == "s":
        if coins >= 5:
            player.backpack.append("sword")
            coins -= 5
        else:
            # print("5個{lang.coins} = 1個{lang.attackup}")
            print(lang.e5ceq1s)


eat_food_btn = Button(game, text=lang.eatfood, command=eat_food)
get_food_btn = Button(game, text=lang.getfood, command=get_food)
skip_night_btn = Button(game, text=lang.skipnight, command=skip_night)
buy_health_btn = Button(game, text=lang.buyh, command=lambda: buy("h"))
buy_sword_btn = Button(game, text=lang.buys, command=lambda: buy("s"))
get_coin_btn = Button(game, text=lang.getcoin, command=get_coin)
eat_food_btn.place(relx=0.2, rely=0.1, anchor="ne")
get_food_btn.place(relx=0.2, rely=0.2, anchor="ne")
skip_night_btn.place(relx=0.2, rely=0.3, anchor="ne")
buy_health_btn.place(relx=0.22, rely=0.4, anchor="ne")
buy_sword_btn.place(relx=0.22, rely=0.5, anchor="ne")
get_coin_btn.place(relx=0.2, rely=0.6, anchor="ne")


def opengamesettings():
    gamesettings = Toplevel(game)
    gamesettings.title(lang.gamesettings)
    gamesettings.geometry("400x300")
    pwentry = Entry(gamesettings)
    pwentry.place(relx=0.05, rely=0.1, anchor="w")

    def getentry():
        global usersetpw
        usersetpw = pwentry.get()
        savefile(usersetpw, cs, "password")
        restart()

    Button(
        gamesettings, text=lang.resetpw, command=getentry
    ).place(relx=0.95, rely=0.1, anchor="e")


opengamesettings_btn = Button(game, text=lang.opengamesettings, command=opengamesettings)
opengamesettings_btn.place(relx=0.22, rely=0.7, anchor="ne")

canplay = False


def download_xiaozitv_live():
    global canplay
    if not can_use_os_system_function:
        print(lang.cannotusecmd)
        return
    cmd(f"start d_live.py")
    while True:
        if exists("video.mp4"):
            break
        else:
            slp(5)
            a = None
            for proc in psutil.process_iter():
                if "streamlink" in proc.name():
                    a = True
                    break
            if a:
                print(lang.waitingvideod)
            else:
                print(lang.videonotd)
                return
    canplay = True


def stopdownload():
    global canplay
    for proc in psutil.process_iter():
        if "streamlink" in proc.name():
            kill(proc.pid, k)
            print(lang.stoppeddlive)
            canplay = False
            break
        else:
            print(lang.notdlive)


def playxiaozilive():
    print(lang.preparingplive)
    download_xiaozitv_live()
    if not can_use_os_system_function:
        print(lang.cannotusecmd)
        return
    elif canplay:
        cmd("start play_xiaozi_live.py")


def openxiaozitv():
    xiaozitv = Toplevel(game)
    xiaozitv.title("xiaozi tv")
    xiaozitv.geometry("500x400")
    # Button(xiaozitv, text="下載直播(方可播放)", command=download_xiaozitv_live).pack()
    Button(xiaozitv, text=lang.stopdlive, command=stopdownload).pack()
    Button(xiaozitv, text=lang.playlive, command=playxiaozilive).pack()


openxiaozitv_btn = Button(game, text=lang.openxztvlive, command=openxiaozitv)
openxiaozitv_btn.place(relx=0.24, rely=0.8, anchor="ne")

refresh_()

game.protocol("WM_DELETE_WINDOW", saveexit)

game.mainloop()
