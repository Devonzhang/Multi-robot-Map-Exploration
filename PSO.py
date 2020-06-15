# coding=utf-8
import copy
import numpy as np
import math
import random
import codecs
from random import randint

p=0
chess_size = 30
Start_x = 0
Start_y = 0
End_x = 0
End_y = 0
MAZE=[]
OpenListPosition = 0  # 指针标记open列表数组当前存放元素个数（position总指向最后一个元素的后一位置）
CloseListPosition = 0  # 指针标记Close列表数组当前存放元素个数（position总指向最后一个元素的后一位置）
OpenList = []  # open列表(定义成数组形式)
CloseList = []  # close列表
chessboard=[]
lv=0


item = [[0, 0], 0, 0]
Area = []  # 完成  子区域生成
i = 0
itemline = []
a = 20
Grid = []
while i < 3:
    j = 0
    while j < 3:
        item = [[0, 0], i * 3 + j, 0]
        item[2]='0'
        itemline.append(copy.deepcopy(item))
        j += 1
    Area.append(copy.deepcopy(itemline))
    itemline = []
    i += 1

def DivideMap():  # 完成      大地图分割
    g = 30
    itemline = []
    i = 0
    j = 0
    Grid = []
    while i < g:
        j = 0
        while j < g:
            item = [[0, 0], i * g + j, 0, 0, 0]
            itemline.append(copy.deepcopy(item))
            j += 1
        Grid.append(copy.deepcopy(itemline))
        itemline = []
        i += 1

    for i in range(g):
        for j in range(g):
            Grid[i][j][0][0] = Grid[i][j][0][0] + (i + 1)
            Grid[i][j][0][1] = Grid[i][j][0][1] + (j + 1)

            Grid[i][j][3] = '0'  # 可过节点的标号
            Grid[i][j][4]='0'
            if((i==0)|(j==0)|(i==29)|(j==29)):
                Grid[i][j][3] = '2'

    return Grid

DivideM = DivideMap()  # 全局总地图
print(DivideM)
DivideM[3][4][4]='1'
DivideM[6][5][4]='1'
DivideM[8][2][4]='1'
DivideM[7][7][4]='1'
DivideM[6][6][4]='1'
DivideM[10][12][4]='1'
DivideM[8][18][4]='1'
DivideM[7][14][4]='1'
DivideM[6][28][4]='1'
DivideM[10][12][4]='1'
DivideM[28][24][4]='1'

DivideM[18][22][4]='1'
DivideM[11][19][4]='1'

DivideM[1][19][4]='1'
DivideM[24][19][4]='1'
DivideM[14][19][4]='1'
DivideM[4][19][4]='1'
DivideM[18][4][4]='1'
print(DivideM)

print('fjakjgioejgoisjgoshgpiajgoiajspoigjasoipgjoerngpaeoijgoaisjgoi')

class Uav():  # 完成   机器人类
    def __init__(self, x_position, y_position):
        self.x_position = x_position
        self.y_position = y_position
        self.x_location = int((self.x_position) / 10)
        self.y_location = int((self.y_position) / 10)

    def upward(self):
        self.y_position = self.y_position + 1

    def downward(self):
        self.y_position = self.y_position - 1

    def rightward(self):
        self.x_position = self.x_position + 1

    def leftward(self):
        self.x_position = self.x_position - 1

    def stop(self):
        self.x_position = self.x_position
        self.y_position = self.y_position

    def change(self):
        self.x_location=int((self.x_position) / 10)
        self.y_location = int((self.y_position) / 10)


    def Area(self):
        self.SubArea = []
        self.SubArea.append(self.x_location)
        self.SubArea.append(self.y_location)
        return self.SubArea


UavGroup = []  # 完成   机器人群组生成
for i in range(4):
    uav = Uav(5*i+1,5*i+1)
    UavGroup.append(uav)
print(UavGroup[1].x_position)

