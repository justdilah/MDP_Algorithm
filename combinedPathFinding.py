import pygame
import math
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
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0) 
GREY = (128, 128, 128) #used as virtual barrier
DGREY = (100, 100, 100)
TURQUOISE = (64, 224, 208)
        

class Obs:
	def __init__(self, row, col, width, orientation, grid): #width of obs
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = BLACK
		self.orient = orientation
		self.width = width
		self.grid = grid

		#to make the virtual barrier
		grid[row][col].make_barrier()
		grid[row-1][col-1].make_barrier()
		grid[row+1][col+1].make_barrier()
		grid[row-1][col].make_barrier()
		grid[row+1][col].make_barrier()
		grid[row][col+1].make_barrier()
		grid[row][col-1].make_barrier()
		grid[row+1][col-1].make_barrier()
		grid[row-1][col+1].make_barrier()



	
	def get_pos(self):
		return self.row, self.col

	def draw(self, win):
		#pygame.draw.rect(win, self.color, (self.x-self.width, self.y-self.width, self.width*3, self.width*3))
		if self.orient == 90:
			pygame.draw.line(win, BLUE, (self.x, self.y), (self.x+self.width, self.y), 2)
		elif self.orient == 0:
			pygame.draw.line(win, BLUE, (self.x+self.width, self.y), (self.x+self.width, self.y+self.width), 2)
		elif self.orient == 270:
			pygame.draw.line(win, BLUE, (self.x, self.y+self.width), (self.x+self.width, self.y+self.width), 2)
		elif self.orient == 180:
			pygame.draw.line(win, BLUE, (self.x, self.y), (self.x, self.y+self.width), 2)
        

class Spot:
    #width is how wide is the spot
    def __init__(self,row,col,width,total_rows):
        self.row = row
        self.col = col

        #need to know the position to draw the cube 
        self.x = row * width
        self.y = col * width

        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows


    def get_pos(self):
        return self.row,self.col

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
    
    def is_vbarrier(self):
        return self.color == DGREY

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

    	#make virtual barrier
    def make_vbarrier(self):
        self.color = DGREY

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
        
    def update_neighbors(self, grid):
		#up down left right, if not barrier add into neighbours list
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			#spot is not in the last row, mark the spot under it as a neighbour unless is barrier
            self.neighbors.append(grid[self.row + 1][self.col])
            
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])
            


    # add the valid spots that can be neighbours

    #need to determine the white squares that are the neighbours and not the barriers
    #check up,down, left, right if they are barriers
    #if not, add to the neighbours

# heuristic function
# figure out the distance between p1 to p2 
# manhattan distance(guessing distance)
def h(p1,p2):
    x1, y1 = p1
    x2, y2 = p2 
    return abs(x1- x2) + abs(y1 - y2)

def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start)) #add to the priority queue start node with f score of 0
	#count is for breaking ties
    came_from = {} #what node did this node come from/keeping track of parents
    g_score = {spot: float("inf") for row in grid for spot in row} #for every spot, initialise g score to inf
    g_score[start] = 0 #start serves as an identifier
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos()) #distance to end node
    open_set_hash = {start} #keeps track of items in the priority queue
    while not open_set.empty():
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2] #grab the highest priority node
        open_set_hash.remove(current) #remove from set that keeps track of whats in priority queue
        if current == end: #found shortest path, make path
            end.make_end()
            return reconstruct_path(came_from, end, draw, start)
			
        for neighbor in current.neighbors: #go through list of neighbours for current spot
            temp_g_score = g_score[current] + 1 #alt path from start to the neighbor node is +1 from current node
            if temp_g_score < g_score[neighbor]: #update shortest path to neighbor
                came_from[neighbor] = current #update parent of neighbor
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash: #no duplicates in priority queue
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
                    
        draw()
        if current != start:
            current.make_closed() #
            
    return None #if no path found


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

#-------------------------- Generate Path -----------------------------------------------------------------

