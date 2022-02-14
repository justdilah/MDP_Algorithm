import math

class Direction:
    def rotateRight90(curDirection):
        if(curDirection == 0):
            return 'S'
        elif(curDirection == 90):
            return 'E'
        elif(curDirection == 180):
            return 'N'
        elif(curDirection == 270):
            return 'W'
        return None

    def rotateLeft90(curDirection):
        if(curDirection == 0):
            return 'N'
        elif(curDirection == 90):
            return 'W'
        elif(curDirection == 180):
            return 'S'
        elif(curDirection == 270):
            return 'E'
        return None
        