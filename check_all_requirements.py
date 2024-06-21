import sys
from os import system as cmd

def run():
    with open("req.req", "r") as req:
        requirements = req.readlines()

    for req in requirements:
        try:
            exec(f"import {req}")
        except ImportError:
            print(f"模塊{req}不存在，正在為您安裝...")
            cmd(sys.executable + " -m pip install {curreq}")
