import pyMeow as pw
from module.offsets import Offsets
from module.entity import Entity

class WallHack:
    def __init__(self, process, module):
        self.process = process
        self.module = module

    def GetEntities(self):
        entityList = pw.r_int64(self.process, self.module + Offsets.dwEntityList)
        localPlayer = pw.r_int64(self.process, self.module + Offsets.dwLocalPlayerController)

        for _ in range(1, 65):
            try:
                entryPointer = pw.r_int64(self.process, entityList + (8 * (_ & 0x7FFF) >> 9) + 16)
                controllerPointer = pw.r_int64(self.process, entryPointer + 120 * (_ & 0x1FF))

                if controllerPointer == localPlayer:
                    continue

                controllerPawnPointer = pw.r_int64(self.process, controllerPointer + Offsets.m_hPlayerPawn)
                listEntityPointer = pw.r_int64(self.process, entityList + 0x8 * ((controllerPawnPointer & 0x7FFF) >> 9) + 16)
                pawnPointer = pw.r_int64(self.process, listEntityPointer + 120 * (controllerPawnPointer & 0x1FF))
            except:
                continue

            yield Entity(controllerPointer, pawnPointer, self.process)

    def Render(self):
        matrix = pw.r_floats(self.process, self.module + Offsets.dwViewMatrix, 16)
        
        for entity in self.GetEntities():
            if entity.Wts(matrix) and entity.Health() > 0:
                head = entity.pos2d["y"] - entity.headPos2d["y"]
                width = head / 2
                center = width / 2
                color = pw.get_color("blue") if entity.Team() != 2 else pw.get_color("orange")
                fill = pw.fade_color(pw.get_color("#242625"), 0.5)

                # Fill
                pw.draw_rectangle(entity.headPos2d["x"] - center, entity.headPos2d["y"] - center / 2, width, head + center / 2, fill)

                # Box
                pw.draw_rectangle_lines(entity.headPos2d["x"] - center, entity.headPos2d["y"] - center / 2, width, head + center / 2, color, 0.8)

        pw.end_drawing()