def Update(Uav):  # 完成      更新地图
    global DivideM
    DivideM[Uav.x_position][Uav.y_position][3] = '2'

    if (DivideM[Uav.x_position + 1][Uav.y_position][4] == '1'):
        DivideM[Uav.x_position + 1][Uav.y_position][3] = '2'
    if (DivideM[Uav.x_position - 1][Uav.y_position][4] == '1'):
        DivideM[Uav.x_position - 1][Uav.y_position][3] = '2'
    if (DivideM[Uav.x_position][Uav.y_position + 1][4] == '1'):
        DivideM[Uav.x_position][Uav.y_position + 1][3] = '2'
    if (DivideM[Uav.x_position][Uav.y_position - 1][4] == '1'):
        DivideM[Uav.x_position][Uav.y_position - 1][3] = '2'

    if ((DivideM[Uav.x_position + 1][Uav.y_position][3] != '1') & (
            DivideM[Uav.x_position + 1][Uav.y_position][3] != '2')):
        DivideM[Uav.x_position + 1][Uav.y_position][3] = '3'
    if ((DivideM[Uav.x_position - 1][Uav.y_position][3] != '1') & (
            DivideM[Uav.x_position - 1][Uav.y_position][3] != '2')):
        DivideM[Uav.x_position - 1][Uav.y_position][3] = '3'
    if ((DivideM[Uav.x_position][Uav.y_position + 1][3] != '1') & (
            DivideM[Uav.x_position][Uav.y_position + 1][3] != '2')):
        DivideM[Uav.x_position][Uav.y_position + 1][3] = '3'
    if ((DivideM[Uav.x_position][Uav.y_position - 1][3] != '1') & (
            DivideM[Uav.x_position][Uav.y_position - 1][3] != '2')):
        DivideM[Uav.x_position][Uav.y_position - 1][3] = '3'




def find(MAP,Uav):            #探索地图算法                                                                              #完成   最近边界栅格搜寻
    minpoint=[]
    item=[[0,0],0]
    min=1000                 #定义一个较大的距离后面会很快的修改
    for i in range(len(MAP)):
        for j in range(len(MAP)):
            if (MAP[i][j][3]=='3'):
                distance=abs(Uav.x_position-MAP[i][j][0][0])+abs(Uav.y_position-MAP[i][j][0][1])
                if(distance<min):
                    item[0][0] = i
                    item[0][1] = j
                    item[1] = distance
                    min=distance
    minpoint.append(item[0][0])
    minpoint.append(item[0][1])
    return minpoint

def ChangeArea():                                                                                                       #完成      子区域状态改变
    global Area
    global DivideM
    for m in range(3):
        for n in range(3):
            flag1=0                 #未探索栅格
            flag2=0                 #边界栅格
            flag3=0                 #已探索栅格
            for j in range(10):
                for l in range(10):

                    if(DivideM[m*10+j][n*10+l][3]=='0'):
                        flag1=1
                    if(DivideM[m*10+j][n*10+l][3] == '3'):
                        flag2 = 1
                    if(DivideM[m*10+j][n*10+l][3] == '1'):
                        flag3 = 1
            if ((flag1==0)&(flag2==0)):                                     #已探索子区域
                Area[m][n][2]='2'
            if ((flag1 ==1)&(flag2==1)&(flag3==1)):                       #正在探索子区域
                Area[m][n][2]='1'
            if (flag3 == 0):                                                  #未被探索子区域
                Area[m][n][2] ='0'

        print('\n')



