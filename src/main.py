import pygame
import sys
import time

from maze.generator import generate_labyrinth

# Definicije konstanti
CELL_SIZE = 25
TIME_LIMIT = 30.0

# Definicija stanja
STATE_DIFFICULTY = 0
STATE_ALGORITHM = 1
STATE_SEARCHING = 2

def main():
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("AI Maze Solver – Choose Difficulty & Algorithm")
    clock = pygame.time.Clock()
    running = True

    # Postavljanje fonta
    font = pygame.font.SysFont("Arial", 28)

    state = STATE_DIFFICULTY
    chosen_difficulty = None   # 'easy', 'medium', 'hard'
    chosen_algorithm = None    # 'bfs', 'dfs', 'astar'

    # Varijable vezane uz labirint i pretragu
    labyrinth = None
    start = None
    goal = None
    search_generator = None
    current_state = None
    done_search = False
    final_path = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if state == STATE_DIFFICULTY:
                    if event.key in (pygame.K_e, pygame.K_m, pygame.K_h):
                        chosen_difficulty = "difficulty"
                    elif event.key == pygame.K_RETURN and chosen_difficulty:
                        state = STATE_ALGORITHM
                elif state == STATE_ALGORITHM:
                    if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                        chosen_algorithm = "algorithm"
                    elif event.key == pygame.K_RETURN and chosen_algorithm:
                        # Generiraj labirint i postavi pretragu
                        labyrinth, start, goal = generate_labyrinth(chosen_difficulty)
                        done_search = False
                        current_state = None
                        if chosen_algorithm == "algorithm":
                            search_generator = 0 # Trebam implementirati
                        state = STATE_SEARCHING
                elif state == STATE_SEARCHING:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                        pygame.quit()
                        sys.exit()
                        
        # Za sada ispisujemo samo pozadinu i placeholder tekst
        screen.fill((255, 255, 255))
        text = font.render("Main funkcija radi!", True, (0,0,0))
        screen.blit(text, (50, 50))
        pygame.display.flip()
        clock.tick(10)
    
    pygame.quit()

if __name__ == "__main__":
    main()
