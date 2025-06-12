"""
ゲームシーンを定義するモジュール
"""
import pygame
import math
from src.utils.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WHITE, BLACK, RED, GREEN, YELLOW,
    BACKGROUND_COLOR, MOOD_DECREASE, PETTING_DISTANCE, SCENE_RESULT,
    GAME_TEXTS
)
from src.player import Player
from src.rabbit import Rabbit
from src.utils.font_manager import FontManager


class GameScene:
    """
    ゲームシーンを表すクラス
    """
    def __init__(self):
        """
        ゲームシーンの初期化
        """
        self.player = Player()
        self.rabbit = Rabbit()
        self.font_manager = FontManager()
        self.game_over = False
        self.game_clear = False
        self.result_timer = 0
        self.result_delay = 2.0  # 結果表示までの遅延（秒）
        self.warning_timer = 0
        self.warning_visible = False

    def handle_event(self, event):
        """
        イベント処理
        
        Args:
            event (pygame.event.Event): 処理するイベント
        
        Returns:
            str or None: 遷移先のシーン名、遷移しない場合はNone
        """
        if self.game_over or self.game_clear:
            # ゲーム終了後は結果シーンへの遷移を待つのみ
            return None
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左クリック
                # うさぎがこちらを向いている場合は移動しない（警告表示のみ）
                if self.rabbit.is_looking_back():
                    self.warning_timer = 1.0
                    self.warning_visible = True
                    # うさぎがこちらを向いている時に動こうとした場合も機嫌度を減少
                    game_over = self.rabbit.decrease_mood(MOOD_DECREASE)
                    print(f"Game scene: Player tried to move while rabbit is looking. Mood decreased to {self.rabbit.get_mood()}")
                    if game_over:
                        print("Game scene: Player detected too many times, game over")
                        self.game_over = True
                else:
                    # うさぎがそっぽを向いている場合は移動可能
                    self.player.set_target(event.pos[0], event.pos[1])
                    
                    # うさぎに十分近い場合は撫でる判定
                    rabbit_pos = self.rabbit.get_position()
                    player_pos = self.player.get_position()
                    distance = math.sqrt((rabbit_pos[0] - player_pos[0])**2 + 
                                         (rabbit_pos[1] - player_pos[1])**2)
                    
                    if distance <= PETTING_DISTANCE:
                        print("Game scene: Player petted the rabbit, game clear")
                        self.game_clear = True
            
            elif event.button == 3:  # 右クリック
                self.player.stop_moving()
        
        return None

    def update(self, dt):
        """
        シーンの状態を更新する
        
        Args:
            dt (float): 経過時間（秒）
        
        Returns:
            str or None: 遷移先のシーン名、遷移しない場合はNone
        """
        if self.game_over or self.game_clear:
            self.result_timer += dt
            if self.result_timer >= self.result_delay:
                print(f"Game scene: Result timer complete, transitioning to result scene. Game over: {self.game_over}, Game clear: {self.game_clear}")
                return SCENE_RESULT
            return None
        
        # プレイヤーの更新
        self.player.update()
        
        # うさぎがこちらを向いた瞬間にプレイヤーが移動中なら停止させる
        if self.rabbit.is_looking_back() and self.player.is_moving():
            # プレイヤーを強制停止
            self.player.stop_moving()
            # 警告表示
            self.warning_timer = 1.0
            self.warning_visible = True
            # 機嫌度を減少させる
            game_over = self.rabbit.decrease_mood(MOOD_DECREASE)
            print(f"Game scene: Rabbit turned to look while player was moving, player forced to stop. Mood decreased to {self.rabbit.get_mood()}")
            if game_over:
                print("Game scene: Player detected too many times, game over")
                self.game_over = True
        
        # うさぎの更新
        player_detected = self.rabbit.update(dt, self.player.get_position(), self.player.is_moving())
        
        # プレイヤーが検出された場合
        if player_detected:
            self.warning_timer = 1.0  # 警告表示時間
            self.warning_visible = True
            # 機嫌度を減少させる（一度に減少する量を調整）
            game_over = self.rabbit.decrease_mood(MOOD_DECREASE)
            print(f"Game scene: Player detected moving while rabbit was looking, mood decreased to {self.rabbit.get_mood()}")
            if game_over:
                print("Game scene: Player detected too many times, game over")
                self.game_over = True
        
        # 警告表示の更新
        if self.warning_visible:
            self.warning_timer -= dt
            if self.warning_timer <= 0:
                self.warning_visible = False
        
        return None

    def draw(self, screen):
        """
        シーンを描画する
        
        Args:
            screen (pygame.Surface): 描画対象の画面
        """
        # 背景を描画
        screen.fill(BACKGROUND_COLOR)
        
        # プレイヤーとうさぎを描画
        self.player.draw(screen)
        self.rabbit.draw(screen)
        
        # 機嫌ゲージを描画
        self._draw_mood_gauge(screen)
        
        # 警告表示
        if self.warning_visible:
            warning_text_en = self.font_manager.render_text(GAME_TEXTS["found"]["en"], 36, RED, False)
            warning_text_ja = self.font_manager.render_text(GAME_TEXTS["found"]["ja"], 36, RED, True)
            screen.blit(warning_text_en, (WINDOW_WIDTH // 2 - warning_text_en.get_width() // 2, 30))
            screen.blit(warning_text_ja, (WINDOW_WIDTH // 2 - warning_text_ja.get_width() // 2, 70))
        
        # うさぎの状態表示
        if self.rabbit.is_looking_back():
            status_text_en = self.font_manager.render_text(GAME_TEXTS["rabbit_looking"]["en"], 24, RED, False)
            status_text_ja = self.font_manager.render_text(GAME_TEXTS["rabbit_looking"]["ja"], 24, RED, True)
            screen.blit(status_text_en, (WINDOW_WIDTH // 2 - status_text_en.get_width() // 2, 10))
            screen.blit(status_text_ja, (WINDOW_WIDTH // 2 - status_text_ja.get_width() // 2, 35))
        
        # ゲームオーバー表示
        if self.game_over:
            game_over_text_en = self.font_manager.render_text(GAME_TEXTS["game_over"]["en"], 36, RED, False)
            game_over_text_ja = self.font_manager.render_text(GAME_TEXTS["game_over"]["ja"], 36, RED, True)
            screen.blit(game_over_text_en, 
                       (WINDOW_WIDTH // 2 - game_over_text_en.get_width() // 2, 
                        WINDOW_HEIGHT // 2 - game_over_text_en.get_height() - 10))
            screen.blit(game_over_text_ja, 
                       (WINDOW_WIDTH // 2 - game_over_text_ja.get_width() // 2, 
                        WINDOW_HEIGHT // 2 + 10))
        
        # ゲームクリア表示
        if self.game_clear:
            clear_text_en = self.font_manager.render_text(GAME_TEXTS["petted"]["en"], 36, GREEN, False)
            clear_text_ja = self.font_manager.render_text(GAME_TEXTS["petted"]["ja"], 36, GREEN, True)
            screen.blit(clear_text_en, 
                       (WINDOW_WIDTH // 2 - clear_text_en.get_width() // 2, 
                        WINDOW_HEIGHT // 2 - clear_text_en.get_height() - 10))
            screen.blit(clear_text_ja, 
                       (WINDOW_WIDTH // 2 - clear_text_ja.get_width() // 2, 
                        WINDOW_HEIGHT // 2 + 10))
        
        # 操作説明
        help_text1_en = self.font_manager.render_text(GAME_TEXTS["left_click"]["en"], 24, BLACK, False)
        help_text1_ja = self.font_manager.render_text(GAME_TEXTS["left_click"]["ja"], 24, BLACK, True)
        help_text2_en = self.font_manager.render_text(GAME_TEXTS["right_click"]["en"], 24, BLACK, False)
        help_text2_ja = self.font_manager.render_text(GAME_TEXTS["right_click"]["ja"], 24, BLACK, True)
        
        screen.blit(help_text1_en, (10, WINDOW_HEIGHT - 80))
        screen.blit(help_text1_ja, (10, WINDOW_HEIGHT - 60))
        screen.blit(help_text2_en, (10, WINDOW_HEIGHT - 40))
        screen.blit(help_text2_ja, (10, WINDOW_HEIGHT - 20))
        
        # うさぎがこちらを向いている時の注意表示
        if self.rabbit.is_looking_back():
            caution_text_en = self.font_manager.render_text(GAME_TEXTS["dont_move"]["en"], 24, RED, False)
            caution_text_ja = self.font_manager.render_text(GAME_TEXTS["dont_move"]["ja"], 24, RED, True)
            screen.blit(caution_text_en, (WINDOW_WIDTH // 2 - caution_text_en.get_width() // 2, WINDOW_HEIGHT - 40))
            screen.blit(caution_text_ja, (WINDOW_WIDTH // 2 - caution_text_ja.get_width() // 2, WINDOW_HEIGHT - 20))
        else:
            # うさぎがそっぽを向いている時は移動OKの表示
            move_text_en = self.font_manager.render_text(GAME_TEXTS["move_ok"]["en"], 24, GREEN, False)
            move_text_ja = self.font_manager.render_text(GAME_TEXTS["move_ok"]["ja"], 24, GREEN, True)
            screen.blit(move_text_en, (WINDOW_WIDTH // 2 - move_text_en.get_width() // 2, WINDOW_HEIGHT - 40))
            screen.blit(move_text_ja, (WINDOW_WIDTH // 2 - move_text_ja.get_width() // 2, WINDOW_HEIGHT - 20))

    def _draw_mood_gauge(self, screen):
        """
        うさぎの機嫌ゲージを描画する
        
        Args:
            screen (pygame.Surface): 描画対象の画面
        """
        gauge_width = 200
        gauge_height = 20
        gauge_x = WINDOW_WIDTH - gauge_width - 20
        gauge_y = 20
        
        # ゲージの背景
        pygame.draw.rect(screen, WHITE, (gauge_x, gauge_y, gauge_width, gauge_height))
        pygame.draw.rect(screen, BLACK, (gauge_x, gauge_y, gauge_width, gauge_height), 2)
        
        # 現在の機嫌度に応じたゲージ
        mood_ratio = self.rabbit.get_mood() / 100.0
        current_width = int(gauge_width * mood_ratio)
        
        # 機嫌度に応じて色を変える
        if mood_ratio > 0.6:
            color = GREEN
        elif mood_ratio > 0.3:
            color = YELLOW
        else:
            color = RED
        
        pygame.draw.rect(screen, color, (gauge_x, gauge_y, current_width, gauge_height))
        
        # ラベル
        mood_text_en = self.font_manager.render_text(f"{GAME_TEXTS['mood']['en']}{self.rabbit.get_mood()}", 24, BLACK, False)
        mood_text_ja = self.font_manager.render_text(f"{GAME_TEXTS['mood']['ja']}{self.rabbit.get_mood()}", 24, BLACK, True)
        screen.blit(mood_text_en, (gauge_x, gauge_y - 50))
        screen.blit(mood_text_ja, (gauge_x, gauge_y - 25))
