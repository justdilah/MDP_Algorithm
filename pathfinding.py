from cmath import cos, sin
from pickle import FALSE
from tkinter import W
import pygame
import math
# from algorithm_try import * 
# from algorithm_try import *
from queue import PriorityQueue
from robot import *
from time import sleep
import random

# state()
WIDTH = 600

#RMB PYGAME WORKS DIFFERENTLY FOR THE DISPLAY, X-AXIS - REMAINS THE SAME, Y-AXIS - 0 - 600 FRON TOP TO BOTTOM
#setting up the display 
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

#colors
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
PURPLE = (128,0,128)
ORANGE = (255,165,0)
GREY = (128,128,128)
TURQUOISE = (64,224,208)

UNIT_LENGTH = 10
# TURN_RADIUS = 20
# TURN_RADIUS_GRID = TURN_RADIUS//UNIT_LENGTH
MAX_IMAGE_VIEW_DISTANCE = 30
MAX_IMAGE_VIEW_DISTANCE_GRID = MAX_IMAGE_VIEW_DISTANCE // UNIT_LENGTH
TURN_ON_SPOT_RADIUS = 30
TURN_ON_SPOT_RADIUS_GRID = TURN_ON_SPOT_RADIUS//UNIT_LENGTH
ROBOT_VIEWING_GRID_LENGTH = 30

class State:
    def __init__(self,pos,orientation):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.face_direction = orientation
        # self.prevState = prevState
        
# WHITE means not visited yet   
# RED means visited
# BLACK means obstacle
# ORANGE means the start node
# TURQUOISE means the last node
# PURPLE means the path

class Spot:
    #width is how wide is the spot
    def __init__(self,row,col,width,total_rows):
        self.row = row
        self.col = col

        #need to know the position to draw the cube 
        self.x = row * width
        self.y = col * width

        self.color = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows


    def get_pos(self):
        return self.row,self.col

    def image_side(self,pos,rotation,map):
        n = 80

        centerx,centery=pos
        x_axis=(centerx + n*math.cos(-rotation),centery + n*math.sin(-rotation))
        # y_axis=(centerx + n*math.cos(-rotation+math.pi/2),
        #         centery + n*math.sin(-rotation+math.pi/2))
        # print(x_axis)
        pygame.draw.line(map,(255,0,0),(centerx,centery),x_axis,3)
        # pygame.draw.line(map,(0,255,0),(centerx,centery),y_axis,3)
    
    def get_state(pos,direction,prevState):
        pass

    def action_reverse(State):
        pass

    # CHECK
    def is_closed(self):
        return self.color == RED

    #may not use this function
    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def is_path(self):
        return self.color == YELLOW

    # SET
    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    
    def make_image(self):
        self.color = BLUE

    def make_barrier(self):
        self.color = BLACK
    
    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def make_yellow(self):
        self.color = YELLOW

    #where to draw
    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))

    def return_center(self):
        return self.width // 2

    def checks_barrier(self,grid):
        check = True
        if self.row < self.total_rows - 1 and self.row > 1:
            if grid[self.row+1][self.col].is_barrier():
                check = False
            if grid[self.row-1][self.col].is_barrier(): # goes up the row
                check = False
        else:
            check = True

        if self.col < self.total_rows - 1 and self.col > 1:
            if grid[self.row][self.col + 1].is_barrier():
                check = False
            if grid[self.row][self.col-1].is_barrier(): # goes left the row
                check = False
        else:
            check = True

        return check

            


    # add the valid spots that can be neighbours

    #need to determine the white squares that are the neighbours and not the barriers
    #check up,down, left, right if they are barriers
    #if not, add to the neighbours
    def update_neighbours(self,grid):
        self.neighbours = []

        # checks if it is a barrier
        # row is lesser than the last row  
        if self.row < self.total_rows - 1 and not grid[self.row+1][self.col].is_barrier() and self.checks_barrier(grid): # goes down the row
            self.neighbours.append(grid[self.row+1][self.col])
        
        # row is more than the first row 
        if self.row > 0 and not grid[self.row-1][self.col].is_barrier() and self.checks_barrier(grid): # goes up the row
            self.neighbours.append(grid[self.row-1][self.col])

        # col less than the last col 
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier() and self.checks_barrier(grid): # goes right the row
            self.neighbours.append(grid[self.row][self.col+1])

        # col more than the first col 
        if self.col > 0 and not grid[self.row][self.col-1].is_barrier() and self.checks_barrier(grid): # goes left the row
            self.neighbours.append(grid[self.row][self.col-1])

    #lt stand for Less Than

    #compare 2 spots 
    def __lt__(self,other):
        return False

