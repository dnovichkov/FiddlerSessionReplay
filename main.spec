# -*- mode: python -*-


import os
import shutil

dist_dir_name = 'dist'
shutil.rmtree(dist_dir_name)

import datetime
current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
os.remove("version.py")
with open("version.py", 'w') as f:
    dt_str = "VERSION = '" + current_datetime + "'\n"
    git_sha = os.popen("git log -1 --pretty=format:%h").read()
    hash_str = "GIT_HASH = '" + git_sha + "'\n"
    f.writelines([dt_str, hash_str])

block_cipher = None


a = Analysis(['main.py'],
             pathex=[],
             binaries=[],
             datas=[
                ('FiddlerSession2.saz', '.'),
                ('README.rst', '.'),
                ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='fiddler_replay',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='main')

archive_filename = 'dist_' + current_datetime
dist_dir_name += '/main'
shutil.make_archive(archive_filename, 'zip', dist_dir_name)
