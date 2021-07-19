# coding: utf-8

from cx_Freeze import setup, Executable

executables = [Executable(
    'main.py', 
    targetName='BioTech Lab.exe',
    base='Win32GUI',
    icon='icon.ico')]

include_files = ['func']

options = {
    'build_exe': {
        'include_msvcr': True,
        'include_files': include_files,
    }
}

setup(name='BioTech Lab',
      version='0.0.1',
      description='First version',
      executables=executables,
      options=options)