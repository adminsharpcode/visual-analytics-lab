import ctypes
from ctypes import wintypes
import subprocess

user32 = ctypes.windll.user32
h_default = user32.OpenDesktopW('Default', 0, False, 0x01FF)
user32.SetThreadDesktop(h_default)

# Get all PIDs related to PBIDesktop
out = subprocess.check_output('powershell -Command "Get-Process -Name PBIDesktop,msedgewebview2,msmdsrv -ErrorAction SilentlyContinue | Select -ExpandProperty Id"', shell=True).decode()
pids = set(int(x.strip()) for x in out.split() if x.strip().isdigit())
print(f"Tracking {len(pids)} PIDs: {pids}")

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

for hwnd, pid, vis, title in windows:
    if pid in pids or 'visual1' in title.lower() or 'power bi' in title.lower():
        print(f"HWND: {hwnd} | PID: {pid} | Vis: {vis} | Title: '{title}'")
