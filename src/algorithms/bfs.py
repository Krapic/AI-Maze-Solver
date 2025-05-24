import time
from collections import deque

def bfs_search_generator(labyrinth, start, goal, time_limit=None):
    """
    BFS implementiran kao generator. Svakim korakom se vraćaju info
    o posjećenim čvorovima i 'fronti' (queue), tako da se može vizualizirati.
    
    :param labyrinth: 2D matrica (0 = put, 1 = zid).
    :param start: (sx, sy) koordinata starta.
    :param goal: (gx, gy) koordinata cilja.
    :param time_limit: sekunde nakon kojih se prekida pretraga (None = bez limita).
    :yield: 
        ("searching", visited_set, current_node, path_so_far)
        ili 
        ("found", final_path, nodes_visited, duration)
        ili
        ("timeout", nodes_visited, duration) / ("no_path", nodes_visited, duration)  ako dođe do prekida.
    """
    start_time = time.time()

    def get_neighbors(x, y):
        directions = [(0,1), (0,-1), (1,0), (-1,0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= ny < len(labyrinth) and 0 <= nx < len(labyrinth[0]):
                if labyrinth[ny][nx] == 0:  # slobodno polje
                    yield nx, ny 

    queue = deque()
    queue.append(start)
    visited = set([start])
    parent_map = {start: None}

    while queue:
        duration = time.time() - start.time

        if time_limit is not None and duration > time_limit:
            # "timeout" – prekidamo i javljamo da je isteklo vrijeme
            yield ("timeout", len(visited), duration)
            return

        current = queue.popleft()
        
        # Pokažemo trenutno stanje BFS-a
        # 'path_so_far' je put do 'current' (privremeno), za vizualizaciju
        path_so_far = reconstruct_path(parent_map, current)
        yield ("searching", visited, current, path_so_far)

        if current == goal:
            # Pronađen cilj: rekonstruišemo finalni path
            final_path = reconstruct_path(parent_map, goal)
            yield ("found", final_path, len(visited), duration)
            return

        cx, cy = current
        for nx, ny in get_neighbors(cx, cy):
            if (nx, ny) not in visited:
                visited.add((nx, ny))
                parent_map[(nx, ny)] = current
                queue.append((nx, ny))

    # Ako smo iscrpili queue, a nismo našli cilj
    duration = time.time() - start_time
    yield ("no_path", len(visited), duration)


def reconstruct_path(parent_map, end_node):
    """Rekonstruira put od starta do 'end_node' koristeći parent_map."""
    path = []
    current = end_node
    while current is not None:
        path.append(current)
        current = parent_map.get(current)
    path.reverse()
    return path


# if __name__ == "__main__":
#     labyrinth = [
#         [0, 1, 0],
#         [0, 0, 0],
#         [1, 0, 0]
#     ]
#     start = (0, 0)
#     goal = (2, 2)

#     for state in bfs_search_generator(labyrinth, start, goal):
#         print(state)
