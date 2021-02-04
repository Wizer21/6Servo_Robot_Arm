import sys
from PyQt5.QtWidgets import*
from PyQt5.QtGui import*
from PyQt5.QtCore import*
from main_gui import*


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # DELETE '?' ON QDIALOG
    app.setAttribute(Qt.AA_DisableWindowContextHelpButton)

    # GET WINDOW SIZE
    rec = QRect(app.primaryScreen().availableGeometry())
    resolution = [rec.width(), rec.height()]

    font_size = int(resolution[0] /  110)
    font_qss = "QWidget{ font-size:" + str(font_size) + "px;}"

    # APPLY STYLESHEET
    with open("./theme.qss") as file:
        theme = file.read()
        app.setStyleSheet(font_qss + theme)

    # SET UP DEFAULT SIZE IN Utils

    gui = main_gui() 
    gui.show()

    sys.exit(app.exec_())