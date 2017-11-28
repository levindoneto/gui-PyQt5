# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QWidget # Basic widgets
from PyQt5.QtGui import QIcon 

class Gui(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI() # Start gui
        
        
    def initUI(self):
        self.setGeometry(100, 100, 1024, 768) # Position(x,y), Size(x,y)
        self.setWindowTitle('Time Tagger | Web Application') # Get the icon
        self.setWindowIcon(QIcon('icon.ico'))        
        self.show() # Show the window to the user
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Gui()
    sys.exit(app.exec_())