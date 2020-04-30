import sys
# PyQT imports
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QRadioButton
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget

__version__ = '0.1'
__author__ = 'James Hinton'

# Set up the main window for CryptoTrading GUI
class CTUI(QMainWindow):
    # GUI initialisation
    def __init__(self):
        # View initialisation
        super().__init__()
        # Set the main windows properties
        self.setWindowTitle('CryptoTradingPlatform')
        self.setFixedSize(900, 600)
        # Set the general layout
        self.generalLayout = QVBoxLayout()
        # Set the central widget
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        # Create the display and the buttons
        self._createDisplay()
        self._createButtons()

    # Create display method
    def _createDisplay(self):
        # Create the display widget
        self.display = QLineEdit()
        # Set some of the properties
        self.display.setFixedHeight(35)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        # Add the display to the general layout
        self.generalLayout.addWidget(self.display)

    # Create the buttons and put into display
    def _createButtons(self):
        # Create a dictionary to put button list into
        self.buttons = {}
        buttonsLayout = QGridLayout()
        # Create buttons and position dictionary
        buttons = {
            'AlgorithmOne': (0, 0),
            'SelfAnalysis': (0, 1),
            'DataGathering': (0, 2),
            'DBSize': (0, 3),
            'RunningOutput': (1, 0),
            'NumCores': (1, 1),
            'CurrentProcesses': (1, 2),
            'MemUsage': (1, 3)
        }
        # Now add them to the grid layout
        for btnText, pos in buttons.items():
            self.buttons[btnText] = QPushButton(btnText)
            self.buttons[btnText].setFixedSize(100, 50)
            buttonsLayout.addWidget(self.buttons[btnText], pos[0], pos[1])
            # Now add to the general layout
            self.generalLayout.addLayout(buttonsLayout)

# Client code
def main():
    # Create an instance of the Qapplication
    cryptoUI = QApplication(sys.argv)
    # Display UI
    view = CTUI()
    view.show()
    # Start the main loop
    sys.exit(cryptoUI.exec())

if __name__ == '__main__':
    main()
