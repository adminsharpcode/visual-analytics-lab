import ctypes
from ctypes import wintypes
import os

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

h_default = user32.OpenDesktopW("Default", 0, False, 0x01FF)
res = user32.SetThreadDesktop(h_default)
print("SetThreadDesktop:", res)

windows = []
def enum_windows_proc(hwnd, lParam):
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    length = user32.GetWindowTextLengthW(hwnd)
    buff = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buff, length + 1)
    visible = user32.IsWindowVisible(hwnd)
    windows.append((hwnd, pid.value, visible, buff.value))
    return True

WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
user32.EnumWindows(WNDENUMPROC(enum_windows_proc), 0)

import subprocess
out = subprocess.check_output('powershell -Command "(Get-Process -Name PBIDesktop -ErrorAction SilentlyContinue).Id"', shell=True).decode()
pbi_pids = set(int(x.strip()) for x in out.split() if x.strip().isdigit())
print("PBI PIDs:", pbi_pids)

for hwnd, pid, vis, title in windows:
    if pid in pbi_pids or any(k in title.lower() for k in ["power bi", "brave"]):
        print(f"HWND: {hwnd} | PID: {pid} | Visible: {vis} | Title: '{title}'")
