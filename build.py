# build.py
import os
import platform
import PyInstaller.__main__
import shutil
from src.wofa_ide.app_info import *


def create_dmg():
    if platform.system() == 'Darwin':
        app_path = f"dist/{APP_EXE}"
        dmg_name = f"{APP_NAME}.dmg"

        # 使用 hdiutil 創建 DMG
        os.system(f'hdiutil create -srcfolder "{app_path}" "{dmg_name}"')
        print(f"DMG 文件創建完成: {dmg_name}")

def build_app():
    try:
        # 檢查圖標文件是否存在
        icon_path = FP_APP_ICON
        if not os.path.exists(icon_path):
            print(f"警告：找不到圖標文件 {icon_path}")
            if platform.system() == 'Darwin':
                print("請確保有 .icns 格式的圖標文件")

        # 清理之前的构建
        if os.path.exists('dist'):
            shutil.rmtree('dist')
        if os.path.exists('build'):
            shutil.rmtree('build')


        # 创建构建命令
        build_args = [
            f'{FP_APP_PY}',
          #  'run.py',  # 改为使用 run.py 作为入口
            '--onefile',
            '--windowed',
          #  '--hidden-import=numpy',
          #  '--hidden-import=scipy',
          #  '--hidden-import=numpy.core._multiarray_umath',
          #  '--hidden-import=numpy.core._dtype_ctypes',
          #  '--hidden-import=scipy._cyutility',
            '--hidden-import=langchain.chains.retrieval',
            '--hidden-import=langchain.chains.history_aware_retriever',
            f'--hidden-import=src.wofa_ide.editors',
            f'--hidden-import=src.wofa_ide.app_info',
            '--name='+ APP_NAME,
            f'--icon={FP_APP_ICON}',
            f'--add-data={FP_LANGUAGES}{SEPARATOR}.',
            f'--add-data={FP_APP_ICON}{SEPARATOR}.',
          #  '--console',
            '--distpath=dist',
            '--workpath=build',
           # '--specpath=build'
        ]

        print(f"開始構建 {APP_NAME} for {platform.system()}...")
        print(f"使用圖標: {FP_APP_ICON}")
        # 执行构建
        PyInstaller.__main__.run(build_args)

        # 复制配置文件（如果有）
        if os.path.exists('src/config.json'):
            shutil.copy('src/config.json', 'src/dist')

        print(f"构建完成！可执行文件{APP_EXE}在 dist 目录中")
    except Exception as e:
            print("安装错误", f"构建过程中发生错误:\n{str(e)}")

if __name__ == '__main__':
    build_app()