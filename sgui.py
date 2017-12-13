"""This module implements an entry point for the user to the
server functionality.
"""
import logging
import sys
import threading

from . import server
from . import config
from . import getVersion

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QByteArray, QDataStream, QIODevice
from PyQt5.QtWidgets import (QApplication, QDialog, QLabel, QHBoxLayout, QMessageBox, QPushButton, QVBoxLayout)
from PyQt5.QtNetwork import QLocalServer
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication) # Basic widgets
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPainter, QColor, QPen # For the background
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QDesktopWidget # To centralize the window
import ctypes

import tkinter
import tkinter.messagebox
import webbrowser

''' Fonts '''
TEXT_FONT = {"Type": "Arial", "Size": "10", "Style": "bold"}
BUTTON_FONT = {"Type": "Arial", "Size": "10", "Style": "bold italic"}
TOOL_TIP = {"Type": "Arial", "Size": "5", "Style": "normal"}

''' Fonts' settings '''
fontText = QtGui.QFont(TEXT_FONT["Type"], int(TEXT_FONT["Size"]), QtGui.QFont.Bold)
fontButton = QtGui.QFont(BUTTON_FONT["Type"], int(BUTTON_FONT["Size"]), QtGui.QFont.Bold)
QToolTip.setFont(QFont(TOOL_TIP["Type"], int(TOOL_TIP["Size"]))) # It user with the hover event

''' Window' settings '''
HEIGHT = 580
WIDTH = 300

PORT = 8888

class Server(QDialog):
    def closeEvent(self, event): # Trigger the dialog's close button
        self.closeServer(self)

    ''' In order to have the icon on the taskbar '''
    myappid = u'mycompany.myproduct.subproduct.version'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    def __init__(self, parent=None):

        PORT = 8888 # ToDo: Get from the current app
        super(Server, self).__init__(parent) # Init the gui server

        ''' Centralize the window and fix a size for it '''
        centerPosition = str(QDesktopWidget().availableGeometry().center()).split("PyQt5.QtCore.QPoint")[-1].split(",")
        centerWidth = int(centerPosition[0].strip('('))
        centerHeight = int(centerPosition[1].strip(')'))
        self.setFixedSize(HEIGHT, WIDTH) # Forbid  resize of the window
        self.setGeometry(centerWidth-HEIGHT/2, centerHeight-WIDTH/2, HEIGHT, WIDTH) # Position(x,y), Size(x,y) -> In the center

        ''' Create Labels: status, port, buttons for opening the client and closing the server '''
        statusLabel = QLabel()
        statusLabel.setWordWrap(True)
        portLabel = QLabel()
        portLabel.setWordWrap(True)
        spaceLabel = QLabel()
        spaceLabel.setWordWrap(True)
        openClientButton = QPushButton("Open Client")
        openClientButton.setAutoDefault(False)
        openClientButton.setFont(fontButton)
        openClientButton.setToolTip('It opens the client in the default browser')
        quitButton = QPushButton("Close")
        quitButton.setAutoDefault(False)
        quitButton.setFont(fontButton)
        quitButton.setToolTip('It closes the server')

        ''' Define texts for the text labels '''
        statusLabel.setText("The server has started running.\n " "It is running at the port ")
        statusLabel.setAlignment(Qt.AlignCenter)
        statusLabel.setFont(fontText)
        portLabel.setText(str(PORT))
        portLabel.setAlignment(Qt.AlignCenter)
        portLabel.setFont(fontText)
        spaceLabel.setText("\n\n")
        spaceLabel.setAlignment(Qt.AlignCenter)

        ''' Define actions for the buttons '''
        openClientButton.clicked.connect(self.openClient)
        quitButton.clicked.connect(self.closeServer)

        ''' Define layout for the buttons '''
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(openClientButton)
        buttonLayout.addWidget(quitButton)
        buttonLayout.addStretch(1)

        ''' Define the main layout with the texts and main button '''
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0, 50, 0, 50)
        mainLayout.addWidget(statusLabel)
        mainLayout.addWidget(portLabel)
        mainLayout.addWidget(spaceLabel)
        mainLayout.addLayout(buttonLayout) # Button for closing the server
        self.setLayout(mainLayout)
        self.setWindowTitle("Time Tagger | Web Application")
        self.setWindowIcon(QIcon('icon.ico'))
        self.setWindowFlags(self.windowFlags() # Just the minimize button is available
            | QtCore.Qt.WindowMinimizeButtonHint
            | QtCore.Qt.WindowSystemMenuHint)

    def getUserPort(self):
        return PORT


    def getServerPath(self):
        print("Retrieving server path")
        hostname = server.getHostname()
        port = str(self.getUserPort())
        path = "http://"+hostname+":"+port
        return path

    def serverIsRunning(self):
        print("Retrieving if sever is running")
        port = "8888" #self.getUserPort()
        return server.isRunning(port)

    def startServer(self):
        print("Toggling server")

        port = "8888" # ToDo: Get from getPort
        if self.serverIsRunning():
            print("Stopping server")
            server.stop(port)
        else:
            print("Starting server")
            self.server_thread = threading.Thread(
                target=server.start,
                args=[port, False]
            )
            self.server_thread.start()
        #self.updateStatus()


    def openClient(self):
        path = self.getServerPath()
        print("Opening server to %s" % path)
        webbrowser.open(path)

    def closeServer(self, event):
        print("Closing server")
        self.close() # Close the window

def run():
    app = QApplication(sys.argv)
    server = Server() # Start the app
    server.startServer()
    server.show() # Show the app's window
    sys.exit(app.exec_()) # Close the window if the user clicks <close> or by the dialog's close event
