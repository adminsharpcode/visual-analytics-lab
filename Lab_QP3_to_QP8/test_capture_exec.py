import ctypes
from ctypes import wintypes
import time
from PIL import Image

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32

h_default = user32.OpenDesktopW("Default", 0, False, 0x01FF)
user32.SetThreadDesktop(h_default)

class RECT(ctypes.Structure):
    _fields_ = [
        ("left", wintypes.LONG),
        ("top", wintypes.LONG),
        ("right", wintypes.LONG),
        ("bottom", wintypes.LONG),
    ]

class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ('biSize', wintypes.DWORD),
        ('biWidth', wintypes.LONG),
        ('biHeight', wintypes.LONG),
        ('biPlanes', wintypes.WORD),
        ('biBitCount', wintypes.WORD),
        ('biCompression', wintypes.DWORD),
        ('biSizeImage', wintypes.DWORD),
        ('biXPelsPerMeter', wintypes.LONG),
        ('biYPelsPerMeter', wintypes.LONG),
        ('biClrUsed', wintypes.DWORD),
        ('biClrImportant', wintypes.DWORD),
    ]

def capture_window(hwnd, save_path):
    # Bring to foreground and restore if iconic
    if user32.IsIconic(hwnd):
        user32.ShowWindow(hwnd, 9) # SW_RESTORE
    user32.SetForegroundWindow(hwnd)
    time.sleep(0.5)

    rc = RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rc))
    w = rc.right - rc.left
    h = rc.bottom - rc.top
    print(f"Window bounds: ({rc.left}, {rc.top}) {w}x{h}")
    if w <= 0 or h <= 0:
        return False

    # Capture using PrintWindow with PW_RENDERFULLCONTENT
    h_dc_win = user32.GetWindowDC(hwnd)
    h_dc_mem = gdi32.CreateCompatibleDC(h_dc_win)
    h_bmp = gdi32.CreateCompatibleBitmap(h_dc_win, w, h)
    gdi32.SelectObject(h_dc_mem, h_bmp)

    # Try PrintWindow
    res = user32.PrintWindow(hwnd, h_dc_mem, 2) # PW_RENDERFULLCONTENT
    if not res:
        res = user32.PrintWindow(hwnd, h_dc_mem, 0)
    
    # If PrintWindow produced a black/empty bitmap or failed, we can also BitBlt from screen DC
    if not res:
        h_screen = user32.GetDC(0)
        gdi32.BitBlt(h_dc_mem, 0, 0, w, h, h_screen, rc.left, rc.top, 0x00CC0020) # SRCCOPY
        user32.ReleaseDC(0, h_screen)

    bmi = BITMAPINFOHEADER()
    bmi.biSize = ctypes.sizeof(BITMAPINFOHEADER)
    bmi.biWidth = w
    bmi.biHeight = -h  # top-down
    bmi.biPlanes = 1
    bmi.biBitCount = 32
    bmi.biCompression = 0

    buffer_size = w * h * 4
    buf = ctypes.create_string_buffer(buffer_size)
    gdi32.GetDIBits(h_dc_mem, h_bmp, 0, h, buf, ctypes.byref(bmi), 0)

    # Cleanup GDI
    gdi32.DeleteObject(h_bmp)
    gdi32.DeleteDC(h_dc_mem)
    user32.ReleaseDC(hwnd, h_dc_win)

    # Convert buffer to PIL Image
    img = Image.frombuffer('RGBA', (w, h), buf, 'raw', 'BGRA', 0, 1)
    img = img.convert('RGB')
    img.save(save_path)
    print(f"Saved: {save_path} ({w}x{h})")
    return True

# Test capture of Power BI and Brave
capture_window(316673518, "c:/Users/ROG/Desktop/Mtech Classwork/Visual analytics/Lab_QP3_to_QP8/screenshots/real_pbi_desktop.png")
capture_window(37818458, "c:/Users/ROG/Desktop/Mtech Classwork/Visual analytics/Lab_QP3_to_QP8/screenshots/real_brave_service.png")
