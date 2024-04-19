import pyMeow as pw
from module.offsets import Offsets

class Entity:
    def __init__(self, pointer, pawnPointer, process):
        self.pointer = pointer
        self.pawnPointer = pawnPointer
        self.process = process
        self.pos2d = None
        self.headPos2d = None

    def Health(self):
        return pw.r_int(self.process, self.pawnPointer + Offsets.m_iHealth)

    def Team(self):
        return pw.r_int(self.process, self.pawnPointer + Offsets.m_iTeamNum)

    def Pos(self):
        return pw.r_vec3(self.process, self.pawnPointer + Offsets.m_vOldOrigin)

    def BonePos(self, bone):
        gameScene = pw.r_int64(self.process, self.pawnPointer + Offsets.m_pGameSceneNode)
        boneArrayPointer = pw.r_int64(self.process, gameScene + 480)
        return pw.r_vec3(self.process, boneArrayPointer + bone * 32)

    def Wts(self, matrix):
        try:
            self.pos2d = pw.world_to_screen(matrix, self.Pos(), 1)
            self.headPos2d = pw.world_to_screen(matrix, self.BonePos(6), 1)
        except:
            return False
        
        return True