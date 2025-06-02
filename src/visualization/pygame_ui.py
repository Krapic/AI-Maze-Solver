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
    # Crta tekst s prelamanjem unutar zadanog pravokutnika
    y = rect.top
    line_spacing = font.get_linesize() # Preporučeni razmak linija za font

    words = text.split(' ')
    lines = []
    current_line = ""

    for word in words:
        # Provjera stane li riječ + razmak na trenutnu liniju
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= rect.width:
            current_line = test_line
        else:
            # Ako ne stane, završi trenutnu liniju
            lines.append(current_line.rstrip())
            current_line = word + " " # Početak nove linije s tom riječi
    lines.append(current_line.rstrip()) # Dodavanje zadnje linije

    for line in lines:
        if not line: # Preskakanje prazne linije ako nastanu
            continue
        # Ako bi sljedeća linija prešla donji rub pravokutnika, a nije prva linija
        if y + line_spacing > rect.bottom and lines.index(line) > 0 :
            available_width = rect.width
            shortened_line = ""
            for char_idx in range(len(line)):
                if font.size(shortened_line + line[char_idx] + "...")[0] > available_width:
                    break
                shortened_line += line[char_idx]
            
            line_surf = font.render(shortened_line + "...", aa, color, bkg)
            surface.blit(line_surf, (rect.left, y))
            break # Prekidamo crtanje daljnjih linija

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
    # Iscrtava vertikalni gradient od top_color do bottom_color na cijeloj površini.
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
        
        value_x_pos = margin + 250
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
    y_offset_instructions = panel_height - 180 # Ostavimo više mjesta za duže upute
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

    title_text = "USPOREDBA NA TRENUTNOM LABIRINTU"
    title_surf = font.render(title_text, True, BLACK)
    title_rect = title_surf.get_rect(topleft=(margin, y_offset))
    surface.blit(title_surf, title_rect)
    y_offset += title_surf.get_height() + 10

    pygame.draw.line(surface, DARK_GRAY, (margin, y_offset), (panel_width - margin, y_offset), 2)
    y_offset += 15

    col_headers = ["Algoritam", "Status", "Put", "Čvorovi", "Vrijeme (s)"]
    available_width_for_cols = panel_width - (2 * margin)
    
    # Širine stupaca
    col_widths = [
        int(available_width_for_cols * 0.25), # Algoritam
        int(available_width_for_cols * 0.35), # Status - dajmo mu više mjesta
        int(available_width_for_cols * 0.15), # Put
        int(available_width_for_cols * 0.25), # Čvorovi
        int(available_width_for_cols * 0.25)  # Vrijeme
    ]
    # Osiguravanje da suma širina ne prelazi dostupnu širinu (opcionalno, ali korisno)
    total_col_width = sum(col_widths)
    if total_col_width > available_width_for_cols:
    # Skaliranje širine
        scale_factor = available_width_for_cols / total_col_width
        col_widths = [int(w * scale_factor) for w in col_widths]


    new_font_size = int(font.get_height() * 0.85)
    is_bold = font.get_bold()
    header_font = pygame.font.Font(None, new_font_size)
    if is_bold:
        header_font.set_bold(True)

    current_x_header = margin
    for i, header in enumerate(col_headers):
        header_surf = header_font.render(header, True, BLACK)
        # Za zaglavlja, lijevo poravnanje s malim paddingom
        header_text_pos_x = current_x_header + 5 # 5px padding s lijeve strane
        surface.blit(header_surf, (header_text_pos_x, y_offset))
        current_x_header += col_widths[i]
    
    y_offset += header_font.get_linesize() + 8

    algorithms_to_display = ['bfs', 'dfs', 'astar']
    cell_padding_x = 5 # Padding unutar svake ćelije za podatke

    for algo_name in algorithms_to_display:
        current_x_data = margin # Resetiranje x pozicije za svaki red podataka
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
                
                # Pozicija teksta unutar ćelije (s paddingom)
                text_pos_x = current_x_data + cell_padding_x

                surface.blit(value_surf, (text_pos_x, y_offset))
                current_x_data += col_widths[i] # Pomicanje na početak sljedećeg stupca
                
                if value_surf.get_height() > max_row_height:
                    max_row_height = value_surf.get_height()
            y_offset += max_row_height + 6 # Malo veći razmak između redova
        else:
            not_run_text = f"{algo_name.upper()}: (nije pokrenut)"
            not_run_surf = font.render(not_run_text, True, DARK_GRAY)
            surface.blit(not_run_surf, (current_x_data + cell_padding_x, y_offset))
            y_offset += font.get_linesize() + 6

    y_offset_instructions = panel_height - 70
    if y_offset > y_offset_instructions - font.get_linesize():
        y_offset_instructions = y_offset + 15
        
    footer_text = "[R] Novi labirint, [ESC] Izlaz, [<-] Nazad"
    footer_rect = pygame.Rect(margin, y_offset_instructions, panel_width - (2*margin), panel_height - y_offset_instructions - margin)
    draw_text_wrapped(surface, footer_text, font, BLACK, footer_rect)