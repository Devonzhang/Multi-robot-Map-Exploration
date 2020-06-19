import pygame
import numpy as np
from pygame.locals import *
from sys import exit
from random import randint
from GameMap import *
from MazeGenerator import *
from AStarSearch import *
from all1 import *
import time

REC_SIZE = 20
REC_WIDTH = 31  # must be odd number
REC_HEIGHT = 31  # must be odd number
BUTTON_HEIGHT = 30
BUTTON_WIDTH = 120
SCREEN_WIDTH = REC_WIDTH * REC_SIZE
SCREEN_HEIGHT = REC_HEIGHT * REC_SIZE + BUTTON_HEIGHT


class Button():
    def __init__(self, screen, type, x, y):
        self.screen = screen
        self.width = BUTTON_WIDTH
        self.height = BUTTON_HEIGHT
        self.button_color = (128, 128, 128)
        self.text_color = [(0, 255, 0), (255, 0, 0)]
        self.font = pygame.font.SysFont(None, BUTTON_HEIGHT * 2 // 3)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.topleft = (x, y)
        self.type = type
        self.init_msg()

    def init_msg(self):
        self.msg_image = self.font.render(generator_types[self.type], True, self.text_color[0], self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def click(self, game):
        game.maze_type = self.type
        self.msg_image = self.font.render(generator_types[self.type], True, self.text_color[1], self.button_color)

    def unclick(self):
        self.msg_image = self.font.render(generator_types[self.type], True, self.text_color[0], self.button_color)


def distance(uav, dir):
    return abs(uav[0] - dir[0]) + abs(uav[1] - dir[1])


def move(map, uavx, uavy, dirx, diry):
    map.setMap(uavx, uavy, MAP_ENTRY_TYPE.MAP_EMPTY)
    map.setMap(dirx, diry, MAP_ENTRY_TYPE.MAP_TARGET)


def updatemap(map, uav0, uav1, uav2, uav3):
    for i in range(1, map.width - 1):
        for j in range(1, map.height - 1):
            # print(i, j)
            if map.map[i][j] == 4:
                if (map.map[i - 1][j] == 0 or map.map[i - 1][j] == 2 or map.map[i + 1][j] == 0 or map.map[i + 1][
                    j] == 2 or map.map[i][j - 1] == 0 or map.map[i][j - 1] == 2 or map.map[i][j + 1] == 0 or map.map[i][
                    j + 1] == 2):
                    map.setMap(j, i, MAP_ENTRY_TYPE.MAP_BORDER)
            if map.map[i][j] == 2:
                if (i, j) != uav0 and (i, j) != uav1 and (i, j) != uav2 and (i, j) != uav3:
                    map.setMap(j, i, MAP_ENTRY_TYPE.MAP_EMPTY)


class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.clock = pygame.time.Clock()
        self.map = Map(REC_WIDTH, REC_HEIGHT)
        self.mode = 0
        self.maze_type = MAZE_GENERATOR_TYPE.RANDOM_PRIM
        self.buttons = []
        self.buttons.append(Button(self.screen, MAZE_GENERATOR_TYPE.RECURSIVE_BACKTRACKER, 0, 0))
        self.buttons.append(Button(self.screen, MAZE_GENERATOR_TYPE.RANDOM_PRIM, BUTTON_WIDTH + 10, 0))
        self.buttons.append(Button(self.screen, MAZE_GENERATOR_TYPE.RECURSIVE_DIVISION, (BUTTON_WIDTH + 10) * 2, 0))
        self.buttons.append(Button(self.screen, MAZE_GENERATOR_TYPE.UNION_FIND_SET, (BUTTON_WIDTH + 10) * 3, 0))
        self.buttons[0].click(self)

    def play(self):
        self.clock.tick(30)

        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(0, 0, SCREEN_WIDTH, BUTTON_HEIGHT))
        for button in self.buttons:
            button.draw()

        for y in range(self.map.height):
            for x in range(self.map.width):
                type = self.map.getType(x, y)
                if type == MAP_ENTRY_TYPE.MAP_EMPTY:
                    color = (255, 255, 255)
                elif type == MAP_ENTRY_TYPE.MAP_BLOCK:
                    color = (0, 0, 0)
                elif type == MAP_ENTRY_TYPE.MAP_TARGET:
                    color = (255, 0, 0)
                elif type == MAP_ENTRY_TYPE.MAP_PATH:
                    color = (0, 255, 0)
                elif type == MAP_ENTRY_TYPE.MAP_UNKNOW:
                    color = (0, 0, 0)
                elif type == MAP_ENTRY_TYPE.MAP_BORDER:
                    color = (0, 255, 255)
                pygame.draw.rect(self.screen, color,
                                 pygame.Rect(REC_SIZE * x, REC_SIZE * y + BUTTON_HEIGHT, REC_SIZE, REC_SIZE))

    def generateMaze(self):
        if self.mode >= 4:
            self.mode = 0
        if self.mode == 0:
            generateMap(self.map, self.maze_type)
        elif self.mode == 1:
            self.source = ((1, 1), (1, 2), (2, 1), (2, 2))
            for i in range(len(self.source)):
                self.map.setMap(self.source[i][1], self.source[i][0], MAP_ENTRY_TYPE.MAP_TARGET)
            updatemap(self.map, (1, 1), (1, 2), (2, 1), (2, 2))
        elif self.mode == 2:
            for i in range(3):
                Update(UavGroup[i])                                             #先更新地图，用于无人机后续运动
            for i in range(3):
                DivideM[UavGroup[i].x_position][UavGroup[i].y_position][3] = '1'
            for i in range(3000):
                game.play()
                pygame.display.update()
                for j in range(30):
                    for k in range(30):
                        if (DivideM[j][k][3] == '3'):
                            flag = 1
                if (flag == 1):
                    for m in range(3):                                              #开始探索前，将无人机所在栅格的状态定义为2
                        DivideM[UavGroup[m].x_position][UavGroup[m].y_position][3] = '2'
                    for n in range(3):                                              #对于每一个无人机调用以下代码
                        Cover(UavGroup[n])                                      #调用无人机运动函数
                        Update(UavGroup[n])                                      #更新地图状态
                        UavGroup[n].change()                                      #更新无人机所在子区域的坐标
                        ChangeArea()                                            #更新子区域状态
                        zflag=0
                        for zx in range(3):                                         #当所有的子区域状态都为2则已经探索完，跳出循环，防止其他无人机继续探索
                            for zy in range(3):
                                if (Area[zx][zy][2]!='2'):
                                    zflag=1
                        if(zflag==0):
                            break

                        UavGroup[n].change()
                    for m in range(3):                                              #三个无人机都探索完一轮后，将无人机所在栅格的状态定义为1，在地图显示时不会多显示障碍栅格
                        DivideM[UavGroup[m].x_position][UavGroup[m].y_position][3] = '1'
                    chessboardTemp = []
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
                    for zr in range(30):
                        for zl in range(30):
                            if chessboardTemp[zr][zl] == '0':
                                self.map.map[zr][zl] = 4
                                #self.map.setMap(zr, zl, MAP_ENTRY_TYPE.MAP_UNKNOW)
                            if chessboardTemp[zr][zl] == '1':
                                self.map.map[zr][zl] = 3
                                #self.map.setMap(zr, zl, MAP_ENTRY_TYPE.MAP_PATH)
                            if chessboardTemp[zr][zl] == '2':
                                self.map.map[zr][zl] = 1
                                #self.map.setMap(zr, zl, MAP_ENTRY_TYPE.MAP_BLOCK)
                            if chessboardTemp[zr][zl] == '3':
                                self.map.map[zr][zl] = 5
                                #self.map.setMap(zr, zl, MAP_ENTRY_TYPE.MAP_BORDER)
                    for m in range(3):
                        self.map.map[UavGroup[m].x_position][UavGroup[m].y_position] = 2
                    for z in range(30):
                        print(chessboardTemp[z])
                    pygame.display.update()
                    print('\n')
                    for x in range(3):
                        print(chessboardTemp1[x])
                    print('\n')
                    print(DivideM)
                    flag = 0
                else:
                    break
        else:
            self.map.resetMap(MAP_ENTRY_TYPE.MAP_EMPTY)
        self.mode += 1





def check_buttons(game, mouse_x, mouse_y):
    for button in game.buttons:
        if button.rect.collidepoint(mouse_x, mouse_y):
            button.click(game)
            for tmp in game.buttons:
                if tmp != button:
                    tmp.unclick()
            break


game = Game()
#for i in range(9):
	#Mapx.append(Divide(i))
while True:
	game.play()
	pygame.display.update()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		if event.type == pygame.KEYDOWN:
			game.generateMaze()
			break
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_buttons(game, mouse_x, mouse_y)
