# Student ID: B073021024
import pygame as pg
import numpy as np
import random
from pygame.locals import QUIT
import sys
import time

global ant_num,FOOD_TAKED,FOOD_MAX

FPS = 3                     # update rate
WHITE = (255, 255, 255)     # white
SEC = 5                     # rounds per second
TIME = 7                    # time
CONFORM_HOME = 10           # arrived home
DETECT_FOOD = 100           # detected food
CONFORM_FOOD = 10           # taked food
FOOD_ADD = 7                # add per 7 round
FOOD_POSSIBILITY = 5        
FOOD_TAKED = 0              # ant with food
FOOD_MAX = 6                # max number of food
FOOD = 2                    # food flag
DETECT_PHEROMONE = 70       # detected pheromone
STEP = 15                   # steps per round
count = 0                   # count rounds
ant_num = 10                # initial ant number
ant_list = []               # ants
food_list = []              # foods
ant_map = np.zeros((800, 600), dtype=np.int)  # map

random_list1 = [1, 2, 3, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8]
random_list2 = [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 6, 7, 8]

# creat home object
class Home(pg.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()
        self.x = x
        self.y = y
        self.raw_image = pg.image.load('/home/jamesqian/Documents/AI/AI_MID/home.png').convert_alpha()
        self.image = pg.transform.scale(self.raw_image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# creat food object
class Food(pg.sprite.Sprite):
    def __init__(self, x, y, time=SEC*10):
        super().__init__()
        self.x = x
        self.y = y
        self.raw_image = pg.image.load('/home/jamesqian/Documents/AI/AI_MID/food.png').convert_alpha()
        self.image = pg.transform.scale(self.raw_image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.count = 3

# creat ant object
class Ant(pg.sprite.Sprite):
    def __init__(self, x=5, y=5, time=SEC*TIME):
        super().__init__()
        self.x = x
        self.y = y
        self.raw_image = pg.image.load('/home/jamesqian/Documents/AI/AI_MID/ant.png').convert_alpha()
        self.image = pg.transform.scale(self.raw_image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.time = time
        self.go_home = False


def init():
    global ant_list, food, home, ant_map
    ant_list.append(Ant(80, 150))
    ant_list.append(Ant(240, 150))
    ant_list.append(Ant(400, 150))
    ant_list.append(Ant(560, 150))
    ant_list.append(Ant(720, 150))
    ant_list.append(Ant(80, 450))
    ant_list.append(Ant(240, 450))
    ant_list.append(Ant(400, 450))
    ant_list.append(Ant(560, 450))
    ant_list.append(Ant(720, 450))
    tmp = random.randrange(0, len(ant_list), 1)
    x = max(ant_list[tmp].x-DETECT_FOOD+2, 0)
    y = max(ant_list[tmp].y-DETECT_FOOD+2, 0)
    food_list.append(Food(x, y))  # set initial food position
    ant_map[x, y] = FOOD
    home = Home()  # set home position


def go_home(ant):
    global ant_num,FOOD_TAKED
    #print("I need go home!")
    x_pn = np.sign(home.x - ant.x)
    y_pn = np.sign(home.y - ant.y)
    dir = random.randrange(0, 2, 1)  # random choose direction (x = 0 ,y = 1)
    if dir == 0:    # x
        ant.x = ant.x + STEP*x_pn
        ant.rect.topleft = (ant.x, ant.y)
    else:           # y
        ant.y = ant.y + STEP*y_pn
        ant.rect.topleft = (ant.x, ant.y)

    #arrived home
    if -1*CONFORM_HOME < ant.x < CONFORM_HOME and -1*CONFORM_HOME < ant.y < CONFORM_HOME:
        ant_num += 1 # add ant
        ant.time = SEC*TIME # reset ant time
        ant.go_home = False # reset go_home flag
        ant.raw_image = pg.image.load('/home/jamesqian/Documents/AI/AI_MID/ant.png').convert_alpha() # reset image
        ant.image = pg.transform.scale(ant.raw_image, (30, 30))  # reset size
        print("New ANT")
        FOOD_TAKED -= 1 # ant with food -1
        if ant_num > 5 or (not food_list): # random choose new position
            x = random.randrange(100, 700, 1)
            y = random.randrange(100, 500, 1)
        else:  
            x = max(food_list[random.randrange(0, len(food_list), 1)].x-DETECT_FOOD+2, 0)
            y = max(food_list[random.randrange(0, len(food_list), 1)].y-DETECT_FOOD+2, 0)
        ant_list.append(Ant(x, y))


def check_food(ant):
    food_pos = []
    bye = False # break loop
    food_around = False
    x_lower = max(0, ant.x-DETECT_FOOD)
    x_upper = min(799, ant.x+DETECT_FOOD)
    y_lower = max(0, ant.y-DETECT_FOOD)
    y_upper = min(599, ant.y+DETECT_FOOD)
    # detect food
    for i in range(x_lower, x_upper):
        for j in range(y_lower, y_upper):
            if ant_map[i, j] == FOOD:
                # print("FOOD!")
                food_pos = [i, j]
            if bye:
                break
        if bye:
            break
    if food_pos: # food detect = True
        ant.time += 10 # add ant time for it to go home
        x_pn = np.sign(food_pos[0] - ant.x) # get x direction
        y_pn = np.sign(food_pos[1] - ant.y) # get y direction
        dir = random.randrange(0, 2, 1)  # random choose direction(x = 0 ,y = 1)
        if dir == 0:     # x
            ant.x = ant.x + STEP*x_pn
            ant.rect.topleft = (ant.x, ant.y)
        else:            # y
            ant.y = ant.y + STEP*y_pn
            ant.rect.topleft = (ant.x, ant.y)
        
        # get food
        if abs(food_pos[0]- ant.x)<CONFORM_FOOD and abs(food_pos[1]- ant.y)<CONFORM_FOOD:
            food_around = True
        if food_around: # get food = True
            global food_is_here,FOOD_TAKED
            # find the food in the food_list
            for i in range(0, len(food_list)):
                if food_list[i].x == food_pos[0] and food_list[i].y == food_pos[1]:
                    food_is_here = i
                    break
            food_list[food_is_here].count -= 1
            if food_list[food_is_here].count == 0:
                # reset ant_map
                ant_map[food_list[food_is_here].x, food_list[food_is_here].y] = 0
                # pop food fron food_list
                food_list.pop(food_is_here)
            FOOD_TAKED += 1
            # change ant image
            ant.raw_image = pg.image.load('/home/jamesqian/Documents/AI/AI_MID/ant_with_food.png').convert_alpha()
            ant.image = pg.transform.scale(ant.raw_image, (30, 30))
            # add time to ant
            ant.time = SEC*TIME*3
            # set go_home flag
            ant.go_home = True
        return True
    return False


def check_pheromone(ant, num):
    pheromone_pos = []
    bye = False
    x_lower = max(0, ant.x-DETECT_PHEROMONE)
    x_upper = min(799, ant.x+DETECT_PHEROMONE)
    y_lower = max(0, ant.y-DETECT_PHEROMONE)
    y_upper = min(599, ant.y+DETECT_PHEROMONE)
    # detect pheromone
    for i in range(x_lower, x_upper):
        for j in range(y_lower, y_upper):
            for k in range(0, len(ant_list)):
                if k != num and i == ant_list[k].x and j == ant_list[k].y:
                    pheromone_pos = [i, j]
            if bye:
                break
        if bye:
            break
    if pheromone_pos:
        # print("pheromone")
        x_pn = np.sign(pheromone_pos[0] - ant.x)
        y_pn = np.sign(pheromone_pos[1] - ant.y)
        dir = random.randrange(0, 2, 1)  # random choose direction(x = 0 ,y = 1)
        if dir == 0:  # x
            ant.x = ant.x + STEP*x_pn
            ant.rect.topleft = (ant.x, ant.y)
        else:         # y
            ant.y = ant.y + STEP*y_pn
            ant.rect.topleft = (ant.x, ant.y)


def walk(ant, p):
    # just walking without purpose
    x = ant.x
    y = ant.y
    if p == 1:
        pos = random_list1[random.randrange(0, len(random_list1), 1)]
    else:
        pos = random_list2[random.randrange(0, len(random_list2), 1)]
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
    ant.x = x
    ant.y = y
    ant.rect.topleft = (x, y)


pg.init()
window_surface = pg.display.set_mode((800, 600))  # load window surface
pg.display.set_caption('AI') # window name
my_font = pg.font.SysFont(None, 30) 
init()

main_clock = pg.time.Clock()

while True:
    global food
    # 偵測事件
    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
            sys.exit()

    # 背景顏色，清除畫面
    window_surface.fill(WHITE)
    pop_list = []
    i = 0
    while True:
        # end of a round
        if i > len(ant_list)-1 or i < 0:
            break
        # ant time - 1
        ant_list[i].time -= 1
        #print ant
        window_surface.blit(ant_list[i].image, ant_list[i].rect)

        if ant_list[i].go_home:         # check go_home flag
            go_home(ant_list[i])
        elif check_food(ant_list[i]):   # detect food
            pass
        else:
            check_pheromone(ant_list[i], i) # detect pheromone
            if(count % 2):    # walk strategy
                walk(ant_list[i], 1)
            else:
                walk(ant_list[i], 2)

        # time for ant to dead
        if ant_list[i].time == 0:
            ant_num -= 1
            print("Kill ANT")
            ant_list.pop(i)
            i -= 1
        i += 1
    
    # print home
    window_surface.blit(home.image, home.rect)

    # print food
    for j in range(0, len(food_list)):
        window_surface.blit(food_list[j].image, food_list[j].rect)

    # add food per "FOOD_ADD" round
    print("count = ",count,not count%(FOOD_ADD),"len(food_list) = ",len(food_list),"FOOD_TAKED = ",FOOD_TAKED)
    if (not count%(FOOD_ADD)) and len(food_list)+FOOD_TAKED<FOOD_MAX:
        if ant_list:
            tmp = random.randrange(0,len(ant_list),1)
            if ant_list[tmp].x<5 and ant_list[tmp].y<5:
                tmp += 1
            food_list.append(Food(max(ant_list[tmp].x-DETECT_FOOD+2, 0),max(ant_list[tmp].y-DETECT_FOOD+2, 0)))
            ant_map[max(ant_list[tmp].x-DETECT_FOOD+2, 0),max(ant_list[tmp].y-DETECT_FOOD+2, 0)] = FOOD
        else:
            x = random.randrange(100,700,1)
            y = random.randrange(100,500,1)
            food_list.append(Food(x,y))
            ant_map[x,y] = FOOD

    count += 1 # cunt rounds

    # print ant number
    text_surface = my_font.render(
        'Number of ANT: {}'.format(ant_num), True, (0, 0, 0))
    window_surface.blit(text_surface, (10, 560))

    pg.display.update()
    # 控制遊戲迴圈迭代速率
    main_clock.tick(FPS)
