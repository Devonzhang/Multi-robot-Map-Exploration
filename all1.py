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
chessboard=[]
lv=0


item = [[0, 0], 0, 0]
Area = []  # 完成  子区域生成
i = 0
itemline = []
a = 20
Grid = []
while i < 3:                                        #生成子区域并将其状态定义为'0'，表示未探索
    j = 0
    while j < 3:
        item = [[0, 0], i * 3 + j, 0]
        item[2]='0'
        itemline.append(copy.deepcopy(item))
        j += 1
    Area.append(copy.deepcopy(itemline))
    itemline = []
    i += 1

def DivideMap():  # 完成      大地图分割               将地图分解成很多的小栅格，这些栅格位于子区域中
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

    for i in range(g):                                             #对栅格的状态进行初始化，将最边缘的栅格定义为边界栅格，将其余的栅格状态定义为'0',表示未被探索
        for j in range(g):
            Grid[i][j][0][0] = Grid[i][j][0][0] + (i + 1)
            Grid[i][j][0][1] = Grid[i][j][0][1] + (j + 1)

            Grid[i][j][3] = '0'  # 可过节点的标号
            Grid[i][j][4]='0'
            if((i==0)|(j==0)|(i==29)|(j==29)):
                Grid[i][j][3] = '2'

    return Grid

DivideM = DivideMap()  # 全局总地图         #调用地图分割函数，生成地图
print(DivideM)
DivideM[3][4][4]='1'                           #生成一些障碍
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


class Uav():  # 完成   机器人类               定义无人机所在的栅格坐标和所在的子区域坐标，并定义无人机的运动和其所在子区域坐标的更新函数
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


UavGroup = []  # 完成   机器人群组生成                 生成无人机群组，并给其分配栅格坐标作为其位置
for i in range(4):
    uav = Uav(5*i+1,5*i+1)
    UavGroup.append(uav)

def Update(Uav):     # 更新地图算法，如果无人机周围的四个栅格中其隐式状态不为障碍，则将其定义为边界栅格。将周围的四个栅格中不为探索过栅格和障碍栅格的定义为边界栅格
    global DivideM

    DivideM[UavGroup[m].x_position][UavGroup[m].y_position][3] = '2'       #在主函数里先令每个无人机所在栅格为障碍栅格，当到了该无人机运动的时候，先将其所在栅格定义为已探索栅格，然后运动，再将新到达的栅格定义为障碍栅格
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




def find(MAP,Uav):           #探索地图算法           找到无人机在地图中的最邻近栅格
    chessboardTemp = []
    for p in range(30):
        fileLine = []
        for o in range(30):
            fileLine += MAP[p][o][3]
            fileLine = ''.join(fileLine)
        chessboardTemp.append(fileLine)
    for z in range(30):
        print(chessboardTemp[z])
    minpoint=[]
    ax=0
    bx=0
    min=100000                 #定义一个较大的距离后面会很快的修改
    for i in range(30):
        for j in range(30):
            if (MAP[i][j][3]=='3'):
                distance=abs(Uav.x_position-MAP[i][j][0][0])+abs(Uav.y_position-MAP[i][j][0][1])
                if(distance<=min):
                    ax = i
                    bx = j
                    min=distance
    minpoint.append(ax)
    minpoint.append(bx)
    return minpoint

'''对子区域的状态进行改变，如果其中不存在边界栅格而且不存在未探索栅格，
则将其定义为已探索子区域。如果其中存在已探索栅格和边界栅格，则将其定义为正在探索子区域。
如果其中不存在已探索栅格，则将其定义为未探索子区域。
'''
def ChangeArea():
    global Area
    global DivideM
    for m in range(3):
        for n in range(3):
            flag1=0                 #未探索栅格
            flag2=0                 #边界栅格
            flag3=0                 #已探索栅格
            for j in range(10):
                for l in range(10):

                    if(DivideM[m*10+j][n*10+l][3]=='0'):        #如果存在未探索栅格则flag1=1
                        flag1=1
                    if(DivideM[m*10+j][n*10+l][3] == '3'):     #如果存在边界栅格则flag2=1
                        flag2 = 1
                    if(DivideM[m*10+j][n*10+l][3] == '1'):     #如果存在已探索栅格则flag3=1
                        flag3 = 1
            if ((flag1==0)&(flag2==0)):                                     #已探索子区域
                Area[m][n][2]='2'
            if ((flag2==1)&(flag3==1)):                                     #正在探索子区域
                Area[m][n][2]='1'
            if (flag3 == 0):                                                  #未被探索子区域
                Area[m][n][2] ='0'

        print('\n')



def A(map):         #A*算法  输入为一个起点为s终点为e的图 返回一条起点到终点的路径
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





