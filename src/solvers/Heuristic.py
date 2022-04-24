from src.model.Direction import Direction

class Heuristic:
    @staticmethod
    def min_manhattan(state):
        best_distance = None
        for position in state.board.walk(state.commands):
            distance = abs(state.board.goal[0] - position[0]) + abs(state.board.goal[1] - position[1])
            if not best_distance or best_distance > distance:
                best_distance = distance
            
        return best_distance

    @staticmethod
    def mandatory_directions(state):
        start_x, start_y = state.board.start
        goal_x, goal_y = state.board.goal

        value = 0

        if start_x < goal_x and Direction.RIGHT not in state.commands:
            value += 1
        if start_x > goal_x and Direction.LEFT not in state.commands:
            value += 1
        if start_y > goal_y and Direction.UP not in state.commands:
            value += 1
        if start_y < goal_y and Direction.DOWN not in state.commands:
            value += 1

        return value
