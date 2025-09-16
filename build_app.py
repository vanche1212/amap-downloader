#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跨平台打包脚本
支持Mac和Windows平台的可执行文件生成
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path
import json
import time

class CrossPlatformBuilder:
    """跨平台构建器"""
    
    def __init__(self):
        self.project_dir = Path.cwd()
        self.dist_dir = self.project_dir / "dist"
        self.build_dir = self.project_dir / "build"
        self.current_system = platform.system().lower()
        self.current_arch = platform.machine().lower()
        
        # 支持的平台配置
        self.platforms = {
            "darwin": {
                "name": "macOS",
                "exe_suffix": "",
                "icon": "icon.icns",
                "arch_map": {
                    "x86_64": "x86_64",
                    "arm64": "arm64"
                }
            },
            "windows": {
                "name": "Windows", 
                "exe_suffix": ".exe",
                "icon": "icon.ico",
                "arch_map": {
                    "amd64": "x64",
                    "x86_64": "x64",
                    "i386": "x86"
                }
            },
            "linux": {
                "name": "Linux",
                "exe_suffix": "",
                "icon": "icon.png",
                "arch_map": {
                    "x86_64": "x64",
                    "aarch64": "arm64"
                }
            }
        }
    
    def setup_conda_environment(self):
        """设置conda环境"""
        print("🐍 设置conda环境...")
        
        env_file = self.project_dir / "environment.yml"
        if not env_file.exists():
            print("❌ 未找到environment.yml文件")
            return False
        
        try:
            # 检查conda是否可用
            result = subprocess.run(["conda", "--version"], 
                                  capture_output=True, text=True, check=True)
            print(f"✅ Conda版本: {result.stdout.strip()}")
            
            # 创建或更新环境
            env_name = "map-downloader"
            print(f"📦 创建/更新conda环境: {env_name}")
            
            subprocess.run([
                "conda", "env", "create", "-f", str(env_file), "--force"
            ], check=True)
            
            print(f"✅ Conda环境 '{env_name}' 已准备就绪")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Conda环境设置失败: {e}")
            return False
        except FileNotFoundError:
            print("❌ 未找到conda命令，请确保已安装Anaconda或Miniconda")
            return False
    
    def install_dependencies(self):
        """安装打包依赖"""
        print("📦 安装打包依赖...")
        
        try:
            # 检查PyInstaller
            try:
                import PyInstaller
                print("✅ PyInstaller已安装")
            except ImportError:
                print("📥 安装PyInstaller...")
                subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller>=5.0"], check=True)
                print("✅ PyInstaller安装完成")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ 依赖安装失败: {e}")
            return False
    
    def clean_build_files(self):
        """清理构建文件"""
        print("🧹 清理构建文件...")
        
        # 删除构建目录
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
        
        if self.dist_dir.exists():
            shutil.rmtree(self.dist_dir)
        
        # 删除spec文件
        for spec_file in self.project_dir.glob("*.spec"):
            spec_file.unlink()
        
        print("✅ 构建文件已清理")
    
    def get_pyinstaller_command(self, target_platform=None):
        """获取PyInstaller命令"""
        if target_platform is None:
            target_platform = self.current_system
        
        platform_config = self.platforms.get(target_platform, {})
        
        cmd = [
            "pyinstaller",
            "--onefile",
            "--windowed",
            "--name", "高德地图下载器",
            "--clean",
            "--noconfirm"
        ]
        
        # 添加图标
        icon_file = platform_config.get("icon")
        if icon_file and Path(icon_file).exists():
            cmd.extend(["--icon", icon_file])
        
        # 隐藏导入的模块
        hidden_imports = [
            "tkinter",
            "tkinter.ttk", 
            "tkinter.messagebox",
            "tkinter.filedialog",
            "requests",
            "json",
            "pathlib",
            "threading",
            "urllib.parse",
            "urllib.request",
            "urllib.error"
        ]
        
        for module in hidden_imports:
            cmd.extend(["--hidden-import", module])
        
        # 排除不需要的模块
        exclude_modules = [
            "matplotlib",
            "numpy", 
            "pandas",
            "scipy",
            "PIL",
            "cv2",
            "tensorflow",
            "torch",
            "jupyter",
            "IPython"
        ]
        
        for module in exclude_modules:
            cmd.extend(["--exclude-module", module])
        
        # 添加数据文件
        cmd.extend([
            "--add-data", "config.py:.",
            "--add-data", "使用说明.md:."
        ])
        
        # 主文件
        cmd.append("map_downloader_gui.py")
        
        return cmd
    
    def build_for_platform(self, target_platform=None):
        """为指定平台构建"""
        if target_platform is None:
            target_platform = self.current_system
        
        platform_config = self.platforms.get(target_platform, {})
        platform_name = platform_config.get("name", target_platform)
        
        print(f"🔨 为 {platform_name} 构建可执行文件...")
        
        # 获取构建命令
        cmd = self.get_pyinstaller_command(target_platform)
        
        print(f"🚀 执行命令: {' '.join(cmd)}")
        
        try:
            # 执行打包
            start_time = time.time()
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            build_time = time.time() - start_time
            
            print(f"✅ {platform_name} 构建成功! (耗时: {build_time:.1f}秒)")
            
            # 查找生成的文件
            exe_name = "高德地图下载器" + platform_config.get("exe_suffix", "")
            exe_path = self.dist_dir / exe_name
            
            if exe_path.exists():
                file_size = exe_path.stat().st_size / (1024 * 1024)  # MB
                print(f"📦 生成文件: {exe_path}")
                print(f"📏 文件大小: {file_size:.1f} MB")
                
                # 重命名为更具描述性的名称
                arch = self.platforms[target_platform]["arch_map"].get(
                    self.current_arch, self.current_arch
                )
                final_name = f"高德地图下载器_{platform_name}_{arch}{platform_config.get('exe_suffix', '')}"
                final_path = self.project_dir / final_name
                
                if final_path.exists():
                    final_path.unlink()
                
                shutil.move(str(exe_path), str(final_path))
                print(f"✨ 最终文件: {final_path}")
                
                return final_path
            else:
                print(f"❌ 未找到生成的可执行文件: {exe_path}")
                return None
                
        except subprocess.CalledProcessError as e:
            print(f"❌ {platform_name} 构建失败:")
            print(f"错误输出: {e.stderr}")
            return None
        except Exception as e:
            print(f"❌ 构建过程中出现错误: {e}")
            return None
    
    def build_all_platforms(self):
        """构建所有支持的平台"""
        print("🎯 开始跨平台构建...")
        print("=" * 60)
        
        built_files = []
        
        # 当前平台构建
        current_file = self.build_for_platform(self.current_system)
        if current_file:
            built_files.append(current_file)
        
        # 如果在Mac上，可以尝试构建Windows版本（需要额外配置）
        if self.current_system == "darwin":
            print("\n💡 提示: 要构建Windows版本，需要在Windows系统上运行此脚本")
            print("   或者使用GitHub Actions等CI/CD服务进行跨平台构建")
        
        return built_files
    
    def create_build_info(self, built_files):
        """创建构建信息文件"""
        build_info = {
            "build_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "builder_system": f"{self.current_system} {self.current_arch}",
            "python_version": sys.version,
            "built_files": [str(f) for f in built_files],
            "platforms": list(self.platforms.keys())
        }
        
        info_file = self.project_dir / "build_info.json"
        with open(info_file, 'w', encoding='utf-8') as f:
            json.dump(build_info, f, indent=2, ensure_ascii=False)
        
        print(f"📋 构建信息已保存到: {info_file}")
    
    def run(self):
        """运行构建流程"""
        print("🎯 高德地图下载器 - 跨平台打包工具")
        print("=" * 60)
        print(f"🖥️  当前系统: {self.current_system} {self.current_arch}")
        print()
        
        # 检查必要文件
        required_files = ["map_downloader_gui.py", "amap_downloader.py", "config.py"]
        missing_files = [f for f in required_files if not Path(f).exists()]
        
        if missing_files:
            print(f"❌ 缺少必要文件: {', '.join(missing_files)}")
            return False
        
        # 安装依赖
        if not self.install_dependencies():
            return False
        
        # 清理构建文件
        self.clean_build_files()
        
        # 构建所有平台
        built_files = self.build_all_platforms()
        
        if built_files:
            print("\n" + "=" * 60)
            print("🎉 构建完成!")
            print(f"📦 成功构建 {len(built_files)} 个文件:")
            for file in built_files:
                size = file.stat().st_size / (1024 * 1024)
                print(f"   📄 {file.name} ({size:.1f} MB)")
            
            # 创建构建信息
            self.create_build_info(built_files)
            
            print("\n💡 使用说明:")
            print("   - 可执行文件可以直接双击运行")
            print("   - 首次运行时请输入高德地图API密钥")
            print("   - 支持拖拽文件到应用图标上打开")
            print("   - 如需在其他平台构建，请在对应系统上运行此脚本")
            
            return True
        else:
            print("\n❌ 构建失败，请检查错误信息")
            return False

def main():
    """主函数"""
    builder = CrossPlatformBuilder()
    success = builder.run()
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()