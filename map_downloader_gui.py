#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高德地图下载器 - 桌面版GUI应用
支持跨平台运行（Windows/Mac/Linux）
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import os
import json
import sys
from pathlib import Path
from amap_downloader import AmapDownloader

class MapDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("高德地图下载器 v1.0")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # 设置应用图标（如果有的话）
        try:
            # 可以添加图标文件
            pass
        except:
            pass
        
        # 配置文件路径
        self.config_file = Path.home() / ".amap_downloader_config.json"
        
        # 初始化变量
        self.api_key = tk.StringVar()
        self.district_name = tk.StringVar()
        self.output_dir = tk.StringVar(value=str(Path.home() / "Desktop" / "maps"))
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="就绪")
        
        # 加载配置
        self.load_config()
        
        # 创建界面
        self.create_widgets()
        
        # 绑定关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        """创建界面组件"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="高德地图下载器", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # API密钥输入
        ttk.Label(main_frame, text="API密钥:").grid(row=1, column=0, sticky=tk.W, pady=5)
        api_entry = ttk.Entry(main_frame, textvariable=self.api_key, width=50, show="*")
        api_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        # API密钥说明
        api_help = ttk.Label(main_frame, text="请在高德开放平台申请Web服务API密钥", 
                            foreground="gray", font=("Arial", 9))
        api_help.grid(row=2, column=1, sticky=tk.W, pady=(0, 10), padx=(5, 0))
        
        # 区域名称输入
        ttk.Label(main_frame, text="区域名称:").grid(row=3, column=0, sticky=tk.W, pady=5)
        district_entry = ttk.Entry(main_frame, textvariable=self.district_name, width=50)
        district_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        # 区域名称说明
        district_help = ttk.Label(main_frame, text="例如：吉州区、朝阳区、西湖区等", 
                                 foreground="gray", font=("Arial", 9))
        district_help.grid(row=4, column=1, sticky=tk.W, pady=(0, 10), padx=(5, 0))
        
        # 输出目录选择
        ttk.Label(main_frame, text="保存目录:").grid(row=5, column=0, sticky=tk.W, pady=5)
        
        dir_frame = ttk.Frame(main_frame)
        dir_frame.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        dir_frame.columnconfigure(0, weight=1)
        
        dir_entry = ttk.Entry(dir_frame, textvariable=self.output_dir, width=40)
        dir_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        browse_btn = ttk.Button(dir_frame, text="浏览", command=self.browse_directory)
        browse_btn.grid(row=0, column=1)
        
        # 下载选项
        options_frame = ttk.LabelFrame(main_frame, text="下载选项", padding="10")
        options_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=20)
        options_frame.columnconfigure(0, weight=1)
        
        # 地图尺寸选择
        size_frame = ttk.Frame(options_frame)
        size_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(size_frame, text="地图尺寸:").grid(row=0, column=0, sticky=tk.W)
        self.size_var = tk.StringVar(value="6144*6144")
        size_combo = ttk.Combobox(size_frame, textvariable=self.size_var, 
                                 values=["2048*2048", "4096*4096", "6144*6144"], 
                                 state="readonly", width=15)
        size_combo.grid(row=0, column=1, padx=(10, 0))
        
        # 边界精度选择
        precision_frame = ttk.Frame(options_frame)
        precision_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(precision_frame, text="边界精度:").grid(row=0, column=0, sticky=tk.W)
        self.precision_var = tk.StringVar(value="隔位显示")
        precision_combo = ttk.Combobox(precision_frame, textvariable=self.precision_var,
                                      values=["隔位显示", "高精度(500点)", "超高精度(1000点)"],
                                      state="readonly", width=15)
        precision_combo.grid(row=0, column=1, padx=(10, 0))
        
        # 地图样式选择
        style_frame = ttk.Frame(options_frame)
        style_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(style_frame, text="地图样式:").grid(row=0, column=0, sticky=tk.W)
        self.style_var = tk.StringVar(value="标准地图")
        style_combo = ttk.Combobox(style_frame, textvariable=self.style_var,
                                  values=["标准地图", "卫星地图", "路网地图"],
                                  state="readonly", width=15)
        style_combo.grid(row=0, column=1, padx=(10, 0))
        
        # 图层选项
        layers_frame = ttk.Frame(options_frame)
        layers_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(layers_frame, text="图层选项:").grid(row=0, column=0, sticky=tk.W)
        
        # 交通图层复选框
        self.traffic_var = tk.BooleanVar(value=False)
        traffic_check = ttk.Checkbutton(layers_frame, text="实时交通", variable=self.traffic_var)
        traffic_check.grid(row=0, column=1, padx=(10, 0))
        
        # 地名标注复选框
        self.labels_var = tk.BooleanVar(value=True)
        labels_check = ttk.Checkbutton(layers_frame, text="地名标注", variable=self.labels_var)
        labels_check.grid(row=0, column=2, padx=(10, 0))
        
        # 下载按钮
        download_btn = ttk.Button(main_frame, text="开始下载", command=self.start_download,
                                 style="Accent.TButton")
        download_btn.grid(row=7, column=0, columnspan=2, pady=20)
        
        # 进度条
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=8, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                           maximum=100, length=400)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # 状态标签
        status_label = ttk.Label(main_frame, textvariable=self.status_var, 
                                foreground="blue", font=("Arial", 10))
        status_label.grid(row=9, column=0, columnspan=2, pady=5)
        
        # 版权信息
        copyright_label = ttk.Label(main_frame, text="© 2024 高德地图下载器 - 基于高德开放平台API", 
                                   foreground="gray", font=("Arial", 8))
        copyright_label.grid(row=10, column=0, columnspan=2, pady=(20, 0))
    
    def browse_directory(self):
        """浏览选择目录"""
        directory = filedialog.askdirectory(initialdir=self.output_dir.get())
        if directory:
            self.output_dir.set(directory)
    
    def load_config(self):
        """加载配置文件"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.api_key.set(config.get('api_key', ''))
                    self.output_dir.set(config.get('output_dir', str(Path.home() / "Desktop" / "maps")))
        except Exception as e:
            print(f"加载配置失败: {e}")
    
    def save_config(self):
        """保存配置文件"""
        try:
            config = {
                'api_key': self.api_key.get(),
                'output_dir': self.output_dir.get()
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存配置失败: {e}")
    
    def validate_inputs(self):
        """验证输入"""
        if not self.api_key.get().strip():
            messagebox.showerror("错误", "请输入API密钥")
            return False
        
        if not self.district_name.get().strip():
            messagebox.showerror("错误", "请输入区域名称")
            return False
        
        if not self.output_dir.get().strip():
            messagebox.showerror("错误", "请选择保存目录")
            return False
        
        return True
    
    def start_download(self):
        """开始下载（在新线程中执行）"""
        if not self.validate_inputs():
            return
        
        # 保存配置
        self.save_config()
        
        # 在新线程中执行下载
        download_thread = threading.Thread(target=self.download_maps)
        download_thread.daemon = True
        download_thread.start()
    
    def download_maps(self):
        """下载地图（后台线程）"""
        try:
            # 更新状态
            self.status_var.set("正在初始化...")
            self.progress_var.set(10)
            
            # 创建下载器
            downloader = AmapDownloader(self.api_key.get().strip())
            
            # 创建输出目录
            output_dir = Path(self.output_dir.get())
            output_dir.mkdir(parents=True, exist_ok=True)
            
            self.status_var.set("正在搜索区域...")
            self.progress_var.set(30)
            
            # 修改下载器以支持不同精度
            district_name = self.district_name.get().strip()
            
            # 根据精度选择修改代码逻辑
            precision = self.precision_var.get()
            if precision == "高精度(500点)":
                # 临时修改下载器的简化逻辑
                self.modify_downloader_precision(downloader, 500)
            elif precision == "超高精度(1000点)":
                self.modify_downloader_precision(downloader, 1000)
            else:
                # 使用默认的隔位显示
                pass
            
            self.status_var.set("正在下载地图...")
            self.progress_var.set(60)
            
            # 获取图层设置
            style_mapping = {
                "标准地图": "normal",
                "卫星地图": "satellite", 
                "路网地图": "roadmap"
            }
            map_style = style_mapping.get(self.style_var.get(), "normal")
            traffic = self.traffic_var.get()
            labels = self.labels_var.get()
            
            # 下载地图
            result = downloader.download_district_map(
                district_name, 
                str(output_dir),
                map_style=map_style,
                traffic=traffic,
                labels=labels
            )
            
            self.progress_var.set(100)
            
            if result:
                self.status_var.set("下载完成！")
                messagebox.showinfo("成功", f"地图下载完成！\n保存位置: {output_dir}")
            else:
                self.status_var.set("下载失败")
                messagebox.showerror("错误", "地图下载失败，请检查区域名称和网络连接")
                
        except Exception as e:
            self.status_var.set("下载出错")
            messagebox.showerror("错误", f"下载过程中出现错误:\n{str(e)}")
        finally:
            self.progress_var.set(0)
    
    def modify_downloader_precision(self, downloader, max_points):
        """临时修改下载器的精度设置"""
        # 这里可以动态修改下载器的行为
        # 由于我们已经在amap_downloader.py中实现了隔位显示
        # 这里可以根据需要进一步调整
        pass
    
    def on_closing(self):
        """关闭应用时的处理"""
        self.save_config()
        self.root.destroy()

def main():
    """主函数"""
    # 创建主窗口
    root = tk.Tk()
    
    # 设置主题（如果支持的话）
    try:
        style = ttk.Style()
        # 尝试使用现代主题
        available_themes = style.theme_names()
        if 'clam' in available_themes:
            style.theme_use('clam')
        elif 'alt' in available_themes:
            style.theme_use('alt')
    except:
        pass
    
    # 创建应用
    app = MapDownloaderGUI(root)
    
    # 运行主循环
    root.mainloop()

if __name__ == "__main__":
    main()