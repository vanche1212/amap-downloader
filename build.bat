@echo off
chcp 65001 >nul
echo 🎯 高德地图下载器 - Windows打包
echo ================================

REM 检查Python环境
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python，请先安装Python
    pause
    exit /b 1
)

REM 安装PyInstaller
echo 📦 检查PyInstaller...
python -m pip install pyinstaller --quiet

REM 清理之前的构建
echo 🧹 清理之前的构建文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del *.spec

REM 开始打包
echo 🚀 开始打包...
python -m PyInstaller ^
    --onefile ^
    --windowed ^
    --name "高德地图下载器" ^
    --clean ^
    --hidden-import tkinter ^
    --hidden-import tkinter.ttk ^
    --hidden-import tkinter.messagebox ^
    --hidden-import tkinter.filedialog ^
    --hidden-import requests ^
    --hidden-import json ^
    --hidden-import pathlib ^
    --hidden-import threading ^
    --hidden-import urllib.parse ^
    --exclude-module matplotlib ^
    --exclude-module numpy ^
    --exclude-module pandas ^
    --exclude-module scipy ^
    --exclude-module PIL ^
    --exclude-module cv2 ^
    map_downloader_gui.py

if %errorlevel% equ 0 (
    echo ✅ 打包成功!
    
    REM 查找生成的文件
    if exist "dist\高德地图下载器.exe" (
        for %%A in ("dist\高德地图下载器.exe") do set file_size=%%~zA
        echo 📦 生成的可执行文件: dist\高德地图下载器.exe
        echo 📏 文件大小: %file_size% 字节
        
        REM 移动到当前目录
        move "dist\高德地图下载器.exe" "高德地图下载器_Windows.exe"
        echo ✨ 最终文件: 高德地图下载器_Windows.exe
        
        echo.
        echo 🎉 打包完成!
        echo 💡 提示:
        echo    - 可执行文件已生成在当前目录
        echo    - 可以直接双击运行
        echo    - 首次运行时请输入高德地图API密钥
    ) else (
        echo ❌ 未找到生成的可执行文件
    )
) else (
    echo ❌ 打包失败
)

REM 清理临时文件
echo 🧹 清理临时文件...
if exist build rmdir /s /q build
if exist *.spec del *.spec

pause