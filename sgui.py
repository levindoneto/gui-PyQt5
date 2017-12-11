

import random
import sys
from PyQt5.QtCore import QByteArray, QDataStream, QIODevice
from PyQt5.QtWidgets import (QApplication, QDialog, QLabel, QHBoxLayout, QMessageBox, QPushButton, QVBoxLayout)
from PyQt5.QtNetwork import QLocalServer
import ctypes
from PyQt5.QtWidgets import (QWidget, QToolTip, QPushButton, QApplication) # Basic widgets
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPainter, QColor, QPen # For the background
from PyQt5.QtCore import Qt


class Server(QDialog):
    ''' Fonts '''
    INPUT_FONT = {"Type": "Arial", "Size": "20", "Style": "bold"}
    LABEL_FONT = {"Type": "Arial", "Size": "20", "Style": "bold italic"}
    TOOL_TIP = {"Type": "Arial", "Size": "8", "Style": "normal"}

    ''' In order to have the icon on the taskbar '''
    myappid = u'mycompany.myproduct.subproduct.version'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    def __init__(self, parent=None):
        PORT = 8888 # ToDo: Get from the current app
        super(Server, self).__init__(parent) # Init the gui server

        # Button for starting the server with a ballon help
        self.setWindowIcon(QIcon('icon.ico'))
        self.setGeometry(100, 100, 580, 300) # Position(x,y), Size(x,y)

        statusLabel = QLabel()
        statusLabel.setWordWrap(True)
        portLabel = QLabel()
        portLabel.setWordWrap(True)
        spaceLabel = QLabel()
        spaceLabel.setWordWrap(True)
        openClientButton = QPushButton("Open Client")
        openClientButton.setAutoDefault(False)
        quitButton = QPushButton("Close")
        quitButton.setAutoDefault(False)

        self.server = QLocalServer()
        if not self.server.listen('data'):
            QMessageBox.critical(self, "Time Tagger Server",
                    "Unable to start the server: %s." % self.server.errorString())
            self.close()
            return

        statusLabel.setText("The server has started running.\n " "It is running at the port ")
        statusLabel.setAlignment(Qt.AlignCenter)
        portLabel.setText(str(PORT))
        portLabel.setAlignment(Qt.AlignCenter)
        spaceLabel.setText("\n\n")
        spaceLabel.setAlignment(Qt.AlignCenter)
        openClientButton.clicked.connect(self.openClient)
        quitButton.clicked.connect(self.close)
        self.server.newConnection.connect(self.startServer)

        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(openClientButton)
        buttonLayout.addWidget(quitButton)
        buttonLayout.addStretch(1)

        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0, 50, 0, 50)
        mainLayout.addWidget(statusLabel)
        mainLayout.addWidget(portLabel)
        mainLayout.addWidget(spaceLabel)
        mainLayout.addLayout(buttonLayout) # Button for closing the server
        self.setLayout(mainLayout)

        self.setWindowTitle("Time Tagger | Web Application")

    def startServer(self):
        block = QByteArray()
        out = QDataStream(block, QIODevice.WriteOnly)
        out.setVersion(QDataStream.Qt_4_0)
        out.writeUInt16(0)
        out.device().seek(0)
        out.writeUInt16(block.size() - 2)

        clientConnection = self.server.nextPendingConnection()
        clientConnection.disconnected.connect(clientConnection.deleteLater)
        clientConnection.write(block)
        clientConnection.flush()
        clientConnection.disconnectFromServer()

    def openClient(self):
        print("Open Client")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    server = Server()
    server.show()
    sys.exit(app.exec_())
