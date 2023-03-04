'''This module defines the functions used to solve the mazes given using a varity of algorithms'''

def read_maze(filepath):
    '''This takes in a filepath to a maze.
    Returns a maze where each row is a list item in an array
    Removes any newline characters and empty lines'''

    matrix_array = []

    with open(filepath, encoding="utf-8") as file:
        for item in file:
            if item == '\n':
                break
            matrix_array.append(list(item.replace('\n', '').replace(' ', '')))

    return matrix_array

def find_start(matrix_array):
    '''This returns the x index of the start node of the array given that 
    the start is always on the top row'''

    for index, char in enumerate(matrix_array[0]):

        if char == '-':
            return index

    return -1

def find_end(matrix_array):
    '''This returns the x index of the start node of the array given that
    the start is always on the bottom row'''

    for index, char in enumerate(matrix_array[-1]):
        if char == '-':
            return index

    return -1


def  depth_first_search(matrix_array):
    '''This peforms depth first search'''

    def valid_move(destinationCords):
        '''This checks if is a move is valid based on the cordinates of the wanted move.
        takes in a tuple of two coordinates and returns true if move is valid false otherwise'''

        if destinationCords[0] < 0 or destinationCords[1] < 0:
            return False
        if destinationCords[0] > (len(matrix_array[0])-1) or destinationCords[1] > (len(matrix_array)-1):
            return False

        if matrix_array[destinationCords[1]][destinationCords[0]] == '-':
            return True

        return False

    def check_cycle(destinationCords):

        for item in routeStack:
            if destinationCords == item:
                return False

        return True


    start = find_start(matrix_array)
    end = find_end(matrix_array)
    if start == -1 or end == -1:
        print("Maze is invalid, the start must be in the top row and the end must be bottom row")

    routeStack = []
    routeStack.append([start, 0])

    routeFound = False

    while not routeFound:

        position = routeStack[-1]

        if position == [end, len(matrix_array)-1]:
            routeFound = True
            return routeStack

        if valid_move([position[0], position[1]-1]) and check_cycle([position[0], position[1]-1]):
            routeStack.append([position[0], position[1]-1])
            
        elif valid_move([position[0]-1, position[1]]) and check_cycle([position[0]-1, position[1]]):
            routeStack.append([position[0]-1, position[1]])

        elif valid_move([position[0], position[1]+1]) and check_cycle([position[0], position[1]+1]):
            routeStack.append([position[0], position[1]+1])
            
        elif valid_move([position[0]+1, position[1]]) and check_cycle([position[0]+1, position[1]]):
            routeStack.append([position[0]+1, position[1]])

        







a = read_maze("test.txt")
print(depth_first_search(a))