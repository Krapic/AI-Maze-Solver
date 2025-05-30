import unittest
from collections import deque
import sys
import os

# Dodaj root projekta u sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from algorithms.bfs import bfs_search_generator

class TestBFSGenerator(unittest.TestCase):

    def test_bfs_found(self):
        """Test BFS generator da pronađe put u jednostavnom labirintu."""
        labyrinth = [
            [0, 0],
            [0, 0]
        ]
        start = (0, 0)
        goal = (1, 1)

        gen = bfs_search_generator(labyrinth, start, goal, time_limit=5.0)

        final_status = None
        final_path = None

        for state in gen:
            status = state[0]
            if status in ("found", "no_path", "timeout"):
                final_status = status
                if status == "found":
                    final_path = state[1]

        self.assertEqual(final_status, "found", "BFS je trebao pronaći put.")
        self.assertIsNotNone(final_path, "Finalni put ne smije biti None.")
        self.assertEqual(final_path[0], start, "Put treba početi na startu.")
        self.assertEqual(final_path[-1], goal, "Put treba završiti na goalu.")

    def test_bfs_no_path(self):
        """Test BFS generatora u labirintu gdje nema puta."""
        labyrinth = [
            [0, 1],
            [1, 1]
        ]
        start = (0, 0)
        goal = (1, 1)

        gen = bfs_search_generator(labyrinth, start, goal, time_limit=5.0)

        final_status = None
        for state in gen:
            status = state[0]
            if status in ("found", "no_path", "timeout"):
                final_status = status
        
        self.assertEqual(final_status, "no_path", "BFS treba yieldati 'no_path' kada put ne postoji.")

    def test_bfs_timeout(self):
        """Test BFS generatora s vrlo malim time_limit da provjerimo prekid zbog vremena."""
        # Labirint 50x50 = 2500 polja, BFS treba neko vrijeme.
        labyrinth = [[0 for _ in range(50)] for _ in range(50)]
        start = (0, 0)
        goal = (49, 49)

        gen = bfs_search_generator(labyrinth, start, goal, time_limit=0.0001)

        final_status = None
        for state in gen:
            status = state[0]
            if status in ("found", "no_path", "timeout"):
                final_status = status
        
        self.assertEqual(final_status, "timeout", "BFS treba yieldati 'timeout' zbog premalog time_limit-a.")

if __name__ == '__main__':
    unittest.main()
