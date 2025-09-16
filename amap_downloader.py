#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高德地图区域范围图片下载器
用于下载指定区域（如吉州区）的地图图片
"""

import requests
import json
import os
from urllib.parse import quote
import time
from config import AMAP_CONFIG, MAP_SIZES, ZOOM_LEVELS

class AmapDownloader:
    def __init__(self, api_key):
        """
        初始化高德地图下载器
        :param api_key: 高德地图API密钥
        """
        self.api_key = api_key
        self.base_url = "https://restapi.amap.com/v3"
        self.static_map_url = "https://restapi.amap.com/v3/staticmap"
        
    def search_district(self, keywords, subdistrict=1):
        """
        搜索行政区域信息
        :param keywords: 搜索关键词（如"吉州区"）
        :param subdistrict: 子级行政区域级别
        :return: 区域信息
        """
        url = f"{self.base_url}/config/district"
        params = {
            'key': self.api_key,
            'keywords': keywords,
            'subdistrict': subdistrict,
            'extensions': 'all'  # 返回详细信息包括边界坐标
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == '1' and data['districts']:
                return data['districts'][0]
            else:
                print(f"搜索失败: {data.get('info', '未知错误')}")
                return None
                
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            return None
    
    def get_static_map(self, center=None, zoom=None, size="2048*2048", markers=None, paths=None, 
                      map_style="normal", traffic=False, labels=True):
        """
        获取静态地图图片（支持高清大图和多种图层）
        :param center: 地图中心点坐标 "经度,纬度"（有paths时可选）
        :param zoom: 缩放级别 (3-18，推荐10-18获得高清效果)（有paths时可选）
        :param size: 图片尺寸 "宽*高"（支持最大2048*2048高清尺寸）
        :param markers: 标记点
        :param paths: 路径/边界
        :param map_style: 地图样式 ("normal"标准, "satellite"卫星, "roadmap"路网)
        :param traffic: 是否显示实时交通 (True/False)
        :param labels: 是否显示地名标注 (True/False)
        :return: 图片二进制数据
        """
        params = {
            'key': self.api_key,
            'size': size,
            'scale': 2,  # 高清图片（2倍分辨率）
            'format': 'png'  # 使用PNG格式保证图片质量
        }
        
        # 设置地图样式
        if map_style == "satellite":
            params['maptype'] = 'satellite'
        elif map_style == "roadmap":
            params['maptype'] = 'roadmap'
        else:
            params['maptype'] = 'normal'
        
        # 构建图层参数
        layers = []
        if traffic:
            layers.append('traffic')
        if not labels and map_style != "satellite":
            # 卫星图默认不显示标注，其他地图可以控制
            layers.append('nolabel')
        
        if layers:
            params['layers'] = ','.join(layers)
        
        # 根据API文档：有paths时，location和zoom可选，系统会自动计算最佳视图
        if paths:
            params['paths'] = paths
            # 有paths时不设置location和zoom，让系统自动计算包含所有路径的最佳视图
        else:
            # 没有paths时必须指定center和zoom
            if center:
                params['location'] = center
            if zoom:
                params['zoom'] = zoom
        
        # 只添加非空的可选参数
        if markers:
            params['markers'] = markers
        
        # 打印请求URL用于调试
        print(f"请求URL: {self.static_map_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}")
        
        try:
            # 增加超时时间以支持大图片下载
            response = requests.get(self.static_map_url, params=params, timeout=60)
            response.raise_for_status()
            
            if response.headers.get('content-type', '').startswith('image'):
                return response.content
            else:
                print(f"获取地图失败: {response.text}")
                return None
                
        except requests.RequestException as e:
            print(f"请求失败: {e}")
            return None
    
    def download_district_map(self, district_name, output_dir="./maps", map_style="normal", 
                             traffic=False, labels=True):
        """
        下载指定行政区域的地图
        :param district_name: 行政区域名称
        :param output_dir: 输出目录
        :param map_style: 地图样式 ("normal"标准, "satellite"卫星, "roadmap"路网)
        :param traffic: 是否显示实时交通
        :param labels: 是否显示地名标注
        :return: 保存的文件路径
        """
        print(f"正在搜索 {district_name} 的区域信息...")
        
        # 搜索区域信息
        district_info = self.search_district(district_name)
        if not district_info:
            print(f"未找到 {district_name} 的信息")
            return None
        
        print(f"找到区域: {district_info['name']}")
        print(f"行政代码: {district_info['adcode']}")
        print(f"中心坐标: {district_info['center']}")
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        # 获取边界路径数据
        paths = ''
        if 'polyline' in district_info and district_info['polyline']:
            # 高德地图静态地图API的paths参数格式
            # 由于URL长度限制，需要简化边界坐标
            boundary_coords = district_info['polyline']
            coords_list = boundary_coords.split(';')
            
            # 隔位显示坐标点：每隔一个点取一个点（如1,3,5,7...）
            simplified_coords = coords_list[::2]  # 每隔一个点取一个点
            
            # 确保形成完整闭环：最后一个点与首个点一致
            if simplified_coords and simplified_coords[-1] != simplified_coords[0]:
                simplified_coords.append(simplified_coords[0])
            
            # 构建paths参数，格式：pathsStyle:location1;location2...
            # pathsStyle格式：weight,color,transparency,fillcolor,fillTransparency
            if simplified_coords:
                # 使用蓝色边框，粗细为8，完全不透明，无填充
                # 根据高德地图API文档：weight[2,15], color[0x000000-0xffffff], transparency[0,1]
                path_style = "8,0x0000FF,1,,"  # 蓝色(0x0000FF)，粗线条，完全不透明
                path_coords = ';'.join(simplified_coords)
                paths = f"{path_style}:{path_coords}"
                print(f"✅ 已获取边界路径数据，原始 {len(coords_list)} 个点，简化为 {len(simplified_coords)} 个点")
                print(f"Paths参数长度: {len(paths)}")
                print(f"Paths参数: {paths[:200]}...")  # 只显示前200个字符
        else:
            print("⚠️  未找到边界路径数据，将显示无边框地图")
        
        # 下载地图 - 使用自动计算的最佳视图
        saved_files = []
        
        if paths:
            # 有边界数据时，让系统自动计算最佳视图以完整显示边界
            print(f"正在下载自适应视图的高清地图（自动包含完整边界范围）...")
            
            # 获取静态地图 - 不指定center和zoom，让系统自动计算
            map_data = self.get_static_map(
                size=AMAP_CONFIG['default_map_size'],
                paths=paths,
                map_style=map_style,
                traffic=traffic,
                labels=labels
            )
            
            if map_data:
                # 保存图片
                style_suffix = ""
                if map_style != "normal":
                    style_suffix += f"_{map_style}"
                if traffic:
                    style_suffix += "_交通"
                if not labels:
                    style_suffix += "_无标注"
                
                filename = f"{district_name}_高清_完整边界{style_suffix}.png"
                filepath = os.path.join(output_dir, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(map_data)
                
                file_size_mb = len(map_data) / (1024 * 1024)  # MB
                print(f"✅ 已保存高清地图: {filename} ({file_size_mb:.2f} MB)")
                saved_files.append(filepath)
            else:
                print(f"❌ 自适应视图地图下载失败")
        else:
            # 没有边界数据时，使用传统的多级别下载
            zoom_levels = AMAP_CONFIG['default_zoom_levels']
            
            for zoom in zoom_levels:
                zoom_desc = ZOOM_LEVELS.get(zoom, f"级别{zoom}")
                print(f"正在下载缩放级别 {zoom} ({zoom_desc}) 的高清地图...")
                
                # 获取静态地图
                map_data = self.get_static_map(
                    center=district_info['center'],
                    zoom=zoom,
                    size=AMAP_CONFIG['default_map_size'],
                    map_style=map_style,
                    traffic=traffic,
                    labels=labels
                )
                
                if map_data:
                    # 保存图片
                    filename = f"{district_name}_高清_zoom_{zoom}_{zoom_desc}.png"
                    filepath = os.path.join(output_dir, filename)
                    
                    with open(filepath, 'wb') as f:
                        f.write(map_data)
                    
                    file_size_mb = len(map_data) / (1024 * 1024)  # MB
                    print(f"✅ 已保存高清地图: {filename} ({file_size_mb:.2f} MB)")
                    saved_files.append(filepath)
                    
                    # 避免请求过于频繁
                    time.sleep(AMAP_CONFIG['request_delay'])
                else:
                    print(f"❌ 缩放级别 {zoom} 的地图下载失败")
        
        return saved_files

def main():
    # 从配置文件获取API密钥
    API_KEY = AMAP_CONFIG['api_key']
    
    if API_KEY == "YOUR_AMAP_API_KEY_HERE":
        print("请先设置您的高德地图API密钥！")
        print("1. 访问 https://console.amap.com/ 注册并申请API密钥")
        print("2. 在 config.py 文件中将 'YOUR_AMAP_API_KEY_HERE' 替换为您的API密钥")
        print("\n申请步骤:")
        print("   - 注册高德开放平台账号")
        print("   - 创建应用并选择 'Web服务' 平台")
        print("   - 获取API Key")
        return
    
    # 创建下载器实例
    downloader = AmapDownloader(API_KEY)
    
    # 下载吉州区高清地图
    district_name = "吉州区"
    print(f"🗺️  开始下载 {district_name} 的高清大图...")
    print(f"📁 输出目录: {AMAP_CONFIG['default_output_dir']}")
    print(f"📐 地图尺寸: {AMAP_CONFIG['default_map_size']} (高清大图)")
    print(f"🔍 缩放级别: {AMAP_CONFIG['default_zoom_levels']} (详细到建筑物级别)")
    print(f"🎯 图片格式: PNG (无损高质量)")
    print("=" * 60)
    
    saved_files = downloader.download_district_map(
        district_name, 
        output_dir=AMAP_CONFIG['default_output_dir']
    )
    
    if saved_files:
        total_size_mb = sum(os.path.getsize(f) for f in saved_files) / (1024 * 1024)
        print(f"\n🎉 成功下载 {len(saved_files)} 张高清地图 (总计 {total_size_mb:.2f} MB):")
        for file in saved_files:
            file_size_mb = os.path.getsize(file) / (1024 * 1024)  # MB
            filename = os.path.basename(file)
            print(f"  📸 {filename} ({file_size_mb:.2f} MB)")
        print(f"\n📂 所有高清地图已保存到: {os.path.abspath(AMAP_CONFIG['default_output_dir'])}")
        print(f"💡 提示: 这些是 {AMAP_CONFIG['default_map_size']} 分辨率的高清大图，适合打印和详细查看")
    else:
        print("❌ 高清地图下载失败")

if __name__ == "__main__":
    main()