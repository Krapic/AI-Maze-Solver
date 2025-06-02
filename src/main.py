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
    draw_final_stats,
    draw_comparison_panel
)

# Fiksne dimenzije prozora
WINDOW_WIDTH  = 1280
WINDOW_HEIGHT = 720

# Veličina ćelije labirinta
CELL_SIZE = 25

# Mjerenje vremena ograničenja
TIME_LIMIT = 10.0

# Stanja aplikacije
STATE_DIFFICULTY = 0
STATE_ALGORITHM  = 1
STATE_SEARCHING  = 2
STATE_FINISHED   = 3
STATE_COMPARE    = 4   # novo stanje za usporedbu

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("AI Maze Solver")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 28)
    state = STATE_DIFFICULTY

    chosen_difficulty = None
    chosen_algorithm  = None

    labyrinth = start = goal = None
    search_generator = None

    # Varijable za statistiku trenutnog algoritma
    final_path         = None
    nodes_visited_live = 0
    time_elapsed_live  = 0.0
    path_length        = 0
    search_status      = "Nije započeto"
    search_start_ts    = 0.0

    # Za usporedbu: rječnik u koji ćemo spremiti rezultate po težini
    results = {
        "bfs":   {"easy": (0, 0.0), "medium": (0, 0.0), "hard": (0, 0.0)},
        "dfs":   {"easy": (0, 0.0), "medium": (0, 0.0), "hard": (0, 0.0)},
        "astar": {"easy": (0, 0.0), "medium": (0, 0.0), "hard": (0, 0.0)}
    }

    # Dimenzije panela
    maze_panel_width  = WINDOW_WIDTH * 2 // 3
    stats_panel_width = WINDOW_WIDTH - maze_panel_width
    stats_panel_x     = maze_panel_width

    # Spremnici za rectove gumbića
    difficulty_btns = []
    algorithm_btns  = []

    running = True
    while running:
        # 1) Prvo nacrtaj izbornik (ili ništa ako smo u pretrazi/rezultatima/uspore)
        if state == STATE_DIFFICULTY:
            difficulty_btns = draw_difficulty_menu(screen, font, chosen_difficulty)
        elif state == STATE_ALGORITHM:
            algorithm_btns = draw_algorithm_menu(screen, font, chosen_algorithm, chosen_difficulty)
        elif state == STATE_COMPARE:
            draw_comparison_panel(screen, font, results)
        # Ako smo u STATE_SEARCHING ili STATE_FINISHED, crtanje je naknadno

        pygame.display.flip()

        # 2) Obrada događaja
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # ESC iz bilo kojeg stanja izlazi
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            # ------ STATE_DIFFICULTY ------
            if state == STATE_DIFFICULTY:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        chosen_difficulty = 'easy'
                    elif event.key == pygame.K_m:
                        chosen_difficulty = 'medium'
                    elif event.key == pygame.K_h:
                        chosen_difficulty = 'hard'
                    elif event.key == pygame.K_RETURN and chosen_difficulty:
                        state = STATE_ALGORITHM

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    for (rect, value) in difficulty_btns:
                        if rect.collidepoint(mx, my):
                            chosen_difficulty = value
                            state = STATE_ALGORITHM
                            break

            # ------ STATE_ALGORITHM ------
            elif state == STATE_ALGORITHM:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        chosen_algorithm = 'bfs'
                    elif event.key == pygame.K_2:
                        chosen_algorithm = 'dfs'
                    elif event.key == pygame.K_3:
                        chosen_algorithm = 'astar'
                    elif event.key == pygame.K_RETURN and chosen_algorithm:
                        labyrinth, start, goal = generate_labyrinth(chosen_difficulty)
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
                        search_start_ts = time.time()
                        state = STATE_SEARCHING

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    for (rect, value) in algorithm_btns:
                        if rect.collidepoint(mx, my):
                            chosen_algorithm = value
                            # Automatski pokreni pretragu
                            labyrinth, start, goal = generate_labyrinth(chosen_difficulty)
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
                            search_start_ts = time.time()
                            state = STATE_SEARCHING
                            break

            # ------ STATE_SEARCHING i STATE_FINISHED ------
            elif state in (STATE_SEARCHING, STATE_FINISHED):
                if state == STATE_FINISHED and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # reset
                        state = STATE_DIFFICULTY
                        chosen_difficulty = None
                        chosen_algorithm = None
                        final_path = None
                        nodes_visited_live = 0
                        time_elapsed_live = 0.0
                        path_length = 0
                        search_status = "Nije započeto"
                        # Reset rezultata
                        results = {
                            "bfs":   {"easy": (0, 0.0), "medium": (0, 0.0), "hard": (0, 0.0)},
                            "dfs":   {"easy": (0, 0.0), "medium": (0, 0.0), "hard": (0, 0.0)},
                            "astar": {"easy": (0, 0.0), "medium": (0, 0.0), "hard": (0, 0.0)}
                        }

                    elif event.key == pygame.K_c:
                        # Pokreni usporedbu: za svaku težinu i algoritam po 3 puta, uzmi prosjek
                        for diff in ("easy", "medium", "hard"):
                            labyrinth_d, start_d, goal_d = generate_labyrinth(diff)

                            for alg in ("bfs", "dfs", "astar"):
                                total_nodes = 0
                                total_time  = 0.0
                                runs = 3
                                for _ in range(runs):
                                    if alg == "bfs":
                                        gen = bfs_search_generator(labyrinth_d, start_d, goal_d, TIME_LIMIT)
                                    elif alg == "dfs":
                                        gen = dfs_search_generator(labyrinth_d, start_d, goal_d, TIME_LIMIT)
                                    else:
                                        gen = astar_search_generator(labyrinth_d, start_d, goal_d, TIME_LIMIT)

                                    last_info = None
                                    for last_info in gen:
                                        pass

                                    status = last_info[0]
                                    if status == "found":
                                        if len(last_info) >= 4:
                                            _, path, nodes, dur = last_info
                                        else:
                                            _, path = last_info
                                            nodes = 0
                                            dur = 0.0
                                    else:
                                        if len(last_info) >= 3:
                                            _, nodes, dur = last_info
                                        else:
                                            nodes = 0
                                            dur = 0.0

                                    total_nodes += nodes
                                    total_time  += dur

                                avg_nodes = total_nodes // runs
                                avg_time  = total_time / runs
                                results[alg][diff] = (avg_nodes, avg_time)

                        state = STATE_COMPARE

            # ------ STATE_COMPARE ------
            elif state == STATE_COMPARE:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Reset i natrag na početak
                        state = STATE_DIFFICULTY
                        chosen_difficulty = None
                        chosen_algorithm = None
                        final_path = None
                        nodes_visited_live = 0
                        time_elapsed_live = 0.0
                        path_length = 0
                        search_status = "Nije započeto"
                        # Reset rezultata
                        results = {
                            "bfs":   {"easy": (0, 0.0), "medium": (0, 0.0), "hard": (0, 0.0)},
                            "dfs":   {"easy": (0, 0.0), "medium": (0, 0.0), "hard": (0, 0.0)},
                            "astar": {"easy": (0, 0.0), "medium": (0, 0.0), "hard": (0, 0.0)}
                        }

        # 3) LOGIKA PRETRAGE
        if state == STATE_SEARCHING:
            try:
                current_state_data = next(search_generator)
                print("DEBUG: current_state_data =", current_state_data)

                if not isinstance(current_state_data, tuple) or len(current_state_data) < 1:
                    raise ValueError("Generator vratio nevažeći format podataka.")

                status = current_state_data[0]

                if status == "searching":
                    if len(current_state_data) < 4:
                        raise IndexError(
                            "Previše malo elemenata za 'searching' status. Primljeno: {}".format(len(current_state_data))
                        )
                    visited      = current_state_data[1]
                    current_node = current_state_data[2]
                    path_so_far  = current_state_data[3]
                    nodes_visited_live = len(visited)
                    time_elapsed_live  = time.time() - search_start_ts
                    search_status = f"Pretraga u tijeku ({chosen_algorithm.upper()})"

                elif status == "found":
                    if len(current_state_data) == 2:
                        final_path = current_state_data[1]
                        nodes_visited_live = 0
                        time_elapsed_live  = time.time() - search_start_ts
                    else:
                        final_path = current_state_data[1]
                        nodes_visited_live = current_state_data[2]
                        time_elapsed_live  = current_state_data[3]

                    path_length   = len(final_path) if final_path else 0
                    search_status = f"Pronađen put ({chosen_algorithm.upper()})"
                    state = STATE_FINISHED

                elif status == "timeout":
                    if len(current_state_data) < 3:
                        raise IndexError(
                            "Previše malo elemenata za 'timeout' status. Primljeno: {}".format(len(current_state_data))
                        )
                    nodes_visited_live = current_state_data[1]
                    time_elapsed_live  = current_state_data[2]
                    final_path   = None
                    path_length  = 0
                    search_status = f"Isteklo vrijeme ({chosen_algorithm.upper()})"
                    state = STATE_FINISHED

                elif status == "no_path":
                    if len(current_state_data) < 3:
                        raise IndexError(
                            "Previše malo elemenata za 'no_path' status. Primljeno: {}".format(len(current_state_data))
                        )
                    nodes_visited_live = current_state_data[1]
                    time_elapsed_live  = current_state_data[2]
                    final_path   = None
                    path_length  = 0
                    search_status = f"Nema puta ({chosen_algorithm.upper()})"
                    state = STATE_FINISHED

                else:
                    raise ValueError(f"Nepoznat status dobiven iz generatora: {status}")

            except StopIteration:
                search_status = "Pretraga završena (nepoznat ishod)"
                state = STATE_FINISHED

            except Exception as e:
                print(f"GREŠKA tijekom pretrage: {e}")
                search_status = f"Greška: {e}"
                state = STATE_FINISHED

        # 4) CRTANJE STATE_SEARCHING i STATE_FINISHED
        if state in (STATE_SEARCHING, STATE_FINISHED):
            screen.fill((255, 255, 255))

            # Labirint
            maze_surface = pygame.Surface((maze_panel_width, WINDOW_HEIGHT))
            maze_surface.fill((255, 255, 255))
            draw_labyrinth(maze_surface, labyrinth, start, goal, final_path, CELL_SIZE)

            if state == STATE_SEARCHING and 'current_state_data' in locals() and current_state_data[0] == "searching":
                visited, current_node, path_so_far = (
                    current_state_data[1],
                    current_state_data[2],
                    current_state_data[3]
                )
                for (vx, vy) in visited:
                    _draw_cell(maze_surface, vx, vy, (150, 200, 255), CELL_SIZE)
                for (px, py) in path_so_far:
                    _draw_cell(maze_surface, px, py, (0, 100, 255), CELL_SIZE)
                cx, cy = current_node
                _draw_cell(maze_surface, cx, cy, (255, 255, 0), CELL_SIZE)

            screen.blit(maze_surface, (0, 0))

            # Statistika (svijetlo-siva pozadina panela)
            stats_surface = pygame.Surface((stats_panel_width, WINDOW_HEIGHT))
            stats_surface.fill((220, 220, 220))
            if state == STATE_SEARCHING:
                draw_live_stats(stats_surface, font, search_status, nodes_visited_live, time_elapsed_live, stats_panel_width)
            else:
                draw_final_stats(stats_surface, font, search_status, path_length, nodes_visited_live, time_elapsed_live, stats_panel_width)
            screen.blit(stats_surface, (stats_panel_x, 0))

            pygame.display.flip()

        # 5) STATE_COMPARE crtanje je već obavljeno gore

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
