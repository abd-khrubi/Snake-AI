import util
from agent import State


def manhattan_distance(state: State):
    head = state.board.snake[0]
    fruit = state.board.fruit_location
    return util.manhattanDistance(head, fruit)


def cyclic_manhattan_distance(state: State):
    board_size = state.board.board_size
    head = state.board.snake[0]
    fruit = state.board.fruit_location
    return util.cyclic_manhattan_distance(head, fruit, board_size)


def manhattan_dead_end(state: State):
    dead_end = util.dead_end(state.board)
    manhattan = manhattan_distance(state)  # or cyclic manhattan

    return 0.5 * manhattan + 0.5 * dead_end


def compact_heuristics(state: State):
    manhattan = manhattan_distance(state)  # or cyclic manhattan

    squareness = util.squareness(state.board.snake)
    compactness = util.compactness(state.board.snake)
    connectivity = util.connectivity(state.board)
    dead_end = util.dead_end(state.board)

    # print(f"{manhattan}, {squareness}, {connectivity}, {dead_end}, {compactness}")
    return manhattan + 2*connectivity + 3*dead_end + compactness
