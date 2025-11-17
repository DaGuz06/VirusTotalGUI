# appPage.py
# appPage.py
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QFileDialog, QMessageBox
import requests
import time

# -----------------------------
# Worker para análisis en segundo plano
# -----------------------------
class AnalysisWorker(QtCore.QThread):
    result_ready = QtCore.pyqtSignal(str)  # señal para enviar el resultado al QTextEdit

    def __init__(self, api_key, analysis_id):
        super().__init__()
        self.api_key = api_key
        self.analysis_id = analysis_id

    def run(self):
        url = f"https://www.virustotal.com/api/v3/analyses/{self.analysis_id}"
        headers = {"x-apikey": self.api_key}

        while True:
            try:
                r = requests.get(url, headers=headers)
                if r.status_code == 200:
                    data = r.json()
                    status = data["data"]["attributes"]["status"]
                    if status == "completed":
                        stats = data["data"]["attributes"]["stats"]
                        summary = "\n".join([f"{k}: {v}" for k, v in stats.items()])
                        self.result_ready.emit(summary)
                        break
                else:
                    self.result_ready.emit(f"Error: {r.status_code}")
                    break
            except Exception as e:
                self.result_ready.emit(f"Error: {e}")
                break
            time.sleep(2)


# -----------------------------
# UI principal
# -----------------------------
class Ui_AppPage(object):
    def setupUi(self, Dialog, api_key=None):
        self.api_key = api_key
        self.Dialog = Dialog
        
        Dialog.setObjectName("Dialog")
        Dialog.resize(446, 415)
        Dialog.setMinimumSize(QtCore.QSize(446, 415))
        Dialog.setMaximumSize(QtCore.QSize(446, 415))
        font = QtGui.QFont()
        font.setPointSize(9)
        Dialog.setFont(font)

        # Logo
        self.label_2 = QtWidgets.QLabel(parent=Dialog)
        self.label_2.setGeometry(QtCore.QRect(380, 10, 61, 61))
        self.label_2.setPixmap(QtGui.QPixmap("resources/VTlogo.svg"))
        self.label_2.setScaledContents(True)

        # Título
        self.labelTitle = QtWidgets.QLabel(parent=Dialog)
        self.labelTitle.setGeometry(QtCore.QRect(200, 10, 171, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.labelTitle.setFont(font)

        # Botón Upload
        self.buttonUpload = QtWidgets.QPushButton(parent=Dialog)
        self.buttonUpload.setGeometry(QtCore.QRect(20, 90, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.buttonUpload.setFont(font)
        self.buttonUpload.setText("Upload file")
        self.buttonUpload.clicked.connect(self.open_file_dialog)

        # Botón Clear
        self.buttonClear = QtWidgets.QPushButton(parent=Dialog)
        self.buttonClear.setGeometry(QtCore.QRect(130, 90, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.buttonClear.setFont(font)
        self.buttonClear.setText("Clear")
        self.buttonClear.clicked.connect(self.clear_results)

        # Recuadro de resultados
        self.textResult = QtWidgets.QTextEdit(parent=Dialog)
        self.textResult.setGeometry(QtCore.QRect(20, 140, 406, 220))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.textResult.setFont(font)
        self.textResult.setReadOnly(True)
        self.textResult.setPlaceholderText("Aquí aparecerá el resultado del análisis")

        # Créditos
        self.labelCredits = QtWidgets.QLabel(parent=Dialog)
        self.labelCredits.setGeometry(QtCore.QRect(330, 380, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelCredits.setFont(font)
        self.labelCredits.setText("Made by DaGuz06")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "VirusTotalGUI"))
        self.labelTitle.setText(_translate("Dialog", "VirusTotal GUI"))
        self.labelCredits.setText(_translate("Dialog", "Made by DaGuz06"))

    # -----------------------------
    # Abrir explorador y subir archivo
    # -----------------------------
    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "Selecciona un archivo", "", "Todos los archivos (*.*)")
        if file_path:
            QMessageBox.information(None, "Archivo seleccionado", f"{file_path}")
            self.upload_file(file_path)

    # -----------------------------
    # Subir archivo a VirusTotal
    # -----------------------------
    def upload_file(self, file_path):
        if not self.api_key:
            QMessageBox.critical(None, "Error", "No hay API Key disponible")
            return

        url = "https://www.virustotal.com/api/v3/files"
        headers = {"x-apikey": self.api_key}

        try:
            with open(file_path, "rb") as f:
                files = {"file": (file_path, f)}
                response = requests.post(url, headers=headers, files=files)

            if response.status_code in [200, 201]:
                data = response.json()
                analysis_id = data["data"]["id"]
                self.textResult.setPlainText("File uploaded successfully. Waiting for analysis...\n")
                self.get_analysis_result(analysis_id)
            else:
                QMessageBox.critical(None, "Error", f"No se pudo subir el archivo:\n{response.text}")
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Error al subir archivo:\n{e}")

    # -----------------------------
    # Consultar análisis usando QThread
    # -----------------------------
    def get_analysis_result(self, analysis_id):
        self.worker = AnalysisWorker(self.api_key, analysis_id)
        self.worker.result_ready.connect(self.show_analysis_result)
        self.worker.start()

    def show_analysis_result(self, summary):
        self.textResult.setPlainText(summary)

    # -----------------------------
    # Limpiar recuadro de resultados
    # -----------------------------
    def clear_results(self):
        self.textResult.clear()
