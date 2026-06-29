#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ashley AI Studio — Master Launcher
Entry point with platform detection, dependency check, and mode routing.
"""

import sys
import os
import platform

# Windows UTF-8 setup
if platform.system() == "Windows":
    os.environ.setdefault("PYTHONUTF8", "1")
    try:
        import ctypes
        ctypes.windll.kernel32.SetConsoleOutputCP(65001)
        ctypes.windll.kernel32.SetConsoleCP(65001)
    except Exception:
        pass

from pathlib import Path
from ashley_ai_studio import main, BANNER, cyan, green, yellow, red, VERSION, FROZEN

if __name__ == "__main__":
    print(BANNER)
    print(f"{cyan('Ashley AI Studio v' + VERSION)}")
    print(f"{yellow('Platform:')} {platform.system()} {platform.release()}")
    print(f"{yellow('Python:')} {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    print(f"{yellow('Frozen:')} {FROZEN}\n")
    
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{yellow('Interrupted by user.')}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{red('FATAL ERROR:')} {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