def A(map):
    def heuristic_distace(Neighbour_node,target_node):
        H = abs(Neighbour_node[0] - target_node[0]) + abs(Neighbour_node[1] - target_node[1])
        return H

    def go_around(direction):
        box_length = 1
        diagonal_line = box_length * 10
        if (direction==0 or direction==2 or direction==6 or direction==8):
            return diagonal_line
        elif (direction==1 or direction==3 or direction==4 or direction==5 or direction==7):
            return box_length

    def find_coordinate(map,symble):
        #store coordinate
        result=[]
        for index1,value1 in enumerate(map):
            if symble in value1:
                row = index1
                for index2, value2 in enumerate(map[index1]):
                    if symble==value2:
                       column = index2
                       result.append([row, column])
        return result



    #these datas are store in the form of list in a singal list

    obstacle = find_coordinate(map,"2")
    start_node = find_coordinate(map,"s")[0]
    target_node = find_coordinate(map,"e")[0]
    current_node = start_node
    path_vertices = [start_node]
    #visited_vertices should be stored in the form of a singal list
    Neighbour_vertices = []

    while current_node != target_node:

        x_coordinate = current_node[0]
        y_coordinate = current_node[1]
        F = []
        Neighbour_vertices =   [[x_coordinate - 1, y_coordinate - 1],
                                [x_coordinate - 1, y_coordinate    ],
                                [x_coordinate - 1, y_coordinate + 1],
                                [x_coordinate,     y_coordinate - 1],
                                [x_coordinate    , y_coordinate    ],
                                [x_coordinate,     y_coordinate + 1],
                                [x_coordinate + 1, y_coordinate - 1],
                                [x_coordinate + 1, y_coordinate    ],
                                [x_coordinate + 1, y_coordinate + 1]]

        for index, value in enumerate(Neighbour_vertices):
            if value[0] in range(len(map)):
                if value[1] in range(len(map)):
                   if value not in obstacle+path_vertices:
                        F.append(heuristic_distace(value, target_node) + go_around(index))
                   else:
                        F.append(10000)
                else:
                        F.append(10000)
            else:
                        F.append(10000)
                   #a very large number
        current_node=Neighbour_vertices[F.index(min(total_distance for total_distance in F))]

        path_vertices.append(current_node)
          # if current_node not in visited_vertices:
          #     visited_vertices.append(current_node)
          # else:
          #     print("there is no route between")
          #     break

    return path_vertices





