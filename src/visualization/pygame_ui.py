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

def draw_text_wrapped(surface, text, font, color, rect, aa=True, bkg=None):
    """Crta tekst s prelamanjem unutar zadanog pravokutnika."""
    y = rect.top
    line_spacing = font.get_linesize() # Koristi preporučeni razmak linija za font

    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        # Provjeri stane li riječ + razmak na trenutnu liniju
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= rect.width:
            current_line = test_line
        else:
            # Ako ne stane, završi trenutnu liniju (bez zadnjeg razmaka)
            lines.append(current_line.rstrip())
            current_line = word + " " # Započni novu liniju s tom riječi
    lines.append(current_line.rstrip()) # Dodaj zadnju liniju

    for line in lines:
        if not line: # Preskoči prazne linije ako nastanu
            continue
        # Ako bi sljedeća linija prešla donji rub pravokutnika, a nije prva linija (da se izbjegne ...)
        if y + line_spacing > rect.bottom and lines.index(line) > 0 :
            # Uzmi što više stane od linije i dodaj "..."
            available_width = rect.width
            shortened_line = ""
            for char_idx in range(len(line)):
                if font.size(shortened_line + line[char_idx] + "...")[0] > available_width:
                    break
                shortened_line += line[char_idx]
            
            line_surf = font.render(shortened_line + "...", aa, color, bkg)
            surface.blit(line_surf, (rect.left, y))
            break # Prekini crtanje daljnjih linija

        line_surf = font.render(line, aa, color, bkg)
        surface.blit(line_surf, (rect.left, y))
        y += line_spacing
        if y >= rect.bottom: # Ako smo popunili rect vertikalno
            break

def _draw_centered_text(surface, text, font, color, rect):
    surf = font.render(text, True, color)
    text_rect = surf.get_rect(center=rect.center)
    surface.blit(surf, text_rect)

