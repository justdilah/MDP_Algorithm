# from os import curdir
# from tkinter import CENTER
from turtle import heading
import pygame
import math
from time import *


# from pathfinding import ActionStraight
# from testing_sf import RRTGraph
# from testing_sf import RRTMap
# import numpy as np


# 30 - 10 cm 
# 60 - 20 cm - Turning Radius 

TURNING_RADIUS = 60
DIRECTION_MARGIN_OF_ERROR = 1

class State:
    def __init__(self,x,y,face_direction,prev_state):
        self.x = x
        self.y = y
        self.face_direction = face_direction 
        self.prev_state = prev_state

class Robot:
    
    
    def __init__(self,startpos,robotImg,width,win):

        #metres to pixels 
        self.m2p = 3779.52
        self.w = width
        self.distanceBetweenFrontBackWheels = width
        self.x = startpos[0]
        self.y = startpos[1]
        self.x_store = 0
        self.y_store = 0
        self.map = win
        self.angleDegrees = -90
        self.delta_ang = math.pi/180
        self.check = True
        self.text ="turnleft"
        self.movementList = []
        self.directionList = []
        self.distanceList = []
        self.gap = 30
        self.maxTurningAngle = 0


        self.theta = 0

        self.img = pygame.image.load(robotImg)

        self.rotated = pygame.transform.rotozoom(self.img,math.degrees(self.theta),1)

        #pygame creates a new rect with the size of the image and the x,y coordinates
        self.rect = self.rotated.get_rect(center=(self.x,self.y))

    def draw(self,map):
        map.blit(self.rotated,self.rect)

    def updateY(self,ny):
            self.y = ny

    def updateX(self,nx):
            self.x = nx
        
    def updateAngle(self,angle):
        
        self.rotated = pygame.transform.rotozoom(self.img,angle,1)

        #pygame creates a new rect with the size of the image and the x,y coordinates
        self.rect = self.rotated.get_rect(center=(self.x,self.y))
    
    #------------------- Set Angle in the Circle ------------------------------------------------

    #Left
    def setAngleDegrees(self,face_direction):
        if face_direction == 90:
            self.angleDegrees = 0

        elif face_direction == 0:
            self.angleDegrees = -90

        elif face_direction == 180:
            self.angleDegrees = -90

        elif face_direction == 270:
            self.angleDegrees = 0

    #Right
    def setAngleDegrees(self,face_direction):
        if face_direction == 90:
            self.angleDegrees = 0

        elif face_direction == 0:
            self.angleDegrees = -90

        elif face_direction == 180:
            self.angleDegrees = -90

        elif face_direction == 270:
            self.angleDegrees = 0

    #------------------- Turn Forward ------------------------------------------------------------

    def turnRightN(self,face_direction,x,y,nx,ny,headingAngle):

        if face_direction == 90:
            
            self.maxTurningAngle = 90
            if self.angleDegrees <= 90:
                headingAngle-=0.5
                self.theta-=0.5
                self.angleDegrees = self.angleDegrees + 0.5
                nx = (x+TURNING_RADIUS) - round(TURNING_RADIUS * math.cos(math.radians(self.angleDegrees)),2)
                ny = (y) - (round(TURNING_RADIUS * math.sin(math.radians(self.angleDegrees)),2)) 
        
        elif face_direction == 270:
            self.maxTurningAngle = -90
            if self.angleDegrees >= -90:
                headingAngle-=0.5
                self.theta-=0.5
                self.angleDegrees = self.angleDegrees - 0.5
                nx = (x-TURNING_RADIUS) + round(TURNING_RADIUS * math.cos(math.radians(self.angleDegrees)),2)
                ny = (y) - (round(TURNING_RADIUS * math.sin(math.radians(self.angleDegrees)),2)) 
        
        elif face_direction == 180:
            self.maxTurningAngle = 0
            if self.angleDegrees <= 0:
                headingAngle-=0.5
                self.theta-=0.5
                self.angleDegrees = self.angleDegrees + 0.5
                nx = (x) - round(TURNING_RADIUS * math.cos(math.radians(self.angleDegrees)),2)
                ny = (y-TURNING_RADIUS) - (round(TURNING_RADIUS * math.sin(math.radians(self.angleDegrees)),2)) 


        elif face_direction == 0:
            self.maxTurningAngle == 0
            # print(headingAngle)
            if(headingAngle > -90):
                self.angleDegrees = abs(self.angleDegrees)
            if self.angleDegrees >= 0:
                headingAngle-=0.5
                self.theta+=0.5
                # print(headingAngle)
                
                self.angleDegrees = self.angleDegrees - 0.5
                nx = (x) + round(TURNING_RADIUS * math.cos(math.radians(self.angleDegrees)),2)
                ny = (y+TURNING_RADIUS) - (round(TURNING_RADIUS * math.sin(math.radians(self.angleDegrees)),2)) 

        self.rotated = pygame.transform.rotozoom(self.img,headingAngle,1)
        self.rect = self.rotated.get_rect(center=(nx,ny))
        return nx,ny,headingAngle

    def turnLeftN(self,face_direction,x,y,nx,ny,headingAngle):
        if face_direction == 90:
            self.maxTurningAngle = 90
            if self.angleDegrees <= 90:
                self.theta+=0.5
                self.angleDegrees = self.angleDegrees + 0.5
                nx = (x-TURNING_RADIUS) + round(TURNING_RADIUS * math.cos(math.radians(self.angleDegrees)),2)
                ny = (y) - (round(TURNING_RADIUS * math.sin(math.radians(self.angleDegrees)),2)) 
        
        elif face_direction == 270:
            self.maxTurningAngle = -90
            if self.angleDegrees >= -90:
                self.theta+=0.5
                self.angleDegrees = self.angleDegrees - 0.5
                nx = (x+TURNING_RADIUS) - round(TURNING_RADIUS * math.cos(math.radians(self.angleDegrees)),2)
                ny = (y) - (round(TURNING_RADIUS * math.sin(math.radians(self.angleDegrees)),2)) 
        
        elif face_direction == 180:
            self.maxTurningAngle = 0
            self.angleDegrees = abs(self.angleDegrees)
            if self.angleDegrees >= 0:
                self.theta+=0.5
                self.angleDegrees = self.angleDegrees - 0.5
                nx = (x) - round(TURNING_RADIUS * math.cos(math.radians(self.angleDegrees)),2)
                ny = (y+TURNING_RADIUS) - (round(TURNING_RADIUS * math.sin(math.radians(self.angleDegrees)),2)) 


        elif face_direction == 0:
            self.maxTurningAngle == 0
            if self.angleDegrees <= 0:
                self.theta+=0.5
                self.angleDegrees = self.angleDegrees + 0.5
                nx = (x) + round(TURNING_RADIUS * math.cos(math.radians(self.angleDegrees)),2)
                ny = (y-TURNING_RADIUS) - (round(TURNING_RADIUS * math.sin(math.radians(self.angleDegrees)),2)) 
            
            

        self.rotated = pygame.transform.rotozoom(self.img,self.theta,1)
        self.rect = self.rotated.get_rect(center=(nx,ny))
        return nx,ny,headingAngle

    # def doTurn(self,x,y,face_direction):
    #     if(self.maxTurningAngle <= 90):



    #------------------- Turn Backwards -----------------------------------------------------------

    def turnReverseRight(self,face_direction,x,y,nx,ny,headingAngle):

        if face_direction == 90:
            self.maxTurningAngle = -90
            if self.angleDegrees >= -90:
                self.angleDegrees = self.angleDegrees - 0.5
                nx = (x+TURNING_RADIUS) - round(TURNING_RADIUS * math.cos(math.radians(self.angleDegrees)),2)
                ny = (y) - (round(TURNING_RADIUS * math.sin(math.radians(self.angleDegrees)),2)) 

        elif face_direction == 270:
            self.maxTurningAngle = 90
            if self.angleDegrees <= 90:
                self.angleDegrees = self.angleDegrees + 0.5
                nx = (x-TURNING_RADIUS) + round(TURNING_RADIUS * math.cos(math.radians(self.angleDegrees)),2)
                ny = (y) - (round(TURNING_RADIUS * math.sin(math.radians(self.angleDegrees)),2)) 

        elif face_direction == 180:
            self.maxTurningAngle = 0
            if self.angleDegrees <= 0:
                self.angleDegrees = self.angleDegrees + 0.5
                nx = (x) + round(TURNING_RADIUS * math.cos(math.radians(self.angleDegrees)),2)
                ny = (y-TURNING_RADIUS) - (round(TURNING_RADIUS * math.sin(math.radians(self.angleDegrees)),2)) 


        elif face_direction == 0:
            self.maxTurningAngle == 0
            self.angleDegrees = abs(self.angleDegrees)
            if self.angleDegrees >= 0:
                self.angleDegrees = self.angleDegrees - 0.5
                nx = (x) - round(TURNING_RADIUS * math.cos(math.radians(self.angleDegrees)),2)
                ny = (y+TURNING_RADIUS) - (round(TURNING_RADIUS * math.sin(math.radians(self.angleDegrees)),2))

        self.rotated = pygame.transform.rotozoom(self.img,self.theta,1)
        self.rect = self.rotated.get_rect(center=(nx,ny))
        return nx,ny,headingAngle

    def turnReverseLeft(self,face_direction,x,y,nx,ny,headingAngle):

        if face_direction == 90:
            self.maxTurningAngle = -90
            if self.angleDegrees >= -90:
                self.angleDegrees = self.angleDegrees - 0.5
                nx = (x-TURNING_RADIUS) + round(TURNING_RADIUS * math.cos(math.radians(self.angleDegrees)),2)
                ny = (y) - (round(TURNING_RADIUS * math.sin(math.radians(self.angleDegrees)),2)) 

        elif face_direction == 270:
            self.maxTurningAngle = 90
            if self.angleDegrees <= 90:
                self.angleDegrees = self.angleDegrees + 0.5
                nx = (x+TURNING_RADIUS) - round(TURNING_RADIUS * math.cos(math.radians(self.angleDegrees)),2)
                ny = (y) - (round(TURNING_RADIUS * math.sin(math.radians(self.angleDegrees)),2)) 

        elif face_direction == 180:
            self.maxTurningAngle = 0
            self.angleDegrees = abs(self.angleDegrees)
            if self.angleDegrees >= 0:
                self.angleDegrees = self.angleDegrees - 0.5
                nx = (x) + round(TURNING_RADIUS * math.cos(math.radians(self.angleDegrees)),2)
                ny = (y+TURNING_RADIUS) - (round(TURNING_RADIUS * math.sin(math.radians(self.angleDegrees)),2)) 

        elif face_direction == 0:
            self.maxTurningAngle == 0
            if self.angleDegrees <= 0:
                self.angleDegrees = self.angleDegrees + 0.5
                nx = (x) - round(TURNING_RADIUS * math.cos(math.radians(self.angleDegrees)),2)
                ny = (y-TURNING_RADIUS) - (round(TURNING_RADIUS * math.sin(math.radians(self.angleDegrees)),2)) 
        
        self.rotated = pygame.transform.rotozoom(self.img,self.theta,1)
        self.rect = self.rotated.get_rect(center=(nx,ny))
        return nx,ny,headingAngle

    def robot_frame(self,pos,rotation):
        rotation = math.radians(rotation)
        n = 80
        centerx,centery=pos
        x_axis=(centerx + n*math.cos(-rotation),centery + n*math.sin(-rotation))
        y_axis=(centerx + n*math.cos(-rotation+math.pi/2),
                centery + n*math.sin(-rotation+math.pi/2))
        pygame.draw.line(self.map,(255,0,0),(centerx,centery),x_axis,3)
        pygame.draw.line(self.map,(0,255,0),(centerx,centery),y_axis,3)

    def set_theta(self,theta):
        self.theta = theta

    
    def move_forward(self):
        moveGridDistance = 0.5
        self.x = self.x + moveGridDistance * (math.cos(math.radians(self.theta)))
        self.y = self.y - (moveGridDistance * (math.sin(math.radians(self.theta))))
        self.rotated = pygame.transform.rotozoom(self.img,self.theta,1)
        self.rect = self.rotated.get_rect(center=(self.x,self.y))  

    def move_backwards(self):
        moveGridDistance = -0.5
        self.x = self.x + (moveGridDistance * (math.cos(math.radians(self.theta))))
        self.y = self.y - (moveGridDistance * (math.sin(math.radians(self.theta))))
        self.rotated = pygame.transform.rotozoom(self.img,self.theta,1)
        self.rect = self.rotated.get_rect(center=(self.x,self.y))  

    

    def robot_domove(self,endstate,turn):
        if turn == "Right":
            self.turnRightFullCircle(endstate)
        elif turn == "Left":
            self.turnLeftFullCircle(endstate)
                        
    
    def expected_face_direction(obstacle):
        if (obstacle.face_direction == 90):
            return 0
        elif (obstacle.face_direction == 180):
            return 90
        elif (obstacle.face_direction == 270):
            return 180
        elif (obstacle.face_direction == 0):
            return 270

    #------------------------------------- Full Circle turn right ------------------------------------------

    def turnRightFullCircle(self,endstate):
        x = self.x
        y = self.y

        if x <= endstate[0]:
            if(self.text == "turnright"):
                self.move_forward()
            elif self.text == "turnrightupmore":
                    if(self.angleDegrees <= 90):
                        self.x_store,self.y_store = self.turnRight_up(x,y)
            elif self.text == "turnrightup":
                if(self.angleDegrees <= 0):
                    if(self.check == True):
                        self.x_store,self.y_store = self.turnRight_bottomleft(x,y)
                else: 
                    if self.check == True:
                        self.x = self.x_store
                        self.y = self.y_store
                        x = self.x
                        y = self.y
                        self.check = False
                        self.text = "turnrightupmore"
        else:
            if self.text == "turnright":
                if(self.angleDegrees >= 0):
                    # if y <= endstate[1]:
                    self.x_store,self.y_store = self.turnRight(x,y)
                else:
                    if self.check == True:
                        self.x = self.x_store
                        self.y = self.y_store
                        x = self.x
                        y = self.y
                        self.check = False
                        self.text = "turnrightdown"
            elif self.text == "turnrightdown":
                if(self.angleDegrees >= -90):
                    if(self.check == False):
                       self.x_store,self.y_store = self.turnRight_downright(x,y)
                else: 
                    if self.check == False:
                        self.x = self.x_store
                        self.y = self.y_store
                        x = self.x
                        y = self.y
                        self.check = True
                        self.text = "turnrightup"

    def turnRight(self,x,y):
        #draws circle
        if self.angleDegrees >= 0:
            self.angleDegrees = self.angleDegrees - 0.5
            self.theta-=0.5
            x = (x) + round(TURNING_RADIUS * math.cos(math.radians(self.angleDegrees)),2)
            y = (y+TURNING_RADIUS) - round(TURNING_RADIUS * math.sin(math.radians(self.angleDegrees)),2)
            self.rotated = pygame.transform.rotozoom(self.img,self.theta,1)
            self.rect = self.rotated.get_rect(center=(x,y))
        return x,y

    #bottom
    def turnRight_up(self,x,y):
        #draws circle
        if self.angleDegrees <= 90:
            self.theta+=0.5
            self.angleDegrees = self.angleDegrees + 0.5
            x = (self.x+TURNING_RADIUS) - round(TURNING_RADIUS * math.cos(math.radians(self.angleDegrees)),2)
            y = (self.y) - round(TURNING_RADIUS * math.sin(math.radians(self.angleDegrees)),2)
            self.rotated = pygame.transform.rotozoom(self.img,self.theta,1)
            self.rect = self.rotated.get_rect(center=(x,y))
            return x,y


    #bottom_right of the circle
    def turnRight_downright(self,x,y):
        #draws circle
        if self.angleDegrees >= -90:
            self.theta-=0.5
            self.angleDegrees = self.angleDegrees - 0.5
            x = (x-TURNING_RADIUS) + round(TURNING_RADIUS * math.cos(math.radians(self.angleDegrees)),2)
            y = (y) - (round(TURNING_RADIUS * math.sin(math.radians(self.angleDegrees)),2))
            self.rotated = pygame.transform.rotozoom(self.img,self.theta,1)
            self.rect = self.rotated.get_rect(center=(x,y))  
        return x,y  

    def turnRight_bottomleft(self,x,y):
        
        #draws circle
        if self.angleDegrees <= 0:
            self.theta = abs(self.theta)
            self.theta-=0.5
            self.angleDegrees = self.angleDegrees + 0.5
            x = (x) - round(TURNING_RADIUS * math.cos(math.radians(self.angleDegrees)),2)
            y = (y-TURNING_RADIUS) - round(TURNING_RADIUS * math.sin(math.radians(self.angleDegrees)),2)
            self.rotated = pygame.transform.rotozoom(self.img,self.theta,1)
            self.rect = self.rotated.get_rect(center=(x,y))  
        return x,y  

    #-------------------------------------- Full Circle turnleft -------------------------------------------

    def turnLeftFullCircle(self,endstate):
        x = self.x
        y = self.y

        if x <= endstate[0]:
            if(self.text == "turnleft"):
                self.move_forward()
            elif self.text == "turnleftdownmore":
                    if(self.angleDegrees >= -90):
                        self.x_store,self.y_store = self.turnLeft_bottomright(x,y)
            elif self.text == "turnleftdown":
                if(self.angleDegrees >= 0):
                    if(self.check == True):
                        self.x_store,self.y_store = self.turnLeft_downleft(x,y)
                else: 
                    if self.check == True:
                        self.x = self.x_store
                        self.y = self.y_store
                        x = self.x
                        y = self.y
                        self.check = False
                        self.text = "turnleftdownmore"
        else:
            if self.text == "turnleft":
                if(self.angleDegrees <= 0):
                    # if y <= endstate[1]:
                    self.x_store,self.y_store = self.turnLeft(x,y)
                else:
                    if self.check == True:
                        self.x = self.x_store
                        self.y = self.y_store
                        x = self.x
                        y = self.y
                        self.check = False
                        self.text = "turnleftup"
            elif self.text == "turnleftup":
                if(self.angleDegrees <= 90):
                    if(self.check == False):
                       self.x_store,self.y_store = self.turnLeft_up(x,y)
                else: 
                    if self.check == False:
                        self.x = self.x_store
                        self.y = self.y_store
                        x = self.x
                        y = self.y
                        self.check = True
                        self.text = "turnleftdown"

    def turnLeft(self,x,y):
        #draws circle
        if self.angleDegrees <= 0:
            self.theta+=0.5
            self.angleDegrees = self.angleDegrees + 0.5
            x = (x) + round(TURNING_RADIUS * math.cos(math.radians(self.angleDegrees)),2)
            y = (y-TURNING_RADIUS) - (round(TURNING_RADIUS * math.sin(math.radians(self.angleDegrees)),2))
            self.rotated = pygame.transform.rotozoom(self.img,self.theta,1)
            self.rect = self.rotated.get_rect(center=(x,y))  
        return x,y  

    #bottom
    def turnLeft_up(self,x,y):
        if self.angleDegrees <= 90:
            self.angleDegrees = self.angleDegrees + 0.5
            self.theta+=0.5
            x = (x-TURNING_RADIUS) + round(TURNING_RADIUS * math.cos(math.radians(self.angleDegrees)),2)
            y = (y) - round(TURNING_RADIUS * math.sin(math.radians(self.angleDegrees)),2)
            self.rotated = pygame.transform.rotozoom(self.img,self.theta,1)
            self.rect = self.rotated.get_rect(center=(x,y))
        return x,y


    #bottom_right of the circle
    def turnLeft_downleft(self,x,y):
        vectors = []
        #draws circle
        if self.angleDegrees >= 0:
            self.theta+=0.5
            self.angleDegrees = self.angleDegrees - 0.5
            x = (x) - round(TURNING_RADIUS * math.cos(math.radians(self.angleDegrees)),2)
            y = (y+TURNING_RADIUS) - (round(TURNING_RADIUS * math.sin(math.radians(self.angleDegrees)),2))
            self.rotated = pygame.transform.rotozoom(self.img,self.theta,1)
            self.rect = self.rotated.get_rect(center=(x,y))  
        return x,y  

    def turnLeft_bottomright(self,x,y):
        #draws circle
        if self.angleDegrees >= -90:
            self.theta+=0.5
            self.angleDegrees = self.angleDegrees - 0.5
            x = (x+TURNING_RADIUS) - round(TURNING_RADIUS * math.cos(math.radians(self.angleDegrees)),2)
            y = (y) - round(TURNING_RADIUS * math.sin(math.radians(self.angleDegrees)),2)
            self.rotated = pygame.transform.rotozoom(self.img,self.theta,1)
            self.rect = self.rotated.get_rect(center=(x,y))  
        return x,y  


    def move(self,initstate,endstate):
        # robot_fd = self.expected_face_direction(endstate)

        if(initstate.x < endstate.x):
            self.move_straight()
        elif(initstate.x > endstate.x):
            self.turnRight_bottomleft(self.x,self.y)
        else:
            self.turnRight(self.x,self.y)

    def addToQueue(self,command,direction,distance):
        self.movementList.append(command)
        self.directionList.append(direction)
        self.distanceList.append(distance)

    def getDirection(curDirection):
        if(curDirection == 0):
            return 'E'
        elif(curDirection == 90):
            return 'N'
        elif(curDirection == 180):
            return 'W'
        elif(curDirection == 270):
            return 'S'
        return None
    
    def getRelativeDirection(self,robot,dest):
        twoTurnDistance = 2*TURNING_RADIUS
        if(-self.gap //2 <= dest.x) and (self.gap // 2 >= dest.x):
            if(dest.y <=0):
                return "RIGHT"
            elif (dest.y <=0):
                return "BACK"
        elif (-twoTurnDistance >= dest.y):
            if (dest.x <= twoTurnDistance and dest.x >= 0):
                return "FRONT_SLIGHT_RIGHT"
            elif (dest.x >= -twoTurnDistance and dest.x <= 0):
                return "FRONT_SLIGHT_LEFT"
            elif (dest.getX() >= 0):
                return "FRONT_RIGHT"
            elif (dest.getX() <= 0):
                return "FRONT_LEFT"
        elif (twoTurnDistance <= dest.y):
            # // point is behind
            if (dest.x <= twoTurnDistance and dest.x >= 0):
                # // difference between x less than two turn
                return "BACK_SLIGHT_RIGHT"
            elif (dest.x >= -twoTurnDistance and dest.x <= 0):
                return "BACK_SLIGHT_LEFT"
            elif (dest.x >= 0):
                return "BACK_RIGHT"
            elif (dest.x <= 0):
                return "BACK_LEFT"
            
        elif (abs(dest.y) < twoTurnDistance):
            # // within the 2 turn margin of front and back
            if (0 <= dest.x):
                return "CENTER_RIGHT"
            elif (0 >= dest.x):
                return "CENTER_LEFT"

    def addCommand(self,command):
        c = command.charAt(0)
        other = []
        # double dist;
        currDirection = self.theta
        # Direction dir = Direction.NONE;

        if c == "w":
    
            # what it seems is that, the programmer concatenate the command and the dist together
            # other = new char[10];
            # command.getChars(1, command.length(), other, 0);
            # dist = Double.parseDouble(new String(other)) * this.ENVIRONMENT_SCALING_FACTOR;
            # this.getDurationForManeuver(dist) - dist/speed
            # dist - is the real distance
            # this.addToQueue("Forward", this.getDurationForManeuver(dist), Direction.NONE, dist);
            self.addToQueue("Forward",0,None,None)
        elif c == "s":
            self.addToQueue("Reverse", 0, None, None)
        elif c == 'a':
            dir = self.getDirection(currDirection)
    
            self.addToQueue("Left", 1, None, -1)
            self.addToQueue("LF", 1000, dir, -1)
            self.addToQueue("Center", 1, None, -1)
        elif c == 'd':
            dir = self.getDirection(currDirection)
            
            self.addToQueue("Right", 1, None, -1)
            self.addToQueue("RF", 1000, dir, -1)
            self.addToQueue("Center", 1, None, -1)

    def printGeneratedMovements(self):
        for i in range(0,len(self.movementList)):
            print("================================")
            print(self.movementList[0])
            print(self.directionList[0])
            print("================================")

    def getEuclideanDistance(a, b):
        return math.sqrt(math.pow(abs(a.x - b.x), 2) + math.pow(abs(a.y - b.y), 2))
    
    
    #can use this function to straighten the car after a turn
    def getCurrentDirection(self):
        if (abs(self.angleDegrees - (-90)) <= DIRECTION_MARGIN_OF_ERROR):
            return 'N'
        elif (abs(self.angleDegrees - (90)) <= DIRECTION_MARGIN_OF_ERROR):
            return 'S'
        elif (abs(self.angleDegrees) <= DIRECTION_MARGIN_OF_ERROR):
            return 'E'
        elif (abs(self.angleDegrees - 180) <= DIRECTION_MARGIN_OF_ERROR
                or abs(self.angleDegrees - (-180)) <= DIRECTION_MARGIN_OF_ERROR):
            return 'W'
        return None

    # def generateMovements(plannedPath, orderedObsIds) {
    #     this.movementQueue.clear();
    #     this.durationQueue.clear();
    #     this.directionQueue.clear();
    #     this.distanceQueue.clear();
    #     boolean justTurned = false;
    #     double dist;
    #     int obsCounter = 0;
    #     for (int i = 1; i < plannedPath.size(); i++) {
    #         MyPoint src = plannedPath.get(i - 1);
    #         MyPoint dest = plannedPath.get(i);
    #         if (dest.getDirection() == Direction.NONE) {
    #             this.addToQueue("Reached", 1, Direction.NONE,
    #                     orderedObsIds[obsCounter] * this.ENVIRONMENT_SCALING_FACTOR);
    #             obsCounter++;
    #             continue;
    #         }
    #         if (src.getDirection() == Direction.NONE) {
    #             src = plannedPath.get(i - 2);
    #         }
    #         switch (this.getRelativeOrientation(src, dest)) {
    #             case NORTH:
    #                 dist = this.getEuclideanDistance(src, dest);
    #                 if (justTurned) {
    #                     dist -= this.MAX_TURNING_RADIUS;
    #                     justTurned = false;
    #                 }
    #                 switch (this.getRelativeDirection(src, dest)) {
    #                     case BACK:
    #                         if (dist > 0) {
    #                             this.addToQueue("Reverse", this.getDurationForManeuver(dist), Direction.NONE, dist);
    #                         } else {
    #                             this.addToQueue("Forward", this.getDurationForManeuver(-dist), Direction.NONE, -dist);
    #                         }
    #                         justTurned = false;
    #                         break;
    #                     case FRONT:
    #                         if (dist > 0) {
    #                             this.addToQueue("Forward", this.getDurationForManeuver(dist), Direction.NONE, dist);
    #                         } else {
    #                             this.addToQueue("Reverse", this.getDurationForManeuver(-dist), Direction.NONE, -dist);
    #                         }
    #                         justTurned = false;
    #                         break;
    #                     case NONE:
    #                         break;
    #                     default:
    #                         break;
    #                 }
    #                 break;
    #             case SOUTH:
    #                 // dist = this.getEuclideanDistance(src, dest);
    #                 // this.addToQueue("Reverse", this.getDurationForManeuver(dist));
    #                 break;
    #             case EAST:
    #                 dist = this.getEuclideanDistance(src, dest);
    #                 dist -= this.MAX_TURNING_RADIUS;
    #                 if (justTurned) {
    #                     dist -= this.MAX_TURNING_RADIUS;
    #                     justTurned = false;
    #                 }
    #                 if (dist > 0) {
    #                     this.addToQueue("Forward", this.getDurationForManeuver(dist), Direction.NONE, dist);
    #                 } else {
    #                     this.addToQueue("Reverse", this.getDurationForManeuver(-dist), Direction.NONE, -dist);
    #                 }
    #                 this.addToQueue("Right", 1, Direction.NONE, -1);
    #                 this.addToQueue("RF", 1000, dest.getDirection(), -1);
    #                 this.addToQueue("Center", 1, Direction.NONE, -1);
    #                 justTurned = true;
    #                 break;
    #             case WEST:
    #                 dist = this.getEuclideanDistance(src, dest);
    #                 dist -= this.MAX_TURNING_RADIUS;
    #                 if (justTurned) {
    #                     dist -= this.MAX_TURNING_RADIUS;
    #                     justTurned = false;
    #                 }
    #                 if (dist > 0) {
    #                     this.addToQueue("Forward", this.getDurationForManeuver(dist), Direction.NONE, dist);
    #                 } else {
    #                     this.addToQueue("Reverse", this.getDurationForManeuver(-dist), Direction.NONE, -dist);
    #                 }
    #                 this.addToQueue("Left", 1, Direction.NONE, -1);
    #                 this.addToQueue("LF", 1000, dest.getDirection(), -1);
    #                 this.addToQueue("Center", 1, Direction.NONE, -1);
    #                 justTurned = true;
    #                 break;
    #             case NONE:
    #                 break;
    #             default:
    #                 break;

    #         }

    #     }
    # }
    
    
    
        
        
