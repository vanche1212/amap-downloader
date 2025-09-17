# 高德地图区域范围高清大图下载器

这个工具可以帮助您下载指定行政区域（如吉州区）的高德地图高清大图。

## 🌟 功能特点

- 🗺️ 支持下载任意行政区域的高清地图
- 📏 支持最大1024×1024分辨率的高清大图
- 🔍 支持区县级别(10级)和乡镇级别(12级)两个实用缩放级别
- 🎯 自动获取区域边界并在地图上标注（红色边框+半透明填充）
- 💾 批量下载不同缩放级别的高清地图
- 🎨 PNG格式无损高质量输出
- ⚙️ 可配置的参数设置
- 🖥️ 提供简洁易用的图形界面和命令行两种使用方式
- 🎛️ 图形界面简化设计，专注核心功能，操作更便捷
- 📐 严格遵循高德地图API文档规范
- ✨ **高清图支持**：支持普通清晰度(scale=1)和高清晰度(scale=2)两种模式，可配置默认清晰度
- 🎚️ **灵活缩放级别配置**：提供多种预设缩放级别组合，支持自定义缩放级别，满足不同使用场景需求
- 🎯 **GUI界面Zoom控制**：图形界面支持默认级别和自定义级别两种模式，用户可直接在界面中控制缩放级别

## 📋 系统要求

- Python 3.7+
- 稳定的网络连接
- 高德地图API密钥
- PIL/Pillow库（用于图片处理）

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
2. 输入高德地图API密钥
3. 输入要下载的区域名称（如：吉州区）
4. 选择输出目录
5. **🆕 选择Zoom级别**：
   - **使用默认级别**：使用系统推荐的缩放级别组合
   - **自定义级别**：手动输入缩放级别，用逗号分隔（如：8,10,12）
6. 点击"开始下载"按钮

#### 🎯 缩放级别预设选项

| 预设名称 | 缩放级别 | 说明 | 适用场景 |
|----------|----------|------|----------|
| 概览级别 | [8,10] | 市级+区县级 | 大区域概览，城市规划 |
| **默认级别** | [10,12] | 区县级+乡镇级 | 平衡详细度和覆盖范围（推荐） |
| 详细级别 | [12,14] | 乡镇级+村庄级 | 详细街道信息，精细分析 |
| 街道级别 | [14,16] | 村庄级+街道级 | 街道细节，建筑分布 |
| 建筑级别 | [16,18] | 街道级+建筑物级 | 最高精度，建筑物级别 |
| 单一概览 | [8] | 仅市级 | 快速概览，单张图片 |
| 单一区县 | [10] | 仅区县级 | 区县边界清晰显示 |
| 单一乡镇 | [12] | 仅乡镇级 | 乡镇街道详细信息 |
| 大范围 | [6,8,10] | 市级多层次 | 多层次大范围覆盖 |
| 全详细 | [10,12,14,16] | 区县到街道 | 最全面的多级别覆盖 |

**💡 推荐**：首次使用建议选择"默认级别"，可获得最佳的详细度和覆盖范围平衡。



### 命令行使用

```bash
python amap_downloader.py
```

默认会下载吉州区的地图到 `./maps` 目录，使用默认缩放级别 [10,12]。

#### 🔧 编程接口使用

如果您需要在代码中自定义缩放级别，可以这样使用：

