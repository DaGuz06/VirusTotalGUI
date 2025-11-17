# initPage.py
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox, QDialog
import requests

from appPage import Ui_AppPage

class Ui_ObtainAPI(object):
    def setupUi(self, ObtainAPI):
        self.main_window = ObtainAPI
        ObtainAPI.setObjectName("ObtainAPI")
        ObtainAPI.resize(446, 415)
        font = QtGui.QFont()
        font.setPointSize(20)
        ObtainAPI.setFont(font)

        # TextEdit API
        self.textEdit = QtWidgets.QTextEdit(parent=ObtainAPI)
        self.textEdit.setGeometry(QtCore.QRect(100, 250, 281, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.textEdit.setFont(font)

        # Labels
        self.labelTitle = QtWidgets.QLabel(parent=ObtainAPI)
        self.labelTitle.setGeometry(QtCore.QRect(120, 50, 171, 61))

        self.labelDescription = QtWidgets.QLabel(parent=ObtainAPI)
        self.labelDescription.setGeometry(QtCore.QRect(100, 220, 191, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.labelDescription.setFont(font)

        self.labelCredits = QtWidgets.QLabel(parent=ObtainAPI)
        self.labelCredits.setGeometry(QtCore.QRect(330, 380, 111, 31))

        # Botón Continue → validar API
        self.buttonContinue = QtWidgets.QPushButton(parent=ObtainAPI)
        self.buttonContinue.setGeometry(QtCore.QRect(310, 290, 75, 24))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.buttonContinue.setFont(font)
        self.buttonContinue.clicked.connect(self.validate_api_key)

        # Logo
        self.label = QtWidgets.QLabel(parent=ObtainAPI)
        self.label.setGeometry(QtCore.QRect(300, 50, 61, 61))
        self.label.setPixmap(QtGui.QPixmap("resources/VTlogo.svg"))
        self.label.setScaledContents(True)

        self.retranslateUi(ObtainAPI)
        QtCore.QMetaObject.connectSlotsByName(ObtainAPI)

        # Creditos

        self.labelCredits = QtWidgets.QLabel(parent=ObtainAPI)
        self.labelCredits.setGeometry(QtCore.QRect(330, 380, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelCredits.setFont(font)
        self.labelCredits.setText("Made by DaGuz06")

    def retranslateUi(self, ObtainAPI):
        _translate = QtCore.QCoreApplication.translate
        ObtainAPI.setWindowTitle(_translate("ObtainAPI", "VirusTotalGUI"))
        self.textEdit.setPlaceholderText(_translate("ObtainAPI", "Introduce your API key"))
        self.labelTitle.setText(_translate("ObtainAPI", "VirusTotal GUI"))
        self.labelDescription.setText(_translate("ObtainAPI", "Introduce your API key"))
        self.buttonContinue.setText(_translate("ObtainAPI", "Continue"))

    # ------------------------------
    # VALIDAR API KEY
    # ------------------------------
    def validate_api_key(self):
        api_key = self.textEdit.toPlainText().strip()

        if not api_key:
            QMessageBox.warning(None, "Error", "Debes introducir una API key.")
            return

        url = "https://www.virustotal.com/api/v3/users/me"
        headers = {"x-apikey": api_key}

        try:
            r = requests.get(url, headers=headers)

            if r.status_code == 200:
                QMessageBox.information(None, "Correcto", "API key válida.")
                self.open_app_page(api_key)
            else:
                QMessageBox.critical(None, "Incorrecto", "API key inválida.")
        except Exception as e:
            QMessageBox.critical(None, "Error", f"No se pudo conectar:\n{e}")

    # ------------------------------
    # ABRIR LA SIGUIENTE PÁGINA
    # ------------------------------
    def open_app_page(self, api_key):
        self.app_dialog = QDialog()
        self.app_ui = Ui_AppPage()
        self.app_ui.setupUi(self.app_dialog, api_key=api_key)
        self.main_window.close()
        self.app_dialog.show()
