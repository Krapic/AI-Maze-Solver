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
    draw_single_maze_comparison_panel, # NOVA funkcija
    BLACK,
    WHITE,
    RED
)

# Fiksne dimenzije prozora
WINDOW_WIDTH  = 1920
WINDOW_HEIGHT = 1080

# Veličina ćelije labirinta
CELL_SIZE = 25

# Mjerenje vremena ograničenja
TIME_LIMIT = 10.0 # Sekunde

# Stanja aplikacije
STATE_DIFFICULTY = 0
STATE_ALGORITHM  = 1
STATE_SEARCHING  = 2
STATE_FINISHED   = 3
STATE_SINGLE_MAZE_COMPARE = 4

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("AI Maze Solver")
    clock = pygame.time.Clock()
    try:
        font = pygame.font.SysFont("Arial", 28)
    except pygame.error:
        font = pygame.font.Font(None, 32) # Default Pygame font

    state = STATE_DIFFICULTY
    current_state_data = None # Inicijalizacija

    chosen_difficulty = None
    chosen_algorithm  = None 

    labyrinth = start = goal = None
    search_generator = None

    final_path         = None
    nodes_visited_live = 0
    time_elapsed_live  = 0.0
    path_length        = 0
    search_status      = "Nije započeto"
    search_start_ts    = 0.0

    current_maze_comparison_stats = {}
    
    # Za spremanje stanja prije ulaska u STATE_SINGLE_MAZE_COMPARE
    last_active_search_details = {} 

    maze_panel_width  = WINDOW_WIDTH * 2 // 3
    stats_panel_width = WINDOW_WIDTH - maze_panel_width
    stats_panel_x     = maze_panel_width

    difficulty_btns = []
    algorithm_btns  = []

    running = True
    while running:
        screen.fill((255, 255, 255)) 

        if state == STATE_DIFFICULTY:
            difficulty_btns = draw_difficulty_menu(screen, font, chosen_difficulty)
        elif state == STATE_ALGORITHM:
            algorithm_btns = draw_algorithm_menu(screen, font, chosen_algorithm, chosen_difficulty)
        
        elif state in (STATE_SEARCHING, STATE_FINISHED):
            maze_surface = pygame.Surface((maze_panel_width, WINDOW_HEIGHT))
            maze_surface.fill((230, 230, 230)) 
            if labyrinth and start and goal : # Osiguraj da su svi potrebni podaci tu
                draw_labyrinth(maze_surface, labyrinth, start, goal, final_path, CELL_SIZE)
            else: # Ako nema labirinta, prikaži poruku na maze_surface
                placeholder_font = pygame.font.Font(None, 40)
                text_surf = placeholder_font.render("Generiranje labirinta...", True, BLACK)
                text_rect = text_surf.get_rect(center=(maze_panel_width//2, WINDOW_HEIGHT//2))
                maze_surface.blit(text_surf, text_rect)


            if state == STATE_SEARCHING and current_state_data and current_state_data[0] == "searching":
                if len(current_state_data) >= 4:
                    visited_s, current_node_s, path_so_far_s = (
                        current_state_data[1], current_state_data[2], current_state_data[3]
                    )
                    if visited_s:
                        for (vx, vy) in visited_s:
                            _draw_cell(maze_surface, vx, vy, (150, 200, 255), CELL_SIZE) 
                    if path_so_far_s:
                        for (px, py) in path_so_far_s:
                            _draw_cell(maze_surface, px, py, (0, 100, 255), CELL_SIZE) 
                    if current_node_s:
                        cx_s, cy_s = current_node_s
                        _draw_cell(maze_surface, cx_s, cy_s, (255, 255, 0), CELL_SIZE) 
            
            screen.blit(maze_surface, (0, 0))

            stats_surface = pygame.Surface((stats_panel_width, WINDOW_HEIGHT))
            if state == STATE_SEARCHING:
                draw_live_stats(stats_surface, font, search_status, nodes_visited_live, time_elapsed_live, stats_panel_width)
            elif state == STATE_FINISHED: 
                draw_final_stats(stats_surface, font, search_status, path_length, nodes_visited_live, time_elapsed_live, stats_panel_width)
            screen.blit(stats_surface, (stats_panel_x, 0))

        elif state == STATE_SINGLE_MAZE_COMPARE:
            maze_surface = pygame.Surface((maze_panel_width, WINDOW_HEIGHT))
            maze_surface.fill((230, 230, 230))
            if labyrinth and start and goal:
                draw_labyrinth(maze_surface, labyrinth, start, goal, None, CELL_SIZE) 
            screen.blit(maze_surface, (0,0))

            comparison_panel_surface = pygame.Surface((stats_panel_width, WINDOW_HEIGHT))
            draw_single_maze_comparison_panel(comparison_panel_surface, font, current_maze_comparison_stats, stats_panel_width)
            screen.blit(comparison_panel_surface, (stats_panel_x, 0))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False 

            if state == STATE_DIFFICULTY:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e: chosen_difficulty = 'easy'
                    elif event.key == pygame.K_m: chosen_difficulty = 'medium'
                    elif event.key == pygame.K_h: chosen_difficulty = 'hard'
                    elif event.key == pygame.K_RETURN and chosen_difficulty:
                        state = STATE_ALGORITHM
                        chosen_algorithm = None 
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    for btn_rect, value in difficulty_btns:
                        if btn_rect.collidepoint(mx, my):
                            chosen_difficulty = value
                            state = STATE_ALGORITHM
                            chosen_algorithm = None 
                            break
            
            elif state == STATE_ALGORITHM:
                def start_search(algo_name):
                    nonlocal labyrinth, start, goal, final_path, nodes_visited_live, current_state_data
                    nonlocal time_elapsed_live, path_length, search_status, search_generator
                    nonlocal search_start_ts, state, current_maze_comparison_stats
                    
                    # Generira labirint samo ako već ne postoji (npr. ako mijenjamo algoritam na postojećem)
                    # Ovo je logika za PRVO pokretanje nakon odabira algoritma
                    if labyrinth is None or algo_name != chosen_algorithm: # Ili ako se algoritam mijenja
                        labyrinth_data = generate_labyrinth(chosen_difficulty)
                        if labyrinth_data is None: 
                            print(f"Nije moguće generirati labirint za težinu: {chosen_difficulty}")
                            state = STATE_DIFFICULTY 
                            return
                        labyrinth, start, goal = labyrinth_data
                        current_maze_comparison_stats = {} # Resetira samo kad se generira NOVI labirint

                    current_state_data = None # Resetira podatke o stanju pretrage
                    final_path = None
                    nodes_visited_live = 0
                    time_elapsed_live = 0.0
                    path_length = 0
                    search_status = f"Priprema za {algo_name.upper()}..."
                    
                    if algo_name == 'bfs':
                        search_generator = bfs_search_generator(labyrinth, start, goal, TIME_LIMIT)
                    elif algo_name == 'dfs':
                        search_generator = dfs_search_generator(labyrinth, start, goal, TIME_LIMIT)
                    elif algo_name == 'astar':
                        search_generator = astar_search_generator(labyrinth, start, goal, TIME_LIMIT)
                    else:
                        return 

                    search_start_ts = time.time()
                    state = STATE_SEARCHING

                if event.type == pygame.KEYDOWN:
                    temp_chosen_algorithm = None
                    if event.key == pygame.K_1: temp_chosen_algorithm = 'bfs'
                    elif event.key == pygame.K_2: temp_chosen_algorithm = 'dfs'
                    elif event.key == pygame.K_3: temp_chosen_algorithm = 'astar'
                    
                    if temp_chosen_algorithm:
                        chosen_algorithm = temp_chosen_algorithm
                        # Ne pokreće odmah, čeka Enter ili ako je već odabran pa se mijenja
                    
                    elif event.key == pygame.K_RETURN and chosen_algorithm:
                        labyrinth = None # Forsiranje generiranja novog labirinta
                        start_search(chosen_algorithm)


                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    for btn_rect, value in algorithm_btns:
                        if btn_rect.collidepoint(mx, my):
                            chosen_algorithm = value
                            labyrinth = None # Forsiranje generiranja novog labirinta
                            start_search(chosen_algorithm)
                            break
            
            elif state == STATE_FINISHED:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r: 
                        state = STATE_DIFFICULTY
                        chosen_difficulty = None
                        chosen_algorithm = None
                        labyrinth = None 
                        current_maze_comparison_stats = {}
                        last_active_search_details = {}
                    elif event.key == pygame.K_c: 
                        if current_maze_comparison_stats:
                            # Spremanje trenutnih detalja PRIJE NEGO što uđemo u usporedbu
                            last_active_search_details = {
                                'algorithm': chosen_algorithm,
                                'final_path': final_path,
                                'path_length': path_length,
                                'search_status': search_status,
                                'nodes_visited': nodes_visited_live,
                                'time_elapsed': time_elapsed_live
                            }
                            state = STATE_SINGLE_MAZE_COMPARE
                        else:
                            print("Nema podataka za usporedbu.")
                    elif event.key in (pygame.K_b, pygame.K_d, pygame.K_a):
                        algo_to_run = None
                        if event.key == pygame.K_b: algo_to_run = 'bfs'
                        elif event.key == pygame.K_d: algo_to_run = 'dfs'
                        elif event.key == pygame.K_a: algo_to_run = 'astar'

                        if algo_to_run and labyrinth: # Osiguravanje da labirint postoji
                            print(f"Pokretanje {algo_to_run.upper()} na istom labirintu.")
                            chosen_algorithm = algo_to_run 
                            
                            final_path = None
                            nodes_visited_live = 0
                            time_elapsed_live = 0.0
                            path_length = 0
                            search_status = f"Priprema za {chosen_algorithm.upper()}..."
                            current_state_data = None

                            if chosen_algorithm == 'bfs':
                                search_generator = bfs_search_generator(labyrinth, start, goal, TIME_LIMIT)
                            elif chosen_algorithm == 'dfs':
                                search_generator = dfs_search_generator(labyrinth, start, goal, TIME_LIMIT)
                            else: 
                                search_generator = astar_search_generator(labyrinth, start, goal, TIME_LIMIT)
                            
                            search_start_ts = time.time()
                            state = STATE_SEARCHING 

            elif state == STATE_SINGLE_MAZE_COMPARE:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r: 
                        state = STATE_DIFFICULTY
                        chosen_difficulty = None
                        chosen_algorithm = None
                        labyrinth = None
                        current_maze_comparison_stats = {}
                        last_active_search_details = {}
                    elif event.key == pygame.K_BACKSPACE: 
                        if last_active_search_details:
                            chosen_algorithm = last_active_search_details.get('algorithm')
                            final_path = last_active_search_details.get('final_path')
                            path_length = last_active_search_details.get('path_length',0)
                            search_status = last_active_search_details.get('search_status',"Status nepoznat")
                            nodes_visited_live = last_active_search_details.get('nodes_visited',0)
                            time_elapsed_live = last_active_search_details.get('time_elapsed',0.0)
                            state = STATE_FINISHED
                        else: # Fallback ako nema spremljenih detalja
                            state = STATE_DIFFICULTY
                            chosen_difficulty = None
                            chosen_algorithm = None
                            labyrinth = None
                            current_maze_comparison_stats = {}


        if state == STATE_SEARCHING:
            if search_generator is None: # Osiguranje da generator postoji
                print("Greška: search_generator nije inicijaliziran.")
                state = STATE_ALGORITHM # Vraćanje na odabir algoritma
                continue # Preskakanje ostatka petlje za ovaj frame

            try:
                current_state_data = next(search_generator)
                status_from_gen = current_state_data[0]

                if status_from_gen == "searching":
                    if len(current_state_data) < 4:
                        raise IndexError(f"Nedovoljno elemenata za 'searching': {len(current_state_data)}")
                    nodes_visited_live = len(current_state_data[1]) if current_state_data[1] else 0
                    time_elapsed_live  = time.time() - search_start_ts
                    search_status = f"Pretraga u tijeku ({chosen_algorithm.upper()})"

                elif status_from_gen in ("found", "timeout", "no_path"):
                    state = STATE_FINISHED 

                    if status_from_gen == "found":
                        if len(current_state_data) < 4: raise IndexError(f"Nedovoljno elemenata za 'found': {len(current_state_data)}")
                        final_path = current_state_data[1]
                        nodes_visited_live = current_state_data[2]
                        time_elapsed_live = current_state_data[3]
                        path_length = len(final_path) if final_path else 0
                        search_status = f"Pronađen put ({chosen_algorithm.upper()})"
                    
                    elif status_from_gen == "timeout":
                        if len(current_state_data) < 3: raise IndexError(f"Nedovoljno elemenata za 'timeout': {len(current_state_data)}")
                        nodes_visited_live = current_state_data[1]
                        time_elapsed_live = current_state_data[2]
                        final_path = None
                        path_length = 0
                        search_status = f"Isteklo vrijeme ({chosen_algorithm.upper()})"

                    elif status_from_gen == "no_path":
                        if len(current_state_data) < 3: raise IndexError(f"Nedovoljno elemenata za 'no_path': {len(current_state_data)}")
                        nodes_visited_live = current_state_data[1]
                        time_elapsed_live = current_state_data[2]
                        final_path = None
                        path_length = 0
                        search_status = f"Nema puta ({chosen_algorithm.upper()})"
                    
                    clean_status_for_comparison = search_status.split('(')[0].strip()
                    current_maze_comparison_stats[chosen_algorithm] = {
                        'status': clean_status_for_comparison,
                        'path_length': path_length,
                        'nodes': nodes_visited_live,
                        'time': time_elapsed_live
                    }
                    print(f"Spremljeni rezultati za {chosen_algorithm}: {current_maze_comparison_stats[chosen_algorithm]}")

                else:
                    raise ValueError(f"Nepoznat status iz generatora: {status_from_gen}")

            except StopIteration:
                print("Generator zaustavljen bez konačnog statusa.")
                search_status = f"Pretraga ({chosen_algorithm.upper()}) - nepoznat ishod"
                if chosen_algorithm and chosen_algorithm not in current_maze_comparison_stats : 
                    current_maze_comparison_stats[chosen_algorithm] = {
                        'status': "Nepoznat ishod", 'path_length': 0, 
                        'nodes': nodes_visited_live, 'time': time.time() - search_start_ts
                    }
                state = STATE_FINISHED
            
            except Exception as e:
                print(f"GREŠKA tijekom pretrage ({chosen_algorithm.upper()}): {e}")
                import traceback
                traceback.print_exc() 
                search_status = f"Greška ({chosen_algorithm.upper()})"
                if chosen_algorithm and chosen_algorithm not in current_maze_comparison_stats:
                    current_maze_comparison_stats[chosen_algorithm] = {
                        'status': "Greška", 'path_length': 0,
                        'nodes': nodes_visited_live, 'time': time.time() - search_start_ts
                    }
                state = STATE_FINISHED
        
        clock.tick(60) 

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()