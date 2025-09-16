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

# 缩放级别说明
ZOOM_LEVELS = {
    3: '国家级',
    4: '省级', 
    5: '省级',
    6: '市级',
    7: '市级',
    8: '市级',
    9: '区县级',
    10: '区县级',
    11: '区县级', 
    12: '乡镇级',
    13: '乡镇级',
    14: '村庄级',
    15: '街道级',
    16: '街道级',
    17: '建筑物级',
    18: '建筑物级'
}

# 使用说明:
# 1. 将此文件复制为 config.py
# 2. 在 https://console.amap.com/ 申请API密钥
# 3. 将上面的 'YOUR_AMAP_API_KEY_HERE' 替换为您的真实API密钥
# 4. 根据需要调整其他参数