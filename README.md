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
scripts/启动指示牌.bat        # 或 scripts/qidong_zhishipai.bat（纯英文名，制作快捷方式更稳）

# 方式二：命令行（注意先 cd 到 scripts 目录，否则 pythonw 找不到文件也不会报错）
cd scripts
pythonw input_indicator.pyw
```

## 创建桌面快捷方式（Windows）

用 PowerShell 一键创建：

```powershell
$desktop = [Environment]::GetFolderPath('Desktop')
$target = 'C:\path\to\input-indicator-skill\scripts\qidong_zhishipai.bat'
$shortcutPath = Join-Path $desktop 'InputIndicator.lnk'

$shell = New-Object -ComObject WScript.Shell
$lnk = $shell.CreateShortcut($shortcutPath)
$lnk.TargetPath = $target
$lnk.WorkingDirectory = Split-Path $target
$lnk.IconLocation = 'C:\Windows\System32\imageres.dll,109'
$lnk.Save()
```

将 `$target` 换成你本机的实际路径即可。推荐用 `qidong_zhishipai.bat`（纯英文文件名）而不是中文名 `.bat`，避免部分环境下中文路径解析异常。

## 作为 Skill 使用

本仓库遵循 Skill 目录规范，包含 [SKILL.md](SKILL.md) 与 `scripts/`。
可直接放入 `~/.claude/skills/` 或对应 Skill 目录后调用。

## 环境要求

- Windows
- Python 3（Windows 自带的即可，需含 `tkinter`）

## 许可

MIT
