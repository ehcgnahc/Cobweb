import win32gui

while(True):
    desktop = win32gui.GetDesktopWindow()
    current = win32gui.GetForegroundWindow()
    desktop_name = win32gui.GetClassName(desktop)
    current_name = win32gui.GetClassName(current)
    
    print(f"Desktop: {desktop}, Current: {current}, Desktop_Name: {desktop_name}, Current_Name: {current_name}")