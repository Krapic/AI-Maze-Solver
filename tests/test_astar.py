import unittest
import time

from src.labyrinth.generator import generate_labyrinth
from src.algorithms.astar import astar_search_generator


class TestAStarAlgorithm(unittest.TestCase):
    """ Testovi za A* algoritam. """

    def test_astar_easy_maze(self):
        """
        Test: A* treba uspješno pronaći put u 'easy' labirintu.
        """
        labyrinth, start, goal = generate_labyrinth(difficulty='easy')

        # Provjera da nije None
        self.assertIsNotNone(labyrinth, "Generator nije vratio labirint (easy).")

        # Dajemo dovoljno vremena (3 sekunde), očekujemo 'found' umjesto 'timeout'
        time_limit = 3.0
        generator = astar_search_generator(labyrinth, start, goal, time_limit)

        final_status = None
        found_path = None

        for step in generator:
            status = step[0]
            if status in ["found", "timeout", "no_path"]:
                final_status = status
                if status == "found":
                    found_path = step[1]
                break

        # Očekujemo da A* PRONAĐE put
        self.assertEqual(final_status, "found", f"Očekivan 'found', ali dobiveno '{final_status}'.")
        self.assertIsNotNone(found_path, "Put je trebao biti pronađen, ali je None.")
        self.assertGreater(len(found_path), 1, "Pronađeni put trebao bi imati više od 1 čvora.")

    def test_astar_no_path(self):
        """
        Test: Ako nema puta, A* treba vratiti 'no_path'.
        Ovdje ručno kreiramo mali 'neprohodni' 3x3 labirint.
        """
        # "labyrinth" je 3x3,
        # Drugi redak [1,1,1] znači neprohodne zidove
        labyrinth = [
            [0, 0, 0],
            [1, 1, 1],
            [0, 0, 0]
        ]
        start = (0, 0)
        goal = (2, 2)

        time_limit = 2.0
        generator = astar_search_generator(labyrinth, start, goal, time_limit)

        final_status = None
        for step in generator:
            status = step[0]
            if status in ["found", "timeout", "no_path"]:
                final_status = status
                break

        self.assertEqual(final_status, "no_path", f"Očekivan 'no_path', dobiveno '{final_status}'.")

    def test_astar_timeout(self):
        width = 300
        height = 300
        labyrinth = [[0 for _ in range(width)] for _ in range(height)]
        start = (0, 0)
        goal = (width-1, height-1)

        time_limit = 0.001
        generator = astar_search_generator(labyrinth, start, goal, time_limit)

        final_status = None
        for step in generator:
            status = step[0]
            if status in ["found", "timeout", "no_path"]:
                final_status = status
                break

        self.assertEqual(final_status, "timeout", f"Očekivan 'timeout', ali dobiveno '{final_status}'.")



# Omogućuje pokretanje testova direktno npr.:
#   python -m unittest tests/test_astar.py
if __name__ == "__main__":
    unittest.main()
