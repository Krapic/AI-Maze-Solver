import time

def dfs_search_generator(labyrinth, start, goal, time_limit=None):

    #biljezimo pocetno vrijeme
    start_time = time.time()

    #pomocna funkcija koju koristimo za dobivanje susjednih cvorova
    def get_neighbors(x, y):
        directions = [(0,1),(0,-1),(1,0),(-1,0)]
        for dx, dy in directions:
            nx, ny = x+dx, y+dy
            if 0 <= ny < len(labyrinth) and 0 <= nx < len(labyrinth[0]):
                if labyrinth[ny][nx] == 0:
                    yield nx, ny

    #inicijalizacija stoga, posjecenih cvorova i mape koja sprema "roditelja" svakog cvora - zbog rekonstrukcije puta
    stack = []
    stack.append(start)
    visited = set([start])
    parent_map = {start: None}

    #glavna petlja
    while stack:
        
        duration = time.time() - start_time
        #ako je vrijeme isteklo => timeout
        if time_limit is not None and (time.time() - start_time) > time_limit:
            yield ("timeout", )
            return

        #vadimo trenutni cvor sa stoga i rekonstruiramo put
        current = stack.pop()
        path_so_far = reconstruct_path(parent_map, current)
        yield ("searching", visited, current, path_so_far)

        #jesmo li na cilju
        #ako jesmo, rekonstruiramo put koji je algoritam pronasao i zavrsavamo
        if current == goal:
            final_path = reconstruct_path(parent_map, goal)
            yield ("found", final_path, len(visited), duration)
            return

        #"razdvajamo" koordinate trenutnog cvora
        cx, cy = current

        #iteracija kroz susjede trenutnog cvora => kako bi ih algoritam mogao kasnije obici
        for nx, ny in get_neighbors(cx, cy):
            if (nx, ny) not in visited:
                visited.add((nx, ny))
                parent_map[(nx, ny)] = current
                stack.append((nx, ny))

    #ispali smo iz petlje => put nije pronaden
    duration = time.time() - start_time
    yield ("no_path", len(visited), duration)


#funkcija za rekonstrukciju puta od odredenog cvora do pocetka
def reconstruct_path(parent_map, end_node):
    path = []
    current = end_node
    while current is not None:
        path.append(current)
        current = parent_map.get(current)
    path.reverse()
    return path