```python
from amap_downloader import AmapDownloader
from config import ZOOM_PRESETS

# 创建下载器（自动使用配置文件中的默认清晰度）
downloader = AmapDownloader("您的API密钥")

# 🆕 使用推荐的缩放级别组合
overview_levels = downloader.get_recommended_zoom_levels('overview')    # [6, 8, 10]
detailed_levels = downloader.get_recommended_zoom_levels('detailed')    # [10, 12, 14]
precision_levels = downloader.get_recommended_zoom_levels('precision')  # [14, 16, 18]

# 🆕 获取缩放级别详细信息
zoom_info = downloader.get_zoom_level_info(12)
print(f"缩放级别12: {zoom_info['name']} - {zoom_info['description']}")

# 使用预设缩放级别
zoom_levels = ZOOM_PRESETS['detailed']  # [12, 14]
result = downloader.download_district_map("吉州区", "./maps", zoom_levels=zoom_levels)

# 或者自定义缩放级别
custom_zoom_levels = [8, 10, 12, 14]
result = downloader.download_district_map("吉州区", "./maps", zoom_levels=custom_zoom_levels)

# ✨ 控制图片清晰度
result = downloader.download_district_map("吉州区", "./maps", 
                                        zoom_levels=[12], 
                                        scale=1)  # 普通清晰度
result = downloader.download_district_map("吉州区", "./maps", 
                                        zoom_levels=[12], 
                                        scale=2)  # 高清晰度（默认）

# 控制边界显示
result = downloader.download_district_map("吉州区", "./maps", 
                                        zoom_levels=[12], 
                                        show_boundary=True)   # 显示边界
result = downloader.download_district_map("吉州区", "./maps", 
                                        zoom_levels=[12], 
                                        show_boundary=False)  # 不显示边界

# 控制坐标简化间隔（解决坐标点过多问题）
result = downloader.download_district_map("吉州区", "./maps", 
                                        zoom_levels=[12], 
                                        boundary_simplify_step=2)  # 默认间隔
result = downloader.download_district_map("复杂区域", "./maps", 
                                        zoom_levels=[12], 
                                        boundary_simplify_step=3)  # 更大间隔，适合复杂边界



# 下载指定区域地图
result = downloader.download_district("吉州区", "./maps", 
                                     zoom_levels=[12])
```

### 自定义配置

您可以修改 `config.py` 文件来自定义：

- **缩放级别**: `default_zoom_levels` - 控制地图的详细程度
- **地图尺寸**: `default_map_size` - 控制图片分辨率
- **输出目录**: `default_output_dir` - 设置保存位置
- **请求间隔**: `request_delay` - 避免请求过于频繁
- **默认清晰度**: `default_scale` - 设置默认图片清晰度（1=普通，2=高清）
- **推荐缩放组合**: `RECOMMENDED_ZOOM_COMBINATIONS` - 预设的缩放级别组合，适用于不同场景

#### 🎚️ 缩放级别组合配置

程序提供了多种预设的缩放级别组合，您可以根据需要选择：

```python
RECOMMENDED_ZOOM_COMBINATIONS = {
    'overview': [6, 8, 10],      # 概览模式：城市到区县级别
    'detailed': [10, 12, 14],    # 详细模式：区县到村庄级别
    'precision': [14, 16, 18],   # 精确模式：村庄到建筑级别
    'multi_scale': [8, 12, 16],  # 多尺度模式：跨级别分析
    'default': [8, 10, 12, 14]   # 默认组合：平衡覆盖
}
```

#### ✨ 高清图配置

```python
AMAP_CONFIG = {
    'default_scale': 2,  # 默认使用高清模式
    # 1 = 普通清晰度（512×512像素）
    # 2 = 高清晰度（1024×1024像素，推荐）
}
```

### 🔍 缩放级别说明

| 级别 | 显示范围 | 适用场景 | 推荐用途 |
|------|----------|----------|----------|
| 10   | 区县级   | 区域概览 | 行政区域全貌，整体规划 |
| 12   | 乡镇级   | 街道布局 | 道路网络分析，详细地理信息 |

**💡 优势**: 1024×1024分辨率，平衡了图片质量和文件大小，符合高德地图API规范！

## 📸 输出文件

程序会为每个缩放级别生成一张高清地图图片，文件名包含缩放级别和对应的行政级别：

**默认级别 [10,12] 输出示例**：
```
maps/
├── 吉州区_Z10.png   # 区域概览 (约1-2MB)
└── 吉州区_Z12.png   # 街道布局 (约1.5-3MB)
```

**详细级别 [12,14] 输出示例**：
```
maps/
├── 吉州区_Z12.png   # 乡镇街道 (约1.5-3MB)
└── 吉州区_Z14.png   # 村庄详情 (约2-4MB)
```

**建筑级别 [16,18] 输出示例**：
```
maps/
├── 吉州区_Z16.png   # 街道细节 (约3-5MB)
└── 吉州区_Z18.png # 建筑物级 (约4-6MB)
```

**🎯 文件特点**:
- 分辨率: 1024×1024像素
- 格式: PNG无损压缩
- 边界标注: 红色边框+半透明填充
- 大小: 1-6MB（根据缩放级别和地图复杂度）
- 命名规则: `区域名_Z级别.png` (如: 吉州区_Z12.png)



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

