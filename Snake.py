import pygame
pygame.init()
import time
import random

clock = pygame.time.Clock()

win = pygame.display.set_mode((600,600))

emptyBlockColour = (50,50,50)
borderColour = (0,0,0)
backgroundColour = (97, 109, 200)
snakeColour = (255,255,255)

def mainGame():
    running = True
    snakeLocations = [[0,0]]
    direction = "Right"
    justMoved = "Right"
    moveTimer = 0
    foodTimer = 0
    foodLocation = []
    eaten = False

    while running:
        pygame.display.set_caption("Snake")
        clock.tick(15)
        moveTimer += 0.0667 
        foodTimer += 0.0667

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # all the movement presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            if justMoved != "Down":
                # these conditions prevent the snake doubling back on itself
                direction = "Up"
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            if justMoved != "Up":
                direction = "Down"
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if justMoved != "Right":
                direction = "Left"
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if justMoved != "Left":
                direction = "Right"


        win.fill(backgroundColour)
        

        for i in range (13):
            # first drawing the boxes for each row (j), then incrementing (i) for each column
            for j in range (13):
                # drawing 2 boxes, one of which creates a border for the inner box
                pygame.draw.rect(win, borderColour, (40+40*i, 40+40*j, 40, 40))
                # the boxes start 40 pixels away from the side of the screen, and repeat every 40 pixels
                # the border size is 2 pixels long, so the inner box has to be smaller by 4
                pygame.draw.rect(win, emptyBlockColour, (40+2+40*i, 40+2+40*j, 36, 36))

        for l in range (len(snakeLocations)):
            # this goes through each location the snake is covering and draws a block there
            pygame.draw.rect(win, snakeColour, (40+2+40*snakeLocations[l][0], 40+2+40*snakeLocations[l][1], 36, 36))
            # l is used to cycle through each location in the array, then [0] and [1] are used to reference the x and y location
            if direction == "Up":
                pygame.draw.circle(win, (emptyBlockColour), (40+2+10+40*snakeLocations[len(snakeLocations) - 1][0], 40+2+10+40*snakeLocations[len(snakeLocations) - 1][1]), 5)
                pygame.draw.circle(win, (emptyBlockColour), (40+2+25+40*snakeLocations[len(snakeLocations) - 1][0], 40+2+10+40*snakeLocations[len(snakeLocations) - 1][1]), 5)

            if direction == "Down":
                pygame.draw.circle(win, (emptyBlockColour), (40+2+10+40*snakeLocations[len(snakeLocations) - 1][0], 40+2+25+40*snakeLocations[len(snakeLocations) - 1][1]), 5)
                pygame.draw.circle(win, (emptyBlockColour), (40+2+25+40*snakeLocations[len(snakeLocations) - 1][0], 40+2+25+40*snakeLocations[len(snakeLocations) - 1][1]), 5)
            
            if direction == "Right":
                pygame.draw.circle(win, (emptyBlockColour), (40+2+25+40*snakeLocations[len(snakeLocations) - 1][0], 40+2+10+40*snakeLocations[len(snakeLocations) - 1][1]), 5)
                pygame.draw.circle(win, (emptyBlockColour), (40+2+25+40*snakeLocations[len(snakeLocations) - 1][0], 40+2+25+40*snakeLocations[len(snakeLocations) - 1][1]), 5)
            
            if direction == "Left":
                pygame.draw.circle(win, (emptyBlockColour), (40+2+10+40*snakeLocations[len(snakeLocations) - 1][0], 40+2+10+40*snakeLocations[len(snakeLocations) - 1][1]), 5)
                pygame.draw.circle(win, (emptyBlockColour), (40+2+10+40*snakeLocations[len(snakeLocations) - 1][0], 40+2+25+40*snakeLocations[len(snakeLocations) - 1][1]), 5)
            

        if moveTimer > 0.25:
            # ensures the snake moves every 0.25 seconds
            if direction == "Right":
                if snakeLocations[len(snakeLocations) - 1][0] == 12:
                    # if the head of the snake is already in the right-most column
                    # the head is the final element of the array
                    gameOver()
                else:
                    head = snakeLocations[len(snakeLocations) - 1]
                    newhead = [head[0]+1, head[1]]
                    # the x-location of the head is moved right 1
                    snakeLocations.append(newhead)
                    justMoved = "Right"
                
            if direction == "Left":
                if snakeLocations[len(snakeLocations) - 1][0] == 0:
                    # if the head of the snake is already in the left-most column
                    gameOver()
                else:
                    head = snakeLocations[len(snakeLocations) - 1]
                    newhead = [head[0]-1, head[1]]
                    # the x-location of the head is moved left 1
                    snakeLocations.append(newhead)
                    justMoved = "Left"

            if direction == "Up":
                if snakeLocations[len(snakeLocations) - 1][1] == 0:
                    # if the head of the snake is already in the up-most row
                    gameOver()
                else:
                    head = snakeLocations[len(snakeLocations) - 1]
                    newhead = [head[0], head[1]-1]
                    # the y-location of the head is moved up 1
                    snakeLocations.append(newhead)
                    justMoved = "Up"

            if direction == "Down":
                if snakeLocations[len(snakeLocations)- 1][1] == 12:
                    # if the head of the snake is already in the down-most row
                    gameOver()
                else:
                    head = snakeLocations[len(snakeLocations) - 1]
                    newhead = [head[0], head[1]+1]
                    # the y-location of the head is moved down 1
                    snakeLocations.append(newhead)
                    justMoved = "Down"

            if snakeLocations[len(snakeLocations) - 1] == foodLocation:
                # if the head of the snake is on top of the food
                foodTimer = 0
                foodLocation = []
                eaten = True
                # eaten variable stops the tail from being removed from array
            else:
                eaten = False

            if eaten == False:
                snakeLocations.remove(snakeLocations[0])
                # the first element of the array (the tail) is removed
            moveTimer = 0

        
        if foodTimer > 1 and foodLocation == []:
            foodLocation = [random.randint(0,12), random.randint(0,12)]
            # food randomly spawns every 3 seconds, unless there is already food on screen
            while snakeLocations.count(foodLocation) == 1:
                # checks whether the food overlaps with the snake
                foodLocation = [random.randint(0,12), random.randint(0,12)]

        if foodLocation != []:
            pygame.draw.circle(win, (255,0,0), (60+ 40*foodLocation[0], 60+ 40*foodLocation[1]), 15)
            # food is spawned in the centre of the block its been assigned
            # pygame draws circles from the center, so 40*index determined what block, 
            # and 60+ is for the 40 pixels at the side of the screen and 20 into the block to get to the center

        if snakeLocations.count(snakeLocations[len(snakeLocations) - 1])> 1:
            # if the same location appears twice, the snake is overlapping itself
            gameOver()

        pygame.display.update()


