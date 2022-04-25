# Robot Mazes

## Usage

This program was tested with `Python 3.9` and requires the `pygame 2.1.2` library.

To run the program, run the file `main.py` with python. For example, on the project root folder, use the command `python3 main.py`.

## Gamemodes

The player can choose one of the 6 available problems to solve in two different gamemodes:

- **Play**: The player can play the game by writting the sequence of instructions and running the solution. The player may also ask for hints from a solver of their choice, receiving one hint at the time.
- **AI**: The player can choose a solver of their choice to solve the problem and run the solution.

## Souce-code structure

The source code includes the folders `model`, `graphics` and `controller` to implement a user interface with pygame following the MVC pattern. More importantly, there is also a `solvers` folder with the implementation of the search and optimization algorithms used in this problem.

## Problem Specification

Given a grid-like map, with walls placed in between some cells, a robot must be programmed with a set of instructions of minimal size which, when repeated sequentially, find a valid path between the Start and Finish position.

![image](https://user-images.githubusercontent.com/45906176/161929742-70377ba9-6e93-4512-a3e5-3b3196c40319.png)

## Problem Formulation

### State Representation

Instruction List (e.g `[U, D, R]`)

### Initial State

For search algorithms, the initial state is the empty list (`[]`).	For optimization algorithms, the initial state is a list initialized with N random instructions, where N is the optimal number of commands to solve the puzzle (given as an input).

### Objective Test

Run the instructions while there are no cycles, i.e a set of instructions does not end up on a previously starting square.

### As a search problem

#### Operators

- Add_Right - Adds the ‘R’ instruction to the end of the instruction list
- Add_Left - Adds the ‘L’ instruction to the end of the instruction list
- Add_Up - Adds the ‘U’ instruction to the end of the instruction list
- Add_Down - Adds the ‘D’ instruction to the end of the instruction list

#### Heuristics

Heuristics for this problem are hard to define due to:

- the cyclic and infinite nature of the instruction list
- the interactions with the walls on the grid

These properties elevate the potential of a single new instruction to near-limitless, which severely limits the admissibility of heuristics.

Defined heuristics:

- Minimize Manhattan distance - not admissible
- Have mandatory directions - admissible

#### Algorithms

- Breath First Search
- Iterative Deepening Search
- Greedy Search
- A* Search

### As an optimization problem

#### Neighbourhood/Mutation

- Either adds, removes or changes one instruction at random

#### Crossover

- Selects the element of index i either from parent 1 or parent 2
- Splits parent 1, complements with parent 2

#### Algorithms

- Simulated Annealing
    - Linear, exponential, logarithmic, linear and quadratic multiplicative
- Genetic Algorithms
    - Random and roulette selections, split crossover
