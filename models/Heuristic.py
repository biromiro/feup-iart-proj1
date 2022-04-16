from models.Direction import Direction


class Heuristic:
    @staticmethod
    def min_manhattan(state):
        return state.board.walk(state)[1]

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