def draw_vertical_gradient(surface, top_color, bottom_color):
    """Iscrtava vertikalni gradient od top_color do bottom_color na cijeloj površini."""
    h = surface.get_height()
    w = surface.get_width()
    if h <=1: # Izbjegavanje dijeljenja s nulom ako je visina premala
        if h == 1:
             pygame.draw.line(surface, top_color, (0,0), (w,0))
        return

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
    header_text_content = f"Težina: {chosen_difficulty.upper()}" if chosen_difficulty else "Odaberite težinu"
    header_text = font.render(header_text_content, True, WHITE)
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
    instr_text_content = "Pritisnite [ENTER] ili kliknite gumb za potvrdu"
    instr_text_surf = font.render(instr_text_content, True, WHITE)
    instr_rect = instr_text_surf.get_rect(center=(screen_width // 2, screen_height - 80))
    screen.blit(instr_text_surf, instr_rect)

    return rects


# 3) DRAW_LABYRINTH ---------------------------------------------------------

def draw_labyrinth(surface, labyrinth, start, goal, final_path=None, cell_size=25):
    if labyrinth is None:
        surface.fill(LIGHT_GRAY) # Iscrtaj sivu pozadinu ako nema labirinta
        error_font = pygame.font.Font(None, 36) # Koristi default font za poruku
        error_text = error_font.render("Labirint nije generiran!", True, RED)
        text_rect = error_text.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
        surface.blit(error_text, text_rect)
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
    if start and goal: # Provjeri postoje li start i goal prije crtanja
        sx, sy = start
        gx, gy = goal
        _draw_cell(surface, sx, sy, GREEN, cell_size)
        _draw_cell(surface, gx, gy, RED, cell_size)


def _draw_cell(surface, x, y, color, cell_size):
    rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, DARK_GRAY, rect, 1) # Okvir ćelije


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
    y_offset += title_surf.get_height() + 10 # Dinamički razmak

    # Linija razdjelnika
    pygame.draw.line(screen, DARK_GRAY, (margin, y_offset), (panel_width - margin, y_offset), 2)
    y_offset += 15 # Razmak nakon linije

    stats_lines = [
        ("Status:", status_text),
        ("Posjećeni čvorovi:", str(nodes_visited)),
        ("Vrijeme:", f"{time_elapsed:.3f} s") # Format na 3 decimale
    ]
    for label, value in stats_lines:
        label_surf = font.render(label, True, BLACK)
        value_surf = font.render(value, True, BLACK)
        
        # Provjera da vrijednost ne prelazi širinu panela
        value_x_pos = margin + 180 # Podesi X poziciju za vrijednosti
        if value_x_pos + value_surf.get_width() > panel_width - margin:
            # Ako prelazi, smjesti vrijednost ispod labele ili prelomi (za sada samo ispod)
             screen.blit(label_surf, (margin, y_offset))
             y_offset += label_surf.get_height() + 2 # Mali razmak
             screen.blit(value_surf, (margin + 10, y_offset)) # Malo uvučeno
             y_offset += value_surf.get_height() + 8
        else:
            screen.blit(label_surf, (margin, y_offset))
            screen.blit(value_surf, (value_x_pos, y_offset))
            y_offset += max(label_surf.get_height(), value_surf.get_height()) + 8 # Dinamički razmak

    # Upute
    y_offset_instructions = panel_height - 70 # Malo više mjesta od dna za upute
     # Osiguraj da se upute ne preklapaju sa statistikama
    if y_offset > y_offset_instructions - font.get_linesize():
        y_offset_instructions = y_offset + 15

    instruction_text_live = "Pretraga u tijeku... Pritisnite [ESC] za izlaz."
    instr_rect_live = pygame.Rect(margin, y_offset_instructions, panel_width - (2 * margin), panel_height - y_offset_instructions - margin)
    draw_text_wrapped(screen, instruction_text_live, font, BLACK, instr_rect_live)


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
    y_offset += title_surf.get_height() + 10 # Dinamički razmak

    # Razdjelna linija
    pygame.draw.line(screen, DARK_GRAY, (margin, y_offset), (panel_width - margin, y_offset), 2)
    y_offset += 15 # Razmak

    # Odredi boju i tekst statusa
    st_upper = status.upper()
    info_text = status # Defaultni tekst
    color = BLACK    # Defaultna boja

    if "PRONAĐEN PUT" in st_upper:
        info_text = "Put pronađen!"
        color = GREEN
    elif "NEMA PUTA" in st_upper:
        info_text = "Nema puta!"
        color = RED
    elif "ISTEKLO VRIJEME" in st_upper:
        info_text = "Vremensko ograničenje isteklo!"
        color = ORANGE
    # Dodajmo i za grešku, ako se takav status koristi
    elif "GREŠKA" in st_upper or "ERROR" in st_upper:
        info_text = "Dogodila se greška!"
        color = (128, 0, 128) # Ljubičasta za grešku
    
    status_surf = font.render(info_text, True, color)
    status_rect = status_surf.get_rect(topleft=(margin, y_offset))
    screen.blit(status_surf, status_rect)
    y_offset += status_surf.get_height() + 15 # Veći razmak nakon statusa

    stats_lines = [
        ("Duljina puta:", str(path_length)),
        ("Posjećeni čvorovi:", str(nodes_visited)),
        ("Vrijeme izvršavanja:", f"{time_elapsed:.3f} s") # Format na 3 decimale
    ]
    for label, value in stats_lines:
        label_surf = font.render(label, True, BLACK)
        value_surf = font.render(value, True, BLACK)
        
        value_x_pos = margin + 220 # Podesi X poziciju, možda treba više mjesta
        if value_x_pos + value_surf.get_width() > panel_width - margin:
             screen.blit(label_surf, (margin, y_offset))
             y_offset += label_surf.get_height() + 2
             screen.blit(value_surf, (margin + 10, y_offset))
             y_offset += value_surf.get_height() + 8
        else:
            screen.blit(label_surf, (margin, y_offset))
            screen.blit(value_surf, (value_x_pos, y_offset))
            y_offset += max(label_surf.get_height(), value_surf.get_height()) + 8

    # Novi način ispisa uputa koristeći draw_text_wrapped
    y_offset_instructions = panel_height - 90 # Ostavimo više mjesta za duže upute
    if y_offset > y_offset_instructions - font.get_linesize() * 2: # Provjera preklapanja
        y_offset_instructions = y_offset + 20

    instruction_text = (
        "Pritisnite: [B]FS, [D]FS, [A]* za usporedbu na ovom labirintu. "
        "[C] za prikaz usporedbe. [R] za novi labirint. [ESC] za izlaz."
    )
    instr_rect = pygame.Rect(margin, y_offset_instructions, panel_width - (2 * margin), panel_height - y_offset_instructions - margin)
    draw_text_wrapped(screen, instruction_text, font, BLACK, instr_rect)


# 6) DRAW_SINGLE_MAZE_COMPARISON_PANEL (prethodno DRAW_COMPARISON_PANEL) -----

def draw_single_maze_comparison_panel(surface, font, comparison_stats, panel_width):
    """
    Crta panel za usporedbu rezultata algoritama na JEDNOM labirintu.
    comparison_stats: dict oblika {'algo_name': {'status': ..., 'path_length': ..., 'nodes': ..., 'time': ...}}
    """
    panel_height = surface.get_height()
    surface.fill(LIGHT_GRAY) 

    margin = 20
    y_offset = margin

    # Naslov panela
    title_text = "USPOREDBA NA TRENUTNOM LABIRINTU"
    title_surf = font.render(title_text, True, BLACK)
    title_rect = title_surf.get_rect(topleft=(margin, y_offset))
    surface.blit(title_surf, title_rect)
    y_offset += title_surf.get_height() + 10

    # Linija ispod naslova
    pygame.draw.line(surface, DARK_GRAY, (margin, y_offset), (panel_width - margin, y_offset), 2)
    y_offset += 15

    col_headers = ["Algoritam", "Status", "Put", "Čvorovi", "Vrijeme (s)"]
    available_width_for_cols = panel_width - (2 * margin)
    # Prilagođene širine da bolje odgovaraju sadržaju
    col_widths = [
        int(available_width_for_cols * 0.20), # Algoritam
        int(available_width_for_cols * 0.25), # Status
        int(available_width_for_cols * 0.15), # Put
        int(available_width_for_cols * 0.15), # Čvorovi
        int(available_width_for_cols * 0.25)  # Vrijeme
    ]
    
    # Manji font za zaglavlja tablice
    new_font_size = int(font.get_height() * 0.85) # Malo manji
    is_bold = font.get_bold()
    header_font = pygame.font.Font(None, new_font_size)
    if is_bold:
        header_font.set_bold(True)

    # Crtanje zaglavlja tablice
    current_x = margin
    for i, header in enumerate(col_headers):
        header_surf = header_font.render(header, True, BLACK)
        header_rect = header_surf.get_rect(topleft=(current_x + 3, y_offset)) # Mali padding
        surface.blit(header_surf, header_rect)
        current_x += col_widths[i]
    
    y_offset += header_font.get_linesize() + 6 # Razmak

    algorithms_to_display = ['bfs', 'dfs', 'astar']

    for algo_name in algorithms_to_display:
        current_x = margin
        if algo_name in comparison_stats:
            stats = comparison_stats[algo_name]
            display_values = [
                algo_name.upper(),
                str(stats.get('status', 'N/A')),
                str(stats.get('path_length', 'N/A')),
                str(stats.get('nodes', 'N/A')),
                f"{stats.get('time', 0.0):.3f}"
            ]
            
            max_row_height = 0
            for i, value_str in enumerate(display_values):
                value_surf = font.render(value_str, True, BLACK)
                # Osiguraj da tekst ne prelazi širinu stupca - za sada samo crtamo
                value_rect = value_surf.get_rect(topleft=(current_x + 3, y_offset))
                surface.blit(value_surf, value_rect)
                current_x += col_widths[i]
                if value_surf.get_height() > max_row_height:
                    max_row_height = value_surf.get_height()
            y_offset += max_row_height + 4 # Manji razmak između redova
        else:
            not_run_text = f"{algo_name.upper()}: (nije pokrenut)"
            not_run_surf = font.render(not_run_text, True, DARK_GRAY)
            surface.blit(not_run_surf, (margin + 3, y_offset))
            y_offset += font.get_linesize() + 4

    # Upute na dnu panela
    y_offset_instructions = panel_height - 70
    if y_offset > y_offset_instructions - font.get_linesize():
        y_offset_instructions = y_offset + 15
        
    footer_text = "[R] Novi labirint, [ESC] Izlaz, [<-] Nazad" # Dodan Backspace kao opcija
    footer_rect = pygame.Rect(margin, y_offset_instructions, panel_width - (2*margin), panel_height - y_offset_instructions - margin)
    draw_text_wrapped(surface, footer_text, font, BLACK, footer_rect)

# Stara funkcija draw_comparison_panel za usporedbu po težinama (može ostati ako je potrebna)
# Ako je ne trebate, možete je obrisati.
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
    legend_y = title_y + font.get_height() + 10 # Prilagođen y_offset za legendu
    legend_items = [("BFS", MEDIUM_BLUE), ("DFS", ORANGE), ("A*", RED)]
    current_legend_x = margin
    for name, color in legend_items:
        pygame.draw.rect(screen, color, (current_legend_x, legend_y, 20, 20))
        screen.blit(font.render(name, True, BLACK), (current_legend_x + 25, legend_y))
        current_legend_x += font.size(name)[0] + 45 # Prilagođen razmak

    chart_area_top = legend_y + font.get_height() + 20
    chart_width  = w - 2 * margin
    # Visina za svaki grafikon, s malim razmakom između njih
    chart_height = (h - chart_area_top - margin - 30) // 2 # 30 je za razmak i X-osi labele

    x_group_width = chart_width // 3
    x_centers = [margin + x_group_width * i + x_group_width // 2 for i in range(3)]
    
    bar_group_width_factor = 0.6 # Koliko širine grupe zauzimaju barovi
    bar_width = (x_group_width * bar_group_width_factor) / 3 # Širina pojedinačnog bara

    # --- Bar-chart za broj posjećenih čvorova ---
    all_nodes = []
    for alg_key in results: # Iteriraj kroz ključeve u results (bfs, dfs, astar)
        for diff_key in results[alg_key]: # Iteriraj kroz ključeve u težinama (easy, medium, hard)
            if isinstance(results[alg_key][diff_key], tuple) and len(results[alg_key][diff_key]) >= 1:
                all_nodes.append(results[alg_key][diff_key][0])
    max_nodes = max(all_nodes) if all_nodes else 1

    chart1_top = chart_area_top
    y_axis_bottom1 = chart1_top + chart_height

    title1 = font.render("Broj posjećenih čvorova", True, BLACK)
    t1_rect = title1.get_rect(center=(w // 2, chart1_top - font.get_height() // 2 - 5)) # Iznad grafa
    screen.blit(title1, t1_rect)
    
    difficulties = ["easy", "medium", "hard"]
    algorithms_data = {"bfs": MEDIUM_BLUE, "dfs": ORANGE, "astar": RED}

    for i, diff in enumerate(difficulties):
        x_group_start = x_centers[i] - (x_group_width * bar_group_width_factor) / 2
        for j, (alg_name, alg_color) in enumerate(algorithms_data.items()):
            if diff in results.get(alg_name, {}): # Provjeri postoji li rezultat za tu težinu
                val = results[alg_name][diff][0]
                
                bar_h_ratio = (val / max_nodes) if max_nodes > 0 else 0
                bar_h = int(bar_h_ratio * (chart_height - 20)) # 20px za tekst iznad
                
                bar_x = x_group_start + j * bar_width
                bar_y = y_axis_bottom1 - bar_h
                
                pygame.draw.rect(screen, alg_color, (bar_x, bar_y, bar_width, bar_h))
                
                # Tekst iznad bara
                txt_surf = font.render(str(val), True, BLACK)
                txt_rect = txt_surf.get_rect(center=(bar_x + bar_width / 2, bar_y - 10))
                screen.blit(txt_surf, txt_rect)
            
        # Oznaka težine ispod grupe barova
        diff_label_surf  = font.render(diff.capitalize(), True, BLACK)  
        diff_label_rect  = diff_label_surf.get_rect(center=(x_centers[i], y_axis_bottom1 + 15))
        screen.blit(diff_label_surf, diff_label_rect)

    # --- Bar-chart za vrijeme ---
    chart2_top = y_axis_bottom1 + 30 # Razmak između grafova
    y_axis_bottom2 = chart2_top + chart_height
    
    all_times = []
    for alg_key in results:
        for diff_key in results[alg_key]:
             if isinstance(results[alg_key][diff_key], tuple) and len(results[alg_key][diff_key]) >= 2:
                all_times.append(results[alg_key][diff_key][1])
    max_time = max(all_times) if all_times else 1.0
    if max_time == 0: max_time = 1.0 # Izbjegavanje dijeljenja s nulom

    title2 = font.render("Vrijeme izvršavanja (s)", True, BLACK)
    t2_rect = title2.get_rect(center=(w // 2, chart2_top - font.get_height() // 2 - 5))
    screen.blit(title2, t2_rect)

    for i, diff in enumerate(difficulties):
        x_group_start = x_centers[i] - (x_group_width * bar_group_width_factor) / 2
        for j, (alg_name, alg_color) in enumerate(algorithms_data.items()):
            if diff in results.get(alg_name, {}):
                time_val = results[alg_name][diff][1]

                bar_h_ratio = (time_val / max_time) if max_time > 0 else 0
                bar_h = int(bar_h_ratio * (chart_height - 20))

                bar_x = x_group_start + j * bar_width
                bar_y = y_axis_bottom2 - bar_h
                
                pygame.draw.rect(screen, alg_color, (bar_x, bar_y, bar_width, bar_h))
                
                txt_surf = font.render(f"{time_val:.2f}", True, BLACK)
                txt_rect = txt_surf.get_rect(center=(bar_x + bar_width / 2, bar_y - 10))
                screen.blit(txt_surf, txt_rect)

        diff_label_surf  = font.render(diff.capitalize(), True, BLACK)
        diff_label_rect  = diff_label_surf.get_rect(center=(x_centers[i], y_axis_bottom2 + 15))
        screen.blit(diff_label_surf, diff_label_rect)
    
    # Uputa za izlaz na dnu ekrana
    instr_content = "[R] Novi labirint   [ESC] Izlaz"
    instr_surf = font.render(instr_content, True, BLACK)
    instr_rect = instr_surf.get_rect(center=(w // 2, h - margin + 15)) # Malo pomaknuto dolje
    screen.blit(instr_surf, instr_rect)