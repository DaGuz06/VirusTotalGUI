import sys
from PyQt6.QtWidgets import QApplication, QDialog
from initPage  import Ui_ObtainAPI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = QDialog()
    ui = Ui_ObtainAPI()
    ui.setupUi(dialog)
    dialog.show()
    sys.exit(app.exec())