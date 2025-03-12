from PyQt5 import QtWidgets, QtGui, QtCore
import os
import sys
import sqlite3
import target

class App(QtWidgets.QWidget):
    def __init__(self, database_conn):
        super().__init__()
        self.setObjectName("MainWindow")
        self.setWindowTitle('CobWeb')
        self.resize(600, 400)
        self.setStyleSheet("#MainWindow { background-color: #fcc; }")
        
        self.initTray()
        self.database_conn = database_conn
        self.mode = "interactive"
        self.info = self.show_info()
        
        if self.mode == "interactive":
            self.selection_box = self.create_selection_box()
            # self.info.setDisabled(False)
        else:
            self.selection_box = None
            self.load_events()
            # self.info.setDisabled(True)

    def initTray(self):
        show = QtWidgets.QAction("Show", self, triggered=self.show) #　顯示
        background = QtWidgets.QAction("Background", self, triggered=self.lower) # 背景
        quit = QtWidgets.QAction("Quit", self, triggered=self.close) # 關閉
        
        self.tray_menu = QtWidgets.QMenu()
        self.tray_menu.addAction(show)
        self.tray_menu.addAction(background)
        self.tray_menu.addAction(quit)

        icon = os.path.join("icon.png")
        
        self.tray_icon = QtWidgets.QSystemTrayIcon(self)
        self.tray_icon.setIcon(QtGui.QIcon(icon))
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()
        
        
        
    def create_selection_box(self):
        selection_box = QtWidgets.QComboBox(self)
        selection_box.addItem("請選擇學校")
        selection_box.addItem("ALL")

        for site in target.sites:
            selection_box.addItem(site['school'])

        selection_box.setGeometry(10, 10, 200, 30)
        selection_box.move(50, 50)
        
        selection_box.currentIndexChanged.connect(lambda: self.load_events())

        return selection_box
    
    def show_info(self):
        info = QtWidgets.QListWidget(self)
        info.move(200, 100)
        info.resize(800, 600)
        info.setStyleSheet("color: #00c; font-size: 20px;")
        
        if self.mode == "interactive":
            info.clicked.connect(lambda: self.link_clicked())
        
        return info

    def load_events(self):
        self.info.clear()
        
        if self.selection_box is None:
            selected_school = "ALL"
        else:
            selected_school = self.selection_box.currentText()

        if selected_school == "請選擇學校":
            return

        try:
            cursor = self.database_conn.cursor()

            if selected_school == "ALL":
                cursor.execute("SELECT School, Title, Title_Simplified, Link FROM events ORDER BY ID ASC")
            else:
                cursor.execute("SELECT School, Title, Title_Simplified, Link FROM events WHERE School = ? ORDER BY ID ASC", (selected_school,))

            results = cursor.fetchall()

            if results:
                for row in results:
                    school, title, title_simplified, link = row
                    item = QtWidgets.QListWidgetItem(f"🏫 {school}\n📌 {title}\n")
                    self.info.addItem(item)
            else:
                self.info.addItem("查無資料")

        except Exception as e:
            self.info.addItem(f"發生錯誤: {e}")

    def link_clicked(self):
        selected_school = self.info.currentItem().text().split("\n")[0][2:]
        selected_title = self.info.currentItem().text().split("\n")[1][2:]
        # print(selected_school)
        # print(selected_title)
        
        try:
            cursor = self.database_conn.cursor()
            
            cursor.execute("SELECT Link FROM events WHERE School = ? AND Title = ?", (selected_school, selected_title))
            result = cursor.fetchone()
            if result:
                link = result[0]
                QtWidgets.QMessageBox.information(self, "活動連結", f"即將前往:\n{selected_school} - {selected_title}\n{link}")
                # webbrowser.open(link)
            else:
                QtWidgets.QMessageBox.warning(self, "錯誤", "查無連結")
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "錯誤", f"發生錯誤: {e}")
        
    
def launch_gui(database_path, blacklist_path):
    database_conn = sqlite3.connect(database_path)
    
    app = QtWidgets.QApplication([])
    window = App(database_conn)
    window.show()
    app.exec_()
    
    database_conn.close()
