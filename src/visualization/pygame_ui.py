import pygame

def draw_difficulty_menu(screen, font, chosen_difficulty):
    lines = [
        "ODABERITE TEŽINU:",
        "[E] Easy",
        "[M] Medium",
        "[H] Hard",
        "Pritisnite ENTER za potvrdu."
    ]
    for i, line in enumerate(lines):
        surf = font.render(line, True, (0, 0, 0))
        screen.blit(surf, (50, 100 + i * 40))
    if chosen_difficulty:
        text = f"Odabrano: {chosen_difficulty.upper()}"
        green = font.render(text, True, (0, 128, 0))
        screen.blit(green, (50, 350))

def draw_algorithm_menu(screen, font, chosen_algorithm, chosen_difficulty):
    header = font.render(f"Težina: {chosen_difficulty.upper()}", True, (0, 0, 0))
    screen.blit(header, (50, 50))
    lines = [
        "ODABERITE ALGORITAM:",
        "[1] BFS",
        "[2] DFS",
        "[3] A*",
        "Pritisnite ENTER za potvrdu."
    ]
    for i, line in enumerate(lines):
        surf = font.render(line, True, (0, 0, 0))
        screen.blit(surf, (50, 150 + i * 40))
    if chosen_algorithm:
        text = f"Odabrano: {chosen_algorithm.upper()}"
        green = font.render(text, True, (0, 128, 0))
        screen.blit(green, (50, 350))

def draw_labyrinth(surface, labyrinth, start, goal, final_path=None, cell_size=25):
    """
    Crtanje labirinta na danu površinu (surface).
    """
    if labyrinth is None:
        return
    rows, cols = len(labyrinth), len(labyrinth[0])
    
    for y in range(rows):
        for x in range(cols):
            color = (0,0,0) if labyrinth[y][x]==1 else (220,220,220)
            _draw_cell(surface, x, y, color, cell_size)
    
    # start & goal
    sx, sy = start; gx, gy = goal
    _draw_cell(surface, sx, sy, (0,255,0), cell_size) # Zelena za start
    _draw_cell(surface, gx, gy, (255,0,0), cell_size) # Crvena za cilj
    
    # final path
    if final_path:
        # Prekriži crvenom bojom start i cilj ako su dio puta
        # Prvo nacrtaj cijeli put žuto
        for (px,py) in final_path:
            _draw_cell(surface, px, py, (255,255,0), cell_size) # Žuta za put
        # Zatim ponovno nacrtaj start i cilj kako bi bili vidljivi preko puta
        _draw_cell(surface, sx, sy, (0,255,0), cell_size)
        _draw_cell(surface, gx, gy, (255,0,0), cell_size)


def _draw_cell(surface, x, y, color, cell_size):
    """
    Pomoćna funkcija za crtanje jedne ćelije na danu površinu.
    """
    rect = (x * cell_size, y * cell_size, cell_size, cell_size)
    pygame.draw.rect(surface, color, rect)
    pygame.draw.rect(surface, (100,100,100), rect, 1) # Dodaj rub ćelije za bolju vidljivost

def draw_live_stats(screen, font, status_text, nodes_visited, time_elapsed, panel_width):
    """
    Prikazuje statistiku u stvarnom vremenu u bočnom panelu.
    """
    # Naslov
    title_surf = font.render("STATISTIKA PRETRAGE", True, (0, 0, 0))
    screen.blit(title_surf, (10, 10))

    # Linije statistike
    stats_lines = [
        f"Status: {status_text}",
        f"Posjećeni čvorovi: {nodes_visited}",
        f"Vrijeme: {time_elapsed:.4f} s"
    ]

    for i, line in enumerate(stats_lines):
        stat_surf = font.render(line, True, (0, 0, 0))
        screen.blit(stat_surf, (10, 50 + i * 30))

    # Upute
    instructions = [
        "", # Prazna linija za razmak
        "Pritisnite [ESC] za izlaz."
    ]
    for i, line in enumerate(instructions):
        instr_surf = font.render(line, True, (0, 0, 0))
        screen.blit(instr_surf, (10, screen.get_height() - len(instructions) * 30 + i * 30 - 20))


def draw_final_stats(screen, font, status, path_length, nodes_visited, time_elapsed, panel_width):
    """
    Prikazuje završnu statistiku nakon pretrage.
    """
    # Naslov
    title_surf = font.render("REZULTATI PRETRAGE", True, (0, 0, 0))
    screen.blit(title_surf, (10, 10))

    if status == "Pronađen put":
        info_text = "Put pronađen!"
        color = (0, 128, 0)
    elif status == "Nema puta":
        info_text = "Nema puta!"
        color = (255, 0, 0)
    elif status == "Isteklo vrijeme":
        info_text = "Vremensko ograničenje isteklo!"
        color = (255, 165, 0)
    else:
        info_text = status # Za ostale nepoznate statuse
        color = (0, 0, 0)

    # Ispisivanje statusa
    status_surf = font.render(info_text, True, color)
    screen.blit(status_surf, (10, 50))

    # Ispisivanje statistike
    stats_lines = [
        f"Duljina puta: {path_length}",
        f"Posjećeni čvorovi: {nodes_visited}",
        f"Vrijeme izvršavanja: {time_elapsed:.4f} s",
        "",
        "Pritisnite [R] za novi labirint (odaberite težinu),", # Ažurirana poruka
        "Pritisnite [ESC] za izlaz."
    ]

    for i, line in enumerate(stats_lines):
        stat_surf = font.render(line, True, (0, 0, 0))
        screen.blit(stat_surf, (10, 100 + i * 30))