def Cover(Uav):                                                                                                         #完成      覆盖算法                 问题在这里在这里在这里在这里

    global p
    print('我是无人机                          我所在的子区域是', Uav.y_location, Uav.x_location)
    if (Area[Uav.x_location][Uav.y_location][2] != '2'):
        if ((DivideM[Uav.x_position][Uav.y_position+1][3]=='3')&((Uav.y_position+1)<((Uav.y_location+1)*10))):                   #如果上面是边界栅格
            Uav.upward()
        elif((DivideM[Uav.x_position+1][Uav.y_position][3]=='3')&((Uav.x_position + 1) < ( (Uav.x_location+1)*10))):
            Uav.rightward()
        elif((DivideM[Uav.x_position -1][Uav.y_position][3] == '3')&((Uav.x_position - 1) > (((Uav.x_location)*10)-1))):
            Uav.leftward()
        elif((DivideM[Uav.x_position][Uav.y_position-1][3] == '3')&((Uav.y_position - 1) > ((Uav.y_location)*10)-1)):
            Uav.downward()

        else:                                                                                                           #如果
            minpoint = []
            item = [[0, 0], 0]
            min = 1000  # 定义一个较大的距离后面会很快的修改
            for i in range(30):
                for j in range(30):
                    if (DivideM[i][j][3] == '3'):
                        distance = abs((Uav.x_position - i) )+ abs((Uav.y_position -j))
                        if ((distance < min)&(int((i/10))==Uav.x_location)&(int((j/10))==Uav.y_location)):
                            item[0][0] = i
                            item[0][1] = j
                            item[1] = distance
                            min = distance
            minpoint.append(item[0][0])
            minpoint.append(item[0][1])
            print('hhhhhhhhhhhhhhhhhhhhh',minpoint)

            end1=minpoint
            start=[]
            start.append(Uav.x_position)
            start.append(Uav.y_position)

            a=[]
            for i in range(30):
                item=[]
                for j in range(30):
                    item.append(DivideM[i][j][3])
                a.append(item)
            print(Uav.x_position)
            print(Uav.y_position)
            # 迷宫地图
            print('我是终点',end1)
            print(start)
            print('安居房我今儿佛i骄傲i各环节如果牛肉火锅i奥尔加哦i经全文欧冠i欸哦人给u让你iu阿尔韩国二级人工i角色哦i如果静安寺哦给你欸群聚感染和i二u啊很尖锐共i阿娇io')
            a[end1[0]][end1[1]]='e'
            a[start[0]][start[1]]='s'
            path=A(a)
            a[end1[0]][end1[1]] = '3'
            a[start[0]][start[1]] = '2'
            if(path!=[]):
                if (p < len(path)-1):
                    Uav.x_position = path[p+1][0]
                    Uav.y_position = path[p+1][1]
                    p += 1

                else:
                    p = 0
            else:
                Uav.stop()
    else:
        print('kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk',Area[Uav.x_location][Uav.y_location][2])
        # 计算距离机器人最近的边界栅格
        end2 = find(DivideM, Uav)
        start = []
        start.append(Uav.x_position)
        start.append(Uav.y_position)
        print(end2)
        print(start)

        a = []
        for i in range(30):
            item = []
            for j in range(30):
                item.append(DivideM[i][j][3])
            a.append(item)

        # 迷宫地图
        a[end2[0]][end2[1]] = 'e'
        a[start[0]][start[1]] = 's'
        path2 = A(a)
        a[end2[0]][end2[1]] = '3'
        a[start[0]][start[1]] = '2'


        def Get_Smaller(a, b):
            if a <= b:
                return a
            else:
                return b

        def Get_Bigger(a, b):
            if a >= b:
                return a
            else:
                return b

        # 计算个体历史最优--邻居栅格里面在A*算法求出的去最近的边界栅格的路上的四个栅格中的一个
        def Get_Personal_Best_Grid(Uav, Map):
            end2 = find(DivideM, Uav)
            start = []
            start.append(Uav.x_position)
            start.append(Uav.y_position)
            print(end2)
            print(start)

            a = []
            for i in range(30):
                item = []
                for j in range(30):
                    item.append(DivideM[i][j][3])
                a.append(item)

                # 迷宫地图
            a[end2[0]][end2[1]] = 'e'
            a[start[0]][start[1]] = 's'
            path2 = A(a)
            a[end2[0]][end2[1]] = '3'
            a[start[0]][start[1]] = '2'
            print('看这里看这里看这里看这里',path2,path2[1])
            Direction=Get_Direction(Uav, path2[1])
            print('Personal_Best_Grid:',Direction)

            return Direction

        # 求个体最优的方向
        def Get_Direction(Uav, AStar_Road_No1):
            Direction = -1
            # 先判断东西(左右)
            Uav.Area()
            if Uav.x_position != AStar_Road_No1[0]:
                if Uav.x_position > AStar_Road_No1[0]:
                    # 机器人x坐标比格子x坐标大，格子在机器人左侧（西方）
                    Direction = 3
                else:
                    # 否则格子在机器人右侧（东方）
                    Direction = 1
            elif Uav.y_position != AStar_Road_No1[1]:
                if Uav.y_position > AStar_Road_No1[1]:
                    # 机器人y坐标比格子y坐标大，格子在机器人下面（南方）
                    Direction = 2
                else:
                    # 否则在上面（北方）
                    Direction = 0

            return Direction

        # 求全局最优--机器人数量最少方向
        def Get_Least_Robot_Direction(Uav, Area):
            # 每个方向上面机器人数量，初始为0，顺序为北(上)、东(Area右)、南(下)、西(左)
            Direction_Robot_num = [0, 0, 0, 0]
            # 下面循环部分需要改，看给的地图数据结构
            Searched_Score = 0.5
            Uav.Area()
            # 北面
            for i in range(0, Uav.SubArea[1]):

                if Area[Uav.SubArea[0]][i][2] == '1':
                    Direction_Robot_num[0] += 1
                elif Area[Uav.SubArea[0]][i][2] == '2':
                    Direction_Robot_num[0] += Searched_Score

            # 南面
            for i in range(Uav.SubArea[1] + 1, 3):
                if Area[Uav.SubArea[0]][i][2] == '1':
                    Direction_Robot_num[1] += 1
                elif Area[Uav.SubArea[0]][i][2] == '2':
                    Direction_Robot_num[0] += Searched_Score

            # 东面

            for i in range(0, Uav.SubArea[0]):
                if Area[i][Uav.SubArea[0]][2] == '1':
                    Direction_Robot_num[2] += 1
                elif Area[i][Uav.SubArea[0]][2] == '2':
                    Direction_Robot_num[0] += Searched_Score
            # 西面
            for i in range(Uav.SubArea[0] + 1, 3):
                if Area[i][Uav.SubArea[0]][2] == '1':
                    Direction_Robot_num[3] += 1
                elif Area[i][Uav.SubArea[0]][2] == '2':
                    Direction_Robot_num[0] += Searched_Score

            Direction=Get_Min(Direction_Robot_num)
            print('Least_Robot_Direction:',Direction)

            return Direction
        def Get_Min(Direction_Robot_num):
            a=Direction_Robot_num[0]
            index=0
            for i in range(len(Direction_Robot_num)):
                if Direction_Robot_num[i]<a:
                    a=Direction_Robot_num[i]
                    index=i
            return index

        # 粒子群算法
        # Uav是一个机器人，Map是大地图矩阵，Area是子区域矩阵
        def PSO_choose(Uav, Map, Area):
            global lv
            label = []
            choose=0
            # 对个体最优的加权
            c1 = 20 * random.random()
            # 对全局最优的加权
            c2 = 0 * random.random()
            # 随机算子加权
            c3 = 0 * random.random()
            # 计算个体最优以及全局最优
            label.append(c1)
            label.append(c2)
            label.append(c3)
            print(label)
            maxDir = 0

            Personal_Best = Get_Personal_Best_Grid(Uav, Map)
            Overall_Best = Get_Least_Robot_Direction(Uav, Area)

            for i in range(3):
                if (label[i] > maxDir):
                    choose = i
                    maxDir = label[i]
            print('我是所选择的方向', choose)
            if (choose == 0):
                Direction = Personal_Best
            elif (choose == 1):
                Direction = Overall_Best
            else:
                Direction = lv
            print('我是choose',choose)
            print('这里是三个量',Personal_Best,Overall_Best,lv)
            return Direction

        dir = PSO_choose(Uav, DivideM, Area)  # 获取方向
        flag1=0
        while flag1==0:

            flag1 = 1
            if dir == 4:
                dir = 0
            if ((dir == 0) ):
                if(DivideM[Uav.x_position][Uav.y_position + 1][3] != '2'):
                    Uav.upward()
                else:
                    flag1=0
            elif ((dir == 1) ):
                if((DivideM[Uav.x_position + 1][Uav.y_position][3] != '2')):
                    Uav.rightward()
                else:
                    flag1=0
            elif ((dir == 2) ):
                if (DivideM[Uav.x_position][Uav.y_position - 1][3] != '2'):
                    Uav.downward()
                else:
                    flag1=0
            elif ((dir == 3) ):
                if(DivideM[Uav.x_position - 1][Uav.y_position][3] != '2'):
                    Uav.leftward()
                else:
                    flag1=0
            #else:
                #print('出大问题')
                #flag_big_problem = 1
            if flag1 == 0 :
                dir += 1
                print('被调用了哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈哈')





