# install/build.py
import os
import PyInstaller.__main__
import shutil
from pathlib import Path
import sys
import os
from src.wofa_ide.app_info import *

# 添加根目錄到路徑
ROOT_DIR = str(Path(__file__).parent)
sys.path.insert(0, ROOT_DIR)

INSTALLER_NAME = APP_WIN + "_installer"
BUILD_DIR = ROOT_DIR + "/installer_build"

def build_installer():
    print(f"開始構建安裝程序: {INSTALLER_NAME}")

    # 清理並創建構建目錄
    #if Path(BUILD_DIR).exists():
    #    shutil.rmtree(BUILD_DIR)
    #Path(BUILD_DIR).mkdir(parents=True, exist_ok=True)
#
    ## 複製所需文件到構建目錄（您的建議方案）
    #files_to_copy = [
    #    (ROOT_DIR + "/dist/" + APP + "/"+APP_WIN_EXE, BUILD_DIR+ "/" + APP_WIN_EXE),
    #    (FP_APP_ICON, BUILD_DIR+ "/" + APP_ICON),
    #    (FP_LANGUAGES, BUILD_DIR+ "/" + LANGUAGES),
    #   # (ROOT_DIR / "installer.py", BUILD_DIR / "installer.py")
    #]
#
    #for source, target in files_to_copy:
    #    if Path(source).exists():
    #        shutil.copy2(source, target)
    #        print(f"✓ 已複製: {source} -> {target}")
    #    else:
    #        print(f"❌ 錯誤: 源文件不存在 {source}")
    #        return False
    main_exe_path = f"{ROOT_DIR}/dist/{APP_EXE}"
    if not os.path.exists(main_exe_path):
        print(f"❌ 錯誤: 主程式 {APP_EXE} 不存在，請先運行 build.py")
        return False

    # 確保資源文件存在
    if not os.path.exists(FP_LANGUAGES):
        print(f"❌ 錯誤: 語言文件不存在 {FP_LANGUAGES}")
        return False

    if not os.path.exists(FP_APP_ICON):
        print(f"❌ 錯誤: 圖標文件不存在 {FP_APP_ICON}")
        return False
    # 创建构建命令

    build_args = [
       # str(BUILD_DIR / "installer.py"),
        "installer.py",
        '--onefile',
        '--windowed',
        f"--name={INSTALLER_NAME}",
        f"--icon={FP_APP_ICON}",
        f"--add-data={main_exe_path}{SEPARATOR}.",
        f"--add-data={FP_LANGUAGES}{SEPARATOR}.",
        f"--add-data={FP_APP_ICON}{SEPARATOR}.",
       #f"--icon={BUILD_DIR}/{APP_ICON}",
       #f"--add-data={BUILD_DIR}/{APP_WIN_EXE}{SEPARATOR}.",
       #f"--add-data={BUILD_DIR}/{LANGUAGES}{SEPARATOR}.",
       #f"--add-data={BUILD_DIR}/{APP_ICON}{SEPARATOR}.",
        "--noconfirm",
        "--clean",
        f"--distpath=dist",  # 輸出到項目dist目錄
        f"--workpath=build",  # 臨時文件放到構建目錄
      #  f"--specpath={BUILD_DIR}"
    ]
    # 執行構建
    print("開始PyInstaller構建...")
    try:
        PyInstaller.__main__.run(build_args)
        print("✅ 安裝程序構建完成！")
        print(f"安裝程序位置: {ROOT_DIR}/dist/{INSTALLER_NAME}.exe")
    except Exception as e:
        print(f"❌ 構建失敗: {e}")
        return False
    #finally:
        # 可選：是否保留構建目錄用於調試
       #if Path(BUILD_DIR).exists():
       #    shutil.rmtree(BUILD_DIR)
       #    print("🧹 已清理構建臨時文件")
#
    return True


if __name__ == "__main__":
    success = build_installer()
    sys.exit(0 if success else 1)