#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Launcher для Metallurgy Advisor Pro — совместим с PyInstaller (--onefile)
Запускает Streamlit через внутренний bootstrap API, без subprocess.
"""

import os
import sys
import tempfile
import threading
import time
import webbrowser
from pathlib import Path

APP_CODE_RESOURCE = "metallurgy_advisor_pro.py"
PORT = 8501


def get_app_script_path():
    """
    В замороженном EXE скрипт хранится как data-файл рядом с EXE.
    В режиме разработки — просто ищем .py рядом с launcher.
    """
    if getattr(sys, 'frozen', False):
        # PyInstaller распаковывает data-файлы во временный каталог _MEIPASS
        base = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    else:
        base = os.path.dirname(os.path.abspath(__file__))

    candidates = [
        os.path.join(base, APP_CODE_RESOURCE),
        os.path.join(os.path.dirname(sys.executable), APP_CODE_RESOURCE),
        os.path.join(os.getcwd(), APP_CODE_RESOURCE),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None


def open_browser_delayed(url: str, delay: float = 3.0):
    """Открывает браузер через delay секунд."""
    def _open():
        time.sleep(delay)
        try:
            webbrowser.open(url, new=2, autoraise=True)
        except Exception:
            pass
    t = threading.Thread(target=_open, daemon=True)
    t.start()


def main():
    print("\n" + "=" * 60)
    print("  🏭 Metallurgy Advisor Pro")
    print("=" * 60)

    app_file = get_app_script_path()
    if app_file is None:
        print(f"\n❌ ОШИБКА: файл {APP_CODE_RESOURCE!r} не найден.")
        print("   Поместите его в одну папку с EXE.")
        input("\nНажмите Enter для выхода...")
        return 1

    print(f"\n  📄 Приложение: {app_file}")
    print(f"  🌐 URL:         http://localhost:{PORT}")
    print("\n  Если браузер не открылся — перейдите по ссылке выше.")
    print("  Для остановки нажмите Ctrl+C.\n")
    print("=" * 60 + "\n")

    # Открываем браузер через 3 секунды (пока сервер стартует)
    open_browser_delayed(f"http://localhost:{PORT}", delay=3.0)

    # Запускаем Streamlit через внутренний bootstrap
    # Это работает и в обычном режиме, и внутри PyInstaller-EXE
    from streamlit.web import bootstrap

    flag_options = {
        "server.port": PORT,
        "server.headless": True,          # не открывает браузер самостоятельно
        "logger.level": "warning",
        "client.showErrorDetails": False,
        "client.toolbarMode": "minimal",
        "global.developmentMode": False,
    }

    bootstrap.run(
        main_script_path=app_file,
        is_hello=False,
        args=[],
        flag_options=flag_options,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
