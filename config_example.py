#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件示例
请复制此文件为 config.py 并填入您的API密钥
"""

# 高德地图API配置
AMAP_CONFIG = {
    # 请在此处填入您的高德地图API密钥
    # 申请地址: https://console.amap.com/
    # 示例: 'api_key': 'abcd1234567890abcd1234567890abcd',
    'api_key': 'YOUR_AMAP_API_KEY_HERE',
    
    # 默认地图参数
    'default_zoom_levels': [8, 10, 12, 14],  # 可选范围: 3-18
    'default_map_size': '1024*1024',         # 可选: 512*512, 1024*1024, 2048*2048
    'default_output_dir': './maps',          # 输出目录
    'default_scale': 2,                      # 默认图片清晰度 (1=普通, 2=高清)
    'default_zoom_levels': [8, 10, 12, 14],  # 默认缩放级别组合
    
    # 请求参数
    'request_delay': 0.5,  # 请求间隔（秒），避免频率限制
    'timeout': 30,         # 请求超时时间（秒）
}

# 支持的地图尺寸选项
MAP_SIZES = {
    'small': '512*512',
    'medium': '1024*1024', 
    'large': '2048*2048'
}

# 缩放级别说明（根据高德地图API文档，支持3-18级）
ZOOM_LEVELS = {
    3: {'name': '国家级', 'description': '显示整个国家，适合全国概览'},
    4: {'name': '省级', 'description': '显示省份轮廓，适合省级区域分析'}, 
    5: {'name': '省级', 'description': '显示省份详情，适合大区域规划'},
    6: {'name': '市级', 'description': '显示城市轮廓，适合城市群分析'},
    7: {'name': '市级', 'description': '显示城市详情，适合市级规划'},
    8: {'name': '市级', 'description': '显示城市区域，适合城市概览'},
    9: {'name': '区县级', 'description': '显示区县轮廓，适合区县分析'},
    10: {'name': '区县级', 'description': '显示区县详情，适合区域规划'},
    11: {'name': '区县级', 'description': '显示区县细节，适合详细分析'}, 
    12: {'name': '乡镇级', 'description': '显示乡镇轮廓，适合乡镇规划'},
    13: {'name': '乡镇级', 'description': '显示乡镇详情，适合社区分析'},
    14: {'name': '村庄级', 'description': '显示村庄详情，适合村级规划'},
    15: {'name': '街道级', 'description': '显示街道详情，适合街区分析'},
    16: {'name': '街道级', 'description': '显示街道细节，适合精细规划'},
    17: {'name': '建筑物级', 'description': '显示建筑轮廓，适合建筑分析'},
    18: {'name': '建筑物级', 'description': '显示建筑细节，适合精确定位'}
}

# 推荐的缩放级别组合
RECOMMENDED_ZOOM_COMBINATIONS = {
    'overview': [6, 8, 10],      # 概览模式：城市到区县
    'detailed': [10, 12, 14],    # 详细模式：区县到村庄
    'precision': [14, 16, 18],   # 精确模式：村庄到建筑
    'multi_scale': [8, 12, 16],  # 多尺度：跨级别分析
    'default': [8, 10, 12, 14]   # 默认组合：平衡覆盖
}

# 使用说明:
# 1. 将此文件复制为 config.py
# 2. 在 https://console.amap.com/ 申请API密钥
# 3. 将上面的 'YOUR_AMAP_API_KEY_HERE' 替换为您的真实API密钥
# 4. 根据需要调整其他参数