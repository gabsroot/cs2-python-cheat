from time import sleep
import pymem, pymem.process
from pynput.mouse import Controller, Button
from random import uniform
from module.offsets import Offsets

class TriggerBot:
    def __init__(self, ignoreTeam=False):
        self.ignoreTeam = ignoreTeam
        self.mouse = Controller()
        self.pm = pymem.Pymem("cs2.exe")
        self.client = pymem.process.module_from_name(self.pm.process_handle, "client.dll").lpBaseOfDll

    def Shoot(self):
        sleep(uniform(0.01, 0.03))
        self.mouse.press(Button.left)
        sleep(uniform(0.01, 0.05))
        self.mouse.release(Button.left)
        sleep(0.1)

    def Enable(self):
        player = self.pm.read_longlong(self.client + Offsets.dwLocalPlayerPawn)
        entityId = self.pm.read_int(player + Offsets.m_iIDEntIndex)

        if entityId > 0:
            entList = self.pm.read_longlong(self.client + Offsets.dwEntityList)
            entEntry = self.pm.read_longlong(entList + 0x8 * (entityId >> 9) + 0x10)
            entity = self.pm.read_longlong(entEntry + 120 * (entityId & 0x1FF))
            entityTeam = self.pm.read_int(entity + Offsets.m_iTeamNum)
            playerTeam = self.pm.read_int(player + Offsets.m_iTeamNum)
            entityHp = self.pm.read_int(entity + Offsets.m_iHealth)

            if self.ignoreTeam or (entityTeam != playerTeam) and entityHp > 0:
                self.Shoot()