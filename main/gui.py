from PyQt5 import QtWidgets
import target

class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.setWindowTitle('CobWeb')
        self.resize(600, 400)
        self.setStyleSheet("#MainWindow { background-color: #fcc; }")
        self.selection_box = self.create_selection_box()
        self.info = self.create_info()

    def create_selection_box(self):
        selection_box = QtWidgets.QComboBox(self)
        selection_box.addItem("請選擇學校")
        selection_box.addItem("ALL")
        for site in target.sites: 
            selection_box.addItem(site['school'])
        selection_box.setGeometry(10, 10, 200, 30)
        selection_box.move(50, 50)
        selection_box.currentIndexChanged.connect(self.selection_changed)
        return selection_box
    
    def create_info(self):
        info = QtWidgets.QLabel(self)
        info.move(200, 100)
        info.setText(self.selection_box.currentText())
        info.setStyleSheet("color: #00c; font-size: 20px;")
        return info

    def selection_changed(self):
        self.info.setText(self.selection_box.currentText())

def launch_gui():
    app = QtWidgets.QApplication([])
    window = App()
    window.show()
    app.exec_()
