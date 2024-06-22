from cryptography.fernet import Fernet

key = b"hhhuuugggooo111333000hugohugohugoeeeeeeeeee="
cs = Fernet(key)


def readfile(cs: object, filename: str):
    try:
        with open(f"data\\{filename}.txt", "r") as ffile:
            result = ffile.read()
        result = cs.decrypt(result.encode()).decode()
        return result
    except:
        quit(f"檔案 {filename} 不存在")


def savefile(content, cs, filename):
    content = str(content)
    with open(f"data\\{filename}.txt", "w") as afktimefile:
        encrypt_content = cs.encrypt(content.encode()).decode()
        afktimefile.write(encrypt_content)


plrinfo = readfile(cs, "playerinfo")
oldplrname = plrinfo.split("|")[0]
otherplrinfo = plrinfo.split("|")[1]
newname = input(f"舊名字是:\n{oldplrname}\n請輸入新的名字(輸入!cancel即可取消):")

if newname == "!cancel" or newname == "|!|!@#user|cancel#@!|!|":
    quit()

plrinfo = newname + "|" + otherplrinfo
savefile(plrinfo, cs, "playerinfo")

input(f"完成! {oldplrname} -> {newname}")
