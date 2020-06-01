import copy
import numpy as np
import math
import random
global Map
Map = []
item = [[0, 0], 0, 0]
Area = []
i = 0
itemline = []
a = 20
Grid = []
Uav = []
while i < 3:
    j = 0
    while j < 3:
        item = [[0, 0], i * 3 + j, 0]
        itemline.append(copy.deepcopy(item))
        j += 1
    Area.append(copy.deepcopy(itemline))
    itemline = []
    i += 1
print(Area)

for i in range(3):
    for j in range(3):
        Area[i][j][0][0] = Area[i][j][0][0] + (2 * i + 1) * a
        Area[i][j][0][1] = Area[i][j][0][1] + (2 * j + 1) * a

print(Area)


def Divide(x):
    t = 10
    itemline = []
    i = 0
    j = 0
    Grid = []
    while i < t:
        j = 0
        while j < t:
            item = [[0, 0], i * t + j, 0, 0,0]
            itemline.append(copy.deepcopy(item))
            j += 1
        Grid.append(copy.deepcopy(itemline))
        itemline = []
        i += 1

    for i in range(t):
        for j in range(t):
            Grid[i][j][2] = x
            Grid[i][j][0][0] = Grid[i][j][0][0] + ( i + 1) * (a / 20)
            Grid[i][j][0][1] = Grid[i][j][0][1] + ( j + 1) * (a / 20)
    for i in range(t):
        for j in range(t):
            m = x % 3
            n = x // 3
            Grid[i][j][0][1] = Grid[i][j][0][1] + 100 * m
            Grid[i][j][0][0] = Grid[i][j][0][0] + 100 * n

    return Grid




for i in range(3):
    Map.append(Divide(i))

print(Divide(0))
class UAV():
    def __init__(self, x_v, y_v, x_position, y_position):
        self.x_v = x_v
        self.y_v = y_v
        self.x_position = x_position
        self.y_position = y_position

    def x_vChange(self, xc):
        self.x_v = xc

    def y_vChange(self, yc):
        self.y_v = yc

    def remew(self):
        self.x_position = self.x_position + self.x_v
        self.y_position = self.y_position + self.y_v

    def stop(self):
        self.x_v = 0
        self.y_v = 0


for i in range(10):
    a = UAV(0, 0, 0, 0)
    Uav.append(a)

for i in range(10):
    Uav[i].x_position=random.random()*10
    Uav[i].y_position=random.random()*10
    print(Uav[i].x_position)
    print(Uav[i].y_position)

distance = np.zeros((10, 10))
degree = np.zeros((10, 10))

for i in range(10):
    for j in range(10):
        distance[i][j] = math.sqrt((Uav[j].x_position - Uav[i].x_position) **2 + (Uav[j].y_position - Uav[i].y_position) ** 2)
        if(Uav[j].x_position== Uav[i].x_position):
            if((Uav[j].y_position - Uav[i].y_position)>0):
                degree[i][j]=math.pi/2
            if((Uav[j].y_position - Uav[i].y_position)<0):
                degree[i][j]=math.pi*3/2
            else:
                degree[i][j]=math.atan((Uav[j].y_position - Uav[i].y_position)/(Uav[j].x_position - Uav[i].x_position))