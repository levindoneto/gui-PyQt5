# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication) # Basic widgets
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPainter, QColor, QPen # For the background
from PyQt5.QtCore import Qt
import ctypes

class Gui(QWidget):
    ''' In order to have the icon on the taskbar '''
    myappid = u'mycompany.myproduct.subproduct.version'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    INPUT_FONT = {"Type": "Arial", "Size": "20", "Style": "bold"}
    LABEL_FONT = {"Type": "Arial", "Size": "20", "Style": "bold italic"}
    TOOL_TIP = {"Type": "Arial", "Size": "8", "Style": "normal"}
    def __init__(self):
        super().__init__()
        self.initUI() # Start gui

    def initUI(self):
        QToolTip.setFont(QFont(self.TOOL_TIP["Type"], int(self.TOOL_TIP["Size"])))
        self.setGeometry(100, 100, 1024, 768) # Position(x,y), Size(x,y)

        ''' Set window background color '''
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.blue)
        self.setPalette(p) # Set color to the background

        # Button for starting the server with a ballon help
        startServer = QPushButton('Start server', self)
        startServer.setToolTip('Click it to start the server in the localhost') # ToDo: Change the size
        startServer.resize(startServer.sizeHint())
        startServer.move(50, 50)

        # Button for stopping the server with a ballon help
        stopServer = QPushButton('Stop server', self)
        stopServer.setToolTip('Click it to stop the server') # ToDo: Change the size
        stopServer.resize(stopServer.sizeHint())
        stopServer.move(200, 50)

        # Button for opening the client with a ballon help
        stopServer = QPushButton('Open client', self)
        stopServer.setToolTip('Click it to stop the server') # ToDo: Change the size
        stopServer.resize(stopServer.sizeHint())
        stopServer.move(350, 50)

        # Button for refreshing the server with a ballon help
        refresh = QPushButton('Refresh', self)
        refresh.setToolTip('Click it to refresh this page') # ToDo: Change the size
        refresh.resize(refresh.sizeHint())
        refresh.move(500, 50)

        self.setWindowTitle('Time Tagger | Web Application')
        self.setWindowIcon(QIcon('icon.ico'))
        self.show() # Show the window to the user


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Gui()
    sys.exit(app.exec_())
