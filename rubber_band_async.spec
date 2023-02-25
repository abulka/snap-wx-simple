# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['src/rubber_band_async.py'],
             pathex=['/Users/Andy/Devel/wxpython-github-actions/wxpython-actions-multi'],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='rubber_band_async',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='icons/Dakirby309-Simply-Styled-Mac-Front-Row.icns')
app = BUNDLE(exe,
             name='rubber_band_async.app',
             icon='icons/Dakirby309-Simply-Styled-Mac-Front-Row.icns',
             bundle_identifier=None)
