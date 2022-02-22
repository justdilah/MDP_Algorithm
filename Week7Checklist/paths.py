class Paths:
    def __init__(self):
        self.paths = []

    def addPath(self,movements):
        for i in range(0,len(movements)):
            self.paths.append(movements[i])

    def printPath(self):
        for i in range(0,len(self.paths)):
            print(self.paths[i])
