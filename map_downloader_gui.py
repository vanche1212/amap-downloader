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
        self.root.title("高德地图下载器 v1.1.1")
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
        
        # Zoom级别选择框架
        zoom_frame = ttk.LabelFrame(main_frame, text="缩放级别设置", padding="10")
        zoom_frame.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Zoom级别选择模式
        self.zoom_mode_var = tk.StringVar(value="default")
        
        # 默认级别选项
        default_radio = ttk.Radiobutton(zoom_frame, text="默认级别 (推荐)", 
                                       variable=self.zoom_mode_var, value="default")
        default_radio.grid(row=0, column=0, sticky=tk.W, padx=5)
        
        # 自定义级别选项
        custom_radio = ttk.Radiobutton(zoom_frame, text="自定义级别", 
                                      variable=self.zoom_mode_var, value="custom",
                                      command=self.on_zoom_mode_change)
        custom_radio.grid(row=1, column=0, sticky=tk.W, padx=5)
        
        # 自定义zoom级别输入框
        self.zoom_custom_frame = ttk.Frame(zoom_frame)
        self.zoom_custom_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(self.zoom_custom_frame, text="级别 (用逗号分隔):").grid(row=0, column=0, sticky=tk.W, padx=(20, 5))
        
        self.zoom_levels_var = tk.StringVar(value="10,12,14")
        self.zoom_entry = ttk.Entry(self.zoom_custom_frame, textvariable=self.zoom_levels_var, width=20)
        self.zoom_entry.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # Zoom级别说明
        zoom_help = ttk.Label(zoom_frame, text="级别越高越详细，建议范围：8-18", 
                             foreground="gray", font=("Arial", 9))
        zoom_help.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(5, 0))
        
        # 初始状态设置
        self.on_zoom_mode_change()
        
        # 下载按钮
        download_btn = ttk.Button(main_frame, text="开始下载", command=self.start_download)
        download_btn.grid(row=8, column=0, columnspan=2, pady=20)
        
        # 进度条
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=9, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                           maximum=100, length=400)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # 状态标签
        status_label = ttk.Label(main_frame, textvariable=self.status_var, 
                                foreground="blue", font=("Arial", 10))
        status_label.grid(row=10, column=0, columnspan=2, pady=5)
        
        # 版权信息
        copyright_label = ttk.Label(main_frame, text="© 2024 高德地图下载器 - 基于高德开放平台API", 
                                   foreground="gray", font=("Arial", 8))
        copyright_label.grid(row=11, column=0, columnspan=2, pady=(20, 0))
    
    def on_zoom_mode_change(self):
        """处理zoom模式切换"""
        if hasattr(self, 'zoom_mode_var'):
            if self.zoom_mode_var.get() == "custom":
                # 启用自定义输入框
                for widget in self.zoom_custom_frame.winfo_children():
                    widget.configure(state='normal')
            else:
                # 禁用自定义输入框
                for widget in self.zoom_custom_frame.winfo_children():
                    if isinstance(widget, ttk.Entry):
                        widget.configure(state='disabled')
    
    def get_zoom_levels(self):
        """获取用户选择的zoom级别"""
        if self.zoom_mode_var.get() == "default":
            return None  # 使用默认级别
        else:
            # 解析自定义级别
            try:
                zoom_str = self.zoom_levels_var.get().strip()
                if not zoom_str:
                    return None
                
                zoom_levels = []
                for level in zoom_str.split(','):
                    level = level.strip()
                    if level:
                        zoom_level = int(level)
                        if 1 <= zoom_level <= 20:  # 合理的zoom级别范围
                            zoom_levels.append(zoom_level)
                        else:
                            raise ValueError(f"Zoom级别 {zoom_level} 超出范围 (1-20)")
                
                return zoom_levels if zoom_levels else None
            except ValueError as e:
                messagebox.showerror("错误", f"Zoom级别格式错误: {e}")
                return None
    
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
        
        district_name = self.district_name.get().strip()
        if not district_name:
            messagebox.showerror("错误", "请输入区域名称")
            return False
        
        # 验证区域名称格式（应该是中文地名，不是哈希值）
        if len(district_name) > 20 or any(c.isdigit() and len(district_name) > 10 for c in district_name):
            messagebox.showerror("错误", "请输入有效的区域名称（如：吉州区、朝阳区等）")
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
            
            # 验证API密钥
            api_key = self.api_key.get().strip()
            if not api_key:
                self.status_var.set("错误: API密钥为空")
                self.root.after(0, lambda: messagebox.showerror("错误", "请输入有效的API密钥"))
                return
            
            # 验证区域名称
            district_name = self.district_name.get().strip()
            if not district_name:
                self.status_var.set("错误: 区域名称为空")
                self.root.after(0, lambda: messagebox.showerror("错误", "请输入要下载的区域名称"))
                return
            
            # 验证输出目录
            output_dir_str = self.output_dir.get().strip()
            if not output_dir_str:
                self.status_var.set("错误: 输出目录为空")
                self.root.after(0, lambda: messagebox.showerror("错误", "请选择输出目录"))
                return
            
            # 创建下载器
            try:
                downloader = AmapDownloader(api_key)
            except Exception as e:
                self.status_var.set("错误: 下载器初始化失败")
                error_msg = str(e)
                self.root.after(0, lambda: messagebox.showerror("错误", f"下载器初始化失败:\n{error_msg}"))
                return
            
            # 创建输出目录
            try:
                output_dir = Path(output_dir_str)
                output_dir.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                self.status_var.set("错误: 无法创建输出目录")
                error_msg = str(e)
                self.root.after(0, lambda: messagebox.showerror("错误", f"无法创建输出目录:\n{error_msg}"))
                return
            
            self.status_var.set("正在搜索区域...")
            self.progress_var.set(30)
            
            self.status_var.set("正在下载地图...")
            self.progress_var.set(60)
            
            # 获取用户选择的zoom级别
            zoom_levels = self.get_zoom_levels()
            if zoom_levels is None and self.zoom_mode_var.get() == "custom":
                # 自定义模式但解析失败
                return
            
            # 设置默认下载参数
            map_style = "normal"  # 标准地图样式
            traffic = False       # 不显示交通信息
            labels = True         # 显示标注
            
            # 开始下载地图
            try:
                if zoom_levels:
                    self.status_var.set(f"正在下载地图 (级别: {zoom_levels})...")
                else:
                    self.status_var.set("正在下载地图 (使用默认级别)...")
                
                result = downloader.download_district(
                    district_name,
                    str(output_dir),
                    zoom_levels=zoom_levels,
                    map_style=map_style,
                    traffic=traffic,
                    labels=labels
                )
            except Exception as e:
                error_msg = str(e)
                self.status_var.set(f"下载错误: {error_msg}")
                self.root.after(0, lambda msg=error_msg: messagebox.showerror("错误", f"下载错误: {msg}"))
                return
            
            self.progress_var.set(100)
            
            # 处理下载结果 - 返回的是文件路径列表
            if result and isinstance(result, list) and len(result) > 0:
                # 下载成功，result是保存的文件路径列表
                file_count = len(result)
                self.status_var.set(f"下载完成！共保存 {file_count} 个文件")
                
                # 保存变量以避免lambda作用域问题
                name = district_name
                count = file_count
                files = result
                
                # 构建简洁的成功消息
                if count == 1:
                    success_msg = f"{name} 下载完成！"
                else:
                    success_msg = f"{name} 下载完成！\n共 {count} 个文件"
                
                self.root.after(0, lambda: messagebox.showinfo("下载完成", success_msg))
            elif result and isinstance(result, list) and len(result) == 0:
                # 返回空列表，表示下载失败
                self.status_var.set("下载失败: 没有成功下载任何文件")
                self.root.after(0, lambda: messagebox.showerror("错误", "下载失败: 没有成功下载任何文件"))
            else:
                # 返回None或其他异常情况
                self.status_var.set("下载失败: 返回结果异常")
                self.root.after(0, lambda: messagebox.showerror("错误", "下载失败: 返回结果异常"))
                
        except Exception as e:
            self.status_var.set("下载出错")
            # 使用root.after在主线程中显示错误消息
            error_msg = str(e)  # 先保存错误消息
            self.root.after(0, lambda: messagebox.showerror("错误", f"下载过程中出现错误:\n{error_msg}"))
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