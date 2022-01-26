# coding: utf-8

from cx_Freeze import Executable, setup

executables = [Executable(
    'main.py',
    targetName='BioTech Lab.exe',
    base='Win32GUI',
    icon='icon.ico'
    )
]

include_files = ['func', 'data', 'style']
excludes = []

options = {
    'build_exe': {
        'include_msvcr': True,
        'include_files': include_files,
        'build_exe': 'build_windows',
        'excludes': excludes,
    }
}

setup(name='BioTech Lab',
      version='0.0.1',
      description='First version',
      executables=executables,
      options=options)
