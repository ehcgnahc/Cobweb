from PyQt5 import QtWidgets, QtGui, QtCore
from ctypes import windll
import os
import sys
import win32gui, win32con
import webbrowser
import sqlite3
import target

class App(QtWidgets.QWidget):
    def __init__(self, database_conn):
        super().__init__()
        self.setObjectName("MainWindow")
        self.setWindowTitle('CobWeb')
        self.resize(800, 320)
        self.setStyleSheet("#MainWindow { background-color: #fcc; }")
        
        self.mode = "show"
        self.initTray()
        self.raise_
        self.database_conn = database_conn
        self.info = self.show_info()
        self.selection_box = self.create_selection_box()
        self.load_events()
        
        self.desktop_timer = QtCore.QTimer(self)
        self.desktop_timer.timeout.connect(self.check_desktop)
        self.desktop_timer.start(100)
        # self.info.setDisabled(True)
        
    def initTray(self):
        icon = os.path.join("icon.png")
        head = QtWidgets.QAction("CobWeb", self) # 標題
        show = QtWidgets.QAction("Show", self) #　顯示
        hide = QtWidgets.QAction("Hide", self) # 隱藏
        background = QtWidgets.QAction("Background", self) # 背景
        quit = QtWidgets.QAction("Quit", self, triggered = self.close) # 關閉
        
        head.setIcon(QtGui.QIcon(icon))
        head.setDisabled(True)
        show.triggered.connect(self.show_window)
        hide.triggered.connect(self.hide_window)
        background.triggered.connect(self.background_window)
        
        self.tray_menu = QtWidgets.QMenu()
        self.tray_menu.addAction(head)
        self.tray_menu.addSeparator()
        self.tray_menu.addAction(show)
        self.tray_menu.addAction(hide)
        # self.tray_menu.addAction(background)
        self.tray_menu.addAction(quit)
        
        self.tray_menu.setStyleSheet("""
            QMenu {
                background-color: rgb(31, 31, 31);
                color: rgba(255, 255, 255, 0.92);
                padding: 2px 5px
            }
            QMenu::item {
                padding: 8px 25px
            }
            QMenu::item:selected {
                background-color: rgba(93, 93, 93, 0.2);
            }
            QMenu::separator {
                background-color: rgba(155, 155, 155, 0.5);
                height: 1px;
                margin: 5px 0px 5px 0px;
            }
        """)
        
        self.tray = QtWidgets.QSystemTrayIcon(self)
        self.tray.setToolTip("CobWeb")
        self.tray.setIcon(QtGui.QIcon(icon))
        self.tray.setContextMenu(self.tray_menu)
        self.tray.show()
    
    def show_window(self):
        self.show()
        self.raise_()
        self.mode = "show"
        self.selection_box.setDisabled(False)
    
    def hide_window(self):
        self.hide()
        self.mode = "hide"
    
    def background_window(self):
        self.lower()
        self.mode = "background"
        self.selection_box.setDisabled(True)
    
    def check_desktop(self):
        if self.mode == "background":
            self.lower()
            # desktop_hwnd = win32gui.GetDesktopWindow()
            # current_hwnd = win32gui.GetForegroundWindow()
            # desktop_text = windll.user32.GetWindowTextW(desktop_hwnd)
            # current_text = windll.user32.GetWindowTextW(current_hwnd)
            # print(f"current_hwnd: {current_hwnd}, current_text: {current_text}, desktop_hwnd: {desktop_hwnd}, desktop_text: {desktop_text}")
            # if current_hwnd == desktop_hwnd:
            #     self.show()
            #     self.raise_()
            # else:
            #     self.hide()
        
    def create_selection_box(self):
        selection_box = QtWidgets.QComboBox(self)
        selection_box.addItem("請選擇學校")
        selection_box.addItem("ALL")

        for site in target.sites:
            selection_box.addItem(site['school'])

        selection_box.setGeometry(10, 10, 200, 30)
        selection_box.move(2, 2)
        
        selection_box.currentIndexChanged.connect(lambda: self.load_events())

        return selection_box
    
    def show_info(self):
        info = QtWidgets.QListWidget(self)
        info.move(2, 33)
        info.resize(800, 300)
        info.setStyleSheet("color: #00c; font-size: 20px;")
        
        if self.mode == "show":
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
                cursor.execute(
                    """
                    SELECT School, Title, Title_Simplified, Link, Post_Date
                    FROM events
                    ORDER BY Post_Date DESC, ID ASC
                    """
                )
            else:
                cursor.execute(
                    """
                    SELECT School, Title, Title_Simplified, Link, Post_Date
                    FROM events
                    WHERE School = ?
                    ORDER BY Post_Date DESC, ID ASC
                    """,
                    (selected_school,)
                )

            results = cursor.fetchall()

            if results:
                for row in results:
                    school, title, title_simplified, link, post_date = row
                    item = QtWidgets.QListWidgetItem(f"{post_date[:10]}\n🏫 {school}\n📌 {title}\n")
                    self.info.addItem(item)
            else:
                self.info.addItem("查無資料")

        except Exception as e:
            self.info.addItem(f"發生錯誤: {e}")

    def link_clicked(self):
        selected_school = self.info.currentItem().text().split("\n")[1][2:]
        selected_title = self.info.currentItem().text().split("\n")[2][2:]
        # print(selected_school)
        # print(selected_title)
        
        try:
            cursor = self.database_conn.cursor()
            
            cursor.execute(
                """
                SELECT Link
                FROM events
                WHERE School = ? AND Title = ?
                """,
                (selected_school, selected_title)
            )
            result = cursor.fetchone()
            if result:
                link = result[0]
                reply = QtWidgets.QMessageBox.question(self, "活動連結", f"即將前往:\n{selected_school} - {selected_title}", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.Yes:
                    webbrowser.open(link)
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
