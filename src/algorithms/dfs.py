import time

def dfs_search_generator(labyrinth, start, goal, time_limit=None):

    start_time = time.time()

    def get_neighbors(x, y):
        directions = [(0,1),(0,-1),(1,0),(-1,0)]
        for dx, dy in directions:
            nx, ny = x+dx, y+dy
            if 0 <= ny < len(labyrinth) and 0 <= nx < len(labyrinth[0]):
                if labyrinth[ny][nx] == 0:
                    yield nx, ny

    stack = []
    stack.append(start)
    visited = set([start])
    parent_map = {start: None}