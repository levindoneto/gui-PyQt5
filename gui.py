import sys
from PyQt5.QtWidgets import QApplication, QWidget # Basic widgets

app = QApplication(sys.argv) # The app ought to create an object

w = QWidget() # It is the base class for all the UI objects
w.resize(1024, 768)
w.move(300, 300)
w.setWindowTitle('Time Tagger | Web Application')
w.show()
  
sys.exit(app.exec_()) # Main loop used for keeping the window open until the user closes it