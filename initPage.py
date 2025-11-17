# initPage.py
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QFileDialog

class Ui_ObtainAPI(object):
    def setupUi(self, ObtainAPI):
        ObtainAPI.setObjectName("ObtainAPI")
        ObtainAPI.resize(446, 415)
        font = QtGui.QFont()
        font.setPointSize(20)
        ObtainAPI.setFont(font)
        ObtainAPI.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))

        # TextEdit
        self.textEdit = QtWidgets.QTextEdit(parent=ObtainAPI)
        self.textEdit.setGeometry(QtCore.QRect(100, 250, 281, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.textEdit.setFont(font)
        self.textEdit.setObjectName("textEdit")

        # Labels
        self.labelTitle = QtWidgets.QLabel(parent=ObtainAPI)
        self.labelTitle.setGeometry(QtCore.QRect(120, 50, 171, 61))
        self.labelTitle.setObjectName("labelTitle")

        self.labelDescription = QtWidgets.QLabel(parent=ObtainAPI)
        self.labelDescription.setGeometry(QtCore.QRect(100, 220, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.labelDescription.setFont(font)
        self.labelDescription.setObjectName("labelDescription")

        self.labelCredits = QtWidgets.QLabel(parent=ObtainAPI)
        self.labelCredits.setGeometry(QtCore.QRect(330, 380, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelCredits.setFont(font)
        self.labelCredits.setObjectName("labelCredits")

        # Botón Continue
        self.buttonContinue = QtWidgets.QPushButton(parent=ObtainAPI)
        self.buttonContinue.setGeometry(QtCore.QRect(310, 290, 75, 24))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.buttonContinue.setFont(font)
        self.buttonContinue.setObjectName("buttonContinue")
        self.buttonContinue.clicked.connect(self.open_file_dialog)

        # Logo
        self.label = QtWidgets.QLabel(parent=ObtainAPI)
        self.label.setGeometry(QtCore.QRect(300, 50, 61, 61))
        self.label.setPixmap(QtGui.QPixmap("resources/VTlogo.svg"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")

        self.retranslateUi(ObtainAPI)
        QtCore.QMetaObject.connectSlotsByName(ObtainAPI)

    def retranslateUi(self, ObtainAPI):
        _translate = QtCore.QCoreApplication.translate
        ObtainAPI.setWindowTitle(_translate("ObtainAPI", "VirusTotalGUI"))
        self.textEdit.setPlaceholderText(_translate("ObtainAPI", "Introduce your API key"))
        self.labelTitle.setText(_translate("ObtainAPI", "VirusTotal GUI"))
        self.labelDescription.setText(_translate("ObtainAPI", "Introduce your API key"))
        self.labelCredits.setText(_translate("ObtainAPI", "Made by DaGuz06"))
        self.buttonContinue.setText(_translate("ObtainAPI", "Continue"))

    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            None,
            "Selecciona un archivo",
            "",
            "Todos los archivos (*.*)"
        )
        if file_path:
            print(f"Archivo seleccionado: {file_path}")
