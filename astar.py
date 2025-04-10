import time
import heapq

def astar_search_generator(labyrinth, start, goal, time_limit):
    """
    Implementacija A* pretrage – dodana logika za susjede i heuristika.
    """
    start_time = time.time()
    visited = set()
    cost_so_far = {start: 0}
    open_list = []

    def heuristic(a, b):
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def get_neighbors(x, y):
        possible_moves = [(0,1), (1,0), (0,-1), (-1,0)]
        for dx, dy in possible_moves:
            nx, ny = x + dx, y + dy
            if 0 <= ny < len(labyrinth) and 0 <= nx < len(labyrinth[0]):
                if labyrinth[ny][nx] == 0:
                    yield (nx, ny)

    initial_priority = heuristic(start, goal)
    open_list.append((initial_priority, [start]))
    heapq.heapify(open_list)

    while open_list:
        if (time.time() - start_time) > time_limit:
            yield ("timeout", )
            return

        current_priority, current_path = heapq.heappop(open_list)
        current_node = current_path[-1]
        visited.add(current_node)
        yield ("searching", visited, current_node, current_path)

        if current_node == goal:
            yield ("found", current_path)
            return

        current_cost = cost_so_far[current_node]

        for nb in get_neighbors(*current_node):
            new_cost = current_cost + 1
            if nb not in cost_so_far or new_cost < cost_so_far[nb]:
                cost_so_far[nb] = new_cost
                priority = new_cost + heuristic(nb, goal)
                new_path = current_path + [nb]
                heapq.heappush(open_list, (priority, new_path))

    yield ("no_path", )
