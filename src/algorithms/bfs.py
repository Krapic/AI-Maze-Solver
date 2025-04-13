import time
from collections import deque

def bfs_search_generator(labyrinth, start, goal, time_limit=None):
    """
    BFS implementiran kao generator. Svakim korakom se vraćaju informacije
    o posjećenim čvorovima i 'fronti' (queue), tako da se može vizualizirati.

    :param labyrinth: 2D matrica (0 = put, 1 = zid).
    :param start: Tuple (x, y) koordinata početne točke.
    :param goal: Tuple (x, y) koordinata ciljne točke.
    :param time_limit: Maksimalno vrijeme pretrage u sekundama (None = bez limita).
    :yield: 
        - ("searching", visited_set, current_node, path_so_far)
        - ("found", final_path)
        - ("timeout", ) / ("no_path", ) ako dođe do prekida.
    """
    start_time = time.time()

    def get_neighbors(x, y):
        """Vraća susjedne čvorove za trenutnu poziciju (x, y) u labirintu."""
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= ny < len(labyrinth) and 0 <= nx < len(labyrinth[0]):
                if labyrinth[ny][nx] == 0:  # slobodno polje
                    yield nx, ny

    queue = deque([start])
    visited = set([start])
    parent_map = {start: None}

    while queue:
        # Provjera vremenskog ograničenja
        if time_limit is not None and (time.time() - start_time) > time_limit:
            yield ("timeout", )
            return

        current = queue.popleft()

        # Rekonstruiraj trenutni put za vizualizaciju
        path_so_far = reconstruct_path(parent_map, current)
        yield ("searching", visited, current, path_so_far)

        # Ako smo pronašli cilj
        if current == goal:
            final_path = reconstruct_path(parent_map, goal)
            yield ("found", final_path)
            return

        cx, cy = current
        for nx, ny in get_neighbors(cx, cy):
            if (nx, ny) not in visited:
                visited.add((nx, ny))
                parent_map[(nx, ny)] = current
                queue.append((nx, ny))

    # Ako smo iscrpili queue bez pronalaska cilja
    yield ("no_path", )

def reconstruct_path(parent_map, end_node):
    """
    Rekonstruira put od početne točke do cilja koristeći parent_map.

    :param parent_map: Mapa koja povezuje svaki čvor s njegovim roditeljem.
    :param end_node: Ciljni čvor.
    :return: Lista koordinata koje čine rekonstruirani put.
    """
    path = []
    current = end_node
    while current is not None:
        path.append(current)
        current = parent_map.get(current)
    path.reverse()
    return path

# Testiranje funkcionalnosti BFS generatora
if __name__ == "__main__":
    labyrinth = [
        [0, 1, 0],
        [0, 0, 0],
        [1, 0, 0]
    ]
    start = (0, 0)
    goal = (2, 2)

    for state in bfs_search_generator(labyrinth, start, goal):
        print(state)
