---
name: input-indicator
description: 在 Windows 桌面显示一个常驻置顶的悬浮指示牌，实时显示当前「中/英」输入法状态和「大写/小写」(Caps Lock) 状态，点击即可切换。当用户想要清晰看到并快速切换输入法中英文、大小写状态时使用。
---

# 输入状态悬浮指示牌 (Input Indicator)

一个 Windows 桌面小工具：常驻置顶的悬浮牌子，实时显示并可一键切换输入法中英文、大小写状态。

## 功能

- **实时显示**当前输入法「中 / 英」状态（红色=中文，蓝色=英文）
- **实时显示**「大写 / 小写」(Caps Lock) 状态（黄色=大写，绿色=小写）
- 每 200ms 自动刷新，键盘切换也能立即跟上
- 点击「中/英」牌子 → 切换输入法中英文
- 点击「大写/小写」牌子 → 切换 Caps Lock
- 按住牌子拖动 → 移动到任意位置（默认屏幕右上角）
- 右键 → 退出

## 环境要求

- 仅支持 **Windows**（依赖 Win32 API：IME 控制、Caps Lock 状态）
- 只需 Windows 自带 Python 的 `tkinter`，**无需安装任何第三方库**

## 使用方法

工具文件位于本 skill 的 `scripts/` 目录：

- `scripts/input_indicator.pyw` — 主程序（`.pyw` 双击运行不弹黑框）
- `scripts/启动指示牌.bat` — 一键启动脚本（用 `pythonw` 运行）

### 运行方式

1. 双击 `scripts/启动指示牌.bat`，或
2. 双击 `scripts/input_indicator.pyw`，或
3. 命令行运行：`pythonw scripts/input_indicator.pyw`

### 使用 skill 时的操作步骤

当用户请求这个工具时：

1. 确认用户是 Windows 系统
2. 将 `scripts/` 下的两个文件复制到用户想要的位置
3. 告诉用户双击 `启动指示牌.bat` 即可运行
4. 如需开机自启，可将 `.bat` 快捷方式放入启动文件夹（`shell:startup`）

## 自定义

在 `input_indicator.pyw` 顶部的界面配置区可调整：

- 颜色：`BG` / `ZH_COLOR` / `EN_COLOR` / `CAPS_ON` / `CAPS_OFF`
- 字体大小：`font=("微软雅黑", 22, "bold")`
- 初始位置：`self.root.geometry(...)`
- 透明度：`self.root.attributes("-alpha", 0.92)`

## 已知限制

- 输入法状态通过前台窗口的 IME 读取；个别第三方输入法可能读不到中英文状态，此时会显示 `—`
- 仅在 Windows 上有效
