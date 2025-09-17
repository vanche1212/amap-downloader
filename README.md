# 高德地图区域范围高清大图下载器

这个工具可以帮助您下载指定行政区域（如吉州区）的高德地图高清大图。

## 🌟 功能特点

- 🗺️ 支持下载任意行政区域的高清地图
- 📏 支持最大2048×2048分辨率的超高清大图
- 🔍 支持10-18级缩放，详细到建筑物级别
- 🎯 自动获取区域边界并在地图上标注
- 💾 批量下载不同缩放级别的高清地图
- 🎨 PNG格式无损高质量输出
- ⚙️ 可配置的参数设置
- 🖥️ 提供图形界面和命令行两种使用方式

## 📋 系统要求

- Python 3.7+
- 稳定的网络连接
- 高德地图API密钥

## 🚀 快速开始

### 1. 安装依赖

```bash
# 使用pip安装
pip install -r requirements.txt

# 或使用conda创建环境（推荐Mac用户）
conda env create -f environment.yml
conda activate amap-downloader
```

### 2. 配置API密钥

1. 访问 [高德开放平台](https://console.amap.com/) 注册账号
2. 创建应用并选择 "Web服务" 平台
3. 获取API Key（参考 [高德官方接口文档](https://amap.apifox.cn/doc-540142)）
4. 编辑 `config.py` 文件，将 `YOUR_AMAP_API_KEY_HERE` 替换为您的API密钥

```python
AMAP_CONFIG = {
    'api_key': '您的API密钥',  # 替换这里
    # ... 其他配置
}
```

**注意**：如果您是首次使用，可以参考 `config_example.py` 文件中的配置示例。

### 3. 运行程序

**图形界面版本（推荐）**：
```bash
python map_downloader_gui.py
```

**命令行版本**：
```bash
python amap_downloader.py
```

**macOS用户特别说明**：
如果您下载的是GitHub Actions构建的macOS可执行文件，请根据您的Mac类型选择对应版本：

**Intel Mac用户**：
```bash
# 下载 amap-downloader_macOS_Intel 文件后
chmod +x amap-downloader_macOS_Intel
xattr -d com.apple.quarantine amap-downloader_macOS_Intel
./amap-downloader_macOS_Intel
```

**Apple Silicon Mac用户**：
```bash
# 下载 amap-downloader_macOS_AppleSilicon 文件后
chmod +x amap-downloader_macOS_AppleSilicon
xattr -d com.apple.quarantine amap-downloader_macOS_AppleSilicon
./amap-downloader_macOS_AppleSilicon
```

**如何确定您的Mac类型**：
- 点击左上角苹果菜单 → "关于本机"
- 如果显示"Intel"处理器，选择Intel版本
- 如果显示"Apple M1/M2/M3"处理器，选择Apple Silicon版本

## 📖 详细使用说明

### 图形界面使用

1. 运行 `python map_downloader_gui.py`
2. 在界面中输入要下载的区域名称（如：吉州区）
3. 选择缩放级别和输出目录
4. 点击"开始下载"按钮

### 命令行使用

```bash
python amap_downloader.py
```

默认会下载吉州区的地图到 `./maps` 目录。

### 自定义配置

您可以修改 `config.py` 文件来自定义：

- **缩放级别**: `default_zoom_levels` - 控制地图的详细程度
- **地图尺寸**: `default_map_size` - 控制图片分辨率
- **输出目录**: `default_output_dir` - 设置保存位置
- **请求间隔**: `request_delay` - 避免请求过于频繁

### 🔍 高清缩放级别说明

| 级别 | 显示范围 | 适用场景 | 推荐用途 |
|------|----------|----------|----------|
| 10   | 区县级   | 区域概览 | 行政区域全貌 |
| 12   | 乡镇级   | 街道布局 | 道路网络分析 |
| 14   | 村庄级   | 详细街道 | 城市规划参考 |
| 16   | 街道级   | 建筑轮廓 | 精细地理分析 |

**💡 高清优势**: 2048×2048分辨率 + 2倍缩放 = 超过400万像素的极致清晰度！

## 📸 输出文件

程序会为每个缩放级别生成一张高清地图图片：

```
maps/
├── 吉州区_高清_zoom_10_区县级.png   # 区域概览 (约2-4MB)
├── 吉州区_高清_zoom_12_乡镇级.png   # 街道布局 (约3-5MB)
├── 吉州区_高清_zoom_14_村庄级.png   # 详细街道 (约4-6MB)
└── 吉州区_高清_zoom_16_街道级.png   # 建筑轮廓 (约5-8MB)
```

**🎯 文件特点**:
- 分辨率: 2048×2048像素
- 格式: PNG无损压缩
- 质量: 2倍高清缩放
- 大小: 单张2-8MB（根据地图复杂度）

## ⚠️ 注意事项

1. **API限制**: 高德地图API有调用频率限制，请合理使用
2. **网络连接**: 需要稳定的网络连接来下载地图数据
3. **存储空间**: 高分辨率地图文件较大，请确保有足够存储空间
4. **API配额**: 免费API有每日调用次数限制

## 🔧 故障排除

### 常见问题

**Q: 提示API密钥错误**
A: 请检查config.py中的API密钥是否正确设置

**Q: 下载失败或图片为空**
A: 可能是网络问题或API配额用完，请稍后重试

**Q: 找不到指定区域**
A: 请确认区域名称正确，可以尝试使用完整名称如"江西省吉安市吉州区"

**Q: 地图没有边界线**
A: 部分区域可能没有详细的边界数据，这是正常现象

**Q: macOS提示"无法打开应用程序"或"来自身份不明开发者"**
A: 这是macOS的安全机制，请使用以下方法解决：
1. 在终端中运行：`xattr -d com.apple.quarantine 可执行文件名`
2. 或在系统偏好设置 > 安全性与隐私 > 通用 中点击"仍要打开"

**Q: macOS可执行文件没有执行权限**
A: 在终端中运行：`chmod +x 可执行文件名`

**Q: macOS提示"bad CPU type in executable"或"cannot execute binary file"**
A: 这是架构不匹配问题，请确保下载了正确的版本：
- Intel Mac用户：下载 `amap-downloader_macOS_Intel`
- Apple Silicon Mac用户：下载 `amap-downloader_macOS_AppleSilicon`
- 可通过"关于本机"查看您的Mac处理器类型

## 📚 参考资源

- [高德开放平台](https://console.amap.com/)
- [高德地图API官方文档](https://amap.apifox.cn/doc-540142)
- [静态地图服务说明](https://amap.apifox.cn/doc-540142)

## 📦 项目结构

```
amap-downloader/
├── map_downloader_gui.py    # 图形界面版本
├── amap_downloader.py       # 命令行版本
├── config_example.py        # 配置文件示例
├── requirements.txt         # Python依赖
├── environment.yml          # Conda环境配置
├── 使用说明.md              # 详细使用说明
└── README.md               # 项目说明
```

## 📝 更新日志

### v1.0.10 (2024-12-17)
- 🏗️ 修复GitHub Actions构建配置，解决macOS架构不匹配问题
- 🍎 分别为Intel Mac和Apple Silicon Mac构建专用版本
- 📦 更新文件命名：`amap-downloader_macOS_Intel` 和 `amap-downloader_macOS_AppleSilicon`
- 🔧 添加PyInstaller的`--target-arch`参数，确保正确的架构编译
- 📚 完善README文档，详细说明不同Mac架构的下载和使用方法
- 🐛 修复"bad CPU type in executable"和"cannot execute binary file"错误

### v1.0.9 (2024-12-16)
- 🍎 修复macOS版本可执行文件的权限和安全问题
- 🔧 优化GitHub Actions构建配置，为macOS添加特殊处理
- 📝 添加macOS运行脚本 `run_macos.sh`，自动处理权限设置
- 🛡️ 增加macOS代码签名和隔离属性处理
- 📚 完善macOS用户使用说明和故障排除指南
- 🔗 添加SSL/TLS相关依赖，提高网络请求稳定性

### v1.0.8 (2024-12-16)
- 🔧 修复缩放级别问题，确保不同级别生成不同详细程度的地图
- 🎯 优化默认配置，移除不必要的18级缩放
- 📊 调整地图分辨率为2048×2048，平衡质量和文件大小
- 🛠️ 改进API调用逻辑，支持边界显示的同时指定缩放级别
- 🐛 修复macOS系统UI警告问题
- ✅ 增强输入验证，防止无效区域名称导致的搜索失败

## 📄 许可证

本项目仅供学习和个人使用，请遵守高德地图API的使用条款。