# to be able to specify type annotations and static type checkeyer mypy
from typing import List, Any, Set, Dict, Tuple, Optional, Iterator
# to be able to use arguments
import sys
# to create 2-D array
import numpy as np
# to checkey if file path exists
import os.path

"""
Helper dictionarys for the encoding and decoding of the maze
"""
mapping = {
    0: "*",
    1: " ",
    2: "A",
    3: "B",
    5: " ",
    6: "N",
    7: "E",
    8: "S",
    9: "W"
}

rev_mapping = {"*": 0, " ": 1, "A": 2, "B": 3}

class UnsolvableError(Exception):
    """No solution exception, raised when the algorithm can't find a solution for the maze"""
    def __init__(self, msg: str):
        super().__init__(msg)

def iter_neighbour_coordinates(x: int, y: int) -> Iterator[Tuple[int, int]]:
    """Iterator to find the 4 adjacent squares of the maze array"""
    yield x, y + 1
    yield x + 1, y
    yield x - 1, y
    yield x, y - 1

class Maze:
    """
    Takes a file with special encoding to resemble a maze as input.
    Converts the input to a 2-Demensional int Array with help of the lookup tables (dictonarys).
    Tries to solve the maze. if its unsuccesfull the program aborts with an apropriate message.
    If it succeedes, the path from start to finish is stored directly in the maze using cardinal directions (N,E,S,W).
    Before terminating the program prints the maze to the console,
    together with the solution string containing the letter N,E,S,W in the right order.
    """
    def __init__(self, filepath: str) -> None:
        """
        When the object is created the constructor passes the path to the maze file
        to a method which returns the converted 2-D maze array and stores it.
        """
        self.__maze = self.read_file_to_array(filepath)

    @staticmethod
    def read_file_to_array(filepath: str) -> np.ndarray:
        """Reads the input file, validates the symbols in it and stores it in a list of lists before converting it to a 2-D array."""
        if not os.path.exists(filepath):
            sys.exit("Enter a valid path. " + filepath + " does not exist")

        with open(filepath, "r") as f:
            try:
                res = [[rev_mapping[c] for c in l if c.replace("\n", "")]
                    for l in f.readlines() if l.strip()]
            except KeyError:
                sys.exit("Found an unsupported char in the textfile. Aborting the program")
        
        return np.array(res)

    def solve_maze(self) -> int:
        """
        Algorithm based on BFS, check here for more information: https://en.wikipedia.org/wiki/Breadth-first_search
        My specific implementation:
        The algorithm iterates over the maze to find the field with the key value 2 which is our start point.
        After it finds it, it checkes all 4 adjacent squares to check if there is the value 1 stored there,
        this value represents a clear path. If such a value is found it gets replaced with key + 2.
        After the whole maze has been interated the key value is incremented by 2 and it serches for the values wich
        were set during the previous iteration. Until either one of two scenarios happen:
        1: The value 3 is in an adjacent cell -> Success: method returns the curent value of the key
        2: All the adjacent fields for all key values habe been checked and there is no path left -> No Success -> Program terminates
        This solution always finds the fastest way from point A to B if such a path exists.
        """
        key = 0
        no_solution = False

        while not no_solution:
            no_solution = True
            key += 2
            for i in range(len(self.__maze)):
                for j in range(len(self.__maze[i])):
                    if self.__maze[i][j] == key:   
                        for k, l in iter_neighbour_coordinates(i, j):
                            if self.__maze[k][l] == 3:
                                return key

                            if self.__maze[k][l] == 1:
                                self.__maze[k][l] = key + 2
                                no_solution = False
        raise UnsolvableError("The algorithm found no solution for this maze!")
        
    def clean_up_maze(self, key: int) -> None:
        """
        Finds the end point and reconstructs the most efficent path back the the start point.
        All used cells for the path have their value changed to 5.
        The other cells which were changed but didnt lead to the solution  are changed back to the original value (1)
        """
        endx = endy = 0
        for i in range(len(self.__maze)):
            for j in range(len(self.__maze[i])):
                if self.__maze[i][j] == 3:
                    endx = i
                    endy = j

        while key > 2:
            for x, y in iter_neighbour_coordinates(endx, endy):
                if self.__maze[x][y] == key:
                    self.__maze[x][y] = 5
                    endx = x
                    endy = y
                    key -= 2
        
        for i in range(len(self.__maze)):
            for j in range(len(self.__maze[i])):
                if (self.__maze[i][j] > 5 or self.__maze[i][j] == 4):
                    self.__maze[i][j] = 1

    def __str__(self) -> str:
        """
        Print method for this object
        First it finds the starting point which has the value 2 by iteratinf over the maze and stores the coordinates.
        Then it follows the path till it finds the end (value 3) all the while it prints the cardinal directions,
        based on in which direction the path follows. The string of the path is also stored.
        It returns the end version of the maze with the solution string at the end. 
        """
        solution_string = []

        for i in range(len(self.__maze)):
            for j in range(len(self.__maze[i])):
                if self.__maze[i][j] == 2:
                    startx = i
                    starty = j

        while 3 not in [
            self.__maze[startx-1][starty],
            self.__maze[startx][starty-1],
            self.__maze[startx+1][starty],
            self.__maze[startx][starty+1]
        ]:
            if self.__maze[startx-1][starty] == 5:
                self.__maze[startx-1][starty] = 6
                startx = startx-1
                solution_string.append("N")
            if self.__maze[startx][starty+1] == 5:
                self.__maze[startx][starty+1] = 7
                starty = starty+1
                solution_string.append("E")
            if self.__maze[startx+1][starty] == 5:
                self.__maze[startx+1][starty] = 8
                startx = startx+1
                solution_string.append("S")
            if self.__maze[startx][starty-1] == 5:
                self.__maze[startx][starty-1] = 9
                starty = starty-1
                solution_string.append("W")
        try:
            return "".join(["".join([mapping[c] for c in l]) + "\n"
                            for l in self.__maze]) + "".join(solution_string)
        except KeyError:
             sys.exit("The Prgram couldn't reverse the maze encoding and print it.")


def main():
    """ Lauchner """
    try:
        maze = Maze(sys.argv[1])
    except IndexError:
        sys.exit("Programm needs a file as argument to workey! e.g: maze.py file.txt")
    
    try:
        key = maze.solve_maze()
    except UnsolvableError as e:
        sys.exit(e)
    
    maze.clean_up_maze(key)
    print(maze)

if __name__ == "__main__":
    main()