def reconstruct_path(came_from, current, draw, start):
	#create a list to store the path
	path = []
	while current in came_from: #back track and draw path, start node not in current
		path.insert(0,current)
		current = came_from[current]
		current.make_path()
		draw()
	#append start spot to the beginning
	path.insert(0, start)
	directForSimu = [] #create an array to hold the centre points and instructions

	#process to get the centre points
	for spot in path:
		tempX, tempY = generateCenterPoint((spot.x, spot.y))
		directForSimu.append([(tempX, tempY), 'F', None]) #append a list, make a 2D list, in the list: centre coords, 'R', orientation

	#print(directForSimu)
	#process points
	find_turningpoint(directForSimu) #add "R", "L", "X" for in between turns and the orientation
	#for i in directForSimu:
		#print(i)
	add_reverse(directForSimu) #insert reverse instructions for turns that are too tight
	for i in directForSimu:
		print(i)

	return directForSimu
		
	# put 'R' if turning right
	# put 'L' if turning left
	# put 'X' in between turns
	#findStartEndPointofTurn(turningPoints)

def add_reverse(directForSimu):
	i = 0
	previousTurn = -1
	while i < len(directForSimu):
		if directForSimu[i][1] == 'L' or directForSimu[i][1] == 'R':
			if previousTurn == -1:
				previousTurn = i #store current index as first turn
			elif i - previousTurn > 3: #if theres enough space after a turn
				previousTurn = i #store the current turn as previous turn
			elif i - previousTurn < 4: #not enough space
				#how many rev to add
				addRev = 4 - (i - previousTurn)
				tempX = directForSimu[i][0][0] #x coord
				tempY = directForSimu[i][0][1] #y coord
				orient = directForSimu[i][2]
				for j in range(addRev):
					#add revs
					if orient == 0:
						directForSimu.insert(i, [(tempX + (addRev - j)*30 - 30, tempY),'Rev', 180])
					elif orient == 90:
						directForSimu.insert(i, [(tempX, tempY - (addRev - j)*30 + 30), 'Rev', 270])
					elif orient == 180:
						directForSimu.insert(i, [(tempX - (addRev - j)*30 + 30, tempY), 'Rev', 0])
					elif orient == 270:
						directForSimu.insert(i, [(tempX, tempY + (addRev - j)*30 - 30), 'Rev', 90])
					i += 1 #adding rev, we need to add at index i,  before the current turn
				previousTurn = i #store the current turn as the prev turn, after reversing, theres enough space
		i += 1 #ensure we do not check the same L/R


#not needed, keep just in case
def findStartEndPointofTurn(turningPoints):
	startEndCoords = []
	for turningPoint in turningPoints:
		turningSpot = turningPoint[0] #first index is the turning element
		iniOrient = turningPoint[1]
		finalOrient = turningPoint[2]
		if iniOrient == 0 and finalOrient == 90:
			startEndCoords.append(((turningSpot.x - TURNING_RADIUS, turningSpot.y), (turningSpot.x, turningSpot.y - TURNING_RADIUS))) #using the top-left coords instead of centre
		elif iniOrient == 0 and finalOrient == 270:
			startEndCoords.append(((turningSpot.x - TURNING_RADIUS, turningSpot.y), (turningSpot.x, turningSpot.y + TURNING_RADIUS)))
		elif iniOrient == 90 and finalOrient == 0:
			startEndCoords.append(((turningSpot.x, turningSpot.y + TURNING_RADIUS), (turningSpot.x + TURNING_RADIUS, turningSpot.y)))
		elif iniOrient == 90 and finalOrient == 180:
			startEndCoords.append(((turningSpot.x, turningSpot.y + TURNING_RADIUS), (turningSpot.x - TURNING_RADIUS, turningSpot.y)))
		elif iniOrient == 180 and finalOrient == 90:
			startEndCoords.append(((turningSpot.x + TURNING_RADIUS, turningSpot.y), (turningSpot.x, turningSpot.y - TURNING_RADIUS)))
		elif iniOrient == 180 and finalOrient == 270:
			startEndCoords.append(((turningSpot.x + TURNING_RADIUS, turningSpot.y), (turningSpot.x, turningSpot.y + TURNING_RADIUS)))
		elif iniOrient == 270 and finalOrient == 0:
			startEndCoords.append(((turningSpot.x, turningSpot.y - TURNING_RADIUS), (turningSpot.x + TURNING_RADIUS, turningSpot.y)))
		elif iniOrient == 270 and finalOrient == 180:
			startEndCoords.append(((turningSpot.x, turningSpot.y - TURNING_RADIUS), (turningSpot.x - TURNING_RADIUS, turningSpot.y)))
	for coord in startEndCoords:
		print(coord)

