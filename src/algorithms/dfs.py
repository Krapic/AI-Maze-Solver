import time

# Funkcija reconstruct_path ostaje nepromijenjena ako je koriste drugi dijelovi koda,
# ali DFS će sada interno graditi putanju.
def reconstruct_path(parent_map, end_node):
    path = []
    current = end_node
    while current is not None:
        path.append(current)
        current = parent_map.get(current)
    path.reverse()
    return path

def dfs_search_generator(labyrinth, start, goal, time_limit=None):
    start_time = time.time()

    def get_neighbors(x, y):
        # Smjerovi mogu biti fiksni ili se mogu miješati (random.shuffle) za različito ponašanje DFS-a
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)] # Dolje, Desno, Gore, Lijevo
        # directions = [(0, -1), (0, 1), (-1, 0), (1, 0)] # Npr. Gore, Dolje, Lijevo, Desno
        # import random; random.shuffle(directions)
        
        neighbors_list = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= ny < len(labyrinth) and 0 <= nx < len(labyrinth[0]):
                if labyrinth[ny][nx] == 0:
                    neighbors_list.append((nx, ny))
        return neighbors_list

    # Stog sada čuva par: (čvor, putanja_do_tog_čvora)
    stack = [(start, [start])]
    
    # 'visited' čuva čvorove koji su bili dodani na stog (i time obrađeni ili će biti obrađeni)
    # Ovo sprječava cikluse i ponovnu obradu.
    visited_nodes = set([start])

    while stack:
        duration = time.time() - start_time
        if time_limit is not None and duration > time_limit:
            yield ("timeout", len(visited_nodes), duration)
            return

        current_node, current_path = stack.pop()

        # Yield stanje pretrage: skup svih posjećenih čvorova do sada, trenutni čvor, putanja do njega
        yield ("searching", visited_nodes, current_node, current_path)

        if current_node == goal:
            duration = time.time() - start_time # Ponovno dohvati vrijeme za točnost
            yield ("found", current_path, len(visited_nodes), duration)
            return
        
        # Istraži susjede. Dodajemo ih obrnutim redoslijedom na stog
        # kako bi se "prvi" susjed (po definiciji get_neighbors) prvi obradio (LIFO).
        # Ako želite da se npr. 'gornji' susjed prvi istraži, stavite ga zadnjeg u 'directions'.
        for neighbor in reversed(get_neighbors(current_node[0], current_node[1])):
            if neighbor not in visited_nodes:
                visited_nodes.add(neighbor)
                new_path = current_path + [neighbor]
                stack.append((neighbor, new_path))
    
    # Ako stog postane prazan, a cilj nije pronađen
    duration = time.time() - start_time
    yield ("no_path", len(visited_nodes), duration)