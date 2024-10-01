import sys
import os
sys.path.append(os.path.abspath('../../'))

from src.ui.gui import create_gui

report_list = []

if __name__ == "__main__":
    create_gui()
