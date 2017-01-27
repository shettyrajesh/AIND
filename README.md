# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: The constraint in naked twins problem states that no squares outside the two naked twins squares can contain the twin values. In the solution the constraints were applied on each of the units from the puzzle. This is a way to narrow the area to work with and keeping the overall goals/constraints of the sudoku rule in mind. The units could be rows, columns, 3x3 areas or diagonals. For each of the units the other box elements with these naked twins digits were replaced with '' to meet the constraint.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: One of the ways to solve diagonal sudoku could be by including the diagonals into the unitlist, units and peers dictionaries. This way the existing logic in place for eliminate, only_choice, reduce_puzzle and search functions can be equally applied as a constraint to the new units (for diagonals). The constraint propogation was done similar to a regular sudoku with having a loop for eliminate and only_choice functions till the puzzle is reduced and is ready for search. The recursive depth first search algorithm that follows tries various potential box values until the puzzle is completely solved.

On a related note, this was a thouroughly insighful and enjoyable experience, I will continue improvising this code long after AIND is done :-). Will apply various startegies that are out there, with some of mine that I use for sudoku.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in function.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.