import time
import heapq

def astar_search_generator(labyrinth, start, goal, time_limit):
    """
    A* pretraživanje labirinta, vraća generator koji u svakoj iteraciji
    yielda stanje pretrage (korak vizualizacije).
    
    Yield vraća tuple formata:
        1) ("searching", visited, current_node, current_path)
        2) ("found", current_path)
        3) ("timeout", )
        4) ("no_path", )
    
    :param labyrinth: 2D matrica (0=prohodno, 1=zid), npr. labyrinth[y][x].
    :param start: (sx, sy) koordinata starta
    :param goal: (gx, gy) koordinata cilja
    :param time_limit: vremenski limit u sekundama (float)
    """

    # 1. Inicijalizacija: mjeri početno vrijeme
    start_time = time.time()

    # Za prikaz i statistiku
    visited = set()
    
    # cost_so_far čuva najmanju poznatu “cijenu” (g) do pojedinog čvora
    cost_so_far = {start: 0}

    # Min-heap (priority queue) za A*
    # Format spremanja: (prioritet, put)
    #   - prioritet = g + h (g=kost do sad, h=heuristika do cilja)
    #   - put je lista čvorova od start do current
    open_list = []

    # Heuristička funkcija – ovdje Manhattan udaljenost
    def heuristic(a, b):
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    # Pomoćna za susjede
    def get_neighbors(x, y):
        possible_moves = [(0,1), (1,0), (0,-1), (-1,0)]
        for dx, dy in possible_moves:
            nx, ny = x + dx, y + dy
            # provjera granica i je li polje prohodno
            if 0 <= ny < len(labyrinth) and 0 <= nx < len(labyrinth[0]):
                if labyrinth[ny][nx] == 0:
                    yield (nx, ny)

    # Početni čvor
    initial_priority = heuristic(start, goal)
    open_list.append((initial_priority, [start]))

    # koristimo heapq za min-heap
    heapq.heapify(open_list)

    # 2. Glavna petlja
    while open_list:
        # Provjera vremenskog ograničenja
        if (time.time() - start_time) > time_limit:
            yield ("timeout", )
            return

        current_priority, current_path = heapq.heappop(open_list)
        current_node = current_path[-1]  # zadnji čvor u pathu
        visited.add(current_node)

        # Pošaljemo trenutnu sliku pretrage
        yield ("searching", visited, current_node, current_path)

        # Ako smo na cilju
        if current_node == goal:
            yield ("found", current_path)
            return

        # Dosadašnji trošak
        current_cost = cost_so_far[current_node]

        # Istraži susjede
        for nb in get_neighbors(*current_node):
            new_cost = current_cost + 1  # svaki korak košta 1
            # Ako susjed još nije obrađen ili smo našli bolju (jeftiniju) putanju
            if nb not in cost_so_far or new_cost < cost_so_far[nb]:
                cost_so_far[nb] = new_cost
                priority = new_cost + heuristic(nb, goal)
                new_path = current_path + [nb]
                heapq.heappush(open_list, (priority, new_path))

    # Ako iscrpimo open_list, znači nema rješenja
    yield ("no_path", )
