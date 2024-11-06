import sys
from pathlib import Path

# Dynamically find the `Coordinate-Force-Language-Robotics/src/` directory relative to this file's location
src_path = Path(__file__).resolve().parent

# Add `Coordinate-Force-Language-Robotics/src/` to the Python path if not already included
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

def main():
    pass

if __name__ == '__main__':
    main()