#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试不同图层组合的地图下载效果
"""

import os
from amap_downloader import AmapDownloader
from config import AMAP_CONFIG

def test_different_layers():
    """测试不同图层组合"""
    
    # 从配置文件读取API密钥
    api_key = AMAP_CONFIG.get('api_key', '')
    if not api_key:
        print("❌ 请先在config.py中配置API密钥")
        return
    
    # 创建下载器
    downloader = AmapDownloader(api_key)
    
    # 测试区域
    test_district = "吉州区"
    output_dir = "./maps/layer_test"
    
    # 创建测试目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 测试不同的图层组合
    test_cases = [
        {
            "name": "标准地图_带交通_带标注",
            "map_style": "normal",
            "traffic": True,
            "labels": True
        },
        {
            "name": "路网地图_带交通_带标注", 
            "map_style": "roadmap",
            "traffic": True,
            "labels": True
        },
        {
            "name": "卫星地图_无交通_无标注",
            "map_style": "satellite",
            "traffic": False,
            "labels": False
        },
        {
            "name": "标准地图_无交通_无标注",
            "map_style": "normal", 
            "traffic": False,
            "labels": False
        }
    ]
    
    print(f"🧪 开始测试不同图层组合，测试区域: {test_district}")
    print(f"📂 测试结果保存到: {output_dir}")
    print("=" * 60)
    
    success_count = 0
    total_count = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔄 测试 {i}/{total_count}: {test_case['name']}")
        print(f"   地图样式: {test_case['map_style']}")
        print(f"   实时交通: {'开启' if test_case['traffic'] else '关闭'}")
        print(f"   地名标注: {'开启' if test_case['labels'] else '关闭'}")
        
        try:
            # 下载地图
            result = downloader.download_district_map(
                test_district,
                output_dir,
                map_style=test_case['map_style'],
                traffic=test_case['traffic'],
                labels=test_case['labels']
            )
            
            if result:
                print(f"   ✅ 成功下载: {len(result)} 个文件")
                success_count += 1
            else:
                print(f"   ❌ 下载失败")
                
        except Exception as e:
            print(f"   ❌ 下载出错: {str(e)}")
    
    print("\n" + "=" * 60)
    print(f"🎯 测试完成！成功 {success_count}/{total_count} 个测试用例")
    
    if success_count > 0:
        print(f"📂 请查看 {output_dir} 目录中的地图文件，对比不同图层的显示效果")
        print("💡 建议对比以下方面:")
        print("   - 标准地图 vs 路网地图 vs 卫星地图的基础样式差异")
        print("   - 开启/关闭实时交通图层的道路颜色变化")
        print("   - 开启/关闭地名标注的文字显示差异")
        print("   - 不同图层组合对街道细节的显示效果")

if __name__ == "__main__":
    test_different_layers()