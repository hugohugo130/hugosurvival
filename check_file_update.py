def cfu(file="game.py"):
    from github import Github as g

    link = "hugohugo130/hugosurvival"
    filename = "game.py"
    git = g("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")
    git = git.get_repo(link)
    git = git.get_contents(filename)
    latestfile = git.decoded_content
    with open(file, "rb") as gamefile:
        gamefilec = gamefile.read()
    if gamefilec != latestfile:
        return 1
    else:
        return 0


if __name__ == "__main__":
    from os.path import exists

    if not exists("game.py"):
        file = "..\\game.py"
    else:
        file = "game.py"
    input(cfu(file))