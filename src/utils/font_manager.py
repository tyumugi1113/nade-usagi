"""
フォント管理モジュール
"""
import pygame
import sys
from src.utils.constants import JAPANESE_FONTS

class FontManager:
    """
    フォント管理クラス
    """
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FontManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if FontManager._initialized:
            return
        
        self.default_font = None
        self.japanese_font = None
        self._find_japanese_font()
        FontManager._initialized = True
    
    def _find_japanese_font(self):
        """
        システムから日本語フォントを探す
        """
        available_fonts = pygame.font.get_fonts()
        
        # 日本語フォントの候補から使用可能なものを探す
        for font_name in JAPANESE_FONTS:
            if font_name.lower() in available_fonts:
                self.japanese_font = font_name
                print(f"Found Japanese font: {font_name}")
                return
        
        # 候補が見つからない場合はシステムのデフォルトフォントを使用
        print("No Japanese font found. Using default font.")
        self.japanese_font = None
    
    def get_font(self, size, use_japanese=True):
        """
        指定したサイズのフォントを取得する
        
        Args:
            size (int): フォントサイズ
            use_japanese (bool): 日本語フォントを使用するかどうか
        
        Returns:
            pygame.font.Font: フォントオブジェクト
        """
        if use_japanese and self.japanese_font:
            try:
                return pygame.font.SysFont(self.japanese_font, size)
            except:
                print(f"Failed to load Japanese font: {self.japanese_font}")
        
        # 日本語フォントが使用できない場合はデフォルトフォントを使用
        return pygame.font.SysFont(None, size)
    
    def render_text(self, text, size, color, use_japanese=True):
        """
        テキストをレンダリングする
        
        Args:
            text (str): レンダリングするテキスト
            size (int): フォントサイズ
            color (tuple): 色 (R, G, B)
            use_japanese (bool): 日本語フォントを使用するかどうか
        
        Returns:
            pygame.Surface: レンダリングされたテキスト
        """
        font = self.get_font(size, use_japanese)
        return font.render(text, True, color)
