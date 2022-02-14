import math
from robot import Robot

TURNING_RADIUS = 20

class Path:
    def __init__(self):
        self.shortestpath = []
        self.orderedObsIds = []
        self.plannedpath = []

    def getShortestPath(self,grid, robot, flipObstacleDirections):
        # this.reset()
        # this.polygon.reset();
        src = (robot.x,robot.y)
        inputs = grid.getObstacleFronts()
        obsIds = grid.getObstacleIDs()
        n = len(inputs)

        #  adds origin and all input points into single ArrayList
        pointList = []
        pointList.append(src)
        for i in range(0,n):
            pointList.append(inputs[i])

        # pointsArray = pointList.toArray(new MyPoint[0]);

        # // get adjacency matrix to be used for shortest path algo
        # double[][] adjacencyMatrix = getAdjacencyMatrix(pointsArray);
        # printAdjacencyMatrix(adjacencyMatrix);

        # use whichever algo you want here
        #  eg, return [1, 4, 2, 3] means go to
        #  1st -> 4th -> 2nd -> 3rd node of pointsArray
        #  pointsArray[0] -> pointsArray[3] -> pointsArray[1] -> pointsArray[2]
        # shortestPathPointIndex = getShortestPathWithChecking(pointList, grid, robot)

        # ////
        # // obsID = [2,4,3] ids of obstacles in same order as pointsArray
        # // pointsArray = [robot, obs2, obs4, obs3]

        # // create new Point[] to be returned
        # shortestpath = []
        # MyPoint[] shortestPath = new MyPoint[n + 1];
        # orderedObsIds = []
        # ArrayList<Integer> orderedObsIds = new ArrayList<>();
        # // int[] orderedObsIds = new int[n];
        # for (int i = 0; i < n + 1; i++) {
        #     shortestPath[i] = pointsArray[shortestPathPointIndex[i]];
        #     if (i == 0) {
        #         continue;
        #     }
        #     orderedObsIds.add(obsIds[shortestPathPointIndex[i] - 1]);
        # }

        # # this.repaint();

        # self.shortestPath = shortestPath;
        # this.orderedObsIds = orderedObsIds.stream().mapToInt(i -> i).toArray();
        # return shortestPath;
    

    # def generatePlannedPath(self,grid, robot):
    #     isValid = True
    #     workingPath = []
    #     self.plannedpath.append((robot.x,robot.y))
    #     turnradius2 = (int) (TURNING_RADIUS * 2)
    #     turnradius1 = (int) (TURNING_RADIUS)
        

