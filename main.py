import pyMeow as pw
from module.wallhack import WallHack
from module.triggerbot import TriggerBot

# Config
WALLHACK = True
TRIGGERBOT = True
IGNORE_TEAM = True

class Program:
    def __init__(self):
        self.window = "Counter-Strike 2"
        self.fps = 144
        self.process = pw.open_process("cs2.exe")
        self.module = pw.get_module(self.process, "client.dll")["base"]
        self.trigger = TriggerBot(ignoreTeam=IGNORE_TEAM)
        self.wall = WallHack(self.process, self.module)

    def Run(self):
        pw.overlay_init(target=self.window, title=self.window, fps=self.fps)

        while pw.overlay_loop():
            try:
                if WALLHACK:
                    self.wall.Render()

                if TRIGGERBOT:
                    self.trigger.Enable()
            except: pass

if __name__ == "__main__":
    program = Program()
    program.Run()