def find_turningpoint(path):
	#reiterate over path, find where the orientation changes
	orientation = compare(path[0][0], path[1][0]) #set orientation as the first and second spot in the path
	i = 0

	for i in range(len(path)-1):
		tempOrientation = compare(path[i][0], path[i+1][0])
		if tempOrientation != orientation:
			#turningPoint found
			#1 before and 1 after, and point itself mark as x
			path[i][1] = 'X'
			path[i-1][1] = 'X'
			path[i+1][1] = 'X'

			#at the turningPoint we need to add 'R'/'L'
			if orientation == 0 and tempOrientation == 90:
				path[i-2][1] = 'L'
			elif orientation == 0 and tempOrientation == 270:
				path[i-2][1] = 'R'
			elif orientation == 90 and tempOrientation == 180:
				path[i-2][1] = 'L'
			elif orientation == 90 and tempOrientation == 0:
				path[i-2][1] = 'R'
			elif orientation == 180 and tempOrientation == 90:
				path[i-2][1] = 'R'
			elif orientation == 180 and tempOrientation == 270:
				path[i-2][1] = 'L'
			elif orientation == 270 and tempOrientation == 0:
				path[i-2][1] = 'L'
			elif orientation == 270 and tempOrientation == 180:
				path[i-2][1] = 'R'
		#add the orientation regardless
		path[i][2] = tempOrientation
		orientation = tempOrientation

def draw_vector(x,y,win):
        pygame.draw.circle(win,RED,(x,y),2,2)

def createVirtualBarrier(grid, total_rows, obs1, end):
	if obs1.orient == 0:
		#virtual obs
		grid[end.row-1][end.col].make_vbarrier()
		grid[end.row-2][end.col].make_vbarrier() #not sure if can sense image if goal is so far away, but it aids in turning to go to next obs
		for i in range(2):
			for j in range(1,4):
				if not grid[end.row+i][end.col+j].is_barrier() and end.row+i < total_rows and end.col+j < total_rows:
					grid[end.row+i][end.col+j].make_vbarrier()
				if not grid[end.row+i][end.col-j].is_barrier() and end.row+i < total_rows and end.col-j >= 0:
					grid[end.row+i][end.col-j].make_vbarrier()
	elif obs1.orient == 90: 
		#make virtual barriers to make the robot face the correct orientation
		#make virtual barriers another color. everytime we are about to go to a different obstacle. scan grid and remove all virtual barriers
		grid[end.row][end.col+1].make_vbarrier()
		grid[end.row][end.col+2].make_vbarrier()
		for i in range(2):
			for j in range(1,4):
				if not grid[end.row+j][end.col-i].is_barrier() and end.row+j < total_rows and end.col-i >= 0:
					grid[end.row+j][end.col-i].make_vbarrier()
				if not grid[end.row-j][end.col-i].is_barrier() and end.row-j >= 0 and end.col-i >= 0:
					grid[end.row-j][end.col-i].make_vbarrier()
	elif obs1.orient == 180: 
		#virtual obs
		grid[end.row+1][end.col].make_vbarrier()
		grid[end.row+2][end.col].make_vbarrier()
		for i in range(2):
			for j in range(1,4):
				if not grid[end.row-i][end.col+j].is_barrier() and end.row-i >= 0 and end.col+j < total_rows:
					grid[end.row-i][end.col+j].make_vbarrier()
				if not grid[end.row-i][end.col-j].is_barrier() and end.row-i >= 0 and end.col-j >= 0:
					grid[end.row-i][end.col-j].make_vbarrier()
	elif obs1.orient == 270: 
		#virtual obs
		grid[end.row][end.col-1].make_vbarrier()
		grid[end.row][end.col-2].make_vbarrier()
		for i in range(2):
			for j in range(1,4):
				if not grid[end.row+j][end.col+i].is_barrier() and end.row+j < total_rows and end.col+i < total_rows:
					grid[end.row+j][end.col+i].make_vbarrier()
				if not grid[end.row-j][end.col+i].is_barrier() and end.row-j >= 0 and end.col+i < total_rows:
					grid[end.row-j][end.col+i].make_vbarrier()
