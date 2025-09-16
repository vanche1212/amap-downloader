# Windows可执行文件打包说明

由于PyInstaller的限制，无法在Mac上直接打包Windows可执行文件。以下提供几种解决方案：

## 方案1：GitHub Actions自动构建（推荐）

### 优点
- ✅ 完全自动化，无需本地环境
- ✅ 同时构建Mac、Windows、Linux版本
- ✅ 支持版本发布管理
- ✅ 免费使用

### 使用步骤
1. 将项目推送到GitHub仓库
2. 创建tag触发自动构建：
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
3. 在GitHub Actions中查看构建进度
4. 下载构建好的可执行文件

### 配置文件
已创建 `.github/workflows/build.yml` 配置文件，包含：
- macOS x86_64 构建
- Windows x86_64 构建  
- Linux x86_64 构建
- 自动发布到GitHub Releases

## 方案2：Docker容器构建

### 优点
- ✅ 可在Mac本地运行
- ✅ 使用Wine模拟Windows环境
- ✅ 一次性构建

### 前置条件
- 安装Docker Desktop for Mac
- 确保Docker服务运行

### 使用步骤
1. 启动Docker Desktop
2. 运行构建脚本：
   ```bash
   ./build_windows_docker.sh
   ```
3. 等待构建完成（首次运行需要下载镜像，约10-15分钟）
4. 在 `dist/` 目录找到生成的Windows可执行文件

### 注意事项
- 首次构建需要下载约2GB的Docker镜像
- 构建时间较长（20-30分钟）
- 需要足够的磁盘空间（至少5GB）

## 方案3：Windows虚拟机或双系统

### 优点
- ✅ 原生Windows环境
- ✅ 构建速度快
- ✅ 兼容性最好

### 使用步骤
1. 在Windows环境中安装Python 3.9
2. 安装项目依赖：
   ```cmd
   pip install -r requirements.txt
   pip install pyinstaller>=5.0
   ```
3. 运行Windows构建脚本：
   ```cmd
   build.bat
   ```

## 方案4：在线构建服务

### 可选服务
- GitHub Codespaces
- GitPod
- Replit

### 使用方法
1. 在在线环境中打开项目
2. 选择Windows环境
3. 运行构建脚本

## 推荐方案

**对于个人开发者**：推荐使用 **GitHub Actions**
- 免费、自动化、支持多平台
- 适合开源项目和版本发布

**对于快速测试**：推荐使用 **Docker方案**
- 可在本地快速构建
- 适合开发阶段测试

**对于频繁开发**：推荐使用 **Windows虚拟机**
- 构建速度最快
- 适合需要频繁调试的场景

## 文件说明

- `.github/workflows/build.yml` - GitHub Actions配置
- `Dockerfile.windows` - Docker构建配置
- `build_windows_docker.sh` - Docker构建脚本
- `build.bat` - Windows原生构建脚本
- `environment.yml` - Conda环境配置

## 常见问题

### Q: Docker构建失败怎么办？
A: 检查Docker Desktop是否正常运行，确保有足够的磁盘空间和内存

### Q: GitHub Actions构建失败？
A: 检查代码是否正确推送，查看Actions日志定位问题

### Q: 生成的exe文件无法运行？
A: 可能缺少Visual C++运行库，建议在目标Windows系统安装Microsoft Visual C++ Redistributable

### Q: 如何减小exe文件大小？
A: 在PyInstaller命令中添加更多 `--exclude-module` 参数排除不需要的库