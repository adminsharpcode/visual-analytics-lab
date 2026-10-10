import ctypes
from ctypes import wintypes

user32 = ctypes.windll.user32
h_default = user32.OpenDesktopW('Default', 0, False, 0x01FF)
user32.SetThreadDesktop(h_default)

hwnd = 316673518
children = []
def enum_child_proc(h, lParam):
    length = user32.GetWindowTextLengthW(h)
    buff = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(h, buff, length + 1)
    cls = ctypes.create_unicode_buffer(256)
    user32.GetClassNameW(h, cls, 256)
    rc = wintypes.RECT()
    user32.GetWindowRect(h, ctypes.byref(rc))
    vis = user32.IsWindowVisible(h)
    children.append((h, cls.value, buff.value, (rc.left, rc.top, rc.right-rc.left, rc.bottom-rc.top), vis))
    return True

WNDENUMCHILDPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
user32.EnumChildWindows(hwnd, WNDENUMCHILDPROC(enum_child_proc), 0)

print(f'Total children: {len(children)}')
for h, cls, title, rc, vis in children:
    if vis and rc[2] > 0 and rc[3] > 0:
        print(f'HWND {h} | Class: {cls} | Title: "{title}" | Rect: {rc}')
