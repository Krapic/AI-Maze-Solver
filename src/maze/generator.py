import random
from collections import deque

def generate_labyrinth(difficulty='easy', attempt=0, max_attempts=100):
    if attempt >= max_attempts:
        print("Failed to generate a valid labyrinth after several attempts.")
        return None

    size = {'easy': 10, 'medium': 20, 'hard': 30}
    width, height = size.get(difficulty, 10), size.get(difficulty, 10)

    # 1. Priprema: cijeli labirint su zidovi (1)
    labyrinth = [[1 for _ in range(width)] for _ in range(height)]

    # 2. Start točka: lijevi rub (uvijek (0, y)), y nasumično unutar granica
    start_y = random.randint(1, height - 2)
    start_x = 0
    labyrinth[start_y][start_x] = 0

    # 3. DFS: iz točke (1, start_y), da bi DFS širio unutar labirinta
    def is_valid(x, y):
        if 0 <= x < width and 0 <= y < height:
            if labyrinth[y][x] == 0:
                return False
            adjacent_zeros = sum(
                (labyrinth[ny][nx] == 0)
                for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
                if 0 <= nx < width and 0 <= ny < height
            )
            return adjacent_zeros <= 1  # malo opuštenije pravilo
        return False

    stack = [(start_x + 1, start_y)]
    labyrinth[start_y][start_x + 1] = 0

    while stack:
        x, y = stack.pop()
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny):
                labyrinth[ny][nx] = 0
                stack.append((nx, ny))

    # 4. Rubovi: postavi sve rubove na zidove
    for x in range(width):
        labyrinth[0][x] = 1
        labyrinth[height - 1][x] = 1
    for y in range(height):
        labyrinth[y][0] = 1
        labyrinth[y][width - 1] = 1

    # 5. OTVORI ULAZ (start) ponovo
    labyrinth[start_y][start_x] = 0

    # 6. PRONAĐI izlaz: bilo koja 0 na desnom rubu (x = width - 2)
    candidates = [(width - 2, y) for y in range(1, height - 1) if labyrinth[y][width - 2] == 0]
    if not candidates:
        return generate_labyrinth(difficulty, attempt + 1, max_attempts)

    end_x, end_y = width - 1, random.choice(candidates)[1]
    labyrinth[end_y][end_x] = 0

    # 7. Provjera povezanosti
    if not path_exists(labyrinth, start_x, start_y, end_x, end_y):
        return generate_labyrinth(difficulty, attempt + 1, max_attempts)

    # 8. Ispis
    if __name__ == "__main__":
        for y, row in enumerate(labyrinth):
            line = ''
            for x, cell in enumerate(row):
                if (x, y) == (start_x, start_y):
                    line += 'S '
                elif (x, y) == (end_x, end_y):
                    line += 'E '
                else:
                    line += '0 ' if cell == 0 else '1 '
            print(line)

    return labyrinth, (start_x, start_y), (end_x, end_y)



def path_exists(labyrinth, start_x, start_y, end_x, end_y):
    queue = deque([(start_x, start_y)])
    visited = set()
    visited.add((start_x, start_y))

    while queue:
        x, y = queue.popleft()
        if (x, y) == (end_x, end_y):
            return True
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(labyrinth[0]) and 0 <= ny < len(labyrinth) and labyrinth[ny][nx] == 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny))
    return False


if __name__ == "__main__":
    lab, start, end = generate_labyrinth('hard')#ovdje se mijenja tezina labirinta
    
    if lab is None:
        print("Could not generate a valid labyrinth.")
