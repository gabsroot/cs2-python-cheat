import pyMeow as pm
from module.offsets import Offsets
from module.entity import Entity

class WallHack:
    def __init__(self, process, module, wallhackHealth=True):
        self.wallhackHealth = wallhackHealth
        self.process = process
        self.module = module

    def GetEntities(self):
        entityList = pm.r_int64(self.process, self.module + Offsets.dwEntityList)
        localPlayer = pm.r_int64(self.process, self.module + Offsets.dwLocalPlayerController)

        for _ in range(1, 65):
            try:
                entryPointer = pm.r_int64(self.process, entityList + (8 * (_ & 0x7FFF) >> 9) + 16)
                controllerPointer = pm.r_int64(self.process, entryPointer + 120 * (_ & 0x1FF))

                if controllerPointer == localPlayer:
                    continue

                controllerPawnPointer = pm.r_int64(self.process, controllerPointer + Offsets.m_hPlayerPawn)
                listEntityPointer = pm.r_int64(self.process, entityList + 0x8 * ((controllerPawnPointer & 0x7FFF) >> 9) + 16)
                pawnPointer = pm.r_int64(self.process, listEntityPointer + 120 * (controllerPawnPointer & 0x1FF))
            except:
                continue

            yield Entity(controllerPointer, pawnPointer, self.process)

    def Render(self):
        matrix = pm.r_floats(self.process, self.module + Offsets.dwViewMatrix, 16)
        
        for entity in self.GetEntities():
            if entity.Wts(matrix) and entity.Health() > 0:
                head = entity.pos2d["y"] - entity.headPos2d["y"]
                width = head / 2
                center = width / 2
                color = pm.get_color("blue") if entity.Team() != 2 else pm.get_color("orange")
                fill = pm.fade_color(pm.get_color("#242625"), 0.5)

                # Box Fill
                pm.draw_rectangle(entity.headPos2d["x"] - center, entity.headPos2d["y"] - center / 2, width, head + center / 2, fill)

                # Box
                pm.draw_rectangle_lines(entity.headPos2d["x"] - center, entity.headPos2d["y"] - center / 2, width, head + center / 2, color, 0.8)

                if self.wallhackHealth:
                    # Health
                    pm.draw_rectangle(
                        entity.headPos2d["x"] - center - 10,
                        entity.headPos2d["y"] - center / 2 + (head * 0 / 100),
                        3,
                        head + center / 2 - (head * 0 / 100),
                        color,
                    )

                    # Health Fill
                    pm.draw_rectangle(
                        entity.headPos2d["x"] - center - 10,
                        entity.headPos2d["y"] - center / 2 + (head * (100 - entity.Health()) / 100),
                        3,
                        head + center / 2 - (head * (100 - entity.Health()) / 100),
                        pm.get_color("#00FF17"),
                    )


        pm.end_drawing()
