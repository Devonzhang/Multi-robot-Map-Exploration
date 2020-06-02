import numpy as np
import random

'''
Map是大地图矩阵

          Map[9][7][8]表示子区域9上坐标为(7,8)的栅格的所有信息
          Map[9][7][8][0]表示栅格的全局坐标
          Map[9][7][8][1]表示栅格在子区域中的序号
          Map[9][7][8][2]表示栅格属于的子区域序号
          Map[9][7][8][3]='0' or '1' or '2' or '3'  表示机器人可以得知的栅格状态为 未探索、探索过的可达栅格、障碍栅格、边界栅格
          Map[9][7][8][4]=0 or 1 表示地图默认信息 可达、有障碍

Area是子区域矩阵

          Area[0][0][1]=m   表示Area中0行0列元素第1项是第m个子区域
          Area[0][0][2]='0' or '1' or '2'   表示第m个子区域的未探索，正在被探索，已被探索

'''

# 地图大小全局定义
Map_Size = 100


# A*算法，返回最近的路
def AStar_Search(Uav, Robot_Destination):
    road = 0

    return road


# 计算距离机器人最近的边界栅格
def Get_Nearest_Border_Grid(Uav, Map):
    Grid_Position = [-1, -1]
    # 这中间写计算算法计算出位置传给Grid_Position
    Uav_Position = Uav.location
    flag = 0
    while flag == 0:
        # 每次检索的格子大小用n决定
        n = 1
        # i表示x
        for i in range(Get_Smaller(0, Uav_Position[0] - n), Get_Bigger(Map_Size, Uav_Position[0] + n + 1)):
            # j表示y
            for j in range(Get_Smaller(0, Uav_Position[1] - n), Get_Bigger(Map_Size, Uav_Position[1] + n + 1)):
                if Map[Uav.NoSubArea][i][j][3] == '3':
                    Grid_Position[0] = i
                    Grid_Position[1] = j
                    flag = 1
        if (Uav_Position[0] + n + 1) > Map_Size and (Uav_Position[1] + n + 1) > Map_Size:
            flag = -1

        # 没找到，扩大搜索范围
        n += 1

        # 求了个寂寞
    if flag == -1:
        print('搜索完毕全部覆盖')
        return 0
    # 求到了
    else:
        return Grid_Position


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
    Robot_Destination = Get_Nearest_Border_Grid(Uav.SubArea, Map)
    if Robot_Destination == 0:
        print('无最近边界栅格，地图已被探索完毕')
        return 0
    else:
        Robot_Road = AStar_Search(Uav.SubArea, Robot_Destination)
        return Get_Direction(Uav.SubArea, Robot_Road[0])


# 求个体最优的方向
def Get_Direction(Uav, AStar_Road_No1):
    Direction = -1
    # 先判断东西(左右)
    if Uav.SubArea[0] != AStar_Road_No1[0]:
        if Uav.SubArea[0] > AStar_Road_No1[0]:
            # 机器人x坐标比格子x坐标大，格子在机器人左侧（西方）
            Direction = 3
        else:
            # 否则格子在机器人右侧（东方）
            Direction = 1
    elif Uav.SubArea[1] != AStar_Road_No1[1]:
        if Uav.SubArea[1] > AStar_Road_No1[1]:
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

    # 北面
    for i in range(0, Uav.SubArea[1]):

        if Area[Uav.SubArea[0]][i][2] == '1':
            Direction_Robot_num[0] += 1
        elif Area[Uav.SubArea[0]][i][2] == '2':
            Direction_Robot_num[0] += Searched_Score

    # 南面
    for i in range(Uav.SubArea[1] + 1, 4):
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
    for i in range(Uav.SubArea[0] + 1, 4):
        if Area[i][Uav.SubArea[0]][2] == '1':
            Direction_Robot_num[3] += 1
        elif Area[i][Uav.SubArea[0]][2] == '2':
            Direction_Robot_num[0] += Searched_Score

    return Direction_Robot_num.index(min(Direction_Robot_num))


# 粒子群算法
# Uav是一个机器人，Map是大地图矩阵，Area是子区域矩阵
def PSO_choose(Uav, Map, Area):
    # 对个体最优的加权
    c1 = 1
    # 对全局最优的加权
    c2 = 1
    # 随机算子加权
    c3 = 0.5
    # 计算个体最优以及全局最优
    Personal_Best = Get_Personal_Best_Grid(Uav, Map)
    Overall_Best = Get_Least_Robot_Direction(Uav, Area)
    Random_Direction = random.randint(0, 3)

    # 判断方向
    Direction = round((Personal_Best * c1 + Overall_Best * c2 + Random_Direction * c3) / 3)

    return Direction
