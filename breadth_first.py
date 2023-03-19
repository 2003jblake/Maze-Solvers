'''This module defines the functions used to solve the mazes given using Breadth first traveresal'''
import time

import numpy as np



def read_maze(filepath):
    '''This takes in a filepath to a maze.
    Returns a maze where each row is a list item in an array
    Removes any newline characters and empty lines'''

    maze_matrix = []

    with open(filepath, encoding="utf-8") as file:
        for item in file:
            if item == '\n':
                break
            maze_matrix.append(list(item.replace('\n', '').replace(' ', '')))
        

    return maze_matrix

def find_start(maze_matrix):
    '''This returns the x index of the start node of the array given that 
    the start is always on the top row'''

    for index, char in enumerate(maze_matrix[0]):

        if char == '-':
            return index

    return -1

def find_end(maze_matrix):
    '''This returns the x index of the start node of the array given that
    the start is always on the bottom row'''

    for index, char in enumerate(maze_matrix[-1]):
        if char == '-':
            return index

    return -1

def valid_move(possible_move_cords, maze_matrix):
    '''This checks if is a move is possible based on the cordinates of the wanted move.
    takes in a tuple of two coordinates and returns true if move is valid false otherwise
    First checks if move is in bounds, then if the node is a path node that hasnt been visited
    repersented by F'''

    if possible_move_cords[0] < 0 or possible_move_cords[1] < 0:
        return False
    if (possible_move_cords[0] > (len(maze_matrix[0])-1) 
            or possible_move_cords[1] > (len(maze_matrix)-1)):
        return False

    if maze_matrix[possible_move_cords[1]][possible_move_cords[0]] == '-':
        return True

    return False

def find_next_position(current_position, maze_matrix):
    '''This finds the next move, trys in order of North, East, South, West returning the
    first possible valid move. Returns False if there are no valid moves from the
    current position. Else returns the coordinates of the move'''

    directions = ([0, -1],  [1, 0], [0, 1], [-1, 0])

    next_list = []
    for direction in directions:
        if valid_move([current_position[0] + direction[0],
                        current_position[1] + direction[1]], maze_matrix):

            next_list.append([current_position[0] + direction[0],
                            current_position[1] + direction[1]])

    if len(next_list) != 0:
        return next_list

    return False

def draw_path_to_file(route_list, maze_matrix):
    '''This takes the route and draws the path repersented P as in the path, V for visited.
     Saves to output.txt'''

    for index in route_list:
        maze_matrix[index[1]][index[0]] = 'P'

    for y_cord, row in enumerate(maze_matrix):
        for x_cord, _ in enumerate(row):
            if isinstance(maze_matrix[y_cord][x_cord], list):

                maze_matrix[y_cord][x_cord] = 'V'

    np.savetxt('maze-drawing.txt', maze_matrix, fmt='%s')




def  breadth_first_solve(maze_matrix):
    '''This peforms breadth first search to find the end path and the resulting path.
    Takes in the 2d list maze rpersentation. Returns the route, number of nodes explored 
    and an updated version of the maze array repsenting the path and nodes explored. if 
    no paths were foudn this returns just the nodes explroed'''


    #find start and end nodes
    start = find_start(maze_matrix)
    end = find_end(maze_matrix)
    end_goal_cord = [end, len(maze_matrix)-1]
    if start == -1 or end == -1:
        print("Maze is invalid, the start must be in the top row and the end must be bottom row")

    #initalize variables
    route_queue = []

    nodes_visited = 0
    nodes_found = 0

    #add the start to the queue and mark as vistided
    route_queue.append([start, 0])
    maze_matrix[0][start] = 'V'

    nodes_found += 1

    while route_queue:

        #get the node to explore from, from the queue
        current_position = route_queue.pop(0)
        nodes_visited += 1

        #check if current position is the end node
        if current_position == end_goal_cord:


            #back track through the nodes getting the parent nodes to form the route
            route_list = []
            while current_position != [start, 0]:
                route_list.append(current_position)
                current_position = maze_matrix[current_position[1]][current_position[0]]

            route_list.append(current_position)

            return route_list, nodes_visited, nodes_found, maze_matrix


        neighbours_list = find_next_position(current_position, maze_matrix)

        #if next is false, there are no more possible moves, so need to back track
        while neighbours_list is False:

            #if queue is empty, there is no where else to explore and no path was found
            if not route_queue:
                return nodes_visited, nodes_found

            #go to next node to explore and explore unexplored paths,
            current_position = route_queue.pop(0)

            neighbours_list = find_next_position(current_position, maze_matrix)

        for move in neighbours_list:
            route_queue.append(move)
            nodes_found += 1

            #set the position of the neighbour to the current position
            # to keep track of where we came from
            maze_matrix[move[1]][move[0]] = current_position
            

    #If we got to here, there are no more loads left to explore, path not found
    return nodes_visited, nodes_found



if __name__ == "__main__":

    MAZE_LOCATION = input('Please enter location of the maze file you would like to use:   ')

    #starts timer, calls the functions to solve the maze then ends timer.
    startTime = time.time()

    maze = read_maze(MAZE_LOCATION)
    return_array = breadth_first_solve(maze)

    endTime = time.time()

    timeElapsed = endTime - startTime


    #if path is not found
    if len(return_array) == 2:

        print(' <-=[STATS]=->')
        print("    ! No path was found !")
        print('    Algorithim - Breadth First Search')
        print(f'    File - {MAZE_LOCATION}')
        print(f'    Time of execution - {timeElapsed}')
        print(f'    Nodes Explored - {return_array[0]}')
        print(f'    Nodes Found - {return_array[1]}')

    #path has been found
    else:
        route, num_nodes_visited, num_nodes_found, matrix_array = return_array

        draw_path_to_file(route, matrix_array)
        
        with open('path.txt', 'w', encoding="utf-8") as coords:
            for coord in route:
                coords.write("%s\n" % coord)

        print('Route:')
        print(route)
        print(' <-=[STATS]=->')
        print('    Algorithim - Breadth First Search')
        print(f'    File - {MAZE_LOCATION}')
        print(f'    Time of Algorithm Execution - {timeElapsed}')
        print(f'    Nodes Explored - {num_nodes_visited}')
        print(f'    Nodes Found - {num_nodes_found}')
        print(f'    Nodes in Path - {len(route)}')
        print(f'    Steps in Path - {len(route) -1}')
