# coding: utf-8

from cx_Freeze import setup, Executable

executables = [Executable(
    'main.py',
    targetName='BioTech Lab.exe',
    base='Win32GUI',
    icon='icon.ico')]

include_files = ['func', 'data', 'style']

options = {
    'build_exe': {
        'include_msvcr': True,
        'include_files': include_files,
        'build_exe': 'build_windows',
    }
}

setup(name='BioTech Lab',
      version='0.0.1',
      description='First version',
      executables=executables,
      options=options)