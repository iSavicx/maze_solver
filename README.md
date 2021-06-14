# Python maze solver

This project addresses the problem of finding a path in a maze from a point 'A' to a point 'B'.

The program reads a file and if it matches a maze it will try to solve it using an implementation of the breadth first search algorithm.

## Infos
Some example mazefiles can be found in the testfile directory.

The maze file must meet the following requirements for the program to work:<br>
'*' represents a wall<br>
' ' blank space is a free path<br>
'A' represents the start location<br>
'B' represents the end location<br>

The outerline must be a wall ('*' symbol) . The start ('A') and end postion ('B') don't matter. If there is a path the algorithm will find it. If there is more than one it will always return the fastest path.

The program prints the input maze with the four directions 'N' (north), 'S' (south), 'W' (west), and 'E' (east) directly printed on the maze to represent a path from the initial point 'A' to the final point 'B' and the solution string.


## Starting and required module

Make sure numpy is installed.<br>
**pip3 install numpy**

Use the commandline to use the program and use a maze file as argument.<br>
**Examples:**<br>
windows: **`python maze.py testfiles/maze-one.txt`**<br>
linux: **`python3 maze.py testfiles/maze-one.txt`**
 