# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('icon.ico', '.'), ('utils/*', 'utils')],  # 添加资源文件
    hiddenimports=[
        'screeninfo',
        'screeninfo.enumerators',
        'screeninfo.enumerators.win32',  # 显式添加Windows枚举器
        'screeninfo.enumerators.x11',    # Linux X11支持
        'screeninfo.enumerators.osx'     # macOS支持
        'PIL',
        'PIL._tkinter_finder',
        
    ],  # 确保包含所有依赖
    hookspath=['hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MyClock',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 设置为True可查看错误日志
    icon='icon.ico',  # 设置exe图标
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)