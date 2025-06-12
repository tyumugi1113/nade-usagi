"""
結果シーンを定義するモジュール
"""
import pygame
from src.utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT, WHITE, BLACK, GREEN, RED, SCENE_TITLE, GAME_TEXTS
from src.utils.font_manager import FontManager


class ResultScene:
    """
    結果シーンを表すクラス
    """
    def __init__(self, is_clear=False, mood=0):
        """
        結果シーンの初期化
        
        Args:
            is_clear (bool): ゲームクリアしたかどうか
            mood (int): うさぎの最終的な機嫌度
        """
        self.is_clear = is_clear
        self.mood = mood
        self.font_manager = FontManager()
        
        # 英語と日本語の両方のテキストを用意
        if self.is_clear:
            self.result_text_en = self.font_manager.render_text(GAME_TEXTS["game_clear"]["en"], 72, GREEN, False)
            self.result_text_ja = self.font_manager.render_text(GAME_TEXTS["game_clear"]["ja"], 72, GREEN, True)
            self.message_text_en = self.font_manager.render_text(GAME_TEXTS["clear_message"]["en"], 48, BLACK, False)
            self.message_text_ja = self.font_manager.render_text(GAME_TEXTS["clear_message"]["ja"], 48, BLACK, True)
        else:
            self.result_text_en = self.font_manager.render_text(GAME_TEXTS["game_over"]["en"], 72, RED, False)
            self.result_text_ja = self.font_manager.render_text(GAME_TEXTS["game_over"]["ja"], 72, RED, True)
            self.message_text_en = self.font_manager.render_text(GAME_TEXTS["over_message"]["en"], 48, BLACK, False)
            self.message_text_ja = self.font_manager.render_text(GAME_TEXTS["over_message"]["ja"], 48, BLACK, True)
        
        self.continue_text_en = self.font_manager.render_text(GAME_TEXTS["click_to_title"]["en"], 36, BLACK, False)
        self.continue_text_ja = self.font_manager.render_text(GAME_TEXTS["click_to_title"]["ja"], 36, BLACK, True)
        
        # テキスト位置の設定
        self.result_rect_en = self.result_text_en.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4 - 20))
        self.result_rect_ja = self.result_text_ja.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4 + 20))
        self.message_rect_en = self.message_text_en.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
        self.message_rect_ja = self.message_text_ja.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
        self.continue_rect_en = self.continue_text_en.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT * 3 // 4 - 20))
        self.continue_rect_ja = self.continue_text_ja.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT * 3 // 4 + 20))

    def handle_event(self, event):
        """
        イベント処理
        
        Args:
            event (pygame.event.Event): 処理するイベント
        
        Returns:
            str or None: 遷移先のシーン名、遷移しない場合はNone
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            print("Result scene: Mouse button clicked, transitioning to title scene")
            return SCENE_TITLE
        return None

    def update(self, dt):
        """
        シーンの状態を更新する
        
        Args:
            dt (float): 経過時間（秒）
        """
        pass

    def draw(self, screen):
        """
        シーンを描画する
        
        Args:
            screen (pygame.Surface): 描画対象の画面
        """
        # 背景を白で塗りつぶす
        screen.fill(WHITE)
        
        # 結果テキストを描画（英語と日本語の両方）
        screen.blit(self.result_text_en, self.result_rect_en)
        screen.blit(self.result_text_ja, self.result_rect_ja)
        screen.blit(self.message_text_en, self.message_rect_en)
        screen.blit(self.message_text_ja, self.message_rect_ja)
        screen.blit(self.continue_text_en, self.continue_rect_en)
        screen.blit(self.continue_text_ja, self.continue_rect_ja)
        
        # うさぎのイラストを描画（4足歩行版）
        rabbit_size = 60
        rabbit_x = WINDOW_WIDTH // 2
        rabbit_y = WINDOW_HEIGHT * 5 // 8
        color = GREEN if self.is_clear else (200, 200, 200)
        inner_ear_color = (255, 220, 220) if self.is_clear else (230, 200, 200)
        
        # うさぎの体（楕円）- 横長にして4足歩行らしく
        body_width = rabbit_size * 1.5
        body_height = rabbit_size * 0.8
        pygame.draw.ellipse(screen, color, 
                           (rabbit_x - body_width // 2, rabbit_y - body_height // 2, 
                            body_width, body_height))
        
        # うさぎの頭（円）- 体の前方に配置
        head_size = rabbit_size * 0.7
        head_x = rabbit_x - body_width // 3  # 左向き
        head_y = rabbit_y - body_height // 4  # 体より少し上に頭を配置
        pygame.draw.circle(screen, color, (int(head_x), int(head_y)), int(head_size // 2))
        
        # うさぎの耳（長い楕円）
        ear_width = rabbit_size // 5
        ear_length = rabbit_size * 0.9
        ear_spacing = rabbit_size // 4
        
        # 左右の耳の位置を計算
        left_ear_x = head_x - ear_spacing // 2
        right_ear_x = head_x + ear_spacing // 2
        
        # 左耳
        pygame.draw.ellipse(screen, color, 
                           (left_ear_x - ear_width // 2, head_y - head_size // 2 - ear_length,
                            ear_width, ear_length))
        
        # 右耳
        pygame.draw.ellipse(screen, color, 
                           (right_ear_x - ear_width // 2, head_y - head_size // 2 - ear_length,
                            ear_width, ear_length))
        
        # 耳の内側（ピンク）
        inner_ear_width = ear_width * 0.6
        inner_ear_length = ear_length * 0.7
        
        # 左耳の内側
        pygame.draw.ellipse(screen, inner_ear_color, 
                           (left_ear_x - inner_ear_width // 2, 
                            head_y - head_size // 2 - ear_length + ear_length * 0.15,
                            inner_ear_width, inner_ear_length))
        
        # 右耳の内側
        pygame.draw.ellipse(screen, inner_ear_color, 
                           (right_ear_x - inner_ear_width // 2, 
                            head_y - head_size // 2 - ear_length + ear_length * 0.15,
                            inner_ear_width, inner_ear_length))
        
        # 目
        eye_size = max(3, int(head_size // 8))
        eye_y = head_y - head_size // 8
        
        # 左目
        eye_x = head_x - head_size // 4
        pygame.draw.circle(screen, (0, 0, 0), (int(eye_x), int(eye_y)), eye_size)
        
        # 鼻
        nose_x = head_x - head_size // 3
        nose_y = head_y + head_size // 8
        pygame.draw.circle(screen, (255, 150, 150), (int(nose_x), int(nose_y)), max(2, eye_size // 2))
        
        # 口（クリア時は笑顔、ゲームオーバー時は悲しい顔）
        mouth_width = head_size // 2
        mouth_height = head_size // 4
        mouth_x = head_x - mouth_width // 2
        mouth_y = head_y + head_size // 4
        
        if self.is_clear:
            # 笑顔（上向きの弧）
            pygame.draw.arc(screen, (0, 0, 0), 
                           (mouth_x, mouth_y, mouth_width, mouth_height), 
                           0, 3.14, 2)
        else:
            # 悲しい顔（下向きの弧）
            pygame.draw.arc(screen, (0, 0, 0), 
                           (mouth_x, mouth_y - mouth_height, mouth_width, mouth_height), 
                           3.14, 6.28, 2)
        
        # 足（4本）
        leg_width = rabbit_size // 6
        leg_height = rabbit_size // 3
        leg_y = rabbit_y + body_height // 2 - leg_height // 2
        
        # 前足の位置（頭に近い方）
        front_legs_x = rabbit_x - body_width // 3
            
        # 後ろ足の位置（頭から遠い方）
        back_legs_x = rabbit_x + body_width // 3
        
        # 前足（左）
        pygame.draw.ellipse(screen, color, 
                           (front_legs_x - leg_width - leg_width // 2, leg_y,
                            leg_width, leg_height))
        
        # 前足（右）
        pygame.draw.ellipse(screen, color, 
                           (front_legs_x + leg_width // 2, leg_y,
                            leg_width, leg_height))
        
        # 後ろ足（左）
        pygame.draw.ellipse(screen, color, 
                           (back_legs_x - leg_width - leg_width // 2, leg_y,
                            leg_width, leg_height))
        
        # 後ろ足（右）
        pygame.draw.ellipse(screen, color, 
                           (back_legs_x + leg_width // 2, leg_y,
                            leg_width, leg_height))
        
        # しっぽ（小さな円）- 体の後ろ側に表示
        tail_size = rabbit_size // 4
        tail_x = rabbit_x + body_width // 2
        tail_y = rabbit_y
        pygame.draw.circle(screen, color, (int(tail_x), int(tail_y)), tail_size)
