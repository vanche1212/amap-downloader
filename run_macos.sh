#!/bin/bash

# macOS运行脚本 - 高德地图下载器
# 此脚本用于解决macOS系统上的权限和安全问题

echo "=== 高德地图下载器 macOS 启动脚本 ==="
echo ""

# 检查可执行文件是否存在
if [ ! -f "amap-downloader_macOS_x86_64" ]; then
    echo "❌ 错误：未找到可执行文件 'amap-downloader_macOS_x86_64'"
    echo "请确保已下载正确的macOS版本文件"
    exit 1
fi

echo "✅ 找到可执行文件"

# 设置执行权限
echo "🔧 设置执行权限..."
chmod +x amap-downloader_macOS_x86_64

# 检查是否需要移除隔离属性（macOS Gatekeeper）
echo "🔓 移除macOS隔离属性..."
xattr -d com.apple.quarantine amap-downloader_macOS_x86_64 2>/dev/null || true

echo "🚀 启动高德地图下载器..."
echo ""

# 启动应用程序
./amap-downloader_macOS_x86_64

echo ""
echo "=== 应用程序已退出 ==="