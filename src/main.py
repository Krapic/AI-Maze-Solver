import pygame
import sys
import time

from maze.generator import generate_labyrinth
from algorithms.bfs import bfs_search_generator
from algorithms.dfs import dfs_search_generator
from algorithms.astar import astar_search_generator

from visualization.pygame_ui import (
    draw_difficulty_menu,
    draw_algorithm_menu,
    draw_labyrinth,
    _draw_cell,
    draw_live_stats,
    draw_final_stats
)

# Fiksne dimenzije prozora
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# Veličina ćelije labirinta
CELL_SIZE = 25

# Mjerenje vremena ograničenja
TIME_LIMIT = 10.0

# Stanja aplikacije
STATE_DIFFICULTY = 0
STATE_ALGORITHM = 1
STATE_SEARCHING = 2
STATE_FINISHED = 3

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("AI Maze Solver")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 28)
    state = STATE_DIFFICULTY

    chosen_difficulty = None
    chosen_algorithm = None

    labyrinth = start = goal = None
    search_generator = None
    
    # Varijable za statistiku
    final_path = None
    nodes_visited_live = 0
    time_elapsed_live = 0.0
    path_length = 0
    search_status = "Nije započeto"
    search_start_timestamp = 0.0

    # Dimenzije panela za labirint i statistiku
    maze_panel_width = WINDOW_WIDTH * 2 // 3
    stats_panel_width = WINDOW_WIDTH - maze_panel_width
    stats_panel_x = maze_panel_width

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.K_ESCAPE:
                running = False

            elif event.type == pygame.KEYDOWN:
                if state == STATE_DIFFICULTY:
                    if event.key == pygame.K_e:
                        chosen_difficulty = 'easy'
                    elif event.key == pygame.K_m:
                        chosen_difficulty = 'medium'
                    elif event.key == pygame.K_h:
                        chosen_difficulty = 'hard'
                    elif event.key == pygame.K_RETURN and chosen_difficulty:
                        state = STATE_ALGORITHM

                elif state == STATE_ALGORITHM:
                    if event.key == pygame.K_1:
                        chosen_algorithm = 'bfs'
                    elif event.key == pygame.K_2:
                        chosen_algorithm = 'dfs'
                    elif event.key == pygame.K_3:
                        chosen_algorithm = 'astar'
                    elif event.key == pygame.K_RETURN and chosen_algorithm:
                        labyrinth, start, goal = generate_labyrinth(chosen_difficulty)
                        
                        # Resetiranje statistike
                        final_path = None
                        nodes_visited_live = 0
                        time_elapsed_live = 0.0
                        path_length = 0
                        search_status = "Pretraga u tijeku..."

                        if chosen_algorithm == 'bfs':
                            search_generator = bfs_search_generator(labyrinth, start, goal, TIME_LIMIT)
                        elif chosen_algorithm == 'dfs':
                            search_generator = dfs_search_generator(labyrinth, start, goal, TIME_LIMIT)
                        else:
                            search_generator = astar_search_generator(labyrinth, start, goal, TIME_LIMIT)
                        
                        search_start_timestamp = time.time()
                        state = STATE_SEARCHING
                
                elif state == STATE_FINISHED:
                    if event.key == pygame.K_r: # Povratak na odabir težine labirinta
                        state = STATE_DIFFICULTY # Postavi stanje na odabir težine
                        chosen_difficulty = None # Resetiraj odabranu težinu
                        chosen_algorithm = None # Resetiraj odabrani algoritam
                    elif event.key == pygame.K_ESCAPE:
                        running = False

        # LOGIKA PRETRAGE
        if state == STATE_SEARCHING:
            try:
                current_state_data = next(search_generator)
                status = current_state_data[0]

                if status == "searching":
                    visited, current_node, path_so_far = current_state_data[1], current_state_data[2], current_state_data[3]
                    nodes_visited_live = len(visited)
                    time_elapsed_live = time.time() - search_start_timestamp
                    search_status = f"Pretraga u tijeku ({chosen_algorithm.upper()})"
                elif status == "found":
                    final_path, nodes_visited_live, time_elapsed_live = current_state_data[1], current_state_data[2], current_state_data[3]
                    path_length = len(final_path)
                    search_status = f"Pronađen put ({chosen_algorithm.upper()})"
                    state = STATE_FINISHED
                elif status == "timeout":
                    nodes_visited_live, time_elapsed_live = current_state_data[1], current_state_data[2]
                    final_path = None
                    path_length = 0
                    search_status = f"Isteklo vrijeme ({chosen_algorithm.upper()})"
                    state = STATE_FINISHED
                elif status == "no_path":
                    nodes_visited_live, time_elapsed_live = current_state_data[1], current_state_data[2]
                    final_path = None
                    path_length = 0
                    search_status = f"Nema puta ({chosen_algorithm.upper()})"
                    state = STATE_FINISHED

            except StopIteration:
                search_status = "Pretraga završena (nepoznat ishod)"
                state = STATE_FINISHED
            except AttributeError:
                pass


        # CRTANJE
        screen.fill((255, 255, 255))

        if state == STATE_DIFFICULTY:
            draw_difficulty_menu(screen, font, chosen_difficulty)

        elif state == STATE_ALGORITHM:
            draw_algorithm_menu(screen, font, chosen_algorithm, chosen_difficulty)

        elif state == STATE_SEARCHING or state == STATE_FINISHED:
            # Stvaranje površine za labirint
            maze_surface = pygame.Surface((maze_panel_width, WINDOW_HEIGHT))
            maze_surface.fill((255, 255, 255))
            
            # Crtanje labirinta na maze_surface
            draw_labyrinth(maze_surface, labyrinth, start, goal, final_path, CELL_SIZE)
            
            # Animacija posjećanja čvorova (ćelija) na površini labirinta
            if state == STATE_SEARCHING and 'current_state_data' in locals() and current_state_data[0] == "searching":
                visited, current_node, path_so_far = current_state_data[1], current_state_data[2], current_state_data[3]
                for (vx, vy) in visited:
                    _draw_cell(maze_surface, vx, vy, (150, 200, 255), CELL_SIZE)
                for (px, py) in path_so_far:
                    _draw_cell(maze_surface, px, py, (0, 100, 255), CELL_SIZE)
                cx, cy = current_node
                _draw_cell(maze_surface, cx, cy, (255, 255, 0), CELL_SIZE)
            
            screen.blit(maze_surface, (0, 0))

            # Stvaranje površine za statistiku
            stats_surface = pygame.Surface((stats_panel_width, WINDOW_HEIGHT))
            stats_surface.fill((200, 200, 200))
            
            if state == STATE_SEARCHING:
                draw_live_stats(stats_surface, font, search_status, nodes_visited_live, time_elapsed_live, stats_panel_width)
            elif state == STATE_FINISHED:
                draw_final_stats(stats_surface, font, search_status, path_length, nodes_visited_live, time_elapsed_live, stats_panel_width)

            screen.blit(stats_surface, (stats_panel_x, 0))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()