for i in range(3):
    Update(UavGroup[i])
for i in range(3):
    DivideM[UavGroup[i].x_position][UavGroup[i].y_position][3]='1'
for i in range(3000):
    for j in range(30):
        for k in range(30):
            if(DivideM[j][k][3]=='3'):
                flag=1
    if(flag==1):
        for n in range(3):
            Cover(UavGroup[n])
            UavGroup[n].change()
            Update(UavGroup[n])
            #DivideM[]
            ChangeArea()
        for m in range(3):
            DivideM[UavGroup[m].x_position][UavGroup[m].y_position][3]='1'
        chessboardTemp=[]
        for p in range(30):
            fileLine = []
            for o in range(30):
                fileLine += DivideM[p][o][3]
                fileLine = ''.join(fileLine)
            chessboardTemp.append(fileLine)
        chessboardTemp1 = []
        for q in range(3):
            fileLine = []
            for w in range(3):
                fileLine += Area[q][w][2]
                fileLine = ''.join(fileLine)
            chessboardTemp1.append(fileLine)
        print('我是第', i, '次的图')
        for z in range(30):
            print(chessboardTemp[z])
        print('\n')
        for x in range(3):
            print(chessboardTemp1[x])
        print('\n')
        print(DivideM)
        flag=0
    else:
        break


