'''This module defines the functions used to solve the mazes given using depth first traveresal'''
import time

import numpy as np

def read_maze(filepath):
    '''This takes in a filepath for a maze file.
    Returns a maze_matrix where each row is a list item in an array
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
    '''This returns the y index of the wnsnode of the array given that
    the end is always on the bottom row'''
    for index, char in enumerate(maze_matrix[-1]):
        if char == '-':
            return index

    return -1

def valid_move(possible_move_cords, maze_matrix):
    '''This checks if is a move is possible based on the cordinates of the wanted move.
    takes in a list of two coordinates and returns true if move is valid, false otherwise
    Checks the move destination is in bounds and not a wall'''
    try:
        if maze_matrix[possible_move_cords[1]][possible_move_cords[0]] == '-':
            return True
    except IndexError:
        return False

    return False

def find_next_position(current_position, maze_matrix):
    '''This finds the next move, trys in order of North, East, South, West or S,E,W,N
    depending on which line is commented out. (second is more optimal as it trys to go down first)
    Returns the first possible valid move. Returns False if there are no valid moves from the
    current current_position. Else returns the coordinates of the move'''

    #directions = ([0, -1],  [1, 0], [0, 1], [-1, 0])
    directions = ([0, 1], [1, 0], [-1, 0], [0, -1])

    for direction in directions:

        if valid_move([current_position[0] + direction[0],
                        current_position[1] + direction[1]], maze_matrix):

            return [current_position[0] + direction[0], current_position[1] + direction[1]]

    return False

def draw_path_to_file(route_list, maze_matrix):
    '''This takes the route and draws the path repersented P as in the path, V for visited, 
    which should already be set. Saves to output.txt'''

    for index in route_list:
        maze_matrix[index[1]][index[0]] = 'P'

    np.savetxt('maze-drawing.txt', matrix_array, fmt='%s')




def  depth_first_solve(maze_matrix):
    '''This peforms depth first search. Takes in the 2d list maze repersentation.
    Returns the route, number of nodes explored and an updated version of the maze array
    repersenting the path and nodes explored. If no paths were found this returns just the 
    nodes explored'''


    #find start and end nodes
    start = find_start(maze_matrix)
    end = find_end(maze_matrix)
    end_goal_cord = [end, len(maze_matrix)-1]

    if start == -1 or end == -1:
        print("maze_matrix is invalid,"
        " the start must be in the top row and the end must be bottom row")

    #initalize variables
    route_stack = []
    nodes_visited = 0
    nodes_found = 0

    route_stack.append([start, 0])
    maze_matrix[0][start] = 'V'
    nodes_found += 1

    while route_stack:

        current_position = route_stack[-1]
        nodes_visited += 1

        #check if current current_position is the end node
        if current_position == end_goal_cord:

            return route_stack, nodes_visited, nodes_found, maze_matrix

        next_position = find_next_position(current_position, maze_matrix)

        #if next is false, there are no more possible moves, so need to back track
        while next_position is False:

            #go to previous node and explore unexplored paths,
            route_stack.pop()

            #check route stack is not empty
            #if it is we have explored all possible nodes and there is no path
            if not route_stack:
                return [nodes_visited, nodes_found]

            current_position = route_stack[-1]

            next_position = find_next_position(current_position, maze_matrix)


        maze_matrix[next_position[1]][next_position[0]] = 'V'
        nodes_found += 1


        route_stack.append(next_position)

    #If we got to here, there are no more loads left to explore, path not found
    return [nodes_visited, nodes_found]


if __name__ == "__main__":

    MAZE_LOCATION = input('Please enter location of the maze_matrix file you would like to use:   ')

    #starts timer, calls the functions to solve the maze then ends timer.
    start_time = time.time()

    maze = read_maze(MAZE_LOCATION)
    return_array = depth_first_solve(maze)

    end_time = time.time()

    timeElapsed = end_time - start_time


    #if path is not found
    if len(return_array) == 2:

        print(' <-=[STATS]=->')
        print("    ! No path was found !")
        print('    Algorithim - Depth First Search')
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
        print('    Algorithim - Depth First')
        print(f'    File - {MAZE_LOCATION}')
        print(f'    Time of Algorithm Execution - {timeElapsed}')
        print(f'    Nodes Explored - {num_nodes_visited}')
        print(f'    Nodes Found - {num_nodes_found}')
        print(f'    Nodes in Path - {len(route)}')
        print(f'    Steps in Path - {len(route) -1}')
