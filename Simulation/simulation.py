import pygame
from robot import *

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

def simulation(draw,win,robot,movements,start):
    
    nx = 0
    ny = 0
    headingAngle = 0
    print("robot")
    print(robot.x)
    print(robot.y)
    print(robot.theta)
    print("robot")
    # robot = Robot((robot.x,robot.y),"DDR.png",3 * 30,win)
    # robot.theta = robot.theta
    draw()
    for i in range(1,len(movements)):
        # print(movements[i][0][0])
        # print(movements[i][0][1])
        # print("robot")
        
        if movements[i-1][1] == 'F':
            if movements[i-1][2]:
                robot.set_theta(movements[i-1][2])            
            robot.updateAngle(robot.theta)

            if robot.theta == 0:
                while (robot.x) <= movements[i][0][0]:
                    draw()
                    robot.move_forward()
                    robot.draw(win)
                    pygame.display.update()

            elif robot.theta == 180:
                while robot.x >= movements[i][0][0]:
                    draw()
                    robot.move_forward()
                    robot.draw(win)
                    pygame.display.update()

            elif robot.theta == 90:
                # print(movements[i][0][1])
                while robot.y >= movements[i][0][1]:
                    draw()
                    robot.move_forward()
                    robot.draw(win)
                    pygame.display.update()

            elif robot.theta == 270:
                while robot.y <= movements[i][0][1]:
                    draw()
                    robot.move_forward()
                    robot.draw(win)
                    pygame.display.update()
            
            nx = robot.x
            ny = robot.y
        elif movements[i-1][1] == 'L':
            
            robot.setAngleDegrees(robot.theta)
            temp_theta = robot.theta

            if temp_theta == 0:
                while robot.theta < 90:
                    draw()
                    nx,ny,headingAngle = robot.turnLeftN(temp_theta,robot.x,robot.y,nx,ny,headingAngle)
                    robot.draw(win)
                    pygame.display.update()

            elif temp_theta == 180:
                while robot.theta < 270:
                    draw()
                    nx,ny,headingAngle = robot.turnLeftN(temp_theta,robot.x,robot.y,nx,ny,headingAngle)
                    robot.draw(win)
                    pygame.display.update()

            elif temp_theta == 270:
                while robot.theta < 360:
                    draw()
                    nx,ny,headingAngle = robot.turnLeftN(temp_theta,robot.x,robot.y,nx,ny,headingAngle)
                    robot.draw(win)
                    pygame.display.update()

            elif temp_theta == 90:
                 while robot.theta < 180:
                    draw()
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
            
        elif movements[i-1][1] == "T":
            pass

        elif movements[i-1][1] == "R":
            headingAngle = movements[i-1][2]
            robot.setAngleDegrees(movements[i-1][2])

            temp_theta = movements[i-1][2]

            if temp_theta == 0:
                while robot.theta < 90:
                    draw()
                    # print(headingAngle)
                    nx,ny,headingAngle = robot.turnRightN(temp_theta,robot.x,robot.y,nx,ny,headingAngle)
                    robot.draw(win)
                    pygame.display.update()

            elif temp_theta == 180:
                while robot.theta >= 90:
                   
                    draw()
                    # print(headingAngle)
                    nx,ny,headingAngle = robot.turnRightN(temp_theta,robot.x,robot.y,nx,ny,headingAngle)
                    robot.draw(win)
                    pygame.display.update()

            elif temp_theta == 270:
                while robot.theta > 180:
                    draw()
                    # print(headingAngle)
                    nx,ny,headingAngle = robot.turnRightN(temp_theta,robot.x,robot.y,nx,ny,headingAngle)
                    robot.draw(win)
                    pygame.display.update()
                    
            elif temp_theta == 90:
                while robot.theta > 0:
                    
                    draw()
                    nx,ny,headingAngle = robot.turnRightN(temp_theta,robot.x,robot.y,nx,ny,headingAngle)
                    robot.draw(win)
                    pygame.display.update()

            robot.updateX(nx)
            robot.updateY(ny)
            robot.theta = expectedRightTurnTheta(temp_theta)
            robot.updateAngle(robot.theta)
            pygame.display.update()   

        elif movements[i-1][1] == "Rev":
            temp_theta = robot.theta
            # robot.theta = 90

            if robot.theta == 0:
                while robot.x >= (movements[i-1][0][0]):
                    draw()
                    robot.move_backwards()
                    robot.draw(win)
                    pygame.display.update()

            elif robot.theta == 180:
                while robot.x <= (movements[i-1][0][0]):
                    draw()
                    robot.move_backwards()
                    robot.draw(win)
                    pygame.display.update()

            elif robot.theta == 270:
                while robot.y >= (movements[i-1][0][1]):
                    draw()
                    robot.move_backwards()
                    robot.draw(win)
                    pygame.display.update()

            elif robot.theta == 90:    
                while robot.y <= (movements[i-1][0][1]):
                    draw()
                    robot.move_backwards()
                    robot.draw(win)
                    pygame.display.update()

            nx = robot.x
            ny = robot.y

    return nx,ny,robot.theta