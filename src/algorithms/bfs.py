from collections import deque

def bfs(labyrinth, start, goal):
    """
    Implementacija osnovnog BFS algoritma za pretragu labirinta.

    :param labyrinth: 2D matrica (0 = put, 1 = zid).
    :param start: Tuple (x, y) koordinata početne točke.
    :param goal: Tuple (x, y) koordinata ciljne točke.
    :return: Lista koordinata koje čine put od starta do cilja ili None ako put ne postoji.
    """
    queue = deque([start])
    visited = set([start])
    parent_map = {start: None}

    while queue:
        current = queue.popleft()

        # Ako smo pronašli cilj, rekonstruiramo put
        if current == goal:
            return reconstruct_path(parent_map, goal)

        # Dodajemo susjede trenutnog čvora u red
        for neighbor in get_neighbors(current[0], current[1], labyrinth):
            if neighbor not in visited:
                visited.add(neighbor)
                parent_map[neighbor] = current
                queue.append(neighbor)

    return None  # Ako nema puta do cilja

def get_neighbors(x, y, labyrinth):
    """
    Vraća susjedne čvorove za trenutnu poziciju (x, y) u labirintu.

    :param x: Trenutna x koordinata.
    :param y: Trenutna y koordinata.
    :param labyrinth: 2D matrica labirinta.
    :return: Lista tuple-ova koji predstavljaju susjedne čvorove.
    """
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    neighbors = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= ny < len(labyrinth) and 0 <= nx < len(labyrinth[0]):
            if labyrinth[ny][nx] == 0:  # Provjera je li polje slobodno
                neighbors.append((nx, ny))
    return neighbors

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

# Testiranje funkcionalnosti
if __name__ == "__main__":
    labyrinth = [
        [0, 1, 0],
        [0, 0, 0],
        [1, 0, 0]
    ]
    start = (0, 0)
    goal = (2, 2)

    result = bfs(labyrinth, start, goal)
    
    if result:
        print("Put pronaden:", result)
    else:
        print("Put nije pronaden.")
