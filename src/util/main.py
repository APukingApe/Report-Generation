import sys
from pathlib import Path

path = Path(__file__).resolve().parents[2]
sys.path.append(str(path))

from src.ui.gui import create_gui

report_list = []

if __name__ == "__main__":
    create_gui()