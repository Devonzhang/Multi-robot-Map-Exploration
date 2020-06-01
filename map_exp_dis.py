import pygame, sys, random
from pygame.locals import *
import sys
import pygame

# 定义颜色
pinkColor = pygame.Color(255, 182, 193)
blackColor = pygame.Color(0, 0, 0)
whiteColor = pygame.Color(255, 255, 255)


# 定义游戏结束的函数
def gameover():
    pygame.quit()
    sys.exit()


def creat_screen():
    # 初始化pygame
    pygame.init()
    # 设置窗口大小并保存在screen对象中
    screen = pygame.display.set_mode((500, 500))
    # 设置窗口的名字
    pygame.display.set_caption("My First Screen")
    # 需要不断循环来侦听事件
    while True:
        # 给屏幕填充蓝色
        screen.fill((255, 255, 255))
        # 侦听一次事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # 先退出pygame窗口，再退出程序
                pygame.quit()
                sys.exit()
        # 更新整个待显示的 Surface 对象到屏幕上
        pygame.display.flip()


def main():
    # 初始化
    pygame.init()
    # 定义一个变量来控制速度
    time_clock = pygame.time.Clock()

    # 创建窗口，定义标题
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Multi-robot Map Exploration")


#  启动入口函数
if __name__ == '__main__':
    creat_screen()
