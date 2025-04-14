import pygame
import sys

from maze.generator import generate_labyrinth

CELL_SIZE = 25
TIME_LIMIT = 10.0

# Definicija stanja
STATE_DIFFICULTY = 0
STATE_DISPLAY = 1

def main():
    pygame.init()

    # Početni prozor
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Maze Generator – Choose Difficulty")

    clock = pygame.time.Clock()
    running = True

    font = pygame.font.SysFont("Arial", 28)
    state = STATE_DIFFICULTY

    # Varijable za korisnikov odabir i labirint
    chosen_difficulty = None  # 'easy', 'medium', 'hard'
    labyrinth = None
    start = None
    goal = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if state == STATE_DIFFICULTY:
                    if event.key == pygame.K_e:
                        chosen_difficulty = 'easy'
                    elif event.key == pygame.K_m:
                        chosen_difficulty = 'medium'
                    elif event.key == pygame.K_h:
                        chosen_difficulty = 'hard'
                    elif event.key == pygame.K_RETURN and chosen_difficulty is not None:
                        # Generiramo labirint prema odabranoj težini
                        labyrinth, start, goal = generate_labyrinth(chosen_difficulty)
                        # Prilagodba prozora veličini labirinta
                        rows, cols = len(labyrinth), len(labyrinth[0])
                        screen = pygame.display.set_mode((cols * CELL_SIZE, rows * CELL_SIZE))
                        state = STATE_DISPLAY

                elif state == STATE_DISPLAY:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        pygame.quit()
                        sys.exit()

        # Crtanje ekrana
        screen.fill((255, 255, 255))

        if state == STATE_DIFFICULTY:
            draw_difficulty_menu(screen, font, chosen_difficulty)
        elif state == STATE_DISPLAY:
            draw_labyrinth(screen, labyrinth, start, goal)

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()

def draw_difficulty_menu(screen, font, chosen_difficulty):
    # Prikazuje izbornik za odabir težine
    lines = [
        "ODABERITE TEŽINU:",
        "[E] Easy",
        "[M] Medium",
        "[H] Hard",
        "Pritisnite ENTER za potvrdu."
    ]
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, (0, 0, 0))
        screen.blit(text_surface, (50, 100 + i * 40))

    if chosen_difficulty:
        chosen_text = f"Odabrano: {chosen_difficulty.upper()}"
        chosen_surface = font.render(chosen_text, True, (0, 128, 0))
        screen.blit(chosen_surface, (50, 350))

def draw_labyrinth(screen, labyrinth, start, goal):
    # Crtanje labirinta s prikazom početne (zelene) i krajnje točke (crvene)
    if labyrinth is None:
        return

    rows = len(labyrinth)
    cols = len(labyrinth[0])
    sx, sy = start
    gx, gy = goal

    for y in range(rows):
        for x in range(cols):
            color = (0, 0, 0) if labyrinth[y][x] == 1 else (220, 220, 220)
            draw_cell(screen, x, y, color)

    # Početna točka (zelena) i krajnja točka (crvena)
    draw_cell(screen, sx, sy, (0, 255, 0))
    draw_cell(screen, gx, gy, (255, 0, 0))

def draw_cell(screen, x, y, color):
    # Pomoćna funkcija za crtanje pojedinačne ćelije
    rect = (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)

if __name__ == "__main__":
    main()
