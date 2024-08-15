import pyMeow as pm
from module.offsets import Offsets

class Entity:
    def __init__(self, pointer, pawnPointer, process):
        self.pointer = pointer
        self.pawnPointer = pawnPointer
        self.process = process
        self.pos2d = None
        self.headPos2d = None

    def Health(self):
        return pm.r_int(self.process, self.pawnPointer + Offsets.m_iHealth)

    def Team(self):
        return pm.r_int(self.process, self.pawnPointer + Offsets.m_iTeamNum)

    def Pos(self):
        return pm.r_vec3(self.process, self.pawnPointer + Offsets.m_vOldOrigin)

    def BonePos(self, bone):
        gameScene = pm.r_int64(self.process, self.pawnPointer + Offsets.m_pGameSceneNode)
        boneArrayPointer = pm.r_int64(self.process, gameScene + 496) # NOTE: 496 is the current offset for 'm_pBoneArray'. ( THIS WILL BREAK IN FEATURE )
        return pm.r_vec3(self.process, boneArrayPointer + bone * 32)

    def Wts(self, matrix):
        try:
            self.pos2d = pm.world_to_screen(matrix, self.Pos(), 1)
            self.headPos2d = pm.world_to_screen(matrix, self.BonePos(6), 1)
        except:
            return False
        
        return True
