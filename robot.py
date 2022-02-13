from tkinter import CENTER
import pygame
import math
from time import *


# from pathfinding import ActionStraight
from testing_sf import RRTGraph
from testing_sf import RRTMap
import numpy as np


class State:
    def __init__(self,x,y,face_direction,prev_state):
        self.x = x
        self.y = y
        self.face_direction = face_direction 
        self.prev_state = prev_state

MAX_TURNING_ANGLE = 35.94
THETA_WHEELS_DEGREE = 0
directionInDegrees = -90
TURNING_RADIUS = 40
TURNING_ANGLE_DEGREE = 0
thetaWheelsDegree = 0
CHECK = True

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
        self.angleDegrees = 90
        self.delta_ang = math.pi/180
        self.check = True
        self.text ="turnright"
        angleChangePerClick = 5

        self.theta = 0
        camera_orientation = self.theta + math.radians(90)

        self.vl = 0.01 * self.m2p 
        self.vr = 0.01 * self.m2p

        self.maxspeed = 0.02 * self.m2p
        self.minspeed =-0.02 * self.m2p

        MAX_TURNING_RADIUS = abs(self.distanceBetweenFrontBackWheels / math.tan(math.radians(MAX_TURNING_ANGLE)))

        self.img = pygame.image.load(robotImg)

        self.rotated = pygame.transform.rotozoom(self.img,math.degrees(self.theta),1)

        #pygame creates a new rect with the size of the image and the x,y coordinates
        self.rect = self.rotated.get_rect(center=(self.x,self.y))

    def draw(self,map):
        map.blit(self.rotated,self.rect)
    
    def move90(self):
        pass

    def robot_frame(self,pos,rotation):
        n = 80
        centerx,centery=pos
        x_axis=(centerx + n*math.cos(-rotation),centery + n*math.sin(-rotation))
        y_axis=(centerx + n*math.cos(-rotation+math.pi/2),
                centery + n*math.sin(-rotation+math.pi/2))
        pygame.draw.line(self.map,(255,0,0),(centerx,centery),x_axis,3)
        pygame.draw.line(self.map,(0,255,0),(centerx,centery),y_axis,3)

    def set_theta(self,theta):
        self.theta = theta

    
    def move_straight(self):
        moveGridDistance = 0.5
        self.x = self.x + moveGridDistance * (math.cos(math.radians(self.theta)))
        self.y = self.y - (moveGridDistance * (math.sin(math.radians(self.theta))))
        self.rotated = pygame.transform.rotozoom(self.img,math.degrees(0),1)
        self.rect = self.rotated.get_rect(center=(self.x,self.y))       

    def robot_domove(self,endstate):
        x = self.x
        y = self.y 
        
        if x <= 405:
            if(self.text == "turnright"):
                self.move_straight()
            else:
                if self.text == "turnrightupmore":
                    if(self.angleDegrees <= 90):
                        self.x_store,self.y_store = self.turnRight_up(x,y)
        else:
            if self.text == "turnright":
                if(self.angleDegrees >= 0):
                    if y <= 105:
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
            
            elif self.text == "turnrightupmore":
                pass

    def move(self,initstate,endstate):
        # robot_fd = self.expected_face_direction(endstate)

        if(initstate.x < endstate.x):
            self.move_straight()
        elif(initstate.x > endstate.x):
            self.turnRight_bottomleft(self.x,self.y)
        else:
            self.turnRight(self.x,self.y)

                
    def expected_face_direction(obstacle):
        if (obstacle.face_direction == 90):
            return 0
        elif (obstacle.face_direction == 180):
            return 90
        elif (obstacle.face_direction == 270):
            return 180
        elif (obstacle.face_direction == 0):
            return 270
        # return (obstacle.face_direction + 180) % 360
            
    
    def move90(self,dt):
            self.vl=0.035 * self.m2p
            self.x+=((self.vl+self.vr)/2)*math.cos(self.theta) *dt
            self.y-=((self.vl+self.vr)/2)*math.sin(self.theta) *dt
            self.theta+=(self.vr - self.vl) / self.w *dt

            self.rotated = pygame.transform.rotozoom(self.img,math.degrees(self.theta),1)
            self.rect = self.rotated.get_rect(center=(self.x,self.y))

            return self.x,self.y

        
    class Vertex:
        def __init__(self,x,y):
            self.x = x 
            self.y = y

    def turnRight(self,x,y):
        #draws circle
        if self.angleDegrees >= 0:
            self.angleDegrees = self.angleDegrees - 0.5
            self.theta-=0.5
            x = (x) + round(60 * math.cos(math.radians(self.angleDegrees)),2)
            y = (y+60) - round(60 * math.sin(math.radians(self.angleDegrees)),2)
            self.rotated = pygame.transform.rotozoom(self.img,self.theta,1)
            self.rect = self.rotated.get_rect(center=(x,y))
            print("dadsa")
        return x,y

    #bottom
    def turnRight_up(self,x,y):
        #draws circle
        if self.angleDegrees <= 90:
            self.theta+=0.5
            self.angleDegrees = self.angleDegrees + 0.5
            x = (self.x+60) - round(60 * math.cos(math.radians(self.angleDegrees)),2)
            y = (self.y) - round(60 * math.sin(math.radians(self.angleDegrees)),2)
            print(x)
            print(y)
            self.rotated = pygame.transform.rotozoom(self.img,self.theta,1)
            self.rect = self.rotated.get_rect(center=(x,y))
            return x,y


    #bottom_right of the circle
    def turnRight_downright(self,x,y):
        vectors = []
        #draws circle
        if self.angleDegrees >= -90:
            self.theta-=0.5
            self.angleDegrees = self.angleDegrees - 0.5
            x = (x-60) + round(60 * math.cos(math.radians(self.angleDegrees)),2)
            y = (y) - (round(60 * math.sin(math.radians(self.angleDegrees)),2))
            # print(x)
            # print(y)
            self.rotated = pygame.transform.rotozoom(self.img,self.theta,1)
            self.rect = self.rotated.get_rect(center=(x,y))  
        return x,y  

    def turnRight_bottomleft(self,x,y):
        #draws circle
        # print("FUCK")
        if self.angleDegrees <= 0:
            self.theta+=0.5
            self.angleDegrees = self.angleDegrees + 0.5
            x = (x) - round(60 * math.cos(math.radians(self.angleDegrees)),2)
            y = (y-60) - round(60 * math.sin(math.radians(self.angleDegrees)),2)
            print(x)
            print(y)
            self.rotated = pygame.transform.rotozoom(self.img,self.theta,1)
            self.rect = self.rotated.get_rect(center=(x,y))  
        return x,y  

