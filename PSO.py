import numpy as np
import random


# A*算法，返回最近的路
def AStar_Search(Robot_Position, Robot_Destination):
    road = 0

    return road


# 计算距离机器人最近的边界栅格
def Get_Nearest_Border_Grid(Robot_Position, Map):
    Grid_Position = [-1, -1]
    # 这中间写计算算法计算出位置传给Grid_Position

    # 求了个寂寞
    if Grid_Position == [-1, -1]:
        return 0
    # 求到了
    else:
        return Grid_Position


# 计算个体历史最优--邻居栅格里面在A*算法求出的去最近的边界栅格的路上的四个栅格中的一个
def Get_Personal_Best_Grid(Robot_Position, Map):
    Robot_Destination = Get_Nearest_Border_Grid(Robot_Position, Map)
    Robot_Road = AStar_Search(Robot_Position, Robot_Destination)

    return Get_Direction(Robot_Position, Robot_Road[0])


# 求个体最优的方向
def Get_Direction(Robot_Position, AStar_Road_No1):
    Direction = -1
    # 先判断东西(左右)
    if Robot_Position[0] != AStar_Road_No1[0]:
        if Robot_Position[0] > AStar_Road_No1[0]:
            # 机器人x坐标比格子x坐标大，格子在机器人左侧（西方）
            Direction = 3
        else:
            # 否则格子在机器人右侧（东方）
            Direction = 1
    elif Robot_Position[1] != AStar_Road_No1[1]:
        if Robot_Position[1] > AStar_Road_No1[1]:
            # 机器人y坐标比格子y坐标大，格子在机器人下面（南方）
            Direction = 2
        else:
            # 否则在上面（北方）
            Direction = 0

    return Direction


# 求全局最优--机器人数量最少方向
def Get_Least_Robot_Direction(Robot_Position, Map):
    # 每个方向上面机器人数量，初始为0，顺序为北(上)、东(右)、南(下)、西(左)
    Direction_Robot_num = [0, 0, 0, 0]
    # 下面循环部分需要改，看给的地图数据结构
    for North_Son_Area in Map:
        if North_Son_Area.isRobot == 1:
            Direction_Robot_num[0] += 1
    for South_Son_Area in Map:
        if South_Son_Area.isRobot == 1:
            Direction_Robot_num[1] += 1

    for East_Son_Area in Map:
        if East_Son_Area.isRobot == 1:
            Direction_Robot_num[2] += 1

    for West_Son_Area in Map:
        if West_Son_Area.isRobot == 1:
            Direction_Robot_num[3] += 1

    return Direction_Robot_num.index(min(Direction_Robot_num))


# 粒子群算法
def PSO_choose(Robot_Position, Map):
    # 对个体最优的加权
    c1 = 1
    # 对全局最优的加权
    c2 = 1
    # 随机算子加权
    c3 = 0.5
    # 计算个体最优以及全局最优
    Personal_Best = Get_Personal_Best_Grid(Robot_Position, Map)
    Overall_Best = Get_Least_Robot_Direction(Robot_Position, Map)
    Random_Direction = random.randint(0, 3)

    # 判断方向
    Direction = round((Personal_Best * c1 + Overall_Best * c2 + Random_Direction * c3) / 3)

    return Direction
