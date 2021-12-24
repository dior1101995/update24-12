# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['C:/Users/NamCuong/Desktop/Auto/New_BotChucNang_14_12.py'],
             pathex=[],
             binaries=[],
             datas=[('C:/Users/NamCuong/Desktop/Auto/New_Data', 'New_Data/'), ('C:/Users/NamCuong/Desktop/Auto/Gui', 'Gui/'), ('C:/Users/NamCuong/Desktop/Auto/DataText', 'DataText/'), ('C:/Users/NamCuong/Desktop/Auto/adb.exe', '.'), ('C:/Users/NamCuong/Desktop/Auto/AdbAdress.cmd', '.'), ('C:/Users/NamCuong/Desktop/Auto/AdbWinApi.dll', '.'), ('C:/Users/NamCuong/Desktop/Auto/AdbWinUsbApi.dll', '.'), ('C:/Users/NamCuong/Desktop/Auto/icon.PNG', '.'), ('C:/Users/NamCuong/Desktop/Auto/icon2.ico', '.'), ('C:/Users/NamCuong/Desktop/Auto/lic.txt', '.')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
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
          name='New_BotChucNang_14_12',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , icon='C:\\Users\\NamCuong\\Desktop\\Auto\\icon2.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='New_BotChucNang_14_12')
