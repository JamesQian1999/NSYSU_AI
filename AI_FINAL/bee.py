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
GREEN = ( 34, 139,  34)     # green
STEP = 8                    # steps per round
DETECT_FLOWER = 150         # detected flower
CONFORM = 10                # conform zoom
bee_map = np.zeros((800, 600, 3), dtype=np.int) # stamp/dir/time
EIGHT_RANGE = 20
STAMP_RANGE = 8*EIGHT_RANGE
TIME = 8*EIGHT_RANGE
STAMP = 8*EIGHT_RANGE

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
        self.collection = 0

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
    def __init__(self, x=5, y=5,strategy =-1,go_eight_flag=False ,blood = 48):
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
        self.stamp = 0
        self.go_eight_flag = go_eight_flag
        self.go_eight = 8*EIGHT_RANGE


def init():
    global bee_list, flower_list, home
    bee_list.append(Bee(80, 150, 1,go_eight_flag=True))
    bee_list.append(Bee(240, 150,go_eight_flag=True))
    bee_list.append(Bee(400, 150, 1,go_eight_flag=True))
    bee_list.append(Bee(560, 150,go_eight_flag=True))
    bee_list.append(Bee(720, 150, 1,go_eight_flag=True))
    bee_list.append(Bee(80, 450,go_eight_flag=True))
    bee_list.append(Bee(240, 450, 1,go_eight_flag=True))
    bee_list.append(Bee(400, 450,go_eight_flag=True))
    bee_list.append(Bee(560, 450, 1,go_eight_flag=True))
    bee_list.append(Bee(720, 450,go_eight_flag=True))
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
            home.collection += 1
            if home.collection >= 5:
                x = random.randrange(100,700)
                y = random.randrange(100,500)
                s = random.randrange(0,2)
                e = random.randrange(0,2)
                bee_list.append(Bee(x, y,strategy=s,go_eight_flag=e))
                home.collection = 0
    else:
        if bee_list[index].found_flower and bee_list[index].flower[0]-CONFORM < bee_list[index].x < bee_list[index].flower[0]+CONFORM and bee_list[index].flower[1]-CONFORM < bee_list[index].y < bee_list[index].flower[1]+CONFORM:
            found = -1
            for i in range(0,len(flower_list)):
                if flower_list[i].x == bee_list[index].flower[0] and flower_list[i].y == bee_list[index].flower[1]:
                    found = i
                    break
            if found >= 0:
                if bee_list[index].go_eight_flag: bee_list[index].go_eight = 8*EIGHT_RANGE
                bee_map[bee_list[index].x,bee_list[index].y,0] = STAMP_RANGE
                bee_map[bee_list[index].x,bee_list[index].y,2] = TIME
                bee_list[index].stamp = STAMP
                bee_list[index].blood += 20
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
    
    if bee_list[i].go_eight_flag and bee_list[i].stamp and bee_list[i].go_eight > 0 and bee_list[i].with_flower:
        eight(bee_list[i])
        return

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

def check(x,y):
    if x > 799:
        x = 799
    if y > 599:
        y = 599
    if x < 0:
        x = 0
    if y < 0:
        y = 0
    return x,y

def eight(bee):
    x = bee.x
    y = bee.y
    r = EIGHT_RANGE
    if 7*r < bee.go_eight <= 8*r:       # /
        #print("/")
        x -= STEP
        y += STEP
    elif 5*r < bee.go_eight <= 7*r:     # |
        #print("|")
        y -= STEP
    elif 3*r < bee.go_eight <= 5*r:      # \
        #print("\\")
        x += STEP
        y += STEP
    elif r < bee.go_eight <= 3*r:       # |
        #print("|")
        y -= STEP
    else:                               # /
        #print("/")
        x -= STEP                            
        y += STEP

    x,y = check(x,y)
    bee.x = x
    bee.y = y
    bee.rect.topleft = (x, y)
    bee.stamp -= 1
    bee_map[x, y,0] = bee.stamp
    bee_map[x, y,1] = 6
    bee_map[x, y,2] = TIME
    bee.go_eight -= 1
    #print(bee.go_eight)

def walk(bee, p , s = 0): 
    x = bee.x
    y = bee.y
    if p == 2:
        #print("p = 2 ~~~~~~~~~~~")
        pos = [5,6,7,8][random.randrange(0, len([5,6,7,8]), 1)]
    elif p == 1:
        #print("p = 1 ~~~~~")
        pos = [1, 2, 3, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8][random.randrange(0, len([1, 2, 3, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8]), 1)]
    else:
        #print("p = 0 ~")
        pos = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 6, 7, 8][random.randrange(0, len([1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 6, 7, 8]), 1)]

    if bee.pre_count != 5 and bee.pre_count != -1:
        pos = bee.pre_dir
        bee.pre_count += 1
    else :
        bee.pre_dir = pos
        bee.pre_count = 0

    if s == 1 and bee_map[bee.x,bee.y,0] and bee_map[bee.x,bee.y,2]>0:
        #print("bee_map")
        pos = 9 - bee_map[bee.x,bee.y,1]

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

    x,y = check(x,y)

    # renew ant object
    bee.x = x
    bee.y = y
    bee.rect.topleft = (x, y)
    if bee.stamp:
        bee.stamp -= 1
        bee_map[x,y,0] = bee.stamp
        bee_map[x,y,1] = pos
        bee_map[x,y,2] = TIME



pg.init()
window_surface = pg.display.set_mode((800, 600))  # load window surface
pg.display.set_caption('AI') # window name
my_font = pg.font.SysFont(None, 30) 
init()

count = 0
main_clock = pg.time.Clock()
while True:
    # print("")
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
        #print("bee[%d]"%i)
        bee_map[:,:,2] -= 1
        found_flower()

        if bee_list[i].with_flower or bee_list[i].found_flower:
            go_specific_place(i)
        elif bee_list[i].strategy == 1:
            walk(bee_list[i],p=random.randrange(0,2),s=1)
        else:
            if bee_list[i].get_out:
                walk(bee_list[i],p=2)
                bee_list[i].get_out -= 1
            else:
                walk(bee_list[i],p=random.randrange(0,2))
    
        window_surface.blit(bee_list[i].image, bee_list[i].rect)
        pg.draw.rect(window_surface, GREEN, pg.Rect(bee_list[i].x-4,bee_list[i].y-5,48,5),1) 
        pg.draw.rect(window_surface, GREEN, pg.Rect(bee_list[i].x-4,bee_list[i].y-5,bee_list[i].blood,5))
        
        if bee_list[i].blood<=12: bee_list[i].strategy = 1

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
            x = random.randrange(100,700)
            y = random.randrange(100,500)
            flower_list.append(Flower(x, y))
            i -= 1 
        i += 1

    pg.display.flip() 

    # print home
    window_surface.blit(home.image, home.rect)

    
    count += 1
    pg.display.update()
    # 控制遊戲迴圈迭代速率
    main_clock.tick(FPS)