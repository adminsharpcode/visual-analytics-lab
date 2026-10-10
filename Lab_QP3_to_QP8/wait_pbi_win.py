import ctypes
from ctypes import wintypes
import time
import subprocess

user32 = ctypes.windll.user32
h_default = user32.OpenDesktopW('Default', 0, False, 0x01FF)
user32.SetThreadDesktop(h_default)

for attempt in range(12):
    out = subprocess.check_output('powershell -Command "(Get-Process -Name PBIDesktop -ErrorAction SilentlyContinue).Id"', shell=True).decode()
    pbi_pids = set(int(x.strip()) for x in out.split() if x.strip().isdigit())
    
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
    
    pbi_wins = [w for w in windows if w[1] in pbi_pids]
    vis_wins = [w for w in pbi_wins if w[2] and w[3]]
    if vis_wins:
        print(f"Attempt {attempt}: Visible PBI Window Found!")
        for w in vis_wins:
            print(f"  HWND: {w[0]} | Title: '{w[3]}'")
        break
    else:
        print(f"Attempt {attempt}: Waiting... ({len(pbi_wins)} total windows for PBI, {len(vis_wins)} visible)")
    time.sleep(3)
