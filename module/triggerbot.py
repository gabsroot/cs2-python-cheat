import pyMeow as pm
from time import sleep
from random import uniform
from module.offsets import Offsets

class TriggerBot:
    def __init__(self, process, module, ignoreTeam=False):
        self.ignoreTeam = ignoreTeam
        self.process = process
        self.module = module

    def Shoot(self):
        sleep(uniform(0.01, 0.03))
        pm.mouse_down(button='left')
        sleep(uniform(0.01, 0.05))
        pm.mouse_up(button='left')
        sleep(0.1)

    def Enable(self):
        player = pm.r_uint64(self.process, self.module + Offsets.dwLocalPlayerPawn)
        entityId = pm.r_int(self.process, player + Offsets.m_iIDEntIndex)

        if entityId > 0:
            entList = pm.r_uint64(self.process, self.module + Offsets.dwEntityList)
            entEntry = pm.r_uint64(self.process,entList + 0x8 * (entityId >> 9) + 0x10)
            entity = pm.r_uint64(self.process,entEntry + 120 * (entityId & 0x1FF))
            entityTeam = pm.r_int(self.process,entity + Offsets.m_iTeamNum)
            playerTeam = pm.r_int(self.process,player + Offsets.m_iTeamNum)
            entityHp = pm.r_int(self.process,entity + Offsets.m_iHealth)

            if self.ignoreTeam or (entityTeam != playerTeam) and entityHp > 0:
                self.Shoot()
