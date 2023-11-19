# script_app.spec
block_cipher = None
# Импортируем необходимые модули PyInstaller
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import collect_submodules

# Настройки исполняемого файла
a = Analysis(['script_app.py'],
             pathex=['D:\\Repositories\\EGA_consult'],  # Путь к вашему скрипту
             binaries=[],
             datas=collect_data_files('D:\\Repositories\\EGA_consult\\app_files'),  # Путь к папке с вашими данными
             hiddenimports=collect_submodules('PyQt5'),
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

# Опции сборки
pyz = PYZ(a.pure, a.zipped_data,
          cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='EGA system',
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon='D:\\Repositories\\EGA_consult\\data\\ega_app_logo.png' )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='ega_system')
