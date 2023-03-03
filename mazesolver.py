def readMaze(filepath):
    matrixArray = []

    with open(filepath) as file:
        for item in file:
            if item == '\n':
                break
            matrixArray.append(item.replace("\n", ""))


    return matrixArray


print(readMaze("maze-Easy.txt"))