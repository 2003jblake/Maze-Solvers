'''This module defines the functions used to solve the mazes given using a varity of algorithms'''

def readMaze(filepath):
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

def findStart(matrix_array):
    '''This returns the x index of the start node of the array given that 
    the start is always on the top row'''

    for index, char in enumerate(matrix_array[0]):

        if char == '-':
            return index

    return -1

def findEnd(matrix_array):
    '''This returns the x index of the start node of the array given that
    the start is always on the bottom row'''

    for index, char in enumerate(matrix_array[-1]):
        if char == '-':
            return index

    return -1


a = readMaze("maze-Easy.txt")
print(findStart(a))