### v1.1.2 (2024-12-17)
- 🔧 **构建修复**：修复GitHub Actions构建配置中PIL模块缺失问题
- 📦 **依赖优化**：确保所有平台的可执行文件正确包含PIL图像处理库
- 🧹 **项目清理**：移除不再需要的macOS运行脚本文件
- 📚 **文档维护**：更新README文档，移除过时的脚本引用
- ✅ **质量保证**：通过本地测试验证构建产物的正确性

### v1.1.1 (2024-12-17)
- 🎨 **界面优化**：移除GUI界面上的下载模式选择功能，简化用户操作
- 📝 **文件命名优化**：简化下载文件的命名格式，使其更简洁易读（如：`吉州区_Z12.png`）
- 💬 **提示信息简化**：优化下载成功的提示信息，减少冗余信息
- 🎯 **边界线功能**：确保图片边界线功能正常工作，默认开启边界显示
- 📚 **文档更新**：更新README.md中的命名示例和使用说明

### v1.1.0 (2024-12-17)
- 🎨 **GUI界面增强**：优化用户界面，提升操作体验
- 📚 **文档完善**：更新使用说明和配置指南
- 🔧 **依赖更新**：优化项目依赖，提升兼容性
- ⚡ **性能优化**：提升下载速度和稳定性

### v1.0.20 (2024-12-17)
- 🐛 **修复字符串索引错误**：解决了"string indices must be integers"的运行时错误
- 🔧 **完善返回值格式**：修正calculate_tile_boundary_paths方法的返回值格式，确保返回正确的字典结构
- ✅ **提升代码稳定性**：增强边界计算逻辑的健壮性，避免类型错误

### v1.0.19 (2024-12-17)
- 🔧 **修复边界重合问题**：解决了边界范围经纬度不重合的问题
- 🎯 **优化边界计算**：改进边界路径计算逻辑，避免边界线断裂
- 📐 **改进坐标处理逻辑**：优化坐标计算方法，精确计算边界点
- ✅ **完善显示算法**：确保边界线正确显示，提升大区域地图的显示质量

### v1.0.18 (2024-12-17)
- 🎨 **优化边界线样式**：将边界线宽度从3像素增加到5像素，提升视觉效果
- 🔵 **更改边界线颜色**：将边界线颜色从红色(0xFF0000)改为蓝色(0x0066FF)，更加美观
- ✨ **提升显示效果**：边界线更加清晰醒目，便于区域识别

### v1.0.17 (2024-12-17)
- 🧩 **优化边界坐标一致性**：确保所有地图使用相同的边界坐标参数，实现完美的边界重合
- ✅ **验证边界功能**：测试并确认多种场景下边界显示正常
- 🎯 **完善边界逻辑**：统一paths参数，避免边界线位置偏差
- 📐 **测试复杂区域**：验证东城区、丰台区等不同大小区域的边界显示效果

### v1.0.16 (2024-12-17)
- 🔧 **修复paths参数格式**：使用正确的高德地图API paths参数格式（weight,color,transparency,fillcolor,fillTransparency）
- ✅ **解决边界显示问题**：完全修复边界显示功能，现在可以正常显示区域边界
- 🎯 **优化URL长度控制**：将URL长度限制调整为2000字符，确保API稳定性
- 📐 **完善动态简化**：智能调整坐标简化间隔，平衡显示效果和API兼容性
- 🧪 **增强测试验证**：添加paths参数格式验证，确保API调用成功
- 🎨 **改进边界样式**：使用3像素红色边框，提供清晰的区域边界显示

### v1.0.15 (2024-12-17)
- 🐛 **修复API错误20003**：解决"UNKNOWN_ERROR"导致的地图下载失败问题
- 📏 **增强URL长度检查**：动态调整坐标简化间隔，确保URL不超过高德地图API限制
- 🔍 **智能坐标简化**：自动检测边界复杂度，动态调整简化间隔（2-20）
- 🛠️ **改进错误处理**：添加详细的错误码解析和解决建议
- 📊 **增强调试信息**：显示URL长度、坐标点数、简化过程等详细信息
- ⚡ **性能优化**：对于过于复杂的边界自动禁用边界显示，确保下载成功
- 💡 **用户友好**：提供针对性的错误解决建议和操作指导