#compare 2 spots postions and determine the robot orientation

def clearVBarrier(grid):
	for row in grid:
		for spot in row:
			if spot.is_vbarrier():
				spot.reset()

def createGoal(grid, obs1): # 4 can be change to a shorter value, viewing distance of the robot
	#assume turning radius is 2 spots
	#after turning, we want to end up 2 spots infront of the image, goal point is 4 spot away from image (can be changed)
	if obs1.orient == 0:
		end = grid[obs1.row + 4][obs1.col]
		end.make_end()
	elif obs1.orient == 90: 
		end = grid[obs1.row][obs1.col - 4]
		end.make_end()
	elif obs1.orient == 180: 
		end = grid[obs1.row - 4][obs1.col]
		end.make_end()
	elif obs1.orient == 270: 
		end = grid[obs1.row][obs1.col + 4]
		end.make_end()
	return end #return the spot

def compare(pos,pos2):
    # print(pos[0],pos2[0])
    
    #x coordinate
    if(pos[0] < pos2[0]):
        return 0
    elif (pos[0] > pos2[0]):
        return 180

    #y coordinate
    if (pos[1] > pos2[1]):
        return 90
    elif (pos[1] < pos2[1]):
        return 270
    return 0

def turn_angle():
    pass

def isDestination(currentpos,goalpos):
    return (currentpos.get_pos[0] == goalpos.get_pos[0] and currentpos.get_pos[1] and goalpos.get_pos[1])

