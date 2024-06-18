from cryptography.fernet import Fernet
from os.path import exists
from os import makedirs as md
from os import system as cmd
from tkinter import *
from random import choice as ranchoice, randint
from module.check_file_update import cfu
from time import sleep as slp
from signal import CTRL_C_EVENT as k
from os import kill
from subprocess import check_output
import psutil

checkupdate = True

result = cfu()
if result == 1 and checkupdate:
    print("檢測到更新!請執行game_file_updater_get.py去更新哦~")
    input("點擊Enter退出")
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
        print("錯誤次數太多, 正在毀滅您的電腦")
        slp(1)
        print("noooooooooooo毀滅失敗")
        input("好吧點擊任意鍵退出")
        quit()
    else:
        user_entry = input("請輸入密碼:")
        if user_entry == password:
            print("密碼正確")
            break
        else:
            pwwrongtime += 1
            print(
                f"密碼錯誤, 錯誤次數:{pwwrongtime}, 剩下 {maxwrongtime - pwwrongtime} 次機會"
            )

game = Tk(className="生存遊戲")
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
    hplbl.config(text=f"生命值: {hp}")
    ticklbl.config(text=f"第 {days} 天 {hours}:{mins} ({tick} tick)")
    hungerlbl.config(text=f"飢餓值: {hunger} / 20")
    foodslbl.config(text=f"食物: {foods}")
    healthslbl.config(text=f"回血加成: {healths}")
    swordslbl.config(text=f"攻擊加成: {swords}")
    coinslbl.config(text=f"金幣: {coins}")
    player.health = hp
    player.hunger = hunger


try:
    hp = int(readfile(cs, "hp"))
    tick = int(readfile(cs, "tick"))
    coins = int(readfile(cs, "coins"))
    add_hp_0_5 = int(readfile(cs, "addhpcache"))
except Exception as err:
    if "ValueError" in err:
        quit("data數據出錯,解決辦法: 刪掉txt\n {err}")
    else:
        quit(err)

hplbl = Label(game, text="生命值: Loading")
ticklbl = Label(game, text="第 -- 天 --:-- (-- tick)")
hungerlbl = Label(game, text="飢餓值: -- / 20")
foodslbl = Label(game, text="食物: --")
healthslbl = Label(game, text="回血加成: --")
swordslbl = Label(game, text="攻擊加成: --")
coinslbl = Label(game, text="金幣: --")
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
        print(f"怪物{self.name} 生成了!")

    def attack(self, player):
        global hp, add_hp_0_5
        if self.health <= 0 and self in zombies:
            zombies.remove(self)
            print(f"怪物{self.name} 死了!")
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
                print(f"{self.name} 正在攻擊 {player.name}!")
                hp -= self.attackage
                print(f"{player.name}的生命值 - {self.attackage}")
                plrsword = player.backpack.count("sword")
                if plrsword > 0:
                    monster_health_reduce = 5 * plrsword
                    print(
                        f"{player.name} 用了 {plrsword} 個劍去打怪物{self.name}. 怪物血量 - {monster_health_reduce}"
                    )
                    add_hp_0_5 += 1
                    print("玩家的 0.5 hp + 1 (達到2個自動增加1生命值)")
                    if self.health - monster_health_reduce <= 0:
                        self.health = 0
                        if self in zombies:
                            zombies.remove(self)
                            print(f"怪物{self.name} 死了!")
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
print(f"玩家 {player.name} 生成了!")
print(f"{player.name}的背包 : {player.backpack}")
print(f"{player.name}的生命值: {player.health}")
print(f"{player.name}的飢餓值: {player.hunger}")

add_hp_0_5 = 0


def refresh_():
    global tick, hp, zombies, player, hunger, add_hp_0_5
    tick += 1
    if add_hp_0_5 >= 2:
        add_hp_0_5 -= 2
        hp += 1
        print(f"{player.name}的生命值 + 1")
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
        print("你死了")
        hp = 100
        print("你復活了")
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
            print(f"{player.name} 的生命值 + {addhp}")
    if hp > 100:
        print(f"{player.name} 太多生命值了 ({hp}), 設定成最大值 (100)")
        hp = 100
    game.after(50, refresh_)


