import pygame

# Boje
DARK_BLUE       = (44, 62, 80)
MEDIUM_BLUE     = (52, 152, 219)
LIGHT_GRAY      = (220, 220, 220)
DARK_GRAY       = (100, 100, 100)
WHITE           = (255, 255, 255)
BLACK           = (0, 0, 0)
GREEN           = (0, 255, 0)
RED             = (255, 0, 0)
YELLOW          = (255, 255, 0)
ORANGE          = (255, 165, 0)
SELECTED_BTN    = (52, 152, 219)
UNSELECTED_BTN  = (149, 165, 166)

# Pomoćne funkcije -------------------------------------------------------

def _draw_centered_text(surface, text, font, color, rect):
    surf = font.render(text, True, color)
    text_rect = surf.get_rect(center=rect.center)
    surface.blit(surf, text_rect)

def draw_vertical_gradient(surface, top_color, bottom_color):
    """Iscrtava vertikalni gradient od top_color do bottom_color na cijeloj površini."""
    h = surface.get_height()
    w = surface.get_width()
    for y in range(h):
        ratio = y / (h - 1)
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * ratio)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * ratio)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (w, y))


# 1) DRAW_DIFFICULTY_MENU --------------------------------------------------

def draw_difficulty_menu(screen, font, selected):
    """
    Crta izbornik za odabir težine. 
    Vraća listu tuplova: [(pygame.Rect, "easy"), (pygame.Rect, "medium"), (pygame.Rect, "hard")].
    """
    screen_width  = screen.get_width()
    screen_height = screen.get_height()

    # Pozadina s blagim gradientom
    draw_vertical_gradient(screen, DARK_BLUE, (30, 50, 70))

    # Naslov
    title_text = font.render("Odaberi težinu labirinta", True, WHITE)
    title_rect = title_text.get_rect(center=(screen_width // 2, 100))
    screen.blit(title_text, title_rect)

    options = [("Lako (E)", "easy"), ("Srednje (M)", "medium"), ("Teško (H)", "hard")]
    y_start = 200
    button_width, button_height = 300, 60
    spacing = 20

    rects = []
    for i, (label, value) in enumerate(options):
        x = (screen_width - button_width) // 2
        y = y_start + i * (button_height + spacing)
        rect = pygame.Rect(x, y, button_width, button_height)
        color = SELECTED_BTN if selected == value else UNSELECTED_BTN
        pygame.draw.rect(screen, color, rect, border_radius=8)
        _draw_centered_text(screen, label, font, WHITE, rect)
        rects.append((rect, value))

    return rects


# 2) DRAW_ALGORITHM_MENU ----------------------------------------------------

def draw_algorithm_menu(screen, font, chosen_algorithm, chosen_difficulty):
    """
    Crta izbornik za odabir algoritma. 
    Vraća listu tuplova: [(pygame.Rect, "bfs"), (pygame.Rect, "dfs"), (pygame.Rect, "astar")].
    """
    screen_width  = screen.get_width()
    screen_height = screen.get_height()

    # Pozadina s blagim gradientom
    draw_vertical_gradient(screen, DARK_BLUE, (30, 50, 70))

    # Prikaz odabrane težine
    header_text = font.render(f"Težina: {chosen_difficulty.upper()}", True, WHITE)
    header_rect = header_text.get_rect(center=(screen_width // 2, 80))
    screen.blit(header_text, header_rect)

    # Naslov
    title_text = font.render("Odaberi algoritam", True, WHITE)
    title_rect = title_text.get_rect(center=(screen_width // 2, 140))
    screen.blit(title_text, title_rect)

    options = [("BFS (1)", "bfs"), ("DFS (2)", "dfs"), ("A* (3)", "astar")]
    button_width, button_height = 250, 60
    spacing = 20
    total_height = len(options) * button_height + (len(options) - 1) * spacing
    start_y = (screen_height // 2) - (total_height // 2)

    rects = []
    for i, (label, value) in enumerate(options):
        x = (screen_width - button_width) // 2
        y = start_y + i * (button_height + spacing)
        rect = pygame.Rect(x, y, button_width, button_height)
        color = SELECTED_BTN if chosen_algorithm == value else UNSELECTED_BTN
        pygame.draw.rect(screen, color, rect, border_radius=8)
        _draw_centered_text(screen, label, font, WHITE, rect)
        rects.append((rect, value))

    # Uputa
    instr_text = font.render("Pritisnite [ENTER] ili kliknite gumb za potvrdu", True, WHITE)
    instr_rect = instr_text.get_rect(center=(screen_width // 2, screen_height - 80))
    screen.blit(instr_text, instr_rect)

    return rects


# 3) DRAW_LABYRINTH ---------------------------------------------------------

def draw_labyrinth(surface, labyrinth, start, goal, final_path=None, cell_size=25):
    if labyrinth is None:
        return

    rows, cols = len(labyrinth), len(labyrinth[0])
    surface.fill(LIGHT_GRAY)

    # Crtanje svih ćelija (zid: crno, slobodno: bijelo)
    for y in range(rows):
        for x in range(cols):
            if labyrinth[y][x] == 1:
                color = BLACK
            else:
                color = WHITE
            _draw_cell(surface, x, y, color, cell_size)

    # Crtanje finalnog puta (ako postoji)
    if final_path:
        for (px, py) in final_path:
            _draw_cell(surface, px, py, YELLOW, cell_size)

    # Start i cilj (uvijek “na vrhu”)
    sx, sy = start
    gx, gy = goal
    _draw_cell(surface, sx, sy, GREEN, cell_size)
    _draw_cell(surface, gx, gy, RED, cell_size)


def _draw_cell(surface, x, y, color, cell_size):
    rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, DARK_GRAY, rect, 1)


# 4) DRAW_LIVE_STATS --------------------------------------------------------

def draw_live_stats(screen, font, status_text, nodes_visited, time_elapsed, panel_width):
    panel_height = screen.get_height()
    screen.fill(LIGHT_GRAY)

    margin = 20
    y_offset = margin

    # Naslov
    title_surf = font.render("STATISTIKA PRETRAGE", True, BLACK)
    title_rect = title_surf.get_rect(topleft=(margin, y_offset))
    screen.blit(title_surf, title_rect)
    y_offset += 40

    # Linija razdjelnika
    pygame.draw.line(screen, DARK_GRAY, (margin, y_offset), (panel_width - margin, y_offset), 2)
    y_offset += 20

    stats_lines = [
        ("Status:", status_text),
        ("Posjećeni čvorovi:", str(nodes_visited)),
        ("Vrijeme:", f"{time_elapsed:.4f} s")
    ]
    for label, value in stats_lines:
        label_surf = font.render(label, True, BLACK)
        value_surf = font.render(value, True, BLACK)
        screen.blit(label_surf, (margin, y_offset))
        screen.blit(value_surf, (margin + 200, y_offset))
        y_offset += 30

    # Upute
    y_offset = panel_height - 60
    instr_surf = font.render("Pritisnite [C] za usporedbu, [R] za novi labirint ili [ESC] za izlaz.", True, BLACK)
    screen.blit(instr_surf, (margin, y_offset))


# 5) DRAW_FINAL_STATS -------------------------------------------------------

def draw_final_stats(screen, font, status, path_length, nodes_visited, time_elapsed, panel_width):
    panel_height = screen.get_height()
    screen.fill(LIGHT_GRAY)

    margin = 20
    y_offset = margin

    # Naslov
    title_surf = font.render("REZULTATI PRETRAGE", True, BLACK)
    title_rect = title_surf.get_rect(topleft=(margin, y_offset))
    screen.blit(title_surf, title_rect)
    y_offset += 40

    # Razdjelna linija
    pygame.draw.line(screen, DARK_GRAY, (margin, y_offset), (panel_width - margin, y_offset), 2)
    y_offset += 20

    # Odredi boju i tekst statusa
    st_upper = status.upper()
    if "PRONAĐEN PUT" in st_upper:
        info_text = "Put pronađen!"
        color = GREEN
    elif "NEMA PUTA" in st_upper:
        info_text = "Nema puta!"
        color = RED
    elif "ISTEKLO VRIJEME" in st_upper:
        info_text = "Vremensko ograničenje isteklo!"
        color = ORANGE
    else:
        info_text = status
        color = BLACK

    status_surf = font.render(info_text, True, color)
    screen.blit(status_surf, (margin, y_offset))
    y_offset += 40

    stats_lines = [
        ("Duljina puta:", str(path_length)),
        ("Posjećeni čvorovi:", str(nodes_visited)),
        ("Vrijeme izvršavanja:", f"{time_elapsed:.4f} s")
    ]
    for label, value in stats_lines:
        label_surf = font.render(label, True, BLACK)
        value_surf = font.render(value, True, BLACK)
        screen.blit(label_surf, (margin, y_offset))
        screen.blit(value_surf, (margin + 200, y_offset))
        y_offset += 30

    y_offset += 20
    instr_lines = [
        ("[C] Usporedi algoritme", BLACK),
        ("[R] Novi labirint", BLACK),
        ("[ESC] Izlaz", BLACK)
    ]
    for i, (txt, col) in enumerate(instr_lines):
        instr_surf = font.render(txt, True, col)
        screen.blit(instr_surf, (margin, y_offset + i * 30))


# 6) DRAW_COMPARISON_PANEL --------------------------------------------------

def draw_comparison_panel(screen, font, results):
    """
    Crta “high‐tech” usporedbu: po težini (Easy, Medium, Hard) 
    crta bar-chart za broj posjećenih čvorova i vrijeme za BFS, DFS, A*.

    results: dict oblika {
        "bfs":   {"easy": (nodes, time),   "medium": (...),   "hard": (...)} ,
        "dfs":   {"easy": ...,            "medium": ...,     "hard": ...},
        "astar": {"easy": ...,            "medium": ...,     "hard": ...}
    }
    """
    screen.fill(LIGHT_GRAY)
    w = screen.get_width()
    h = screen.get_height()
    margin = 40
    title_y = margin

    # Naslov cijelog ekrana
    title = font.render("Usporedba algoritama po težini", True, BLACK)
    title_rect = title.get_rect(topleft=(margin, title_y))
    screen.blit(title, title_rect)

    # Legenda ispod naslova
    legend_y = title_y + 30
    pygame.draw.rect(screen, MEDIUM_BLUE, (margin, legend_y, 20, 20))
    screen.blit(font.render("BFS", True, BLACK), (margin + 25, legend_y))
    pygame.draw.rect(screen, ORANGE, (margin + 100, legend_y, 20, 20))
    screen.blit(font.render("DFS", True, BLACK), (margin + 125, legend_y))
    pygame.draw.rect(screen, RED, (margin + 200, legend_y, 20, 20))
    screen.blit(font.render("A*", True, BLACK), (margin + 225, legend_y))

    # Postavljanje dimenzija i pozicija za grafove
    chart_width  = w - 2 * margin
    chart_height = (h - (legend_y + 40) - margin) // 2  # podijeljeno na dva dijela

    # X-koordinate središta svake skupine (Easy, Medium, Hard)
    x_group_width = chart_width // 3
    x_centers = [margin + x_group_width * i + x_group_width // 2 for i in range(3)]

    # -----------------------
    # 1) Bar-chart za broj posjećenih čvorova
    # -----------------------
    # Prvo pronađi maksimum kroz sve rezultate
    all_nodes = []
    for alg in ("bfs", "dfs", "astar"):
        for diff in ("easy", "medium", "hard"):
            all_nodes.append(results[alg][diff][0])
    max_nodes = max(all_nodes) if all_nodes else 1

    chart1_top = legend_y + 40
    y_axis_bottom1 = chart1_top + chart_height

    # Naslov prvog charta iznad njega
    title1 = font.render("Broj posjećenih čvorova", True, BLACK)
    t1_rect = title1.get_rect(center=(w // 2, chart1_top - 20))
    screen.blit(title1, t1_rect)

    # Debljina polovine grupe za tri algoritma
    half_group = x_group_width // 4

    for i, diff in enumerate(("easy", "medium", "hard")):
        x_center = x_centers[i]

        # Vrijednosti za svaki algoritam
        bfs_nodes   = results["bfs"][diff][0]
        dfs_nodes   = results["dfs"][diff][0]
        astar_nodes = results["astar"][diff][0]

        vals = [bfs_nodes, dfs_nodes, astar_nodes]
        colors = [MEDIUM_BLUE, ORANGE, RED]

        for j, val in enumerate(vals):
            # unutar jednog x_centera, odmakni boje za -half, 0, +half
            x_bar_center = x_center + (j - 1) * half_group
            bar_h = int((val / max_nodes) * (chart_height - 20))  # 20 px prostor za vrh
            bar_x = x_bar_center - half_group // 2
            bar_y = y_axis_bottom1 - bar_h
            bar_rect = pygame.Rect(bar_x, bar_y, half_group, bar_h)
            pygame.draw.rect(screen, colors[j], bar_rect)
            # Ispiši vrijednost iznad bara
            txt = font.render(str(val), True, BLACK)
            txt_rect = txt.get_rect(center=(x_bar_center, bar_y - 10))
            screen.blit(txt, txt_rect)

        # Oznaka težine ispod barova
        diff_label = diff.capitalize()
        diff_surf  = font.render(diff_label, True, BLACK)  
        diff_rect  = diff_surf.get_rect(center=(x_center, y_axis_bottom1 + 20))
        screen.blit(diff_surf, diff_rect)

    # -----------------------
    # 2) Bar-chart za vrijeme
    # -----------------------
    all_times = []
    for alg in ("bfs", "dfs", "astar"):
        for diff in ("easy", "medium", "hard"):
            all_times.append(results[alg][diff][1])
    max_time = max(all_times) if all_times else 1.0

    chart2_top = y_axis_bottom1 + 50  # razmak između grafova
    y_axis_bottom2 = chart2_top + chart_height

    # Naslov drugog charta iznad njega
    title2 = font.render("Vrijeme izvršavanja (s)", True, BLACK)
    t2_rect = title2.get_rect(center=(w // 2, chart2_top - 20))
    screen.blit(title2, t2_rect)

    for i, diff in enumerate(("easy", "medium", "hard")):
        x_center = x_centers[i]

        bfs_time   = results["bfs"][diff][1]
        dfs_time   = results["dfs"][diff][1]
        astar_time = results["astar"][diff][1]

        vals_t = [bfs_time, dfs_time, astar_time]
        colors = [MEDIUM_BLUE, ORANGE, RED]

        for j, val in enumerate(vals_t):
            x_bar_center = x_center + (j - 1) * half_group
            bar_h = int((val / max_time) * (chart_height - 20))
            bar_x = x_bar_center - half_group // 2
            bar_y = y_axis_bottom2 - bar_h
            bar_rect = pygame.Rect(bar_x, bar_y, half_group, bar_h)
            pygame.draw.rect(screen, colors[j], bar_rect)
            txt = font.render(f"{val:.2f}", True, BLACK)
            txt_rect = txt.get_rect(center=(x_bar_center, bar_y - 10))
            screen.blit(txt, txt_rect)

        # Oznaka težine ispod barova (ponovo)
        diff_label = diff.capitalize()
        diff_surf  = font.render(diff_label, True, BLACK)
        diff_rect  = diff_surf.get_rect(center=(x_center, y_axis_bottom2 + 20))
        screen.blit(diff_surf, diff_rect)

    # -----------------------
    # Uputa za izlaz na dnu ekrana
    # -----------------------
    instr = font.render("[R] Novi labirint   [ESC] Izlaz", True, BLACK)
    instr_rect = instr.get_rect(center=(w // 2, h - margin))
    screen.blit(instr, instr_rect)
