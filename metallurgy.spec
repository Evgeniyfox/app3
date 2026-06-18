# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec для Metallurgy Advisor Pro
# Версия: 1.0  |  Python 3.11+  |  Streamlit 1.58

import sys
from PyInstaller.utils.hooks import collect_all

datas, binaries, hiddenimports = [], [], []

# Собираем все пакеты целиком
for pkg in ['streamlit', 'sklearn', 'matplotlib', 'seaborn', 'joblib',
            'pandas', 'numpy', 'docx', 'openpyxl', 'altair', 'pydeck',
            'pyarrow', 'packaging']:
    try:
        d, b, h = collect_all(pkg)
        datas += d; binaries += b; hiddenimports += h
    except Exception as e:
        print(f'[WARN] {pkg}: {e}')

# Основной скрипт кладётся рядом с EXE — Streamlit читает его с диска
datas += [('metallurgy_advisor_pro.py', '.')]

hiddenimports += [
    'streamlit.runtime.scriptrunner',
    'streamlit.web.bootstrap',
    'streamlit.web.cli',
    'sklearn.ensemble._gb',
    'sklearn.utils._cython_blas',
    'sklearn.tree._utils',
]

a = Analysis(
    ['launcher_pyinstaller.py'],
    pathex=['.'],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=['tkinter', 'PyQt5', 'wx', 'IPython', 'notebook'],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='MetallurgyAdvisorPro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,           # Показывать консоль (удобно видеть статус)
    icon=None,
)
