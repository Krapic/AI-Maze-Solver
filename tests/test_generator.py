import unittest

# Dodaj root projekta u sys.path (pretpostavljamo da je generator.py u src/labyrinth)
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
                    
if __name__ == '__main__':
    unittest.main()