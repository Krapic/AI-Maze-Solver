import random
from heapq import heappop, heappush

def generate_labyrinth(difficulty='easy', max_attempts=100):
    size = {'easy': 10, 'medium': 20, 'hard': 30}
    width, height = size.get(difficulty, 10), size.get(difficulty, 10)

    # Inicijalizacija labirinta sa zidovima
    labyrinth = [[1 for _ in range(width)] for _ in range(height)]

    # Početna točka (randomizirana unutar granica)
    start_x, start_y = 1, random.randint(1, height - 2)
    labyrinth[start_y][start_x] = 0

    # Pohranjivanje rubova za MST
    edges = []
    heappush(edges, (random.randint(1, 100), start_x, start_y, start_x + 1, start_y))  # Prvi korak udesno

    # Primov algoritam za generiranje labirinta
    while edges:
        weight, x, y, nx, ny = heappop(edges)
        if labyrinth[ny][nx] == 1:  # Ako nije već posjećeno
            # Pravi prolaz
            labyrinth[ny][nx] = 0
            if nx % 2 == 1 or ny % 2 == 1:  # Ako je točka na neparnoj koordinati, možemo ići dalje
                for dx, dy in [(0, 2), (2, 0), (0, -2), (-2, 0)]:
                    xx, yy = nx + dx, ny + dy
                    if 0 < xx < width-1 and 0 < yy < height-1:
                        heappush(edges, (random.randint(1, 100), nx, ny, xx, yy))
                # Dodavanje poveznih "zidova" koji postaju prolazi
                if x != nx:
                    labyrinth[ny][(x+nx)//2] = 0
                if y != ny:
                    labyrinth[(y+ny)//2][nx] = 0

    # Određivanje izlaza
    end_x, end_y = None, None
    
    for y in range(height-2, 0, -1):
        if labyrinth[y][width-2] == 0:
            end_x, end_y = width-1, y
            labyrinth[end_y][end_x] = 0
            break
        
    # ako ne postoji izlaz na desnom rubu, pobaj donji rub    
    if end_x is None:
        for x in range(width-2, 0, -1):
            if labyrinth[height-2][x] == 0:
                end_x, end_y = x, height-1
                labyrinth[end_y][end_x] = 0
                break    
            
    # Ako jos ne postoji izlaz, napravi na nasumicnom mjestu
    if end_x is None:
        # Nadji sve pristupacne celije na rubovima
        candidates = []
        for y in range(1, height-1):
            if labyrinth[y][1] == 0:
                candidates.append((0, y))  # Lijevi rub
            if labyrinth[y][width-2] == 0:
                candidates.append((width-1, y))  # Desni rub
        
        for x in range(1, width-1):
            if labyrinth[1][x] == 0:
                candidates.append((x, 0))  # Gornji rub
            if labyrinth[height-2][x] == 0:
                candidates.append((x, height-1))  # Donji rub
        
        if candidates:
            end_x, end_y = random.choice(candidates)
            labyrinth[end_y][end_x] = 0
        else:
            # Last resort: Use the start point as end point
            end_x, end_y = start_x, start_y        
        
    print('the bug: ', labyrinth[y][width-2])

    return labyrinth, (start_x, start_y), (end_x, end_y)

# Prikaz labirinta
def print_labyrinth(labyrinth, start, end):
    for y in range(len(labyrinth)):
        line = ''
        for x in range(len(labyrinth[y])):
            if (x, y) == start:
                line += 'S '
            elif (x, y) == end:
                line += 'E '
            else:
                line += '  ' if labyrinth[y][x] == 0 else '█ '
        print(line)

if __name__ == "__main__":
    lab, start, end = generate_labyrinth('hard')
    print_labyrinth(lab, start, end)
