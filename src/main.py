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
    _draw_cell, # Ako se koristi direktno, inače se može maknuti ako je samo interno u pygame_ui
    draw_live_stats,
    draw_final_stats,
    # draw_comparison_panel, # Stari panel za usporedbu po težinama, može ostati ako ga želite zadržati
    draw_single_maze_comparison_panel # NOVA funkcija
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
# STATE_COMPARE    = 4   # novo stanje za usporedbu
STATE_SINGLE_MAZE_COMPARE = 4

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("AI Maze Solver")
    clock = pygame.time.Clock()
    # Pokušajte s generičkim fontom ako "Arial" nije dostupan na svim sustavima
    try:
        font = pygame.font.SysFont("Arial", 28)
    except pygame.error:
        font = pygame.font.Font(None, 32) # Default Pygame font

    state = STATE_DIFFICULTY

    chosen_difficulty = None
    chosen_algorithm  = None # Algoritam koji se trenutno izvršava ili je zadnje izvršen

    labyrinth = start = goal = None
    search_generator = None

    # Varijable za statistiku trenutnog algoritma
    final_path         = None
    nodes_visited_live = 0
    time_elapsed_live  = 0.0
    path_length        = 0
    search_status      = "Nije započeto"
    search_start_ts    = 0.0

    # Rječnik za spremanje rezultata usporedbe algoritama na TRENUTNOM labirintu
    # Format: {'bfs': {'status': '...', 'path_length': X, 'nodes': Y, 'time': Z.ZZ}, ...}
    current_maze_comparison_stats = {}

    # Stari 'results' rječnik za usporedbu po težinama - uklonite ako se više ne koristi ta funkcionalnost
    # results = {
    #     "bfs":   {"easy": (0, 0.0), "medium": (0, 0.0), "hard": (0, 0.0)},
    #     "dfs":   {"easy": (0, 0.0), "medium": (0, 0.0), "hard": (0, 0.0)},
    #     "astar": {"easy": (0, 0.0), "medium": (0, 0.0), "hard": (0, 0.0)}
    # }

    maze_panel_width  = WINDOW_WIDTH * 2 // 3
    stats_panel_width = WINDOW_WIDTH - maze_panel_width
    stats_panel_x     = maze_panel_width

    difficulty_btns = []
    algorithm_btns  = []

    running = True
    while running:
        # 1) CRTANJE ovisno o stanju
        screen.fill((255, 255, 255)) # Očisti ekran na početku svakog frame-a

        if state == STATE_DIFFICULTY:
            difficulty_btns = draw_difficulty_menu(screen, font, chosen_difficulty)
        elif state == STATE_ALGORITHM:
            algorithm_btns = draw_algorithm_menu(screen, font, chosen_algorithm, chosen_difficulty)
        
        elif state in (STATE_SEARCHING, STATE_FINISHED):
            # Labirint dio
            maze_surface = pygame.Surface((maze_panel_width, WINDOW_HEIGHT))
            maze_surface.fill((230, 230, 230)) # Malo drugačija pozadina za labirint
            if labyrinth: # Provjeri postoji li labirint prije crtanja
                 draw_labyrinth(maze_surface, labyrinth, start, goal, final_path, CELL_SIZE)

            if state == STATE_SEARCHING and 'current_state_data' in locals() and current_state_data[0] == "searching":
                # Provjeri postoji li current_state_data i je li ispravnog formata
                if len(current_state_data) >= 4:
                    visited_s, current_node_s, path_so_far_s = (
                        current_state_data[1],
                        current_state_data[2],
                        current_state_data[3]
                    )
                    if visited_s: # Provjeri da nije None
                        for (vx, vy) in visited_s:
                            _draw_cell(maze_surface, vx, vy, (150, 200, 255), CELL_SIZE) # Boja posjećenih
                    if path_so_far_s: # Provjeri da nije None
                        for (px, py) in path_so_far_s:
                            _draw_cell(maze_surface, px, py, (0, 100, 255), CELL_SIZE) # Boja trenutne putanje
                    if current_node_s: # Provjeri da nije None
                        cx_s, cy_s = current_node_s
                        _draw_cell(maze_surface, cx_s, cy_s, (255, 255, 0), CELL_SIZE) # Boja trenutnog čvora (žuta)
            
            screen.blit(maze_surface, (0, 0))

            # Statistički panel dio
            stats_surface = pygame.Surface((stats_panel_width, WINDOW_HEIGHT))
            # stats_surface.fill((220, 220, 220)) # Boja za statistički panel
            if state == STATE_SEARCHING:
                draw_live_stats(stats_surface, font, search_status, nodes_visited_live, time_elapsed_live, stats_panel_width)
            elif state == STATE_FINISHED: # Samo STATE_FINISHED ovdje crta finalne statistike
                draw_final_stats(stats_surface, font, search_status, path_length, nodes_visited_live, time_elapsed_live, stats_panel_width)
            screen.blit(stats_surface, (stats_panel_x, 0))

        elif state == STATE_SINGLE_MAZE_COMPARE:
            # Crtanje labirinta (možda bez istaknutog puta)
            maze_surface = pygame.Surface((maze_panel_width, WINDOW_HEIGHT))
            maze_surface.fill((230, 230, 230))
            if labyrinth:
                draw_labyrinth(maze_surface, labyrinth, start, goal, None, CELL_SIZE) # Bez final_path-a ovdje
            screen.blit(maze_surface, (0,0))

            # Panel za usporedbu statistika za trenutni labirint
            comparison_panel_surface = pygame.Surface((stats_panel_width, WINDOW_HEIGHT))
            # comparison_panel_surface.fill((220,220,220)) # Pozadina za panel usporedbe
            draw_single_maze_comparison_panel(comparison_panel_surface, font, current_maze_comparison_stats, stats_panel_width)
            screen.blit(comparison_panel_surface, (stats_panel_x, 0))

        pygame.display.flip()

        # 2) OBRADA DOGAĐAJA
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False # ESC uvijek izlazi

            # ------ STATE_DIFFICULTY ------
            if state == STATE_DIFFICULTY:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e: chosen_difficulty = 'easy'
                    elif event.key == pygame.K_m: chosen_difficulty = 'medium'
                    elif event.key == pygame.K_h: chosen_difficulty = 'hard'
                    elif event.key == pygame.K_RETURN and chosen_difficulty:
                        state = STATE_ALGORITHM
                        chosen_algorithm = None # Resetiraj odabir algoritma za novi odabir težine
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    for btn_rect, value in difficulty_btns:
                        if btn_rect.collidepoint(mx, my):
                            chosen_difficulty = value
                            state = STATE_ALGORITHM
                            chosen_algorithm = None # Resetiraj
                            break
            
            # ------ STATE_ALGORITHM ------
            elif state == STATE_ALGORITHM:
                # Funkcija za pokretanje pretrage da se izbjegne ponavljanje koda
                def start_search(algo_name):
                    nonlocal labyrinth, start, goal, final_path, nodes_visited_live
                    nonlocal time_elapsed_live, path_length, search_status, search_generator
                    nonlocal search_start_ts, state, current_maze_comparison_stats
                    
                    labyrinth, start, goal = generate_labyrinth(chosen_difficulty)
                    if labyrinth is None: # Ako generator nije uspio
                        print(f"Nije moguće generirati labirint za težinu: {chosen_difficulty}")
                        state = STATE_DIFFICULTY # Vrati na odabir težine
                        return

                    current_maze_comparison_stats = {} # Resetiraj statistike za novi labirint

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
                        return # Nepoznati algoritam

                    search_start_ts = time.time()
                    state = STATE_SEARCHING

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1: chosen_algorithm = 'bfs'
                    elif event.key == pygame.K_2: chosen_algorithm = 'dfs'
                    elif event.key == pygame.K_3: chosen_algorithm = 'astar'
                    elif event.key == pygame.K_RETURN and chosen_algorithm:
                        start_search(chosen_algorithm)

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    for btn_rect, value in algorithm_btns:
                        if btn_rect.collidepoint(mx, my):
                            chosen_algorithm = value
                            start_search(chosen_algorithm)
                            break
            
            # ------ STATE_FINISHED ------
            elif state == STATE_FINISHED:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r: # Reset na odabir težine
                        state = STATE_DIFFICULTY
                        chosen_difficulty = None
                        chosen_algorithm = None
                        labyrinth = None # Resetiraj labirint
                        current_maze_comparison_stats = {}
                    elif event.key == pygame.K_c: # Prikaži usporedbu za trenutni labirint
                        if current_maze_comparison_stats:
                            state = STATE_SINGLE_MAZE_COMPARE
                        else:
                            print("Nema podataka za usporedbu.")
                    # Tipke za pokretanje drugih algoritama na ISTOM labirintu
                    elif event.key in (pygame.K_b, pygame.K_d, pygame.K_a):
                        algo_to_run = None
                        if event.key == pygame.K_b: algo_to_run = 'bfs'
                        elif event.key == pygame.K_d: algo_to_run = 'dfs'
                        elif event.key == pygame.K_a: algo_to_run = 'astar'

                        if algo_to_run:
                            # Ako želimo spriječiti ponovno pokretanje već izvršenog:
                            # if algo_to_run in current_maze_comparison_stats:
                            #    print(f"{algo_to_run.upper()} je već izvršen i spremljen.")
                            #    chosen_algorithm = algo_to_run # Postavi da je on 'trenutni' za prikaz
                            #    # Učitaj njegove spremljene podatke u final_path, path_length, itd. za prikaz
                            #    # Ovo može biti kompliciranije, jednostavnije je samo pokrenuti ponovo ili preskočiti
                            #    continue 
                            
                            print(f"Pokretanje {algo_to_run.upper()} na istom labirintu.")
                            chosen_algorithm = algo_to_run # Postavi novi algoritam kao trenutni
                            
                            # Resetiraj varijable za novo pretraživanje
                            final_path = None
                            nodes_visited_live = 0
                            time_elapsed_live = 0.0
                            path_length = 0
                            search_status = f"Priprema za {chosen_algorithm.upper()}..."

                            if chosen_algorithm == 'bfs':
                                search_generator = bfs_search_generator(labyrinth, start, goal, TIME_LIMIT)
                            elif chosen_algorithm == 'dfs':
                                search_generator = dfs_search_generator(labyrinth, start, goal, TIME_LIMIT)
                            else: # astar
                                search_generator = astar_search_generator(labyrinth, start, goal, TIME_LIMIT)
                            
                            search_start_ts = time.time()
                            state = STATE_SEARCHING # Vrati se u pretragu

            # ------ STATE_SINGLE_MAZE_COMPARE ------
            elif state == STATE_SINGLE_MAZE_COMPARE:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r: # Reset na odabir težine
                        state = STATE_DIFFICULTY
                        chosen_difficulty = None
                        chosen_algorithm = None
                        labyrinth = None
                        current_maze_comparison_stats = {}
                    elif event.key == pygame.K_BACKSPACE: # Povratak na zadnje riješeni algoritam
                         state = STATE_FINISHED 
                         # Ovdje bi trebalo vratiti `final_path`, `path_length` itd. na vrijednosti
                         # od `chosen_algorithm` koji je bio aktivan prije ulaska u usporedbu.
                         # Ovo može zahtijevati spremanje tih vrijednosti.
                         # Jednostavnija opcija je da Backspace također vodi na STATE_DIFFICULTY ili STATE_ALGORITHM.
                         # Za sada, neka R i ESC budu glavne navigacije odavde.

        # 3) LOGIKA PRETRAGE (kada je state == STATE_SEARCHING)
        if state == STATE_SEARCHING:
            try:
                current_state_data = next(search_generator)
                # print("DEBUG: current_state_data =", current_state_data) # Za debugiranje

                if not isinstance(current_state_data, tuple) or len(current_state_data) < 1:
                    print("Generator vratio nevažeći format podataka:", current_state_data)
                    raise ValueError("Generator vratio nevažeći format podataka.")

                status_from_gen = current_state_data[0]

                if status_from_gen == "searching":
                    if len(current_state_data) < 4:
                        raise IndexError(f"Nedovoljno elemenata za 'searching': {len(current_state_data)}")
                    # visited_set, current_node, path_currently_explored = current_state_data[1], current_state_data[2], current_state_data[3]
                    # Ove varijable se koriste direktno u sekciji crtanja za STATE_SEARCHING
                    nodes_visited_live = len(current_state_data[1]) if current_state_data[1] else 0
                    time_elapsed_live  = time.time() - search_start_ts
                    search_status = f"Pretraga u tijeku ({chosen_algorithm.upper()})"

                elif status_from_gen in ("found", "timeout", "no_path"):
                    state = STATE_FINISHED # Prelazak u stanje završetka

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
                    
                    # Spremi rezultate za trenutni algoritam u rječnik za usporedbu
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
                # Ako generator završi bez yieldanja konačnog statusa,
                # to je greška u generatoru. Postavi neki defaultni status.
                search_status = f"Pretraga završena ({chosen_algorithm.upper()}) - nepoznat ishod"
                if chosen_algorithm not in current_maze_comparison_stats : # Ako nije već spremljeno
                    current_maze_comparison_stats[chosen_algorithm] = {
                        'status': "Nepoznat ishod", 'path_length': 0, 
                        'nodes': nodes_visited_live, 'time': time.time() - search_start_ts
                    }
                state = STATE_FINISHED
            
            except Exception as e:
                print(f"GREŠKA tijekom pretrage ({chosen_algorithm.upper()}): {e}")
                import traceback
                traceback.print_exc() # Ispiši cijeli traceback za lakše debugiranje
                search_status = f"Greška ({chosen_algorithm.upper()})"
                if chosen_algorithm not in current_maze_comparison_stats:
                    current_maze_comparison_stats[chosen_algorithm] = {
                        'status': "Greška", 'path_length': 0,
                        'nodes': nodes_visited_live, 'time': time.time() - search_start_ts
                    }
                state = STATE_FINISHED
        
        clock.tick(60) # Ograniči FPS

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
