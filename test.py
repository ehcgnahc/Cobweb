import win32gui, win32con

def is_on_desktop(qt_window):
    # 取得桌面視窗的句柄
    desktop_hwnd = win32gui.GetDesktopWindow()
    # 取得目前 QT 視窗的父視窗
    current_parent = win32gui.GetWindowLong(qt_window.winId(), win32con.GWL_HWNDPARENT)
    
    # 比較父視窗是否為桌面句柄
    return current_parent == desktop_hwnd

# 使用範例
if is_on_desktop(window):
    print("視窗已嵌入桌面")
else:
    print("視窗不在桌面")
