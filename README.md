Requirements:
    numpy

General:

    How to run each algorithm.

        -Run the python file of the corresponding algorithm you would like to use from the terminal
        -You will be prompted to enter the location of the maze file you would like to use, enter location
        -The code will then run, and print to the terminal the path and some statisics
        -A file will also be created called maze-drawing.txt. This has the maze with 'P' now repersenting the path,
         V repersenting any visited nodes, and F repersenting found nodes
        -There will also be another file created listing the coordinates in the path using the below definition for the coordinate system



    !Understanding the path!

        the path consists of x and y coordinates treating the maze as a grid. The upper left is the orign [0,0] coordinate
        and thus if you move down one row the coordinate is now [x, y+1] etc.

    
    Algorithm variations.

        depth_first.py

            In this file you can change the order of traversal directions, this can give significant speedup
            as we know the end goal is down and the the right, so if we try and go in these directions first 
            it goes faster. But depth_first is more traditionaly taught going from one side of the graph to 
            the other

            To chagne the order of directions
                
                in lines 59, 60 comment out the order you dont want to use, make sure to uncomment the one you do
                59 - traditional go as far to the right of the maze first
                60 - optimized try and head straight for the end goal, by going down (default)

            
        A_star.py

            In this file you can change the different heuristics used. This means you can change how the algorithm
            behaves dependent on the use case. The four heuristics implemented are as follows. All are opptimal
            except for calc_manhattan_dist_unoptimal()

                line 94 - calc_euclidiean_dist() - uses euclidiean distance as the heuristic function   (optimal)
                line 101 - calc_manhattan_dist() - uses manhattan distance as the heuristic function   (optimal)(default)
                line 108 - calc_manhattan_dist_unoptimal() - uses manhattan distance * 10 as the heuristic function   (fast)
                line 116 - convert_to_dijkstras() - gets rid of the heuristic function, converting the algorithm to dijkstras   (optimal)

            To use the different heuristics;

                change the function used in lines 154, 220. (note: keep arguments the same)



    Excepted Maze formats.

        The maze formats should be kept the same as the example mazes given. # repersent a wall and - a traversable node.