import sys
import os
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, path)
from PyQt6.QtWidgets import QApplication
from mirarecord.home import HomePage

from mirarecord.editor import Editor


def main():
    # Initialize the PyQt application
    app = QApplication(sys.argv)

    # Create the startup window instance
    home_page = HomePage()
    # home_page = Editor()

    # Show the startup window
    home_page.show()

    # Run the application event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    # Run the main function if this script is executed directly
    main()
