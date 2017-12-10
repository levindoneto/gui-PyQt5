

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
    def __init__(self, parent=None):
        PORT = 8888 # ToDo: Get from the current app
        super(Server, self).__init__(parent) # Init the gui server
        myappid = u'mycompany.myproduct.subproduct.version' # In order to have the icon also in the task bar
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        # Button for starting the server with a ballon help
        self.setWindowIcon(QIcon('icon.ico'))
        self.setGeometry(100, 100, 580, 300) # Position(x,y), Size(x,y)

        statusLabel = QLabel()
        statusLabel.setWordWrap(True)
        portLabel = QLabel()
        portLabel.setWordWrap(True)
        quitButton = QPushButton("Close the Server")
        quitButton.setAutoDefault(False)

        self.server = QLocalServer()
        if not self.server.listen('data'):
            QMessageBox.critical(self, "Time Tagger Server",
                    "Unable to start the server: %s." % self.server.errorString())
            self.close()
            return

        statusLabel.setText("The server is running.\n " "It is running at the port ")
        portLabel.setText(str(PORT))
        quitButton.clicked.connect(self.close)
        self.server.newConnection.connect(self.startServer)

        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(quitButton)
        buttonLayout.addStretch(1)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(statusLabel)
        mainLayout.addWidget(portLabel)
        mainLayout.addLayout(buttonLayout)
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    server = Server()
    server.show()
    sys.exit(app.exec_())
