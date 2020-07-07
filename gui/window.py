import sys
from PySide2.QtWidgets import QApplication, QLabel



def init_gui():

    app = QApplication(sys.argv)
    # label = QLabel("Hello World!")
    label = QLabel("<font color=red size=40>Hello World!</font>")
    label.show()
    app.exec_()