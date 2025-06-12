"""
プレイヤークラスを定義するモジュール
"""
import pygame
from src.utils.constants import PLAYER_SIZE, PLAYER_COLOR, PLAYER_SPEED, WINDOW_WIDTH, WINDOW_HEIGHT


class Player:
    """
    プレイヤーを表すクラス
    """
    def __init__(self):
        """
        プレイヤーの初期化
        """
        self.x = 50  # 初期X座標（左側）
        self.y = WINDOW_HEIGHT // 2  # 初期Y座標
        self.size = PLAYER_SIZE
        self.color = PLAYER_COLOR
        self.speed = PLAYER_SPEED
        self.target_x = self.x
        self.target_y = self.y
        self.moving = False
        self.rect = pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)

    def set_target(self, x, y):
        """
        移動先を設定する
        
        Args:
            x (int): 目標X座標
            y (int): 目標Y座標
        """
        self.target_x = x
        self.target_y = y
        self.moving = True
        print(f"Player moving to: ({x}, {y})")

    def stop_moving(self):
        """
        移動を停止する
        """
        if self.moving:
            print(f"Player forced to stop at: ({self.x}, {self.y})")
        self.moving = False
        self.target_x = self.x
        self.target_y = self.y

    def update(self):
        """
        プレイヤーの状態を更新する
        """
        if self.moving:
            # 目標地点への移動ベクトルを計算
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            
            # 目標地点に到達したら停止
            if distance < self.speed:
                self.x = self.target_x
                self.y = self.target_y
                self.moving = False
                print(f"Player stopped at target: ({self.x}, {self.y})")
            else:
                # 正規化して速度を適用
                self.x += (dx / distance) * self.speed
                self.y += (dy / distance) * self.speed
        
        # 画面外に出ないように制限
        self.x = max(self.size // 2, min(WINDOW_WIDTH - self.size // 2, self.x))
        self.y = max(self.size // 2, min(WINDOW_HEIGHT - self.size // 2, self.y))
        
        # 衝突判定用の矩形を更新
        self.rect.x = self.x - self.size // 2
        self.rect.y = self.y - self.size // 2

    def draw(self, screen):
        """
        プレイヤーを描画する（人間らしいアイコン）
        
        Args:
            screen (pygame.Surface): 描画対象の画面
        """
        # 体（円）
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size // 2)
        
        # 頭（小さい円）
        head_size = self.size // 3
        head_y = self.y - self.size // 2 - head_size // 2
        pygame.draw.circle(screen, self.color, (int(self.x), int(head_y)), head_size)
        
        # 目
        eye_size = max(2, head_size // 5)
        eye_y = head_y - eye_size // 2
        left_eye_x = self.x - head_size // 3
        right_eye_x = self.x + head_size // 3
        pygame.draw.circle(screen, (255, 255, 255), (int(left_eye_x), int(eye_y)), eye_size)
        pygame.draw.circle(screen, (255, 255, 255), (int(right_eye_x), int(eye_y)), eye_size)
        pygame.draw.circle(screen, (0, 0, 0), (int(left_eye_x), int(eye_y)), max(1, eye_size // 2))
        pygame.draw.circle(screen, (0, 0, 0), (int(right_eye_x), int(eye_y)), max(1, eye_size // 2))
        
        # 腕
        arm_length = self.size // 2
        arm_width = max(2, self.size // 8)
        left_arm_start = (self.x - self.size // 3, self.y - self.size // 4)
        left_arm_end = (self.x - self.size // 2 - arm_length // 2, self.y)
        right_arm_start = (self.x + self.size // 3, self.y - self.size // 4)
        right_arm_end = (self.x + self.size // 2 + arm_length // 2, self.y)
        
        pygame.draw.line(screen, self.color, left_arm_start, left_arm_end, arm_width)
        pygame.draw.line(screen, self.color, right_arm_start, right_arm_end, arm_width)
        
        # 足
        leg_length = self.size // 2
        leg_width = max(2, self.size // 6)
        left_leg_start = (self.x - self.size // 4, self.y + self.size // 3)
        left_leg_end = (self.x - self.size // 3, self.y + self.size // 2 + leg_length)
        right_leg_start = (self.x + self.size // 4, self.y + self.size // 3)
        right_leg_end = (self.x + self.size // 3, self.y + self.size // 2 + leg_length)
        
        pygame.draw.line(screen, self.color, left_leg_start, left_leg_end, leg_width)
        pygame.draw.line(screen, self.color, right_leg_start, right_leg_end, leg_width)

    def get_position(self):
        """
        プレイヤーの位置を取得する
        
        Returns:
            tuple: (x, y) 座標のタプル
        """
        return (self.x, self.y)

    def is_moving(self):
        """
        プレイヤーが移動中かどうかを返す
        
        Returns:
            bool: 移動中ならTrue、そうでなければFalse
        """
        return self.moving
