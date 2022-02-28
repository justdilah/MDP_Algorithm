GAP = 30
class Paths:
    def __init__(self):
        self.paths = []
        # self.pathsForAndroid = []

    def addPath(self,movements):
        pathsForAndroid = []
        for i in range(0,len(movements)):
            x = movements[i][0][0]
            y = movements[i][0][1]
            x = x - (GAP//2)
            y = y - (GAP//2)
            # y = 19 - y
            row = (x // 30) + 0.5

            #in pygame y = 0 starts from the top and not from the bottom 
            #hence, it is required to convert it for the android 
            col = (y // 30)
            col = (19 - col) + 0.5
            # row,col = self.getRowAndColForAndroid(int(x),int(y))
            self.paths.append(movements[i])
            pathsForAndroid.append((row,col,movements[i][2]))
        return pathsForAndroid

    def printPath(self):
        for i in range(0,len(self.paths)):
            print(self.paths[i])
    


    # def getRowAndColForAndroid(x,y):
    #     # print(x)
    #     x = x - GAP
    #     y = y - GAP
    #     row = y / 30
    #     col = x / 30
    #     return row,col  

