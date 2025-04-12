
# Dodaj root projekta u sys.path (pretpostavljamo da je generator.py u src/labyrinth)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from maze.generator import generate_labyrinth

