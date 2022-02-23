import pygame
from combinedPathFinding import *
from simulation import simulation
from robot import Robot
from paths import *


def main(win, width):
    ROWS = 20 #size of the grid, grid is 10x10 cm
    grid = make_grid(ROWS, width) #width is the width of the entire grid
    gap = width // ROWS
	#hardcode start end and obs
    movements = []
    storemovs = []

    paths = Paths()

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

	#make obstacles list
    obs1 = Obs(5, 11, width//ROWS, 270, grid)
    obs2 = Obs(17, 16, width//ROWS, 180, grid)
    obs3 = Obs(1, 4, width//ROWS, 0, grid)
    obs4 = Obs(14, 3, width//ROWS, 270, grid)
    obs5 = Obs(10, 9, width//ROWS, 0, grid)
    
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
    
    run = True
    while run:

        robot.draw(win)
		#draw(win, grid, ROWS, width, obs)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end and len(copyObs) >= 0:
                # if event.key == pygame.K_SPACE and start and end: #repeat for all 5 obs
                    # size = len(copyObs)
                    # while size >= 0:
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)
                        movements = algorithm(lambda: draw(win, grid, ROWS, width, obs), grid, start, end)
                        #lambda allows u to call a function inside the algo function, nth important
                        #reset virtual obs:
                        clearVBarrier(grid)
                        if movements:
                            paths.addPath(movements)
                            nx,ny,robottheta = simulation(lambda: draw(win, grid, ROWS, width,obs),win,robot,movements,start)
                            movements.clear()


                        start = end
                        robot.x = nx
                        robot.y = ny

                        if robottheta is not None:
                            robot.theta = robottheta
                            robot.updateAngle(robot.theta)
            
                        #set start as the end for current obs
                        if len(copyObs) > 0:
                            lastOb = tempOb
                            tempOb = copyObs.pop()
                            createOutGuide(grid, ROWS, lastOb, start)
                            end = createGoal(grid, tempOb)
                            createVirtualBarrier(grid, ROWS, tempOb, end)
                        # size-=1
                        

                if event.key == pygame.K_c: #clear entire screen
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                    start = grid[1][18]
                    start.make_start() #color start

        pygame.display.update()

    pygame.quit()
    return paths

paths = main(WIN, WIDTH) #global variables/constantx
paths.printPath()