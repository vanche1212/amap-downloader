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
import math
from PIL import Image
import io
from config import AMAP_CONFIG, MAP_SIZES, ZOOM_LEVELS, RECOMMENDED_ZOOM_COMBINATIONS

class AmapDownloader:
    def __init__(self, api_key=None, default_scale=None):
        """
        初始化高德地图下载器
        
        Args:
            api_key (str, optional): 高德地图API密钥
            default_scale (int, optional): 默认图片清晰度 (1=普通, 2=高清)
        """
        self.api_key = api_key or AMAP_CONFIG.get('api_key', 'YOUR_AMAP_API_KEY_HERE')
        self.default_scale = default_scale or AMAP_CONFIG.get('default_scale', 2)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # 缺失区域检测
        self.missing_regions = []
        self.downloaded_regions = []
        self.base_url = "https://restapi.amap.com/v3"
        self.static_map_url = "https://restapi.amap.com/v3/staticmap"
    
    def get_recommended_zoom_levels(self, mode='default'):
        """
        获取推荐的缩放级别组合
        
        Args:
            mode (str): 模式选择
                - 'overview': 概览模式，适合城市到区县级别
                - 'detailed': 详细模式，适合区县到村庄级别  
                - 'precision': 精确模式，适合村庄到建筑级别
                - 'multi_scale': 多尺度模式，跨级别分析
                - 'default': 默认组合，平衡覆盖
                
        Returns:
            list: 推荐的缩放级别列表
        """
        return RECOMMENDED_ZOOM_COMBINATIONS.get(mode, AMAP_CONFIG.get('default_zoom_levels', [8, 10, 12, 14]))
    
    def get_zoom_level_info(self, zoom_level):
        """
        获取缩放级别的详细信息
        
        Args:
            zoom_level (int): 缩放级别 (3-18)
            
        Returns:
            dict: 包含名称和描述的字典
        """
        if zoom_level in ZOOM_LEVELS:
            return ZOOM_LEVELS[zoom_level]
        else:
            return {'name': f'级别{zoom_level}', 'description': '自定义缩放级别'}
    
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
    
    def analyze_boundary(self, polyline):
        """
        分析区域边界数据，计算最佳地图中心点和覆盖范围
        :param polyline: 边界坐标字符串，格式：'lng1,lat1;lng2,lat2;...'
        :return: dict包含center, bounds, optimal_zoom等信息
        """
        if not polyline:
            return None
            
        coords_list = polyline.split(';')
        if len(coords_list) < 3:
            return None
            
        # 解析坐标点
        lngs, lats = [], []
        for coord in coords_list:
            try:
                lng, lat = map(float, coord.split(','))
                lngs.append(lng)
                lats.append(lat)
            except (ValueError, IndexError):
                continue
                
        if not lngs or not lats:
            return None
            
        # 计算边界框
        min_lng, max_lng = min(lngs), max(lngs)
        min_lat, max_lat = min(lats), max(lats)
        
        # 计算几何中心点
        center_lng = (min_lng + max_lng) / 2
        center_lat = (min_lat + max_lat) / 2
        
        # 计算区域跨度（度数）
        lng_span = max_lng - min_lng
        lat_span = max_lat - min_lat
        
        # 计算实际距离跨度（公里）
        # 纬度1度约111公里，经度1度在不同纬度下距离不同
        lat_distance = lat_span * 111.0
        lng_distance = lng_span * 111.0 * math.cos(math.radians(center_lat))
        
        # 计算最大跨度
        max_distance = max(lat_distance, lng_distance)
        
        # 根据跨度推荐最佳缩放级别
        # 高德地图缩放级别与覆盖范围的大致对应关系
        if max_distance > 200:
            optimal_zoom = [6, 8]  # 大范围：省市级别
        elif max_distance > 100:
            optimal_zoom = [8, 10]  # 中等范围：市区级别
        elif max_distance > 50:
            optimal_zoom = [10, 12]  # 区县级别
        elif max_distance > 20:
            optimal_zoom = [12, 14]  # 乡镇级别
        elif max_distance > 10:
            optimal_zoom = [14, 16]  # 街道级别
        else:
            optimal_zoom = [16, 18]  # 建筑级别
            
        # 计算推荐的地图尺寸
        # 根据区域复杂度和跨度确定最佳尺寸
        if max_distance > 100 or len(coords_list) > 1000:
            recommended_size = "2048*2048"  # 大区域或复杂边界用高分辨率
        elif max_distance > 20 or len(coords_list) > 500:
            recommended_size = "1024*1024"  # 中等区域用标准分辨率
        else:
            recommended_size = "512*512"   # 小区域用较低分辨率
            
        return {
             'center': f"{center_lng},{center_lat}",
             'bounds': {
                 'min_lng': min_lng,
                 'max_lng': max_lng,
                 'min_lat': min_lat,
                 'max_lat': max_lat
             },
             'span': {
                 'lng_span': lng_span,
                 'lat_span': lat_span,
                 'lng_distance_km': lng_distance,
                 'lat_distance_km': lat_distance,
                 'max_distance_km': max_distance
             },
             'optimal_zoom': optimal_zoom,
             'recommended_size': recommended_size,
             'boundary_complexity': len(coords_list)
         }
    

    





    
    def get_static_map(self, center=None, zoom=None, size="1024*1024", markers=None, paths=None, 
                      map_style="normal", traffic=False, labels=True, scale=None):
        """
        获取静态地图图片（根据高德地图API文档规范）
        :param center: 地图中心点坐标 "经度,纬度"（有paths时可选）
        :param zoom: 缩放级别 (3-18)（有paths时可选）
        :param size: 图片尺寸 "宽*高"（最大1024*1024，scale=2时最大512*512）
        :param markers: 标记点
        :param paths: 路径/边界，格式：pathsStyle:location1;location2..
        :param map_style: 地图样式 ("normal"标准, "satellite"卫星, "roadmap"路网)
        :param traffic: 是否显示实时交通 (True/False)
        :param labels: 是否显示地名标注 (True/False)
        :param scale: 图片清晰度 (1=普通, 2=高清)，高清图片实际像素为size的2倍
        :return: 图片二进制数据
        """
        # 使用默认scale值如果未指定
        if scale is None:
            scale = self.default_scale
            
        params = {
            'key': self.api_key,
            'size': size,
            'scale': scale
        }
        
        # 根据API文档，有paths时location和zoom可选填
        # 当请求中无location值时，地图区域以包含所有paths的几何中心为中心点
        # 当请求中无zoom时，系统会计算出合适的zoom值以包含所有paths
        if paths:
            params['paths'] = paths
        
        # 如果明确指定了center和zoom，则使用指定值
        if center:
            params['location'] = center
        if zoom:
            params['zoom'] = zoom
        
        # 只添加非空的可选参数
        if markers:
            params['markers'] = markers
        
        # 构建完整URL用于调试
        full_url = f"{self.static_map_url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
        print(f"请求URL长度: {len(full_url)} 字符")
        print(f"请求URL: {full_url[:500]}...")  # 只显示前500个字符
        
        # 检查URL长度
        if len(full_url) > 8192:
            print(f"❌ URL过长 ({len(full_url)} 字符)，超过高德地图API限制 (8192 字符)")
            return None
        
        try:
            # 增加超时时间以支持大图片下载
            response = requests.get(self.static_map_url, params=params, timeout=60)
            
            # 打印响应状态
            print(f"HTTP状态码: {response.status_code}")
            print(f"响应头Content-Type: {response.headers.get('content-type', 'unknown')}")
            
            response.raise_for_status()
            
            if response.headers.get('content-type', '').startswith('image'):
                print(f"✅ 成功获取地图图片，大小: {len(response.content)} 字节")
                return response.content
            else:
                # 尝试解析JSON错误信息
                try:
                    error_data = response.json()
                    error_code = error_data.get('infocode', 'unknown')
                    error_info = error_data.get('info', 'unknown')
                    print(f"❌ 获取地图失败:")
                    print(f"   错误码: {error_code}")
                    print(f"   错误信息: {error_info}")
                    print(f"   完整响应: {response.text}")
                    
                    # 根据错误码提供解决建议
                    if error_code == "20003":
                        print(f"💡 错误码20003解决建议:")
                        print(f"   1. 检查API密钥是否正确")
                        print(f"   2. 检查请求参数是否符合规范")
                        print(f"   3. 尝试简化边界坐标或禁用边界显示")
                        print(f"   4. 检查网络连接")
                except:
                    print(f"❌ 获取地图失败: {response.text}")
                return None
                
        except requests.RequestException as e:
            print(f"❌ 网络请求失败: {e}")
            return None
    
    def _download_single_tile(self, center, zoom_level, map_style="normal", traffic=False, labels=True, scale=None):
        """
        下载单个瓦片
        
        Args:
            center: 瓦片中心点坐标 [经度, 纬度] 或 "经度,纬度"
            zoom_level: 缩放级别
            map_style: 地图样式
            traffic: 是否显示交通信息
            labels: 是否显示标签
            scale: 图片清晰度 (1=普通, 2=高清)
            
        Returns:
            bytes: 图片二进制数据，失败时返回None
        """
        # 确保center是字符串格式
        if isinstance(center, list):
            center_str = f"{center[0]},{center[1]}"
        else:
            center_str = center
            
        return self.get_static_map(
            center=center_str,
            zoom=zoom_level,
            size="1024*1024",
            map_style=map_style,
            traffic=traffic,
            labels=labels,
            scale=scale
        )
    
    def download_district_map_single(self, district_name, output_dir="./maps", 
                                   map_style="normal", traffic=False, labels=True, 
                                   boundary_simplify_step=2, max_size="2048*2048", scale=None):
        """
        基于边界范围的单图下载方法（推荐）
        利用高德地图静态API的paths参数，一次性获取完整区域的高分辨率图片
        
        :param district_name: 行政区域名称（如"吉州区"）
        :param output_dir: 输出目录
        :param map_style: 地图样式
        :param traffic: 是否显示交通
        :param labels: 是否显示标注
        :param boundary_simplify_step: 边界简化步长
        :param max_size: 最大图片尺寸（高德API最大支持2048*2048）
        :return: 下载结果信息
        """
        print(f"🗺️  开始下载 {district_name} 的地图（单图模式）...")
        
        # 搜索区域信息
        district_info = self.search_district(district_name)
        if not district_info:
            return {"success": False, "error": f"未找到区域: {district_name}"}
        
        # 获取边界坐标
        polyline = district_info.get('polyline', '')
        if not polyline:
            return {"success": False, "error": f"区域 {district_name} 没有边界数据"}
        
        # 分析边界数据
        boundary_analysis = self.analyze_boundary(polyline)
        if not boundary_analysis:
            return {"success": False, "error": "边界数据分析失败"}
        
        # 简化边界坐标以避免URL过长
        simplified_coords = self._simplify_boundary_coords(polyline, boundary_simplify_step)
        if not simplified_coords:
            return {"success": False, "error": "边界坐标简化失败"}
        
        # 构建边界路径参数
        boundary_path = f"5,0x0066FF,1,:{simplified_coords}"
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        # 下载地图图片
        print(f"📍 区域中心: ({boundary_analysis['center']['lng']:.6f}, {boundary_analysis['center']['lat']:.6f})")
        print(f"📏 区域范围: {boundary_analysis['lng_span']:.4f}° × {boundary_analysis['lat_span']:.4f}°")
        print(f"🎯 使用边界路径直接下载，图片尺寸: {max_size}")
        
        # 调用静态地图API
        image_data = self.get_static_map(
            size=max_size,
            paths=boundary_path,
            map_style=map_style,
            scale=scale
        )
        
        if image_data is None:
            return {"success": False, "error": "地图图片下载失败"}
        
        # 保存图片
        filename = f"{district_name}_单张.png"
        filepath = os.path.join(output_dir, filename)
        
        try:
            with open(filepath, 'wb') as f:
                f.write(image_data)
            
            file_size = len(image_data) / 1024 / 1024  # MB
            print(f"✅ 地图下载完成!")
            print(f"📁 保存路径: {filepath}")
            print(f"📊 文件大小: {file_size:.2f} MB")
            
            return {
                "success": True,
                "filepath": filepath,
                "file_size_mb": file_size,
                "boundary_analysis": boundary_analysis,
                "district_info": district_info
            }
            
        except Exception as e:
            return {"success": False, "error": f"保存文件失败: {str(e)}"}
    
    def _simplify_boundary_coords(self, polyline, step=2):
        """
        简化边界坐标以避免URL过长
        :param polyline: 原始边界坐标字符串
        :param step: 简化步长，每step个点取一个
        :return: 简化后的坐标字符串
        """
        if not polyline:
            return None
            
        coords_list = polyline.split(';')
        if len(coords_list) < 3:
            return None
        
        # 按步长简化坐标点
        simplified_coords = []
        for i in range(0, len(coords_list), step):
            simplified_coords.append(coords_list[i])
        
        # 确保闭合（添加第一个点作为最后一个点）
        if simplified_coords and simplified_coords[-1] != simplified_coords[0]:
            simplified_coords.append(simplified_coords[0])
        
        return ';'.join(simplified_coords)

    def download_district(self, district_name, output_dir="./maps", zoom_levels=None, 
                         map_style="normal", traffic=False, labels=True, show_boundary=True, 
                         boundary_simplify_step=2, scale=None):
        """
        下载指定行政区域的地图（别名方法）
        """
        return self.download_district_map(district_name, output_dir, zoom_levels, 
                                        map_style, traffic, labels, show_boundary, 
                                        boundary_simplify_step, scale)
    
    def download_district_map(self, district_name, output_dir="./maps", zoom_levels=None, 
                             map_style="normal", traffic=False, labels=True, show_boundary=True, 
                             boundary_simplify_step=2, scale=None):
        """
        下载指定行政区域的地图（单张地图模式）
        :param district_name: 行政区域名称
        :param output_dir: 输出目录
        :param zoom_levels: 缩放级别列表，如[8,10,12]，None时使用默认配置
        :param map_style: 地图样式 ("normal"标准, "satellite"卫星, "roadmap"路网)
        :param traffic: 是否显示实时交通
        :param labels: 是否显示地名标注
        :param show_boundary: 是否显示区域边界（红色边框线）
        :param boundary_simplify_step: 边界坐标简化间隔，2表示每隔1个点取1个，3表示每隔2个点取1个
        :param scale: 图片清晰度 (1=普通, 2=高清)
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
        
        # 分析区域边界
        boundary_analysis = None
        if 'polyline' in district_info and district_info['polyline']:
            boundary_analysis = self.analyze_boundary(district_info['polyline'])
            if boundary_analysis:
                print(f"📊 边界分析结果:")
                print(f"   几何中心: {boundary_analysis['center']}")
                print(f"   区域跨度: {boundary_analysis['span']['max_distance_km']:.2f} 公里")
                print(f"   边界复杂度: {boundary_analysis['boundary_complexity']} 个坐标点")
                print(f"   推荐缩放级别: {boundary_analysis['optimal_zoom']}")
                print(f"   推荐地图尺寸: {boundary_analysis['recommended_size']}")
                
                # 如果没有指定缩放级别，使用分析推荐的级别
                if zoom_levels is None:
                    zoom_levels = boundary_analysis['optimal_zoom']
                    print(f"🎯 使用智能推荐的缩放级别: {zoom_levels}")
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        # 获取边界路径数据
        paths = None
        
        if show_boundary and 'polyline' in district_info and district_info['polyline']:
            # 高德地图静态地图API的paths参数格式
            # 由于URL长度限制，需要简化边界坐标
            boundary_coords = district_info['polyline']
            coords_list = boundary_coords.split(';')
            
            # 动态调整简化间隔以确保URL长度合理
            current_step = boundary_simplify_step
            max_url_length = 2000  # 更严格的URL长度限制，确保API能正常处理
            
            while current_step <= 20:  # 最大间隔限制
                # 根据当前间隔简化坐标点
                simplified_coords = coords_list[::current_step]
                
                # 确保形成完整闭环：最后一个点与首个点一致
                if simplified_coords and simplified_coords[-1] != simplified_coords[0]:
                    simplified_coords.append(simplified_coords[0])
                
                # 构建paths参数进行长度检查
                if simplified_coords:
                    # 高德地图API paths格式: weight,color,transparency,fillcolor,fillTransparency
                    path_style = "5,0x0066FF,1,,"  # 5像素宽度，蓝色边框，不透明，无填充
                    path_coords = ';'.join(simplified_coords)
                    paths = f"{path_style}:{path_coords}"
                    
                    # 估算完整URL长度（包括基础参数）
                    estimated_url_length = len(self.static_map_url) + len(paths) + 200  # 200为其他参数预留
                    
                    if estimated_url_length <= max_url_length:
                        print(f"✅ 已获取边界路径数据，原始 {len(coords_list)} 个点，简化为 {len(simplified_coords)} 个点（间隔={current_step}）")
                        print(f"Paths参数长度: {len(paths)}")
                        print(f"预估URL长度: {estimated_url_length}")
                        break
                    else:
                        print(f"⚠️  间隔{current_step}时URL过长({estimated_url_length}字符)，尝试增大间隔...")
                        current_step += 1
                        continue
                else:
                    break
            
            # 如果即使最大间隔也无法满足长度要求，则禁用边界显示
            if current_step > 20:
                print(f"❌ 边界坐标过于复杂，无法在URL长度限制内显示，将禁用边界显示")
                paths = None
        elif not show_boundary:
            print("🔲 边界显示已关闭，将显示无边框地图")
        else:
            print("⚠️  未找到边界路径数据，将显示无边框地图")
        
        # 下载地图 - 支持多级别缩放
        saved_files = []
        # 使用传入的缩放级别，如果没有传入则使用默认配置
        if zoom_levels is None:
            zoom_levels = AMAP_CONFIG['default_zoom_levels']
        elif isinstance(zoom_levels, int):
            zoom_levels = [zoom_levels]  # 将单个整数转换为列表
        
        print(f"使用缩放级别: {zoom_levels}")
        
        for zoom in zoom_levels:
            zoom_desc = ZOOM_LEVELS.get(zoom, f"级别{zoom}")
            print(f"正在下载缩放级别 {zoom} ({zoom_desc}) 的地图...")
            
            # 确定最佳中心点和地图尺寸
            if boundary_analysis:
                # 使用边界分析得到的几何中心点，通常比行政中心更适合
                map_center = boundary_analysis['center']
                map_size = boundary_analysis['recommended_size']
                print(f"   使用几何中心: {map_center}")
                print(f"   使用推荐尺寸: {map_size}")
            else:
                # 回退到默认设置
                map_center = district_info['center']
                map_size = AMAP_CONFIG['default_map_size']
                print(f"   使用行政中心: {map_center}")
                print(f"   使用默认尺寸: {map_size}")
            
            # 单张地图模式
            map_data = self.get_static_map(
                center=map_center,
                zoom=zoom,
                size=map_size,
                paths=paths,  # 保留边界显示
                map_style=map_style,
                traffic=traffic,
                labels=labels,
                scale=scale
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
                
                filename = f"{district_name}_Z{zoom}{style_suffix}.png"
                filepath = os.path.join(output_dir, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(map_data)
                
                file_size_mb = len(map_data) / (1024 * 1024)  # MB
                print(f"✅ {filename} ({file_size_mb:.1f}MB)")
                saved_files.append(filepath)
                
                # 避免请求过于频繁
                time.sleep(AMAP_CONFIG['request_delay'])
            else:
                print(f"❌ 缩放级别 {zoom} 的地图下载失败")
        
        return saved_files



if __name__ == "__main__":
    main()