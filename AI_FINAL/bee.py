# Student ID: B073021024
import pygame as pg
import numpy as np
import random
from pygame.locals import QUIT
import sys


FPS = 30                    # update rate
bee_list=[]                 # number
flower_list=[]              # flower   
WHITE = (255, 255, 255)     # white
GREEN = (34,139,34)         # green
STEP = 8                    # steps per round
DETECT_FLOWER = 100         # detected flower
CONFORM = 10                # conform zoom

# creat home object
class Home(pg.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()
        self.x = x
        self.y = y
        self.raw_image = pg.image.load('/home/jamesqian/Documents/AI/AI_FINAL/home.png').convert_alpha()
        self.image = pg.transform.scale(self.raw_image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# creat flower object
class Flower(pg.sprite.Sprite):
    def __init__(self, x, y, take = 3):
        super().__init__()
        self.x = x
        self.y = y
        self.raw_image = pg.image.load('/home/jamesqian/Documents/AI/AI_FINAL/flower.png').convert_alpha()
        self.image = pg.transform.scale(self.raw_image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.take = take

# creat Bee object
class Bee(pg.sprite.Sprite):
    def __init__(self, x=5, y=5,strategy =-1, time=10,blood = 48):
        super().__init__()
        self.x = x
        self.y = y
        self.raw_image = pg.image.load('/home/jamesqian/Documents/AI/AI_FINAL/bee.png').convert_alpha()
        self.image = pg.transform.scale(self.raw_image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.blood = blood 
        self.pre_dir = -1
        self.pre_count = 0
        self.strategy = strategy
        self.with_flower = False
        self.found_flower = False
        self.flower = [-1,-1]
        self.get_out = 0


def init():
    global bee_list, flower_list, home
    bee_list.append(Bee(80, 150,))
    bee_list.append(Bee(240, 150))
    bee_list.append(Bee(400, 150))
    bee_list.append(Bee(560, 150))
    bee_list.append(Bee(720, 150))
    bee_list.append(Bee(80, 450))
    bee_list.append(Bee(240, 450))
    bee_list.append(Bee(400, 450))
    bee_list.append(Bee(560, 450))
    bee_list.append(Bee(720, 450))
    tmp = random.randrange(0, len(bee_list), 1)
    x = max(bee_list[tmp].x-DETECT_FLOWER+2, 0)
    y = max(bee_list[tmp].y-DETECT_FLOWER+2, 0)
    flower_list.append(Flower(x, y))  # set initial flower position
    tmp = random.randrange(0, len(bee_list), 1)
    x = max(bee_list[tmp].x-DETECT_FLOWER+2, 0)
    y = max(bee_list[tmp].y-DETECT_FLOWER+2, 0)
    flower_list.append(Flower(x, y))  # set initial flower position
    home = Home()  # set home position

def found_flower():
    for i in range(0,len(flower_list)):
        for j in range(0,len(bee_list)):
            if not bee_list[j].with_flower and bee_list[j].x < flower_list[i].x+DETECT_FLOWER and bee_list[j].x > flower_list[i].x-DETECT_FLOWER and bee_list[j].y < flower_list[i].y+DETECT_FLOWER and bee_list[j].y > flower_list[i].y-DETECT_FLOWER:
                bee_list[j].found_flower = True
                bee_list[j].flower = [flower_list[i].x,flower_list[i].y]


def conform(index,gohome):
    if gohome: 
        if -1*CONFORM < bee_list[index].x < CONFORM and -1*CONFORM < bee_list[index].y < CONFORM:
            bee_list[index].raw_image = pg.image.load('/home/jamesqian/Documents/AI/AI_FINAL/bee.png').convert_alpha()
            bee_list[index].image = pg.transform.scale(bee_list[index].raw_image, (42, 42))
            bee_list[index].blood = 48
            bee_list[index].with_flower = False
            bee_list[index].found_flower = False
            bee_list[index].flower = [-1,-1]
            bee_list[index].get_out = 5
    else:
        if bee_list[index].found_flower and bee_list[index].flower[0]-CONFORM < bee_list[index].x < bee_list[index].flower[0]+CONFORM and bee_list[index].flower[1]-CONFORM < bee_list[index].y < bee_list[index].flower[1]+CONFORM:
            found = -1
            for i in range(0,len(flower_list)):
                if flower_list[i].x == bee_list[index].flower[0] and flower_list[i].y == bee_list[index].flower[1]:
                    found = i
                    break
            if found >= 0:
                bee_list[index].blood += 10
                bee_list[index].with_flower = True
                bee_list[index].found_flower = False
                bee_list[index].flower = [-1,-1]
                flower_list[found].take -= 1
                # change ant image
                bee_list[index].raw_image = pg.image.load('/home/jamesqian/Documents/AI/AI_FINAL/bee_with_flower.png').convert_alpha()
                bee_list[index].image = pg.transform.scale(bee_list[index].raw_image, (42, 42))
            else:
                bee_list[index].found_flower = False
                bee_list[index].flower = [-1,-1]


def go_specific_place(i,dir=1):
    if bee_list[i].found_flower:
        goto_there = bee_list[i].flower
        gohome = False
    elif bee_list[i].with_flower:
        goto_there = [0,0]
        gohome = True
    
    dir = random.randrange(0,3)
    x_pn = np.sign(goto_there[0] - bee_list[i].x)
    y_pn = np.sign(goto_there[1] - bee_list[i].y)
    if goto_there[0]-bee_list[i].x == 0:
         dir = 1
    if goto_there[1]-bee_list[i].y == 0:
         dir = 0
    if dir ==0:
        bee_list[i].x = bee_list[i].x + STEP*x_pn
        bee_list[i].rect.topleft = (bee_list[i].x, bee_list[i].y)
    elif dir ==1:
        bee_list[i].y = bee_list[i].y + STEP*y_pn
        bee_list[i].rect.topleft = (bee_list[i].x, bee_list[i].y)
    else :
        bee_list[i].x = bee_list[i].x + STEP*x_pn
        bee_list[i].y = bee_list[i].y + STEP*y_pn
        bee_list[i].rect.topleft = (bee_list[i].x, bee_list[i].y)


    conform(i,gohome)
    
    



def walk(bee, p): 
    x = bee.x
    y = bee.y
    if p == 1:
        pos = [1, 2, 3, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8][random.randrange(0, len([1, 2, 3, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8]), 1)]
    else:
        pos = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 6, 7, 8][random.randrange(0, len([1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 6, 7, 8]), 1)]

    if bee.pre_count != 5 and bee.pre_count != -1:
        pos = bee.pre_dir
        bee.pre_count += 1
    else :
        bee.pre_dir = pos
        bee.pre_count = 0

    if pos == 1:
        x -= STEP
        y -= STEP
    elif pos == 2:
        y -= STEP
    elif pos == 3:
        x += STEP
        y -= STEP
    elif pos == 4:
        x -= STEP
    elif pos == 5:
        x += STEP
    elif pos == 6:
        x -= STEP
        y += STEP
    elif pos == 7:
        y += STEP
    else:
        x += STEP
        y += STEP

    if x > 799:
        x = 799
    if y > 599:
        y = 599
    if x < 0:
        x = 0
    if y < 0:
        y = 0

    # renew ant object
    bee.x = x
    bee.y = y
    bee.rect.topleft = (x, y)



pg.init()
window_surface = pg.display.set_mode((800, 600))  # load window surface
pg.display.set_caption('AI') # window name
my_font = pg.font.SysFont(None, 30) 
init()

count = 0
main_clock = pg.time.Clock()
while True:
    global food
    # 偵測事件
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()

    # set background to white
    window_surface.fill(WHITE)

    #print bees and lift bars
    A_second = False
    if not count%10: A_second = True

    i = 0
    while True:
        if i > len(bee_list)-1 or i < 0: break

        found_flower()

        if bee_list[i].with_flower or bee_list[i].found_flower:
            go_specific_place(i)
        elif bee_list[i].strategy == 1:
            pass
        elif bee_list[i].strategy == 2:
            pass
        elif bee_list[i].strategy == 3:
            pass
        else:
            if bee_list[i].get_out:
                walk(bee_list[i],1)
                bee_list[i].get_out -= 1
            else:
                walk(bee_list[i],random.randrange(0,2))
    
        window_surface.blit(bee_list[i].image, bee_list[i].rect)
        pg.draw.rect(window_surface, GREEN, pg.Rect(bee_list[i].x-4,bee_list[i].y-5,48,5),1) 
        pg.draw.rect(window_surface, GREEN, pg.Rect(bee_list[i].x-4,bee_list[i].y-5,bee_list[i].blood,5))

        if A_second: bee_list[i].blood -= 1
        if not bee_list[i].blood:
            bee_list.pop(i)
            i -= 1 
        i += 1

    i = 0
    while True:
        if  i > len(flower_list)-1 or i < 0: break
    
        window_surface.blit(flower_list[i].image, flower_list[i].rect)
        if flower_list[i].take <= 0:
            flower_list.pop(i)
            i -= 1 
        i += 1

    pg.display.flip() 

    # print home
    window_surface.blit(home.image, home.rect)

    
    count += 1
    pg.display.update()
    # 控制遊戲迴圈迭代速率
    main_clock.tick(FPS)