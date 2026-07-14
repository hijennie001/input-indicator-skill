@echo off
REM 一键启动输入状态悬浮指示牌
REM 用 pythonw 运行，不弹命令行黑框
cd /d "%~dp0"
start "" pythonw "input_indicator.pyw"