def generateCenterPoint(obstacle):
    return (30//2 + obstacle[0]),(30//2 + obstacle[1])

def expectedRightTurnTheta(theta):
    if theta == 0:
        return 270
    elif theta == 90:
        return 0
    elif theta == 270:
        return 180
    elif theta == 180:
        return 90

def expectedLeftTurnTheta(theta):
    if theta == 0:
        return 90
    elif theta == 90:
        return 180
    elif theta == 270:
        return 0
    elif theta == 180:
        return 270

def simulation(win,grid,ROWS,width,robot,movements,start):
    nx = 0
    ny = 0
    headingAngle = 0
    robot = Robot((movements[0][0][0],movements[0][0][1]),"DDR.png",3 * 30,win)
    robot.theta = movements[0][2]
    for i in range(1,len(movements)):

        if movements[i-1][1] == 'F':
            if movements[i-1][2]:
                robot.set_theta(movements[i-1][2])
            
            robot.updateAngle(robot.theta)
            if robot.theta == 0:
                while (robot.x) <= movements[i][0][0]:
                    draw(win,grid,ROWS,width)
                    robot.move_forward()
                    robot.draw(win)
                    pygame.display.update()
                continue

            elif robot.theta == 180:
                while robot.x >= movements[i][0][0]:
                    draw(win,grid,ROWS,width)
                    robot.move_forward()
                    robot.draw(win)
                    pygame.display.update()
                continue

            elif robot.theta == 90:
                while robot.y >= movements[i][0][1]:
                    draw(win,grid,ROWS,width)
                    robot.move_forward()
                    robot.draw(win)
                    pygame.display.update()
                continue

            elif robot.theta == 270:
                while robot.y <= movements[i][0][1]:
                    draw(win,grid,ROWS,width)
                    robot.move_forward()
                    robot.draw(win)
                    pygame.display.update()
                continue 
        elif movements[i-1][1] == 'L':
            robot.setAngleDegrees(robot.theta)
            temp_theta = robot.theta

            if temp_theta == 0:
                while robot.theta < 90:
                    draw(win,grid,ROWS,width)
                    nx,ny,headingAngle = robot.turnLeftN(temp_theta,robot.x,robot.y,nx,ny,headingAngle)
                    robot.draw(win)
                    pygame.display.update()

            elif temp_theta == 180:
                while robot.theta < 270:
                    draw(win,grid,ROWS,width)
                    nx,ny,headingAngle = robot.turnLeftN(temp_theta,robot.x,robot.y,nx,ny,headingAngle)
                    robot.draw(win)
                    pygame.display.update()

            elif temp_theta == 270:
                while robot.theta < 360:
                    draw(win,grid,ROWS,width)
                    nx,ny,headingAngle = robot.turnLeftN(temp_theta,robot.x,robot.y,nx,ny,headingAngle)
                    robot.draw(win)
                    pygame.display.update()

            elif temp_theta == 90:
                 while robot.theta < 180:
                    draw(win,grid,ROWS,width)
                    nx,ny,headingAngle = robot.turnLeftN(temp_theta,robot.x,robot.y,nx,ny,headingAngle)
                    robot.draw(win)
                    pygame.display.update()
        
            robot.updateX(nx)
            robot.updateY(ny)
            robot.theta = expectedLeftTurnTheta(temp_theta)
            
            robot.updateAngle(robot.theta)
            robot.draw(win)
            pygame.display.update()   
            
        elif movements[i-1][1] == "X":
            pass

        elif movements[i-1][1] == "R":
            
            headingAngle = robot.theta
            robot.setAngleDegrees(robot.theta)

            temp_theta = robot.theta

            if temp_theta == 0:
                while robot.theta < 90:
                    draw(win,grid,ROWS,width)
                    # print(headingAngle)
                    nx,ny,headingAngle = robot.turnRightN(temp_theta,robot.x,robot.y,nx,ny,headingAngle)
                    robot.draw(win)
                    pygame.display.update()

            elif temp_theta == 180:
                while robot.theta >= 90:
                   
                    draw(win,grid,ROWS,width)
                    # print(headingAngle)
                    nx,ny,headingAngle = robot.turnRightN(temp_theta,robot.x,robot.y,nx,ny,headingAngle)
                    robot.draw(win)
                    pygame.display.update()

            elif temp_theta == 270:
                while robot.theta > 180:
                    draw(win,grid,ROWS,width)
                    # print(headingAngle)
                    nx,ny,headingAngle = robot.turnRightN(temp_theta,robot.x,robot.y,nx,ny,headingAngle)
                    robot.draw(win)
                    pygame.display.update()
                    
            elif temp_theta == 90:
                while robot.theta > 0:
                    draw(win,grid,ROWS,width)
                    # print(headingAngle)
                    nx,ny,headingAngle = robot.turnRightN(temp_theta,robot.x,robot.y,nx,ny,headingAngle)
                    robot.draw(win)
                    pygame.display.update()

            robot.updateX(nx)
            robot.updateY(ny)
            robot.theta = expectedRightTurnTheta(temp_theta)
            robot.updateAngle(robot.theta)
            robot.draw(win)
            pygame.display.update()   

        elif movements[i-1][1] == "Rev":
            temp_theta = robot.theta
            if temp_theta == 0:
                while robot.x >= (movements[i-1][0][0]):
                    draw(win,grid,ROWS,width)
                    robot.move_backwards()
                    robot.draw(win)
                    pygame.display.update()
            elif temp_theta == 180:
                while robot.x <= (movements[i-1][0][0]):
                    draw(win,grid,ROWS,width)
                    robot.move_backwards()
                    robot.draw(win)
                    pygame.display.update()
            elif temp_theta == 270:
                while robot.y >= (movements[i-1][0][1]):
                    draw(win,grid,ROWS,width)
                    robot.move_backwards()
                    robot.draw(win)
                    pygame.display.update()
            elif temp_theta == 90:    
                while robot.y <= (movements[i-1][0][1]):
                    draw(win,grid,ROWS,width)
                    robot.move_backwards()
                    robot.draw(win)
                    pygame.display.update()

    return robot.theta

#main loop
def main(win,width):
    pygame.init()
    ROWS = 20

    count = 0 
    grid = make_grid(ROWS,width)
    gap = width // ROWS

    #Create Barriers
    for row in grid: #first row
        for spot in row:
            row, col = spot.get_pos()
            if row == 0 or col ==0 or row == ROWS-1 or col == ROWS-1:
                spot.make_barrier()

    start = None
    end = None

    paths = []
    start = grid[1][18]
    start.make_start() #color start
    startpos = start.get_pos()
    x = startpos[0] * gap
    y = startpos[1] * gap

    movements = []
    
    robot = Robot((start.return_center() + x,start.return_center() + y),"DDR.png",3 * gap,win)
    x = start.return_center() + x

    run = True
    dt = 0
    lasttime = pygame.time.get_ticks()

    # robot.setAngleDegrees(robot.theta)

    # headingAngle = robot.theta

    # nx = 0
    # ny = 0
    # count = 0
    obs1 = Obs(4, 11, width//ROWS, 270, grid)
    obs2 = Obs(17, 16, width//ROWS, 180, grid)
    obs3 = Obs(4, 3, width//ROWS, 270, grid)
    obs4 = Obs(14, 2, width//ROWS, 180, grid)
    obs5 = Obs(11, 10, width//ROWS, 0, grid)

    obs = []
    obs.append(obs2)
    obs.append(obs5)
    obs.append(obs4)
    obs.append(obs3)
    obs.append(obs1)

    for ob in obs:
        createGoal(grid, ob)

 

    copyObs = obs.copy()
	#initialise the first goal pos
    tempOb = copyObs.pop()
    end = createGoal(grid, tempOb)
 
    while run: 

        draw(win,grid,ROWS,width)
        for ob in obs: #must draw after gridlines if not will cover up
            ob.draw(win)
        # dt = (pygame.time.get_ticks()-lasttime) / 1000
        # lasttime = pygame.time.get_ticks()

        
    #------------------------------- Testing the Turning ------------------------------------------
        
        # nx,ny,headingAngle = robot.turnRightN(robot.theta,robot.x,robot.y,nx,ny,headingAngle)
        # nx,ny = robot.turnLeftN(robot.theta,robot.x,robot.y,nx,ny)
        # nx,ny = robot.turnReverseRight(robot.theta,robot.x,robot.y,nx,ny)
        # nx,ny = robot.turnReverseLeft(robot.theta,robot.x,robot.y,nx,ny)
    
        robot.draw(win)
        # robot.robot_frame((robot.x,robot.y),robot.theta)

    #------------------------------------------Previous A*-----------------------------------------
        # # loop through the event 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end and len(copyObs) >= 0: #repeat for all 5 obs
                    createVirtualBarrier(grid, ROWS, tempOb, end)
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    movements =  algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
					#lambda allows u to call a function inside the algo function, nth important
					#reset virtual obs:
                    clearVBarrier(grid)
					#set start as the end for current obs
                    # print("Pause")
                    if len(copyObs) >= 0:
                        print("Pause")
                        print(movements)
                        if movements:
                            robottheta = simulation(win,grid,ROWS,width,robot,movements,start)
                            movements.clear()
                            
                        start = end
                        startpos = end.get_pos()
                        robot.x = (startpos[0] * 30) + 15
                        robot.y = (startpos[1] * 30) + 15
                        if robottheta is not None:
                            robot.theta = robottheta
                            robot.updateAngle(robot.theta)
                        if copyObs:
                            tempOb = copyObs.pop()
                            end = createGoal(grid, tempOb)

                if event.key == pygame.K_c: #clear entire screen
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                    start = grid[1][18]
                    start.make_start() #color start

        pygame.display.update()
    # if movements:
    #     simulation(win,grid,ROWS,width,robot,movements,start)

    print(movements)
    pygame.quit()

main(WIN,WIDTH)


        
    

