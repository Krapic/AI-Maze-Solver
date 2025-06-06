import unittest
from collections import deque
import sys
import os

#dodaje root projekta u sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from algorithms.dfs import dfs_search_generator

class TestDFSGenerator(unittest.TestCase):

    def test_dfs_found(self):
        #jednostavan, otvoren labirint
        labyrinth = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        start = (0, 0)
        goal = (2, 2)

        #generator algoritma
        gen = dfs_search_generator(labyrinth, start, goal, time_limit=5.0)

        final_status = None
        final_path = None

        #prolazak kroz svaki yield iz algoritma
        #ako je status found, spremamo put
        for state in gen:
            status = state[0]
            if status in ("found", "no_path", "timeout"):
                final_status = status
                if status == "found":
                    final_path = state[1]

        #provjera je li rezultat found i postoji li put
        self.assertEqual(final_status, "found", "DFS treba pronaći put.")
        self.assertIsNotNone(final_path, "Put ne smije biti None.")
        self.assertEqual(final_path[0], start)
        self.assertEqual(final_path[-1], goal)

    #Test u blokiranom labirintu
    def test_dfs_no_path(self):
        labyrinth = [
            [0, 1],
            [1, 1]
        ]
        start = (0, 0)
        goal = (1, 1)

        #generator algoritma 
        gen = dfs_search_generator(labyrinth, start, goal, time_limit=5.0)

        final_status = None

        #prolazak kroz svaki yield iz algoritma
        for state in gen:
            status = state[0]
            if status in ("found", "no_path", "timeout"):
                final_status = status
    
        #ocekujemo da javi da nema puta
        self.assertEqual(final_status, "no_path", "DFS treba yieldati 'no_path' kada nema puta.")


    #Test gdje je time_limit vrlo malen
    def test_dfs_timeout(self):
        labyrinth = [[0 for _ in range(50)] for _ in range(50)]
        start = (0, 0)
        goal = (49, 49)

        #generator s jako malenim time_limitom
        gen = dfs_search_generator(labyrinth, start, goal, time_limit=0.0001)
        
        final_status = None

        #prolazak kroz svaki yield iz algoritma
        for state in gen:
            status = state[0]
            if status in ("found", "no_path", "timeout"):
                final_status = status
        
        #ocekujemo timeout
        self.assertEqual(final_status, "timeout", "DFS treba yieldati 'timeout' zbog premalog limita.")

if __name__ == '__main__':
    unittest.main()
