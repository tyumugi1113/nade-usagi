#!/usr/bin/env python3
"""
ゲームを実行するためのスクリプト
"""
import sys
import os

# srcディレクトリをPythonパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import main

if __name__ == "__main__":
    main()
