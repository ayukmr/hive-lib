from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

path_map = None

def load_map(walls):
    global path_map

    if path_map is None:
        path_map = [[1 for _ in range(15)] for _ in range(15)]

        for wall in walls:
            x, y = wall['x'], wall['y']
            path_map[y][x] = 0

def towards(pos, dest):
    grid = Grid(matrix=path_map)

    p_x, p_y = pos
    d_x, d_y = dest

    start = grid.node(p_x, p_y)
    end = grid.node(d_x, d_y)

    finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
    path, _ = finder.find_path(start, end, grid)

    step = path[1] if len(path) > 1 else None

    if step:
        delta = (step.x - p_x, step.y - p_y)

        dirs = {
            (-1,  0): 'left',
            ( 1,  0): 'right',
            ( 0, -1): 'up',
            ( 0,  1): 'down'
        }

        return dirs[delta]
    else:
        return 'stay'
