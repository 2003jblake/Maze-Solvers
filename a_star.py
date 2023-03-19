'''This module defines the functions used to solve the mazes given using a* algorithm'''
import time
import heapq as hq
import math

import numpy as np


def read_maze(filepath):
    '''This takes in a filepath to a maze file.
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
    takes in a tuple of two coordinates and returns true if move is valid false otherwise
    First checks if move is in bounds, then if the node is a path node that hasnt been visited
    repersented by F'''

    try:
        if maze_matrix[possible_move_cords[1]][possible_move_cords[0]] != '#':
            return True
    except IndexError:
        return False

    return False

def find_neighbours(current_position, maze_matrix):
    '''This finds all the possible neighbours of the current position that arent walls,
    takes in the current position and the maze_matrix, and retruns a list of allowed
    coordinates'''

    neighbours = []
    directions = ([0, 1], [-1, 0], [1, 0], [0, -1])

    for direction in directions:
        if valid_move([current_position[0] + direction[0],
                        current_position[1] + direction[1]], maze_matrix):

            neighbours.append([current_position[0] + direction[0],
                                current_position[1] + direction[1]])

    return neighbours

def draw_path_to_file(route_list, maze_matrix):
    '''This takes the route and draws the path repersented P as in the path, V for visited, 
    and F for found. Saves to output.txt'''

    for coordinates in route_list:
        maze_matrix[coordinates[1]][coordinates[0]] = 'P'

    for y_cord, row in enumerate(maze_matrix):
        for x_cord, _ in enumerate(row):
            if isinstance(maze_matrix[y_cord][x_cord], tuple):

                #mark as V if the algorithm went to that node
                if maze_matrix[y_cord][x_cord][2]["closed"]:

                    maze_matrix[y_cord][x_cord] = 'V'

                #mark as F if the algorithm only added it to the queue to be explored
                # but it was never chosen to be explored
                else:

                    maze_matrix[y_cord][x_cord] = 'F'

    np.savetxt('maze-drawing.txt', maze_matrix, fmt='%s')



#These 4 functions are all heurstic functions that can be
def calc_euclidiean_dist(current_coordinates, end_goal_cord):
    '''This calculates and returns the euclideian distance 
    from the current position to the end goal'''

    return math.sqrt((end_goal_cord[0]-current_coordinates[0])**2
                    + (end_goal_cord[1]-current_coordinates[1])**2)

def calc_manhattan_dist(current_coordinates, end_goal_cord):
    '''This calculates and returns the manhattan distance
    from the current position to the end goal'''

    return (abs(end_goal_cord[0]-current_coordinates[0])
            + abs((end_goal_cord[1]-current_coordinates[1])))

def calc_manhattan_dist_unoptimal(current_coordinates, end_goal_cord):
    '''This calculates and returns the manhattan distance *10
    from the current position to the end goal, this overestimates the distance and thus
    is unoptimal but has a significant peformance increase'''

    return (abs(end_goal_cord[0]-current_coordinates[0]) 
            + abs((end_goal_cord[1]-current_coordinates[1])) * 10)

def convert_to_dijkstras(_ , __):
    '''Converts A* to dijkstras by making the heursitc return 0
    essentialy meaning there is no heuristic'''

    return 0



