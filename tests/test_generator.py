import unittest
import sys
import os
from collections import deque

# Dodaj root projekta u sys.path (pretpostavljamo da je generator.py u src/maze)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from maze.generator import generate_labyrinth

class TestLabyrinthGenerator(unittest.TestCase):
    def test_labyrinth_dimensions(self):
        """ Testira da labirint ima očekivane dimenzije za sve težine. """
        sizes = {'easy': 10, 'medium': 20, 'hard': 30}
        for difficulty, expected_size in sizes.items():
            with self.subTest(difficulty=difficulty):
                labyrinth, _, _ = generate_labyrinth(difficulty)
                self.assertEqual(len(labyrinth), expected_size,
                                 f"Labirint za {difficulty} treba imati {expected_size} redova.")
                for row in labyrinth:
                    self.assertEqual(len(row), expected_size,
                                     f"Svi redovi labirinta za {difficulty} trebaju imati {expected_size} ćelija.")
                    
    def test_walls_and_paths(self):
        """ Testira da labirint sadrži samo vrijednosti 0 i 1. """
        labyrinth, _, _ = generate_labyrinth('medium')
        for row in labyrinth:
            for cell in row:
                self.assertIn(cell, (0, 1), "Labirint sadrži nevažeću vrijednost (nije 0 ili 1).")
                
    def test_labyrinth_path_exists(self):
        """ Provjerava postoji li put od starta do kraja u labirintu. """
        labyrinth, start, end = generate_labyrinth('medium')
        self.assertIsNotNone(labyrinth, "Labirint nije generiran.")
        self.assertTrue(self.check_path(labyrinth, start, end),
                        "Nema valjanog puta od starta do kraja u labirintu.")
    
    def check_path(self, labyrinth, start, end):
        """ Pomoćna funkcija koja koristi BFS za provjeru postoji li put između starta i kraja. """
        queue = deque([start])
        visited = {start}  # dodajemo start odmah u visited
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        while queue:
            x, y = queue.popleft()
            if (x, y) == end:
                return True
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(labyrinth[0]) and 0 <= ny < len(labyrinth):
                    if labyrinth[ny][nx] == 0 and (nx, ny) not in visited:
                        queue.append((nx, ny))
                        visited.add((nx, ny))
        return False
    
    def test_invalid_difficulty(self):
        """Provjera da je nevažeća težina prema zadanoj postavci "lako"."""
        labyrinth, _, _ = generate_labyrinth('invalid_difficulty')
        self.assertEqual(len(labyrinth), 10, "Nevažeća težina trebala bi biti postavljena na 'lako' (10x10)")
        
    # def test_start_and_end_positions(self):
    #     """Provjera jesu li početna i krajnja pozicija važeće staze (vrijednost 0)."""
    #     labyrinth, start, end = generate_labyrinth('medium')
    #     start_x, start_y = start
    #     end_x, end_y = end
        
    #     self.assertEqual(labyrinth[start_y][start_x], 0, "Početna pozicija nije put")
    #     self.assertEqual(labyrinth[end_y][end_x], 0, "Krajnja pozicija nije put")
        
    #     # Check that start is on left side and end is on right side
    #     self.assertTrue(start_x < len(labyrinth[0]) / 2, "Početak bi trebao biti s lijeve strane")
    #     self.assertTrue(end_x > len(labyrinth[0]) / 2, "Kraj bi trebao biti na desnoj strani")
    
    def test_start_to_end_path_exists(self):
        """Provjera postoji li put od početka do kraja."""
        labyrinth, start, end = generate_labyrinth('medium')
    
        # Just check that start and end are connected
        path_exists = self.check_path(labyrinth, start, end)
    
        self.assertTrue(path_exists, "Nema puta od početka do kraja")
        
        
    # TODO: koristi ovaj test
    # def test_all_paths_connected(self):
    #     """Provjera mogu li se sve ćelije staze dosegnuti od početka."""
    #     labyrinth, start, _ = generate_labyrinth('medium')
        
    #     # Count all path cells (0s)
    #     total_paths = sum(row.count(0) for row in labyrinth)
        
    #     # Count reachable cells using BFS
    #     reachable = self.count_reachable_cells(labyrinth, start)
        
    #     self.assertEqual(reachable, total_paths, "Nisu sve ćelije staze povezane")
    
    def count_reachable_cells(self, labyrinth, start):
        """Broji sve ćelije dostupne od početka pomoću BFS-a."""
        queue = deque([start])
        visited = {start}
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        while queue:
            x, y = queue.popleft()
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (0 <= nx < len(labyrinth[0]) and 0 <= ny < len(labyrinth) and 
                    labyrinth[ny][nx] == 0 and (nx, ny) not in visited):
                    queue.append((nx, ny))
                    visited.add((nx, ny))
        
        return len(visited)
    
    def test_print_labyrinth(self):
        """ Ispisuje labirint radi vizualne provjere. """
        labyrinth, start, end = generate_labyrinth('easy')
        print("\nIscrtani labirint:")
        for y, row in enumerate(labyrinth):
            line = ''
            for x, cell in enumerate(row):
                if (x, y) == start:
                    line += 'S '
                elif (x, y) == end:
                    line += 'E '
                else:
                    line += '█ ' if cell == 1 else '. '
            print(line)
        # Ovaj test nema stvarni assert, služi samo za vizualnu provjeru
        self.assertTrue(True)
                    
if __name__ == '__main__':
    unittest.main()