# heuristic function
# figure out the distance between p1 to p2 
# manhattan distance(guessing distance)
def h(p1,p2):
    x1, y1 = p1
    x2, y2 = p2 
    return abs(x1- x2) + abs(y1 - y2)

def reconstruct_path(came_from,current,win,grid,ROWS,width):
    # print(came_from)
    # print(current)
    temp = current
    while current in came_from:
        current = came_from[current]
        row,col = current.get_pos()
        dot1 = grid[row+1][col+1]
        dot2 = grid[row-1][col]
        dot3 = grid[row][col+1]
        dot4 = grid[row][col-1]
        dot1.make_path()
        dot2.make_path()
        dot3.make_path()
        dot4.make_path()
        current.make_path()
        draw(win,grid,ROWS,width)
    return current,temp

def algorithm(win,ROWS,width,grid,start,end):
    
    count = 0
    #keeps track of the nodes, along with the f_score
    #H(n) - estimate from node n to the end node (manhattan distance)
    open_set = PriorityQueue()
    #count is to keep track when I entered this cube in the queue
    #count acts as a tiebreaker if it has the same value
    # 0 - starting point 
    # start - spot 
    #f_score = 0 
    open_set.put((0,count,start))
    #which node it came from
    came_from = {}
    #g_score - current shortest distance from the start node to the n node 
    #f_score - g_score + h_score
    #prioritise based on the f_score - smaller f_score the better
    #keeps track of the current shortest distance from start node to this node
    #initialise all as infinity
    #have not found any path 
    g_score = {spot:float("inf") for row in grid for spot in row}
    #set the g_score for the start to 0 
    g_score[start] = 0

    #estimate the start node and the end node when beginningW
    f_score = {spot:float("inf") for row in grid for spot in row}
    
    f_score[start] = h(start.get_pos(),end.get_pos())

    #keep check of the items in the priority queue
    #it is a duplicate of the open_Set
    current = None
    open_set_hash = {start}
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        #popping the lowest f_score and get the node that is associated with that (spot object)
        #first loop, pop the 1st node 
        #then consider the neighbours of the current node 
        current = open_set.get()[2]
        open_set_hash.remove(current)

        #found the shortest path
        if current == end:
            #to find the path, just back track where it came from, from the end to the start
            #make path
            # reconstruct_path(came_from,end,win,grid,ROWS,width)
            end.make_end()
            return came_from

        #consider all the neighbours of the current node 
        for neighbour in current.neighbours:
            #current node - go another node
            #its the next node 
            temp_g_score = g_score[current] + 1

            #find a better node
            #if it is lesser than the current node 
            #current g_score of neighbour of the current node 
            if temp_g_score < g_score[neighbour]:
                #update the path
                #the current node is where we came from 
                came_from[neighbour] = current

                #update the g_score of the neighbour of the current node 
                g_score[neighbour] = temp_g_score
                #h(n) - estimated distance from the neighbour to the end node 
                f_score[neighbour] = temp_g_score + h(neighbour.get_pos(),end.get_pos())
                #if not in the open_set_hash, add them it  
                if neighbour not in open_set_hash:
                    count+=1
                    open_set.put((f_score[neighbour],count,neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()

        draw(win,grid,ROWS,width)
        #already consider it 
        if current!=start:
            current.make_closed()
    #never run the path
    return False

def make_grid(rows,width):
    grid = []
    #width of the whole grid
    #rows are the total number of rows
    count=0
    gap = width // rows #gap between the rows - width of the blocks
    for i in range(rows):
        # print(i)
        grid.append([])
        #width 
        for j in range(rows):
            spot = Spot(i,j,gap,rows)
            #list inside of list
            grid[i].append(spot)
    return grid


def draw_grid(win, rows, width):
    gap = width // rows #integer division
    for i in range(rows):
        pygame.draw.line(win,GREY,(0,i * gap),(width, i * gap)) 
        for j in range(rows):
            pygame.draw.line(win,GREY, (j * gap,0), (j * gap,width))

def draw(win,grid,rows,width):
    win.fill(WHITE)

    #draw the grid lines
    for row in grid :
        #in a row, there are individual spots
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
     #update the display

def get_clicked_pos(pos,rows,width):
    gap = width // rows
    y,x = pos
    #divide the width of the cube
    row = y // gap
    col = x // gap
    # print(row-1,col-1)
    return row,col

def obstacles(start,grid,gap,win):
    
    nodes = PriorityQueue()
    ori = PriorityQueue()
    obs1 = grid[13][3]
    x = obs1.get_pos()[0] * gap
    y = obs1.get_pos()[1] * gap
     
    b1 = grid[11][2]
    
    obs2 = grid[4][13]
    x = obs2.get_pos()[0] * gap
    y = obs2.get_pos()[1] * gap

    b2 = grid[4][15]

    obs3 = grid[10][5]
    x = obs3.get_pos()[0] * gap
    y = obs3.get_pos()[1] * gap

    b3 = grid[8][5]

    obs4 = grid[17][15]
    x = obs4.get_pos()[0] * gap
    y = obs4.get_pos()[1] * gap

    b4 = grid[17][17]

    obs5 = grid[10][16]
    x = obs5.get_pos()[0] * gap
    y = obs5.get_pos()[1] * gap

    b5 = grid[12][16]
    obs = [obs1,obs2,obs3,obs4,obs5]

    count = 0
    image_cor = [b1,b2,b3,b4,b5]

    obstacles = []
    coordinates = []
    obstacles_coor = []

    for o in obs: 
        o.make_image()
        x = o.get_pos()[0] * gap
        y = o.get_pos()[1] * gap
        # -90 to 90
        vector = State((x,y),90)
        print(x,y)
        obstacles.append(vector)
        obs_coor = (x,y)
        obstacles_coor.append(obs_coor)
        angle = compare(o.get_pos(),obs[count].get_pos())
        # print(angle)
        diff = o.get_pos()[0] - start.get_pos()[0] 
        nodes.put((h(start.get_pos(),o.get_pos()),o,diff))
        # print(h(start.get_pos(),o.get_pos()))

        ori.put((h(start.get_pos(),o.get_pos()),angle))

        count+=1

        # o.image_side((o.return_center() + x,o.return_center() + y),math.radians(90),win)
    for i in range(0,5):
        goal_x , goal_y = generateGoalState(obstacles[i])
        coordinates.append((goal_x,goal_y))
    return nodes,coordinates, obstacles_coor,obstacles

def draw_vector(x,y,win):
        pygame.draw.circle(win,RED,(x,y),2,2)

def random_orientation():
    orientation = [math.radians(0),math.radians(90),math.radians(180),math.radians(270)]
    r = random.randint(0,len(orientation)-1)
    return orientation[r]


#compare 2 spots postions and determine the robot orientation
def compare(pos,pos2):
    # print(pos[0],pos2[0])
    if(pos[0] < pos2[0]):
        return 0
    elif (pos[0] > pos2[0]):
        return 180
    if (pos[1] > pos2[1]):
        return 90
    elif (pos[1] < pos2[1]):
        return 270
    return 0

def turn_angle():
    pass

def isDestination(currentpos,goalpos):
    return (currentpos.get_pos[0] == goalpos.get_pos[0] and currentpos.get_pos[1] and goalpos.get_pos[1])

def generateGoalState(obstacle):
    
    goalXGrid = (30//2 + obstacle.x) + int(math.cos(math.radians(obstacle.face_direction)) * ROBOT_VIEWING_GRID_LENGTH)
    goalYGrid = (30//2 + obstacle.y) - int(math.sin(math.radians(obstacle.face_direction)) * ROBOT_VIEWING_GRID_LENGTH)
    return goalXGrid,goalYGrid

def generateCenterPoint(obstacle):
    return (30//2 + obstacle[0]),(30//2 + obstacle[1])
    

#main loop
def main(win,width):
    pygame.init()
    ROWS = 20

    count = 0 
    #generate the grid
    grid = make_grid(ROWS,width)
    gap = width // ROWS
    # print(gap)
    
    robot_orientation = []
    start = None
    end = None

    store_x = 0
    store_y = 0
    
    paths = []
    start = grid[1][1]
    start.make_start()
    startpos = start.get_pos()
    x = startpos[0] * gap
    y = startpos[1] * gap

    # source = State((x,y),90)
    pathCost = 0

    TURN_RADIUS = 30
    TURN_RADIUS_GRID = (int)(TURN_RADIUS//gap)
    MAX_IMAGE_VIEW_DISTANCE = 30
    MAX_IMAGE_VIEW_DISTANCE_GRID = (int)(MAX_IMAGE_VIEW_DISTANCE//gap)
    TURN_ON_SPOT_RADIUS = 20

    
    # print(startpos)
    robot = Robot((start.return_center() + x,start.return_center() + y),"DDR.png",3 * gap,win)
    # print(start.return_center() + x)
    x = start.return_center() + x
    # print(x)
    # print(y)
    run = True
    r = random_orientation()
    nodes , coor,obs_coor, many_obs = obstacles(start,grid,gap,win)
    
    # print(nodes.get())
    dt = 0
    old = start.return_center() + x,start.return_center() + y
    new = old
    lasttime = pygame.time.get_ticks()
    moveGridDistance = 0.02 * 3779.52
    count = 0

    check = True
    check1 = True

    while run: 

        draw(win,grid,ROWS,width)
        c_x,c_y = generateCenterPoint(obs_coor[0])
        obs_new = State((c_x,c_y),90)
        robot.move(robot,obs_new)
        # if(robot.x <= 500):
            # robot.move_straight()s
        # robot.robot_domove((generateCenterPoint(obs_coor[0])))
        # print((generateCenterPoint(obs_coor[0])))
        for i in range(0,5):
            draw_vector(coor[i][0],coor[i][1],win) 
            c_x,c_y = generateCenterPoint(obs_coor[i])
            draw_vector(c_x,c_y,win)
        # pygame.draw.line(win,RED,old,new,3)   
                
        # new_y = (start.return_center() + y) + moveGridDistancSe*(math.sin(math.pi/180*0))
        # print(new_y)
        dt = (pygame.time.get_ticks()-lasttime) / 1000
        lasttime = pygame.time.get_ticks()
        # ((self.vl+self.vr)/2)*math.cos(self.theta)*dt
        # print(((moveGridDistance+moveGridDistance)/2) * math.cos(math.radians(0))) * dt
        # new_x = robot.x + 2 * dt
        # new_y = robot.y + 4 * math.radians(90) / abs(math.radians(90)) *dt
        # theta = robot.theta
        # robot.set_theta(robot.theta + (theta + 1) % 4)
        # print(robot.theta + math.atan2(new_x,new_y))

        # fl_x,fl_y = robot.move_forward_90_left()
        # draw_vector(fl_x,fl_y,win)
        # fr_x,fr_y = robot.move_forward_90_right()
        # draw_vector(fr_x,fr_y,win)
        # rr_x,rr_y = robot.move_reverse_90_right()
        # draw_vector(rr_x,rr_y,win)
        # rl_x,rl_y = robot.move_reverse_90_left()
        # draw_vector(rl_x,rl_y,win)
        # turnangle = 0 + 360

        #  robot.set_theta(math.atan2(x,y))
        # new_x = robot.x + moveGridDistance*(math.cos(math.radians(90) + robot.theta)) * dt

        # new_y = robot.y + moveGridDistance*(math.sin(math.radians(90) + robot.theta)) * dt
        # new_y = robot.y + moveGridDistance*(math.sin(math.radians(90))) * dt
        # print(new_x)
        # print(new_y)

        # robot.set_theta(robot.x / robot.y * dt)
        # new_x = robot.x + moveGridDistance*(math.cos(math.radians(0))) * dt

        # print(new_x)
        # print(y)
        # # # print(new_x)
        # for i in range(0,200):
        #     draw_vector(vectors[i][0],vectors[i][1],win)
        # draw_vector(temp_x,temp_y,win)
        # print(math.degrees(robot.theta))
        # if robot.theta >= math.radians(-90):
        #     robot.move(dt)
        #     print(math.degrees(robot.theta))
        # else: 

        #find the difference
        # if(robot.theta >= math.radians(-90)):
                # move_x,move_y = robot.move(dt)
        
        # if check == True:
            # robot.move_90()
            # check = False
        # if count <= 30:
        #     robot.move_straight()
        #     count+=1
        #     temp_x, temp_y = robot.move90(dt)
        #     store_x = temp_x
        #     store_y = temp_y
        #     check == False
        #     draw_vector(temp_x,temp_y,win)
        # draw_vector(store)
        # draw_vector(temp_x,temp_y,win)
       
        # if(robot.x >= 230):
        #     if(robot.theta >= math.radians(-90)):
        #         robot.move90(dt)
        # else:
        #     robot.move_straight()
                # move_x,move_y = robot.move(dt)
            # else:
                # if check1 == True:
                    # print(move_x-store_x)
                    # print(move_y-store_y)
                    # check1 = False
                
                
        #         # print(move_y)

        # elif (temp_x > 300):
        #     print(move_x)
        #     robot.move_forward(dt)
        # print(temp_x)
        robot.draw(win)
        robot.robot_frame((robot.x,robot.y), robot.theta)

        
        # y = new_y
        # x = new_x
        # print(x)
        # start.image_side((start.return_center() + x,start.return_center() + y),90,win)
        
        
        
        # # loop through the event 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            start.make_start()

        #     if pygame.mouse.get_pressed()[0]: #press on the left mouse button 
        #         pass
            
        #     elif pygame.mouse.get_pressed()[2]: #press on the right mouse button 
        #         pos = pygame.mouse.get_pos()
        #         #actual spot
        #         row, col = get_clicked_pos(pos,ROWS,width)
        #         spot = grid[row][col]
        #         spot.reset()

        #         if spot == start:
        #             start = None
        #         elif spot == end:
        #             end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbours(grid)
                
                    #number of nodes 
                    for i in range(0,1):
                        temp = nodes.get()[1]
                        # orientation = ori.get()[1]
                    
                        # robot_orientation.append(orientation)
                        # print("shit")
                        # print(source)
                        good = search(source,many_obs[i],pathCost,None)
                        # print("dasda")
                        paths.append(algorithm(win,ROWS,width,grid,start,temp))
                        start = temp
       
                    tracker = []
                    test = 0
                    stack = []
                    index = 0
                    what = 0

                    for path in reversed(paths): 
            
                        current,store = reconstruct_path(path,temp,win,grid,ROWS,width)
                        stack.append(store)
                        test+=1
        #                 what+=1

                        while store in path:
                            store = path[store]
                            stack.append(store)
                            test+=1
        #                     what+=1
                            current.make_path()
                            draw(win,grid,ROWS,width)
                        
                        temp = current
                        test-=1
                        tracker.append(test)
                        test = 0
                        index+=1

                    theta = 0 
                    index-=1
                    test = tracker[index]
                    track = 0
                    # theta = robot_orientation[track]
                    

                    while stack:   
                        if test < 0:
                            track+=1
                            index-=1    
                            test = tracker[index]
                            # print(test)
                            # theta = robot_orientation[track]

                        pos = stack.pop()
                        
                        pos.make_yellow()
                        test-=1    
                    
                        # robotpos = pos.get_pos()
                        # x1 = robotpos[0] * gap
                        # y1 = robotpos[1] * gap
                        # sleep(1)
                        # robot.move(pos.return_center() + x1,pos.return_center() + y1) 
                        # old = (pos.return_center() + x1,pos.return_center() + y1)

                        if stack:
                            pos2 = stack.pop()
                            pos2.make_yellow()
                            test-=1    
                            # robotpos2 = pos2.get_pos()
                            # x2 = robotpos2[0] * gap
                            # y2 = robotpos2[1] * gap
                            # if test < 0: 
                            #     robot.set_theta(theta)
                            # else: 
                            #     robot.set_theta(compare(pos.get_pos(),pos2.get_pos()))
                            # robot.move(pos2.return_center() + x2,pos2.return_center() + y2) 
                            
                            end = pos2

                        else:
                            # if test <= 1:
                                # robot.set_theta(theta)
                                # print(theta)
                            # else:
                                # robot.set_theta(compare(pos.get_pos(),pos2.get_pos()))
                            # sleep(1)
                            # robot.move(pos.return_center() + x1,pos.return_center() + y1) 
                            # new = (pos2.return_center() + x2,pos2.return_center() + y2)
                            # pygame.draw.line(win,RED,old,new,3)
                            end = pos             

                    start.make_start()
                    end.make_end()
            #clear screen 
            if event.type == pygame.K_c:
                start = None
                end = None
                grid = make_grid(ROWS,width)


        pygame.display.update()

    pygame.quit()



main(WIN,WIDTH)


        
    