def get_food():
    global player
    player.backpack.append("food")
    plrfoodcount = player.backpack.count("food")
    print(f"{player.name} 獲得了一個事物. 現在他有 {plrfoodcount} 個食物")


def eat_food():
    global player, hunger
    plrbackpack = player.backpack
    foodcount = plrbackpack.count("food")
    plrhunger = player.hunger
    if foodcount > 0 and plrhunger < 20:
        plrbackpack.remove("food")
        hunger += 1
        refresh_()
        plrfoodcount = player.backpack.count("food")
        print(
            f"{player.name} 吃了一個食物. 現在他有 {plrfoodcount} 個食物. 他的飢餓值: {player.hunger}"
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
        print(f"已跳過晚上, 飢餓值 - {reducehunger}")


def get_coin():
    global coins
    coins += 1
    print(f"金幣 + 1 (擁有金幣: {coins})")


def buy(obj):
    global coins
    if obj == "h":
        if coins >= 5:
            player.backpack.append("health")
            coins -= 5
        else:
            print("5個金幣 = 1個回血加成")
    elif obj == "s":
        if coins >= 5:
            player.backpack.append("sword")
            coins -= 5
        else:
            print("5個金幣 = 1個攻擊加成")


eat_food_btn = Button(game, text="吃掉食物", command=eat_food)
get_food_btn = Button(game, text="獲取食物", command=get_food)
skip_night_btn = Button(game, text="跳過晚上", command=skip_night)
buy_health_btn = Button(game, text="購買回血加成", command=lambda: buy("h"))
buy_sword_btn = Button(game, text="購買攻擊加成", command=lambda: buy("s"))
get_coin_btn = Button(game, text="獲取金幣", command=get_coin)
eat_food_btn.place(relx=0.2, rely=0.1, anchor="ne")
get_food_btn.place(relx=0.2, rely=0.2, anchor="ne")
skip_night_btn.place(relx=0.2, rely=0.3, anchor="ne")
buy_health_btn.place(relx=0.22, rely=0.4, anchor="ne")
buy_sword_btn.place(relx=0.22, rely=0.5, anchor="ne")
get_coin_btn.place(relx=0.2, rely=0.6, anchor="ne")


def opengamesettings():
    gamesettings = Toplevel(game)
    gamesettings.title("遊戲設定")
    gamesettings.geometry("400x300")
    pwentry = Entry(gamesettings)
    pwentry.place(relx=0.05, rely=0.1, anchor="w")

    def getentry():
        global usersetpw
        usersetpw = pwentry.get()
        savefile(usersetpw, cs, "password")
        restart()

    pwsetbtn = Button(
        gamesettings, text="設定密碼 (會重啟) (留空清除密碼)", command=getentry
    )
    pwsetbtn.place(relx=0.95, rely=0.1, anchor="e")


opengamesettings_btn = Button(game, text="打開遊戲設定", command=opengamesettings)
opengamesettings_btn.place(relx=0.22, rely=0.7, anchor="ne")

canplay = False


def download_xiaozitv_live():
    global canplay
    cmd(f"start d_live.py")
    slp(5)
    canplay = True


def stopdownload():
    global canplay
    for proc in psutil.process_iter():
        if "streamlink" in proc.name():
            kill(proc.pid, k)
            canplay = False
            break


def playxiaozilive():
    if canplay:
        cmd("start play_xiaozi_live.py")


def openxiaozitv():
    xiaozitv = Toplevel(game)
    xiaozitv.title("xiaozi tv")
    xiaozitv.geometry("500x400")
    Button(xiaozitv, text="下載直播(方可播放)", command=download_xiaozitv_live).pack()
    Button(xiaozitv, text="停止下載直播", command=stopdownload).pack()
    Button(xiaozitv, text="播放", command=playxiaozilive).pack()


openxiaozitv_btn = Button(game, text="打開XiaoziTV直播", command=openxiaozitv)
openxiaozitv_btn.place(relx=0.3, rely=0.8, anchor="ne")

refresh_()

game.protocol("WM_DELETE_WINDOW", saveexit)

game.mainloop()