def Cover(Uav):                                                               #完成      覆盖算法，核心，机器人的运动全部都在这个算法中
    global Area
    global p
    global DivideM
    DivideM[UavGroup[m].x_position][UavGroup[m].y_position][3] = '1'    #在主函数里先令每个无人机所在栅格为障碍栅格，当到了该无人机运动的时候，先将其所在栅格定义为已探索栅格，然后运动，再将新到达的栅格定义为障碍栅格
    ChangeArea()
    Uav.change()
    if (Area[Uav.x_location][Uav.y_location][2] != '2'):            #如果机器人所在子区域不为已探索子区域的话，执行的是覆盖过程，只允许无人机在子区域内搜索
        if ((DivideM[Uav.x_position][Uav.y_position+1][3]=='3')&((Uav.y_position+1)<((Uav.y_location+1)*10))):                #如果上边是边界栅格且未超过子区域的边界，则无人机向上走
            Uav.upward()
        elif((DivideM[Uav.x_position+1][Uav.y_position][3]=='3')&((Uav.x_position + 1) < ( (Uav.x_location+1)*10))):       #如果右边是边界栅格且未超过子区域的边界，则无人机向右走
            Uav.rightward()
        elif((DivideM[Uav.x_position -1][Uav.y_position][3] == '3')&((Uav.x_position - 1) > (((Uav.x_location)*10)-1))):    #如果左边是边界栅格且未超过子区域的边界，则无人机向左走
            Uav.leftward()
        elif((DivideM[Uav.x_position][Uav.y_position-1][3] == '3')&((Uav.y_position - 1) > ((Uav.y_location)*10)-1)):       #如果下边是边界栅格且未超过子区域的边界，则无人机向下走
            Uav.downward()

        else:         #如果无人机所在位置周围没有边界栅格的话，调用A*算法搜寻最邻近栅格
            minpoint = []
            item = [[0, 0], 0]
            min = 1000  # 定义一个较大的距离后面会很快的修改
            for i in range(30):
                for j in range(30):
                    if (DivideM[i][j][3] == '3'):
                        distance = abs((Uav.x_position - i) )+ abs((Uav.y_position -j))
                        if ((distance < min)&(int((i/10))==Uav.x_location)&(int((j/10))==Uav.y_location)):        #找到子区域中离无人机距离最近的边界栅格作为寻路的终点
                            item[0][0] = i
                            item[0][1] = j
                            item[1] = distance
                            min = distance
            minpoint.append(item[0][0])
            minpoint.append(item[0][1])


            end1=minpoint
            start=[]
            start.append(Uav.x_position)                        #将无人机的位置作为寻路的起点
            start.append(Uav.y_position)

            a=[]
            for i in range(30):
                item=[]
                for j in range(30):
                    item.append(DivideM[i][j][3])
                a.append(item)
            for i in range (30):                #将该子区域外的栅格状态全部定义为障碍栅格，防止A*找到的路径在该子区域外面  这个很重要
                for j in range(30):
                    if (((j)>((Uav.y_location+1)*10))&((i) > ( (Uav.x_location+1)*10))&((i) < (((Uav.x_location)*10)-1))&((j) < ((Uav.y_location)*10)-1)):
                        a[i][j]='2'

            a[end1[0]][end1[1]]='e'                   #对起点和终点的状态进行改变来进行后续的搜寻
            a[start[0]][start[1]]='s'
            path=A(a)                           #调用A*算法获得路径
            a[end1[0]][end1[1]] = '3'
            a[start[0]][start[1]] = '2'
            if(path!=[]):
                if (p < len(path)-1):                       #如果找到了路径，无人机的下一步所到的位置为A*寻路的下一个点
                    Uav.x_position = path[p+1][0]
                    Uav.y_position = path[p+1][1]
                    p += 1

                else:
                    p = 0
            else:
                Uav.stop()        #如果没找到路径，那就是无人机已经被卡死了，即就是周围全部都是边界栅格，以及别的无人机。那么该无人机执行stop()在原地停一次
    else:

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
            end2 = find(DivideM, Uav)                                       #找到全图中距离该无人机最近的边界栅格
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
            path2 = A(a)                                            #A*算法进行寻路
            a[end2[0]][end2[1]] = '3'
            a[start[0]][start[1]] = '2'
            Direction=Get_Direction(Uav, path2[1])

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
        def PSO_choose(Uav, Map, Area):  #PSO算法，定义三个参数C1,C2,C3,这三个参数通过比较大小，确定出最大的参数，如果C1最大，则此次的运动方向为个体最优方向，如果C2最大，则此次的运动方向为群体最优方向，若C3最大，则此次的运动方向为上次的运动方向
            global lv
            label = []
            choose=0
            # 对个体最优的加权
            c1 = 1 * random.random()                #定义C1，C2，C3三个参数，每个参数都为零到一的随机数乘一个系数，这个系数由我们规定
            # 对全局最优的加权
            c2 = 0 * random.random()
            # 随机算子加权
            c3 =0 * random.random()
            # 计算个体最优以及全局最优
            label.append(c1)
            label.append(c2)
            label.append(c3)
            print(label)
            maxDir = 0

            Personal_Best = Get_Personal_Best_Grid(Uav, Map)                        #获取个体最优方向
            Overall_Best = Get_Least_Robot_Direction(Uav, Area)                     #获得群体最优方向

            for i in range(3):
                if (label[i] > maxDir):
                    choose = i
                    maxDir = label[i]
            print('我是所选择的方向', choose)
            if (choose == 0):                                               #根据判断大小来决定此次是哪个方向发挥作用
                Direction = Personal_Best
            elif (choose == 1):
                Direction = Overall_Best
            else:
                Direction = lv
            lv=Direction
            print('我是choose',choose)
            print('这里是三个量',Personal_Best,Overall_Best,lv)
            return Direction

        dir = PSO_choose(Uav, DivideM, Area)  # 获取方向
        flag1=0                                         #定义了一个标记，如果选定了一个方向但是这个方向是障碍栅格的话，就选择下一个方向,并且flag2加一，代表转换了一次方向，转换四次后还不能运动的话，就代表周围都是障碍栅格
        flag2=0
        while flag1==0:
            if(flag2<3):
                flag1 = 1
                if dir == 4:
                    dir = 0
                if ((dir == 0) ):                                       #如果方向为向上
                    if(DivideM[Uav.x_position][Uav.y_position + 1][3] != '2'):          #方向为向上且上方不是边界栅格，那么就向上走
                        Uav.upward()
                    else:                                                               #否则令flag1为0，在下面进行方向的变化，并且继续循环，直到
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
                    flag2+=1
            else:                                                                       #若是周围方向上全部都是障碍栅格，那么就让无人机停止
                Uav.stop()

