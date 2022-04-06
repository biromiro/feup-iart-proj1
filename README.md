# feup-iart-proj
🤖 Proposed project solution for the Artificial Intelligence course @ FEUP

# Robot Mazes

[Assignment](https://erich-friedman.github.io/puzzle/robot/)

## Problem Specification

Given a grid-like map, with walls placed in between some cells, a robot must be programmed with a set of instructions of minimal size which, when repeated sequentially, find a valid path between the Start and Finish position.
![image](https://user-images.githubusercontent.com/45906176/161929742-70377ba9-6e93-4512-a3e5-3b3196c40319.png)

## Problem Formulation

### State Representation

Instruction List (e.g [U, D, R])

### Initial State

Empty Lisr ( [] )

### Objective Test

Run the instructions while there are no cycles, i.e a set of instructions does not end up on a previously starting square.

### Operators

- Add_Right - Adds the ‘R’ instruction to the end of the instruction list
- Add_Left - Adds the ‘L’ instruction to the end of the instruction list
- Add_Up - Adds the ‘U’ instruction to the end of the instruction list
- Add_Down - Adds the ‘D’ instruction to the end of the instruction list

### Heuristics

Heuristics for this problem are hard to define due to:

- the cyclic and infinite nature of the instruction list
- the interactions with the walls on the grid

These properties elevate the potential of a single new instruction to near-limitless, which severely limits the admissibility of heuristics.
