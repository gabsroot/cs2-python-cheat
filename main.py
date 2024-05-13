import pyMeow as pm
import threading
from random import choice
from json import load
from module.wallhack import WallHack
from module.triggerbot import TriggerBot

class Program:
    def __init__(self):
        try:
            self.window = "".join(choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789") for _ in range(8))
            self.fps = 144
            self.config = self.LoadConfig()
            self.process = pm.open_process("cs2.exe")
            self.module = pm.get_module(self.process, "client.dll")["base"]
            self.trigger = TriggerBot(self.process, self.module, ignoreTeam=self.config["ignoreTeam"])
            self.triggerThread = None
            self.wall = WallHack(self.process, self.module)
        except:
            exit("Error: Enable only after opening Counter Strike 2")

    def LoadConfig(self):
        try:
            with open("config.json", "r", encoding="utf-8") as file:
                return load(file)
        except:
            exit("Error when importing configuration, see if the config.json file exists")

    def TriggerThread(self):
        while pm.overlay_loop():
            if self.config["triggerbot"]:
                self.trigger.Enable()

    def Run(self):
        pm.overlay_init(target=self.window, title=self.window, fps=self.fps)

        self.triggerThread = threading.Thread(target=self.TriggerThread)
        self.triggerThread.start()

        while pm.overlay_loop():
            if self.config["wallhack"]:
                self.wall.Render()

        if self.triggerThread:
            self.triggerThread.join()

if __name__ == "__main__":
    program = Program()
    program.Run()
