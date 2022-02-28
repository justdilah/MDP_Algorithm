import pygame
from combinedPathFinding import *
from simulation import simulation
from robot import Robot
from paths import *
# from network import *
# import socket

SERVERIP = "192.168.36.36"
PORT = 5180


def main(win, width):

    # try:
    #     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     print ("Socket successfully created")
    #     sock.connect((SERVERIP,PORT))
    #     print("Successfully connected!")
    # except socket.error as err:
	#     print ("socket creation failed with error %s" %(err))
    
    ROWS = 20 #size of the grid, grid is 10x10 cm
    grid = make_grid(ROWS, width) #width is the width of the entire grid
    gap = width // ROWS
	#hardcode start end and obs
    # movements = []
    # androidmovs = []

    # paths = Paths()

    nx = 0
    ny = 0 

	#make border, to stop robot from stepping out of boundary
    for row in grid: #first row
        for spot in row:
            row, col = spot.get_pos()
            if row == 0 or col ==0 or row == ROWS-1 or col == ROWS-1:
                spot.make_barrier()
    robottheta = None
    start = grid[1][18]
    start.make_start() #color start
    start.make_start() #color start
    startpos = start.get_pos()
    x = startpos[0] * gap
    y = startpos[1] * gap
    robot = Robot((start.return_center() + x,start.return_center() + y),"DDR.png",3 * gap,win)

	# make obstacles list
    #make obstacles list
    obs1 = Obs(5, 11, width//ROWS, 270, grid)
    obs2 = Obs(17, 16, width//ROWS, 180, grid)
    obs3 = Obs(2, 4, width//ROWS, 0, grid)
    obs4 = Obs(14, 3, width//ROWS, 270, grid)
    obs5 = Obs(10, 9, width//ROWS, 0, grid)
    # 
    obs = []
    obs.append(obs2)
    obs.append(obs5)
    obs.append(obs4)
    obs.append(obs3)
    obs.append(obs1)
    
    for ob in obs:
        createGoal(grid, ob)
        
    draw(win, grid, ROWS, width, obs)
    copyObs = obs.copy()
	#initialise the first goal pos
    tempOb = copyObs.pop()
    end = createGoal(grid, tempOb)
    createVirtualBarrier(grid, ROWS, tempOb, end)
    size = len(copyObs)
    prevSpot = None
    run = True
   
    while run:

        robot.draw(win)
		#draw(win, grid, ROWS, width, obs)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end and size >= 0:
                # if event.key == pygame.K_SPACE and start and end: #repeat for all 5 obs
                    # size = len(copyObs)
                    # while size >= 0: 
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)
                        path = algorithm(lambda: draw(win, grid, ROWS, width, obs), grid, start, end)
                        #lambda allows u to call a function inside the algo function, nth important
                        #reset virtual obs:
                        
                        if not path:
                            clearVBarrier(grid)
                            createVirtualBarrier(grid, ROWS, tempOb, end)
                            
                        if prevSpot != None:
                            print("AlteredPath")
                            alteredPath = alterPath(path, prevSpot, start, grid)#current path and prevSpot and startSpot into the function.
                            
                            #result in a path that takes into account the correction to take after arriving at the obstacle.
                            for i in alteredPath:
                                print(i)
                            print("------------------------------")
                            nx,ny,robottheta = simulation(lambda: draw(win, grid, ROWS, width,obs),win,robot,alteredPath,start)
                        else:
                            nx,ny,robottheta = simulation(lambda: draw(win, grid, ROWS, width,obs),win,robot,path,start)
                            

                        prevSpot = path[len(path)-1]
                        robot.x = nx
                        robot.y = ny

                        if robottheta is not None:
                            robot.theta = robottheta
                            robot.updateAngle(robot.theta)
                            print("THETA ANGLE")
                            print(robot.theta)

                        print("TEST PREV SPOT")
                        print(prevSpot)

                        clearVBarrier(grid)

                        
            
                        #set start as the end for current obs
                        if len(copyObs) > 0:
                            start = end
                            lastOb = tempOb
                            tempOb = copyObs.pop()
                            # if len(copyObs) == 1:
                            createOutGuide(grid, ROWS, lastOb, start)
                            end = createGoal(grid, tempOb)
                            
                            createVirtualBarrier(grid, ROWS, tempOb, end)
                        size-=1
                        

                if event.key == pygame.K_c: #clear entire screen
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                    start = grid[1][18]
                    start.make_start() #color start

        pygame.display.update()

    pygame.quit()
    return paths, androidmovs

paths,androidmovs = main(WIN, WIDTH) #global variables/constant
# print(androidmovs)
paths.printPath()