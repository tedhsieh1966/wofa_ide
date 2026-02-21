import platform
from pathlib import Path


#class AppInfo:
#    def __init__(self):
#        self.version = "1.0.0"
#        self.name = "Test WOFA IDE"
#
#    def __str__(self):
#        return f"{self.name} v{self.version}"

ROOT_DIR = str(Path(__file__).parent.parent.parent) # __file__ 指到 app_info.py

IS_LITE = False
BRIEF = "WorkFlow Automation"
DESCRIPTION="整合積累經驗 提升企業智慧"
APP_CAPS = "WOFA_IDE"
APP = "wofa_ide"
APP_DESKTOP_LINK = APP + ".lnk"
APP_WIN = APP if not IS_LITE else  APP + "_lite"
APP_MAC = APP + "_mac" if not IS_LITE else APP + "mac_lite"
APP_WIN_EXE= APP_WIN + ".exe"
APP_MAC_EXE= APP_MAC + ".app"
APP_ICON_WIN = "syntak_blue_128.ico"
APP_ICON_MAC = "syntak_blue_128.icns"
LANGUAGES = "languages.xlsx"

# 跨平台配置
if platform.system() == 'Windows':
    SEPARATOR = ';'
    APP_NAME = APP_WIN
    APP_EXE = APP_WIN_EXE
    APP_ICON = APP_ICON_WIN
elif platform.system() == 'Darwin':  # macOS
    SEPARATOR = ':'
    APP_NAME = APP_MAC
    APP_EXE = APP_MAC_EXE
    APP_ICON = APP_ICON_MAC
else:  # Linux
    SEPARATOR = ':'
    APP_NAME = APP_MAC  # 或創建專門的 Linux 名稱
    APP_EXE = APP_MAC
    APP_ICON = APP_ICON_WIN  # Linux 通常支持 .ico

FP_APP_PY = f"{ROOT_DIR}/src/{APP}/{APP}.py"
FP_APP_ICON = f"{ROOT_DIR}/src/{APP}/images/{APP_ICON}"
FP_LANGUAGES = f"{ROOT_DIR}/src/{APP}/{LANGUAGES}"

def get_relative_path(path: Path) -> str:
    """獲取相對於項目根目錄的路徑字符串"""
    try:
        return str(path.relative_to(ROOT_DIR))
    except ValueError:
        return str(path)