def test():
    running = True
    snakeLocations = [[0,0]]
    direction = "Right"

    while running:
        pygame.display.set_caption("Snake")
        clock.tick(1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        snakeLocations.append([2,0])
        snakeLocations.remove(snakeLocations[0])

def gameOver():
    running = True
    mouseDown = False
    while running:
        pygame.draw.rect(win, borderColour, (140, 140, 320, 320))
        pygame.draw.rect(win, backgroundColour, (150, 150, 300, 300))
        pygame.draw.rect(win, (14,209,69), (200, 325, 75, 75))
        pygame.draw.rect(win, (255,0,0), (325, 325, 75, 75))

        mouseX, mouseY = pygame.mouse.get_pos()

        if 200 < mouseX < 275 and 325 < mouseY < 400:
            pygame.draw.rect(win, (118,227,149), (200, 325, 75, 75))
            if mouseDown:
                mainGame()
        if 325 < mouseX < 400 and 325 < mouseY < 400:
            pygame.draw.rect(win, (255,99,99), (325, 325, 75, 75))
            if mouseDown:
                pygame.quit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseDown = True
            else:
                mouseDown = False

        endFont = pygame.font.SysFont('Consolas', 40)

        endText = endFont.render("Game Over!!!", True, (snakeColour))
        endText2 = endFont.render("Play again?", True, (snakeColour))

        textLocation = endText.get_rect(center = (300, 200))
        textLocation2 = endText2.get_rect(center = (300, 250))
        win.blit(endText, textLocation)        
        win.blit(endText2, textLocation2)



        pygame.display.update()


mainGame()
pygame.quit()