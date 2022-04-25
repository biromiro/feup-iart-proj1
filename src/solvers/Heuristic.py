from src.model.Direction import Direction

class Heuristic:
    """Heuristic functions for the greedy and A* algorithms."""

    @staticmethod
    def min_manhattan(state):
        """The minimum manhattan distance to the goal in the current path. Not admissible."""
        best_distance = None
        for position in state.board.walk(state.commands):
            distance = abs(state.board.goal[0] - position[0]) + abs(state.board.goal[1] - position[1])
            if not best_distance or best_distance > distance:
                best_distance = distance
            
        return best_distance

    @staticmethod
    def mandatory_directions(state):
        """The minimum number of commands that must be appended to reach the solution. Admissible."""
        start_x, start_y = state.board.start
        goal_x, goal_y = state.board.goal

        value = 0

        if start_x < goal_x and Direction.RIGHT not in state.commands:
            # The start is on the left of the goal and the robot has no means to go right.
            value += 1
        if start_x > goal_x and Direction.LEFT not in state.commands:
            # The start is on the right of the goal and the robot has no means to go left.
            value += 1
        if start_y > goal_y and Direction.UP not in state.commands:
            # The start is below the goal and the robot has no means to go up.
            value += 1
        if start_y < goal_y and Direction.DOWN not in state.commands:
            # The start is above the goal and the robot has no means to go down.
            value += 1

        return value
