# -*- coding: utf-8 -*-
"""
桌面输入状态悬浮指示牌 (Windows)

功能：
- 实时显示当前输入法「中 / 英」状态，以及「大写 / 小写」(Caps Lock) 状态
- 点击「中/英」牌子  -> 切换输入法中英文
- 点击「大/小」牌子  -> 切换 Caps Lock
- 鼠标左键按住牌子空白处可拖动移动位置
- 右键菜单可退出

仅依赖 Windows 自带 Python 的 tkinter，无需安装任何第三方库。
双击本文件 (.pyw) 即可运行（不弹黑框）。
"""
import tkinter as tk
import ctypes
from ctypes import wintypes

# ---------------- Win32 接口 ----------------
user32 = ctypes.WinDLL("user32", use_last_error=True)
imm32 = ctypes.WinDLL("imm32", use_last_error=True)

WM_IME_CONTROL        = 0x0283
IMC_GETCONVERSIONMODE = 0x0001
IMC_SETCONVERSIONMODE = 0x0002
IME_CMODE_NATIVE      = 0x0001   # 该位为 1 => 中文，为 0 => 英文

VK_CAPITAL            = 0x14
KEYEVENTF_KEYUP       = 0x0002

user32.SendMessageW.restype = ctypes.c_longlong
user32.SendMessageW.argtypes = [wintypes.HWND, wintypes.UINT,
                                wintypes.WPARAM, ctypes.c_longlong]
user32.GetForegroundWindow.restype = wintypes.HWND
imm32.ImmGetDefaultIMEWnd.restype = wintypes.HWND
imm32.ImmGetDefaultIMEWnd.argtypes = [wintypes.HWND]


def _ime_wnd():
    """取得当前前台窗口对应的 IME 窗口句柄。"""
    fg = user32.GetForegroundWindow()
    if not fg:
        return None
    return imm32.ImmGetDefaultIMEWnd(fg)


def get_ime_is_chinese():
    """返回 True=中文, False=英文, None=无法获取。"""
    ime = _ime_wnd()
    if not ime:
        return None
    mode = user32.SendMessageW(ime, WM_IME_CONTROL, IMC_GETCONVERSIONMODE, 0)
    return bool(mode & IME_CMODE_NATIVE)


def toggle_ime():
    """切换当前输入法中/英文状态。"""
    ime = _ime_wnd()
    if not ime:
        return
    mode = user32.SendMessageW(ime, WM_IME_CONTROL, IMC_GETCONVERSIONMODE, 0)
    mode ^= IME_CMODE_NATIVE
    user32.SendMessageW(ime, WM_IME_CONTROL, IMC_SETCONVERSIONMODE, mode)


def get_caps_on():
    """返回 True=大写锁定开启。"""
    return bool(user32.GetKeyState(VK_CAPITAL) & 0x0001)


def toggle_caps():
    """模拟按下 Caps Lock 键以切换大小写。"""
    user32.keybd_event(VK_CAPITAL, 0, 0, 0)
    user32.keybd_event(VK_CAPITAL, 0, KEYEVENTF_KEYUP, 0)


# ---------------- 界面 ----------------
BG        = "#1e1e2e"   # 背景
ZH_COLOR  = "#f38ba8"   # 中文高亮色
EN_COLOR  = "#89b4fa"   # 英文高亮色
CAPS_ON   = "#f9e2af"   # 大写高亮色
CAPS_OFF  = "#a6e3a1"   # 小写高亮色
DIM       = "#585b70"   # 未选中的暗色


class Indicator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("输入状态指示牌")
        self.root.overrideredirect(True)          # 去掉标题栏
        self.root.attributes("-topmost", True)     # 始终置顶
        self.root.attributes("-alpha", 0.92)
        self.root.configure(bg=BG)

        # 初始位置：屏幕右下角
        sw = self.root.winfo_screenwidth()
        self.root.geometry(f"+{sw - 220}+80")

        pad = {"padx": 10, "pady": 8}

        # 中/英 牌子
        self.ime_lbl = tk.Label(self.root, text="中", font=("微软雅黑", 22, "bold"),
                                width=3, bg=BG, fg=ZH_COLOR, cursor="hand2")
        self.ime_lbl.grid(row=0, column=0, **pad)
        self.ime_lbl.bind("<Button-1>", lambda e: (toggle_ime(), self.refresh()))

        # 分隔线
        tk.Frame(self.root, bg=DIM, width=2, height=40).grid(row=0, column=1, pady=8)

        # 大/小 牌子
        self.caps_lbl = tk.Label(self.root, text="小写", font=("微软雅黑", 18, "bold"),
                                 width=4, bg=BG, fg=CAPS_OFF, cursor="hand2")
        self.caps_lbl.grid(row=0, column=2, **pad)
        self.caps_lbl.bind("<Button-1>", lambda e: (toggle_caps(), self.refresh()))

        # 拖动：绑定在整个窗口背景上
        self.root.bind("<ButtonPress-1>", self._start_move)
        self.root.bind("<B1-Motion>", self._on_move)

        # 右键退出菜单
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="退出", command=self.root.destroy)
        self.root.bind("<Button-3>", lambda e: menu.tk_popup(e.x_root, e.y_root))

        self._drag = {"x": 0, "y": 0}
        self.refresh()
        self._tick()

    def _start_move(self, e):
        self._drag["x"], self._drag["y"] = e.x, e.y

    def _on_move(self, e):
        x = self.root.winfo_x() + e.x - self._drag["x"]
        y = self.root.winfo_y() + e.y - self._drag["y"]
        self.root.geometry(f"+{x}+{y}")

    def refresh(self):
        zh = get_ime_is_chinese()
        if zh is None:
            self.ime_lbl.config(text="—", fg=DIM)
        elif zh:
            self.ime_lbl.config(text="中", fg=ZH_COLOR)
        else:
            self.ime_lbl.config(text="英", fg=EN_COLOR)

        if get_caps_on():
            self.caps_lbl.config(text="大写", fg=CAPS_ON)
        else:
            self.caps_lbl.config(text="小写", fg=CAPS_OFF)

    def _tick(self):
        """定时刷新，捕捉用户用其它方式（如按键）改变的状态。"""
        self.refresh()
        self.root.after(200, self._tick)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    Indicator().run()