class ActionStraight: 
        def __init__(self,travelDistGrid):
            self.travelDistGrid = travelDistGrid
            self.cost = 1
        
        def takeAction(self,initstate):
            moveGridDistance = self.travelDistGrid
            x = initstate.x
            y = initstate.y

            x += moveGridDistance*(int)(math.cos(initstate.face_direction))
            y -= moveGridDistance*(int)(math.sin(initstate.face_direction))
            # print(x,y)
            state = State(x,y,initstate.face_direction,initstate)
            return state

class ActionTurn90Right:
    def __init__(self):
        self.travelDistGrid = 0.05
        self.cost = 1

    def takeAction(self,initstate):  
        faceDirection = math.degrees(initstate.face_direction)
        x = initstate.x
        y = initstate.y

        if faceDirection == 0:
            x+=90
            y+=90
        elif faceDirection == 90:
            x+=90
            y-=90
        elif faceDirection == 180:
            x-=90
            y-=90
        elif faceDirection == 270:
            x-=90
            y+=90

        faceDirection = (faceDirection - 90 + 360) % 360
        endState = State(x,y,faceDirection,initstate)
        # print(x)
        return endState

class ActionTurn90Left: 
    def __init__(self):
        self.travelDistGrid = 0.05
        self.cost = 1
        
    def takeAction(self,initstate):
        faceDirection = math.degrees(initstate.face_direction)
        x = initstate.x
        y = initstate.y

        if faceDirection == 0:
            x+=90
            y-=90
        elif faceDirection == 90:
            x-=90
            y-=90
        elif faceDirection == 180:
            x-=90
            y+=90
        elif faceDirection == 270:
            x-=90
            y+=90

        faceDirection = (faceDirection + 90 + 360) % 360
        endState = State(x,y,faceDirection,initstate)
        return endState

class ActionReverse90right:
    def __init__(self):
        self.travelDistGrid = 0.05
        self.cost = 1

    def takeAction(self,initstate):
        faceDirection = math.degrees(initstate.face_direction)
        x = initstate.x
        y = initstate.y

        if faceDirection == 0:
            x-=90
            y+=90
        elif faceDirection == 90:
            x+=90
            y+=90
        elif faceDirection == 180:
            x+=90
            y-=90
        elif faceDirection == 270:
            x+=90
            y-=90

        faceDirection = (faceDirection + 90 + 360) % 360
        endState = State(x,y,faceDirection,initstate)
        return endState

# class ActionReverse90left:
#     def __init__(self):
#         self.travelDistGrid = 0.05
#         self.cost = 1

#     def takeAction(self,initstate):
#         faceDirection = math.degrees(initstate.face_direction)
#         x = initstate.x
#         y = initstate.y

#         if faceDirection == 0:
#             x-=90
#             y-=90
#         elif faceDirection == 90:
#             x-=90
#             y+=90
#         elif faceDirection == 180:
#             x+=90
#             y+=90
#         elif faceDirection == 270:
#             x-=90
#             y-=90

#         faceDirection = (faceDirection - 90 + 360) % 360
#         endState = State(x,y,faceDirection,initstate)
#         return endState
            

        
