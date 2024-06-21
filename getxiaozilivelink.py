def getlink():
    from github import Github as g
    link = "hugohugo130/hugosurvival"
    filename = "xiaozilivelink.txt"
    git = g("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")
    git = git.get_repo(link)
    git = git.get_contents(filename)
    return git.decoded_content.decode()

if __name__ == "__main__":
    input(getlink())