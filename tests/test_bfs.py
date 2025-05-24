import unittest
import sys
import os

# Dodaj root projekta u sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from algorithms.bfs import bfs_search_generator

class TestBFSGenerator(unittest.TestCase):
    pass  # Prazna testna klasa

if __name__ == '__main__':
    unittest.main()