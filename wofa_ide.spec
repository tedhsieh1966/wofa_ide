# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Projects\\Python\\wofa_ide/src/wofa_ide/wofa_ide.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Projects\\Python\\wofa_ide/src/wofa_ide/languages.xlsx', '.'), ('C:\\Projects\\Python\\wofa_ide/src/wofa_ide/images/syntak_blue_128.ico', '.')],
    hiddenimports=['langchain.chains.retrieval', 'langchain.chains.history_aware_retriever', 'src.wofa_ide.editors', 'src.wofa_ide.app_info'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='wofa_ide',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Projects\\Python\\wofa_ide\\src\\wofa_ide\\images\\syntak_blue_128.ico'],
)
