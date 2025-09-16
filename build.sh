#!/bin/bash
# 快速打包脚本

echo "🎯 高德地图下载器 - 快速打包"
echo "================================"

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python"
    exit 1
fi

# 安装PyInstaller
echo "📦 检查PyInstaller..."
python3 -m pip install pyinstaller --quiet

# 清理之前的构建
echo "🧹 清理之前的构建文件..."
rm -rf build dist *.spec

# 开始打包
echo "🚀 开始打包..."
python3 -m PyInstaller \
    --onefile \
    --windowed \
    --name "高德地图下载器" \
    --clean \
    --hidden-import tkinter \
    --hidden-import tkinter.ttk \
    --hidden-import tkinter.messagebox \
    --hidden-import tkinter.filedialog \
    --hidden-import requests \
    --hidden-import json \
    --hidden-import pathlib \
    --hidden-import threading \
    --hidden-import urllib.parse \
    --exclude-module matplotlib \
    --exclude-module numpy \
    --exclude-module pandas \
    --exclude-module scipy \
    --exclude-module PIL \
    --exclude-module cv2 \
    map_downloader_gui.py

if [ $? -eq 0 ]; then
    echo "✅ 打包成功!"
    
    # 查找生成的文件
    if [ -f "dist/高德地图下载器" ]; then
        file_size=$(du -h "dist/高德地图下载器" | cut -f1)
        echo "📦 生成的可执行文件: dist/高德地图下载器"
        echo "📏 文件大小: $file_size"
        
        # 移动到当前目录
        mv "dist/高德地图下载器" "./高德地图下载器_$(uname -s)_$(uname -m)"
        echo "✨ 最终文件: ./高德地图下载器_$(uname -s)_$(uname -m)"
        
        # 设置执行权限
        chmod +x "./高德地图下载器_$(uname -s)_$(uname -m)"
        
        echo ""
        echo "🎉 打包完成!"
        echo "💡 提示:"
        echo "   - 可执行文件已生成在当前目录"
        echo "   - 可以直接双击运行"
        echo "   - 首次运行时请输入高德地图API密钥"
    else
        echo "❌ 未找到生成的可执行文件"
    fi
else
    echo "❌ 打包失败"
fi

# 清理临时文件
echo "🧹 清理临时文件..."
rm -rf build *.spec