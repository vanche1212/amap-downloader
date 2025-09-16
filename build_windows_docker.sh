#!/bin/bash

# 高德地图下载器 - Windows版本Docker构建脚本
# 在Mac上使用Docker构建Windows可执行文件

echo "🐳 使用Docker构建Windows可执行文件..."

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker Desktop"
    echo "下载地址: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# 检查Docker是否运行
if ! docker info &> /dev/null; then
    echo "❌ Docker未运行，请启动Docker Desktop"
    exit 1
fi

echo "✅ Docker环境检查通过"

# 构建Docker镜像
echo "🔨 构建Docker镜像..."
docker build -f Dockerfile.windows -t amap-downloader-windows .

if [ $? -ne 0 ]; then
    echo "❌ Docker镜像构建失败"
    exit 1
fi

echo "✅ Docker镜像构建成功"

# 运行容器并构建Windows可执行文件
echo "🚀 在容器中构建Windows可执行文件..."
docker run --rm -v "$(pwd)/dist:/app/dist" amap-downloader-windows

if [ $? -eq 0 ]; then
    echo "✅ Windows可执行文件构建成功!"
    echo "📦 输出文件: $(pwd)/dist/高德地图下载器_Windows_x86_64.exe"
    
    # 检查文件是否存在
    if [ -f "dist/高德地图下载器_Windows_x86_64.exe" ]; then
        file_size=$(du -h "dist/高德地图下载器_Windows_x86_64.exe" | cut -f1)
        echo "📏 文件大小: $file_size"
        echo ""
        echo "🎉 构建完成! 现在您有了:"
        echo "   - macOS版本: 高德地图下载器_macOS_x86_64"
        echo "   - Windows版本: dist/高德地图下载器_Windows_x86_64.exe"
    else
        echo "❌ 未找到生成的Windows可执行文件"
        exit 1
    fi
else
    echo "❌ Windows可执行文件构建失败"
    exit 1
fi