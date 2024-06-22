def getlink():
    from requests import get
    return get("https://pastebin.com/raw/VFbHJDKv").content.decode()

if __name__ == "__main__":  
    input(getlink())
