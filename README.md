# CZ3004 MDP Algo
### Brief Description of the Project
A team is required to build a robot that navigates through the obstacles. For each obstacles, an image is pasted on one of the side. The robot is then required to read the image and update the map in the tablet.  

<img width="476" alt="image" src="https://user-images.githubusercontent.com/90826642/236824646-bf82e7b1-966a-45d4-a7d7-95e8f9782f66.png">

1. The map is plotted using an Android tablet by a teammate and is sent to the RPI via bluetooth
2. The coordinates of each obstacles are then sent to the algorithm server
3. The algorithm generates the robot movements for an optimal path to reach to a obstacle and is sent to the RPI
4. The RPI then sents the generated movements to the STM
5. The STM will then inform the RPI that the robot has reached its destination which the camera of the robot is situated in front of the image of the obstacle
6. RPI then activates the camera and takes a picture of the image
7. The image is then submitted to the image recognition server
8. Once a symbol has been recognised from the image, the recognised symbol will then be sent back to the RPI
9. Finally, the recognised symbol is updated in the map

Steps 3 - 9 are then repeated till the robot has reached its final obstacle.

### Brief explanation of the algorithm used
<p>A* algortihm is used to generate an optimal path from the current destination to the next destination. A virtual environment is created for to simulate the robot movements to test the algorithm before integrating it with the rest of the components. </p>

<p>Pygame is used to build the virtual environment.</p>

<img width="451" alt="image" src="https://user-images.githubusercontent.com/90826642/236814082-a0082260-aa63-4d69-9a72-7f9a195d30c1.png">
