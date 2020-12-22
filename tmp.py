
import pygame

start_ticks=pygame.time.get_ticks() #starter tick
pygame.init()
while  1: # mainloop
    seconds=(pygame.time.get_ticks()-start_ticks)/1000 #calculate how many seconds
    if seconds>10: # if more than 10 seconds close the game
        break
    print (seconds) #print how many seconds

# import pygame

# pygame.init()

# #### Create a canvas on which to display everything ####
# window = (400,400)
# screen = pygame.display.set_mode(window)
# #### Create a canvas on which to display everything ####

# #### Create a surface with the same size as the window ####
# background = pygame.Surface(window)
# #### Create a surface with the same size as the window ####

# #### Populate the surface with objects to be displayed ####
# pygame.draw.rect(background,(0,255,0),(120,120,100,50))
# pygame.draw.rect(background,(0,255,0),(120,120,200,50),1)
# #### Populate the surface with objects to be displayed ####


# #### Blit the surface onto the canvas ####
# screen.blit(background,(0,0))
# #### Blit the surface onto the canvas ####

# #### Update the the display and wait ####
# pygame.display.flip()
# done = False
# while not done:
#     pygame.fill(WHITE)
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             done = True
# #### Update the the display and wait ####

# pygame.quit()