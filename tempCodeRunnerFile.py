win32gui.GetDesktopWindow()
current = win32gui.GetForegroundWindow()
desktop_name = win32gui.GetClassName(desktop)
current_name = win32gui.GetClassName(current)

print(f"De