# CZ3004 MDP Algo
### Brief Description of the Project
My team is required to build a robot that navigates through the obstacles. For each obstacle, an image is pasted on one of the side. The robot is then required to detect the symbol shown in the image. After scanning all the images found in each obstacle, the robot has completed the task successfully. All the symbols detected is updated on the map displayed in the Android Tablet.    

<img width="476" alt="image" src="https://user-images.githubusercontent.com/90826642/236824646-bf82e7b1-966a-45d4-a7d7-95e8f9782f66.png">

1. The map is plotted using an Android tablet and coordinates of the obstacles are sent to the RPI via bluetooth
2. The coordinates of each obstacles are then received by the algorithm server
3. The algorithm generates the robot movements for an optimal path from the current coordinate to the coordinate of an obstacle and is sent to the RPI
4. The RPI then sents the generated movements to the STM
5. The STM will perform the movements and inform the RPI that the robot has reached its destination afterwards which the camera of the robot is situated in front of the image of the obstacle
6. RPI then activates the camera and takes a picture of the image
7. The image is then submitted to the image recognition server
8. Once a symbol has been recognised from the image, the recognised symbol will then be sent back to the RPI
9. Finally, the recognised symbol is updated in the map 

Steps 3 - 9 are then repeated till the robot has reached its final obstacle.

### Brief explanation of the algorithm used
<p>A* algorithm is used to generate an optimal path from the current destination to the next destination. A virtual environment is created to simulate the robot movements to test the algorithm before integrating it with the rest of the components. </p>

<p>Pygame is used to build the virtual environment.</p>

<img width="451" alt="image" src="https://user-images.githubusercontent.com/90826642/236814082-a0082260-aa63-4d69-9a72-7f9a195d30c1.png">
