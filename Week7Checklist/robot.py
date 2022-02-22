from turtle import heading
import pygame
import math
from time import *

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

    # #Left
    # def setAngleDegrees(self,face_direction):
    #     if face_direction == 90:
    #         self.angleDegrees = 0

    #     elif face_direction == 0:
    #         self.angleDegrees = -90

    #     elif face_direction == 180:
    #         self.angleDegrees = -90

    #     elif face_direction == 270:
    #         self.angleDegrees = 0

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
    
        
        
