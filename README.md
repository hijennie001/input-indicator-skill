# input-indicator · 输入状态悬浮指示牌

一个 Windows 桌面小工具，同时也是一个 [Claude Code / Ducc Skill](SKILL.md)。

常驻桌面、始终置顶的悬浮牌子，实时显示并一键切换：

- **中 / 英** 输入法状态
- **大写 / 小写** (Caps Lock) 状态

![](docs/preview.png)

## 特性

- 每 200ms 自动刷新，键盘切换也能即时同步
- 点击牌子即可切换输入法 / Caps Lock
- 可拖动移动，右键退出
- 仅依赖 Windows 自带 Python 的 `tkinter`，**零第三方依赖**

## 快速开始

```bash
# 方式一：双击运行
scripts/启动指示牌.bat

# 方式二：命令行
pythonw scripts/input_indicator.pyw
```

## 作为 Skill 使用

本仓库遵循 Skill 目录规范，包含 [SKILL.md](SKILL.md) 与 `scripts/`。
可直接放入 `~/.claude/skills/` 或对应 Skill 目录后调用。

## 环境要求

- Windows
- Python 3（Windows 自带的即可，需含 `tkinter`）

## 许可

MIT