def a_star_solve(maze_matrix):
    '''This peforms a star path finding. Takes in the 2d list maze repersentation.
    Retruns the route, nuber of nodes and explored and an updated version of the maze array
    repersenting the path and node explored. If no paths were found this returns just the nodes 
    explored'''

    #find start and end nodes
    start = find_start(maze_matrix)
    end = find_end(maze_matrix)
    end_goal_cord = [end, len(maze_matrix)-1]
    if start == -1 or end == -1:
        print("Maze is invalid, the start must be in the top row and the end must be bottom row")

    #initalize variables
    priority_queue = []
    nodes_visited = 0
    nodes_found = 0
    #count is a new number for each node so that if there are matching prioritys
    # there is another way to pick a new node
    count = 0

    dist = calc_manhattan_dist([start, 0], end_goal_cord)
    start_node = (dist, count, {
        "h_cost": dist,
        "g_cost": 0,
        "coordinates": [start, 0],
        "closed": False, 
        "parent_coordinates": []
        })

    #adds start node to the priority queue
    priority_queue.append(start_node)
    maze_matrix[0][start] = start_node
    hq.heapify(priority_queue)
    nodes_found += 1

    while priority_queue:

        current = hq.heappop(priority_queue)
        nodes_visited += 1

        current[2]["closed"] = True
        current_coordinates = current[2]["coordinates"]

        #checks if current cordinates are the end goal
        if current_coordinates == end_goal_cord:

            #backtracks through the coordinates fetching their parent nodes,
            # which will produce the route
            route_list = [current_coordinates]

            while current[2]["parent_coordinates"] != []:

                route_list.append(current[2]["parent_coordinates"])
                current = (maze_matrix[current[2]["parent_coordinates"][1]]
                            [current[2]["parent_coordinates"][0]])

            route_list.reverse()

            return  route_list, nodes_visited, nodes_found, maze_matrix


        #gets all the coordinates of the possible neighbours of the current position
        for neighbour_coordinates in find_neighbours(current[2]["coordinates"], maze_matrix):

            neighbour = maze_matrix[neighbour_coordinates[1]][neighbour_coordinates[0]]
            

            #checks if neighbour has already been found or not
            if isinstance(neighbour, tuple):

                #checks if the neighbour has been closed, if so ignore
                if neighbour[2]["closed"]:
                    continue

                #checks if the new path to the neighbour is smaller than current,
                # if so updates neighbour
                if current[2]["g_cost"]+1 < neighbour[2]["g_cost"]:

                    neighbour[2]["g_cost"] = current[2]["g_cost"]+1
                    neighbour[2]["parent_coordinates"] = current[2]["coordinates"]


            else: #executes if neighbour has not been found before

                nodes_found += 1
                count += 1
                dist = calc_manhattan_dist(neighbour_coordinates, end_goal_cord)

                #creates a new node for the new neighbour
                new_node = (current[2]["g_cost"] + 1 + dist, count, {
                    "h_cost": dist,
                    "g_cost": current[2]["g_cost"]+1,
                    "coordinates": neighbour_coordinates,
                    "closed": False,
                    "parent_coordinates": current[2]["coordinates"]  
                })

                hq.heappush(priority_queue, new_node)
                maze_matrix[neighbour_coordinates[1]][neighbour_coordinates[0]] = new_node

    #If we got to here, there are no more loads left to explore, path not found
    return nodes_visited, nodes_found, maze_matrix



if __name__ == "__main__":

    MAZE_LOCATION = input('Please enter location of the maze_matrix file you would like to use:   ')

    #starts timer, calls the functions to solve the maze then ends timer.
    start_time = time.time()

    maze = read_maze(MAZE_LOCATION)
    return_array = a_star_solve(maze)

    end_time = time.time()

    timeElapsed = end_time - start_time


    #if path is not found
    if len(return_array) == 3:

        num_nodes_visited, num_nodes_found, matrix_array = return_array
        print(' <-=[STATS]=->')
        print("    ! No path was found !")
        print('    Algorithim - A star')
        print(f'    File - {MAZE_LOCATION}')
        print(f'    Time of Algorithm Execution - {timeElapsed}')
        print(f'    Nodes Explored - {num_nodes_visited}')
        print(f'    Nodes Found - {num_nodes_found}')

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
        print('    Algorithim - A star')
        print(f'    File - {MAZE_LOCATION}')
        print(f'    Time of Algorithm Execution - {timeElapsed}')
        print(f'    Nodes Explored - {num_nodes_visited}')
        print(f'    Nodes Found - {num_nodes_found}')
        print(f'    Nodes in Path - {len(route)}')
        print(f'    Steps in Path - {len(route) -1}')
