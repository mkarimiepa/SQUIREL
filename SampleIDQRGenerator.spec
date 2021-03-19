# -*- mode: python ; coding: utf-8 -*-
# -*- mode: python ; coding: utf-8 -*-
from kivy_deps import sdl2, glew
from kivy.app import App


block_cipher = None


a = Analysis(['SampleIDQRGenerator.py'],
             pathex=['C:\\Users\\MKARIMI\\PycharmProjects\\SampleIDQRGenerator'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='SampleIDQRGenerator',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='SampleIDQRGenerator')
