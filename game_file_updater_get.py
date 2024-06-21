from github import Github as g
from os.path import exists
from os import system as cmd

result = None

def restart():
    cmd("start game_file_updater_get.py")
    quit()

link = "hugohugo130/hugosurvival"
filename = ["game_file_updater_get.py","game.py","d_live.py","play_xiaozi_live.py","check_all_requirements.py","check_file_update.py","getxiaozilivelink.py"]
for curfilename in filename:
    print(f"正在對{curfilename}操作...")
    git = g("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")
    repo = git.get_repo(link)
    content = repo.get_contents(curfilename)
    latestfile = content.decoded_content
    if not exists(curfilename):
        result = 2
    else:
        with open(curfilename,"rb") as gamefile:
            gamefilec = gamefile.read()
        if gamefilec != latestfile:
            result = 1
        else:
            result = 0

    if result == 1 or result == 2:
        if result == 1:
            print(f"檢測到更新!正在更新{curfilename}...")
        else:
            print(f"正在從github獲取{curfilename}")
        if 3 < filename.index(curfilename) < 7:
            curfilename = "module\\" + curfilename
        with open(curfilename,"wb") as gamefile:
            gamefile.write(latestfile)
            if curfilename == "game_file_updater_get.py":
                restart()
    else:
        print(f"目前你的{curfilename}是最新的,沒有更新!")

input("執行完畢")