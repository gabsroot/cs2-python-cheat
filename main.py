import pyMeow as pw
from json import load
from module.wallhack import WallHack
from module.triggerbot import TriggerBot

class Program:
    def __init__(self):
        try:
            self.window = "Counter-Strike 2"
            self.fps = 144
            self.config = self.LoadConfig()
            self.process = pw.open_process("cs2.exe")
            self.module = pw.get_module(self.process, "client.dll")["base"]
            self.trigger = TriggerBot(ignoreTeam=self.config["ignoreTeam"])
            self.wall = WallHack(self.process, self.module)
        except:
            exit("Error: Enable only after opening Counter Strike 2")

    def LoadConfig(self):
        try:
            with open("config.json", "r", encoding="utf-8") as file:
                return load(file)
        except:
            exit("Error when importing configuration, see if the config.json file exists")

    def Run(self):
        pw.overlay_init(target=self.window, title=self.window, fps=self.fps)

        while pw.overlay_loop():
            try:
                if self.config["wallhack"]:
                    self.wall.Render()

                if self.config["triggerbot"]:
                    self.trigger.Enable()
            except: pass

if __name__ == "__main__":
    program = Program()
    program.Run()