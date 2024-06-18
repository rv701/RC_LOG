# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['RC_LOG_GUI.py'],
    pathex=[],
    binaries=[],
    datas=[('./RC.png', '.'),('./RC.ico', '.')],
    hiddenimports=[],
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
    name='RC_LOG',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch='universal2',
    codesign_identity='7F0F3044C3098675AFACB77F0A730B8532AA5CDA',
    entitlements_file='entitlements.plist',
)
app = BUNDLE(
    exe,
    name='RC_LOG.app',
    icon='RC.ico',
    bundle_identifier='com.techsupportdirect.RCLOG',
    version='0.0.5',
)