### v1.0.14 (2024-12-17)
- 🧠 **智能边界分析**：新增区域边界数据分析功能，自动计算最佳地图中心点和覆盖范围
- 📐 **动态尺寸调整**：根据区域实际大小智能推荐最佳缩放级别和地图尺寸
- 🎯 **精确覆盖策略**：确保完整覆盖目标区域，避免边缘遗漏
- ⚡ **性能优化**：智能判断下载策略，提高效率
- 🔍 **详细进度显示**：显示下载进度和状态
- 📊 **覆盖范围计算**：基于地理坐标精确计算区域跨度和最佳参数

### v1.0.14 (2024-12-17)
- 🐛 **修复智能扩展下载错误**：解决 "'NoneType' object is not subscriptable" 运行时错误
- 🛡️ **增强空值检查**：在 download_by_expansion 方法中添加 grid_info 空值验证
- 🔧 **完善参数验证**：在 analyze_tile_regions 方法中添加网格信息有效性检查
- ⚡ **提升稳定性**：在 _download_by_priority 方法中添加 regions 空值保护
- 🎯 **优化错误处理**：提供更清晰的错误提示信息，便于问题定位
- ✅ **验证修复效果**：确保智能扩展下载功能稳定运行

### v1.0.13 (2024-12-17)
- 🐛 修复GUI界面缩放级别选择器初始化错误
- 🔧 解决"list indices must be integers or slices, not str"运行时错误
- ⚡ 优化下拉菜单选项生成逻辑，确保界面稳定运行
- 🎯 完善标签到键名的映射机制，提高代码健壮性
- ✅ 验证所有缩放级别预设功能正常工作

### v1.0.12 (2024-12-17)
- 🎯 **新增缩放级别参数功能**：支持自定义缩放级别，解决乡镇级别图片不完整问题
- 🎨 **GUI界面增强**：添加缩放级别选择下拉菜单，提供10种预设选项
- ⚙️ **配置文件扩展**：新增ZOOM_PRESETS配置，包含概览、默认、详细等多种缩放级别组合
- 🔧 **编程接口优化**：download_district_map方法支持zoom_levels参数
- 🐛 **修复GUI错误**：解决缩放级别选择时的"list indices must be integers"错误
- 📚 **文档完善**：更新README，详细说明缩放级别预设选项和使用方法

### v1.0.13 (2024-12-17)
- 🐛 修复GUI中的NoneType错误，正确处理download_district_map返回值
- 🛡️ 增强错误处理机制，添加API密钥、区域名称、输出目录的验证
- 🔧 修复中心扩展下载器的参数传递问题，支持地图样式参数
- ✅ 改进下载结果处理逻辑，区分普通模式和中心扩展模式的返回值
- 🎯 优化用户体验，提供更清晰的错误提示和状态反馈
- 📊 完善下载完成后的信息显示，显示保存的文件数量

### v1.0.12 (2024-12-17)
- 🔧 修复map_style等变量未定义错误，添加默认参数设置
- ✨ 优化用户界面，专注于核心下载功能
- 🎯 专注核心功能：API密钥、区域名称、输出目录三个基本设置
- ⚡ 自动使用最优默认配置，提升用户体验和操作便捷性
- 🧹 清理冗余代码，提高程序运行效率
- 📚 更新使用说明，反映界面简化后的操作流程

### v1.0.11 (2024-12-17)
- 🎛️ 简化图形界面设计，移除复杂的下载选项配置
- 🔧 修复线程中调用GUI组件的错误，提升应用稳定性
- 🐛 修复lambda函数中变量作用域问题，解决运行时错误
- 📐 根据高德地图API文档修正静态地图API参数格式
- 🔍 优化缩放级别设置，只保留区县级别(10级)和乡镇级别(12级)两个实用级别
- 🎨 改进边界显示效果：红色边框+半透明填充，更加美观
- 📏 调整默认地图尺寸为1024×1024，符合API规范并平衡质量与文件大小
- 🛠️ 简化paths参数构建逻辑，提高API调用成功率
- 📚 更新文档说明，反映最新的功能特点和使用方法

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