"""
うさぎクラスを定義するモジュール
"""
import pygame
import math
import random
from src.utils.constants import (
    RABBIT_SIZE, RABBIT_COLOR, RABBIT_MOOD_MAX, RABBIT_VIEW_ANGLE,
    RABBIT_VIEW_DISTANCE, RABBIT_TURN_MIN_TIME, RABBIT_TURN_MAX_TIME,
    RABBIT_LOOKING_TIME, WINDOW_WIDTH, WINDOW_HEIGHT
)


class Rabbit:
    """
    うさぎを表すクラス
    """
    def __init__(self):
        """
        うさぎの初期化
        """
        self.x = WINDOW_WIDTH - 100  # 初期X座標（右側）
        self.y = WINDOW_HEIGHT // 2  # 初期Y座標
        self.size = RABBIT_SIZE
        self.color = RABBIT_COLOR
        self.mood = RABBIT_MOOD_MAX  # 機嫌度（最大値から開始）
        self.looking_back = False  # こちらを向いているかどうか（False=そっぽ向いている（右向き）、True=こちらを向いている（左向き））
        self.direction = 0  # 向いている方向（度数法、0が右、180が左）
        self.rect = pygame.Rect(self.x - self.size // 2, self.y - self.size // 2, self.size, self.size)
        
        # タイマー関連
        self.turn_timer = 0
        self.next_turn_time = random.uniform(RABBIT_TURN_MIN_TIME, RABBIT_TURN_MAX_TIME)
        self.looking_timer = 0

    def update(self, dt, player_pos, player_moving):
        """
        うさぎの状態を更新する
        
        Args:
            dt (float): 経過時間（秒）
            player_pos (tuple): プレイヤーの位置 (x, y)
            player_moving (bool): プレイヤーが移動中かどうか
        
        Returns:
            bool: プレイヤーを発見したかどうか
        """
        player_detected = False
        was_looking_back = self.looking_back  # 前フレームの状態を保存
        
        # 振り返りタイマーの更新
        if self.looking_back:
            # こちらを向いている状態（左向き）
            self.looking_timer += dt
            if self.looking_timer >= RABBIT_LOOKING_TIME:
                self.looking_back = False
                self.looking_timer = 0
                self.direction = 0  # そっぽを向く（右向き）
                print("Rabbit turned away (facing right)")
        else:
            # そっぽを向いている状態（右向き）
            self.turn_timer += dt
            if self.turn_timer >= self.next_turn_time:
                self.looking_back = True
                self.turn_timer = 0
                self.next_turn_time = random.uniform(RABBIT_TURN_MIN_TIME, RABBIT_TURN_MAX_TIME)
                self.direction = 180  # こちらを向く（左向き）
                print("Rabbit turned to look at player (facing left)")
        
        # プレイヤーの検出（こちらを向いている間のみ）
        if self.looking_back:
            player_detected = self.detect_player(player_pos, player_moving)
        
        return player_detected

    def detect_player(self, player_pos, player_moving):
        """
        プレイヤーを検出する
        
        Args:
            player_pos (tuple): プレイヤーの位置 (x, y)
            player_moving (bool): プレイヤーが移動中かどうか
        
        Returns:
            bool: プレイヤーを発見したかどうか
        """
        player_x, player_y = player_pos
        
        # プレイヤーとうさぎの距離を計算
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        # 視界内にいるかチェック
        if distance <= RABBIT_VIEW_DISTANCE:
            # 視野角内にいるかチェック
            if self.looking_back:  # こちらを向いている（左向き）
                # 左向きの場合、プレイヤーが左側にいると見える
                angle = math.degrees(math.atan2(-dy, -dx)) % 360
                angle_diff = min(abs(angle - 180), 360 - abs(angle - 180))
                
                if angle_diff <= RABBIT_VIEW_ANGLE / 2:
                    # 視野内にいて、プレイヤーが移動中ならうさぎに見つかる
                    if player_moving:
                        print(f"Rabbit detected player moving: distance={distance:.1f}, angle_diff={angle_diff:.1f}")
                        return True
        
        return False

    def decrease_mood(self, amount):
        """
        機嫌度を減少させる
        
        Args:
            amount (int): 減少量
        
        Returns:
            bool: 機嫌度が0以下になったかどうか
        """
        self.mood = max(0, self.mood - amount)
        return self.mood <= 0

    def draw(self, screen):
        """
        うさぎを描画する（4足歩行の自然なうさぎモデル）
        
        Args:
            screen (pygame.Surface): 描画対象の画面
        """
        # うさぎの体（楕円）- 横長にして4足歩行らしく
        body_width = self.size * 1.5
        body_height = self.size * 0.8
        pygame.draw.ellipse(screen, self.color, 
                           (self.x - body_width // 2, self.y - body_height // 2, 
                            body_width, body_height))
        
        # うさぎの頭（円）- 体の前方に配置
        head_size = self.size * 0.7
        head_offset_x = body_width // 3  # 体の前方に頭を配置
        
        if self.looking_back:  # こちらを向いている時は左向き
            head_x = self.x - head_offset_x
        else:  # そっぽを向いている時は右向き
            head_x = self.x + head_offset_x
            
        head_y = self.y - body_height // 4  # 体より少し上に頭を配置
        pygame.draw.circle(screen, self.color, (int(head_x), int(head_y)), int(head_size // 2))
        
        # うさぎの耳（長い楕円）
        ear_width = self.size // 5
        ear_length = self.size * 0.9
        ear_spacing = self.size // 4
        
        # 左右の耳の位置を計算
        if self.looking_back:  # こちらを向いている時は左向き
            left_ear_x = head_x - ear_spacing // 2
            right_ear_x = head_x + ear_spacing // 2
        else:  # そっぽを向いている時は右向き
            left_ear_x = head_x - ear_spacing // 2
            right_ear_x = head_x + ear_spacing // 2
        
        # 左耳
        pygame.draw.ellipse(screen, self.color, 
                           (left_ear_x - ear_width // 2, head_y - head_size // 2 - ear_length,
                            ear_width, ear_length))
        
        # 右耳
        pygame.draw.ellipse(screen, self.color, 
                           (right_ear_x - ear_width // 2, head_y - head_size // 2 - ear_length,
                            ear_width, ear_length))
        
        # 耳の内側（ピンク）
        inner_ear_width = ear_width * 0.6
        inner_ear_length = ear_length * 0.7
        
        # 左耳の内側
        pygame.draw.ellipse(screen, (255, 200, 200), 
                           (left_ear_x - inner_ear_width // 2, 
                            head_y - head_size // 2 - ear_length + ear_length * 0.15,
                            inner_ear_width, inner_ear_length))
        
        # 右耳の内側
        pygame.draw.ellipse(screen, (255, 200, 200), 
                           (right_ear_x - inner_ear_width // 2, 
                            head_y - head_size // 2 - ear_length + ear_length * 0.15,
                            inner_ear_width, inner_ear_length))
        
        # 目（うさぎの向きによって位置が変わる）
        eye_size = max(3, int(head_size // 8))
        eye_y = head_y - head_size // 8
        
        if self.looking_back:  # こちらを向いている時は左向き
            # 左目
            eye_x = head_x - head_size // 4
            pygame.draw.circle(screen, (0, 0, 0), (int(eye_x), int(eye_y)), eye_size)
            
            # 鼻
            nose_x = head_x - head_size // 3
            nose_y = head_y + head_size // 8
            pygame.draw.circle(screen, (255, 150, 150), (int(nose_x), int(nose_y)), max(2, eye_size // 2))
            
            # 口（小さな曲線）
            mouth_start = (nose_x - eye_size, nose_y + eye_size // 2)
            mouth_end = (nose_x, nose_y + eye_size)
            pygame.draw.arc(screen, (0, 0, 0), 
                           (mouth_start[0], mouth_start[1], 
                            mouth_end[0] - mouth_start[0], mouth_end[1] - mouth_start[1]), 
                           0, 3.14, 1)
            
            # 方向を示す矢印
            arrow_start = (head_x - head_size // 2, head_y)
            arrow_end = (head_x - head_size // 2 - self.size // 2, head_y)
            pygame.draw.line(screen, (100, 100, 100), arrow_start, arrow_end, 2)
            pygame.draw.polygon(screen, (100, 100, 100), [
                arrow_end,
                (arrow_end[0] + 5, arrow_end[1] - 5),
                (arrow_end[0] + 5, arrow_end[1] + 5)
            ])
            
        else:  # そっぽを向いている時は右向き
            # 右目
            eye_x = head_x + head_size // 4
            pygame.draw.circle(screen, (0, 0, 0), (int(eye_x), int(eye_y)), eye_size)
            
            # 鼻
            nose_x = head_x + head_size // 3
            nose_y = head_y + head_size // 8
            pygame.draw.circle(screen, (255, 150, 150), (int(nose_x), int(nose_y)), max(2, eye_size // 2))
            
            # 口（小さな曲線）
            mouth_start = (nose_x, nose_y + eye_size // 2)
            mouth_end = (nose_x + eye_size, nose_y + eye_size)
            pygame.draw.arc(screen, (0, 0, 0), 
                           (mouth_start[0], mouth_start[1], 
                            mouth_end[0] - mouth_start[0], mouth_end[1] - mouth_start[1]), 
                           0, 3.14, 1)
            
            # 方向を示す矢印
            arrow_start = (head_x + head_size // 2, head_y)
            arrow_end = (head_x + head_size // 2 + self.size // 2, head_y)
            pygame.draw.line(screen, (100, 100, 100), arrow_start, arrow_end, 2)
            pygame.draw.polygon(screen, (100, 100, 100), [
                arrow_end,
                (arrow_end[0] - 5, arrow_end[1] - 5),
                (arrow_end[0] - 5, arrow_end[1] + 5)
            ])
        
        # 足（4本）
        leg_width = self.size // 6
        leg_height = self.size // 3
        leg_y = self.y + body_height // 2 - leg_height // 2
        
        # 前足の位置（頭に近い方）
        if self.looking_back:  # こちらを向いている時は左向き
            front_legs_x = self.x - body_width // 3
        else:  # そっぽを向いている時は右向き
            front_legs_x = self.x + body_width // 3
            
        # 後ろ足の位置（頭から遠い方）
        if self.looking_back:  # こちらを向いている時は左向き
            back_legs_x = self.x + body_width // 3
        else:  # そっぽを向いている時は右向き
            back_legs_x = self.x - body_width // 3
        
        # 前足（左）
        pygame.draw.ellipse(screen, self.color, 
                           (front_legs_x - leg_width - leg_width // 2, leg_y,
                            leg_width, leg_height))
        
        # 前足（右）
        pygame.draw.ellipse(screen, self.color, 
                           (front_legs_x + leg_width // 2, leg_y,
                            leg_width, leg_height))
        
        # 後ろ足（左）
        pygame.draw.ellipse(screen, self.color, 
                           (back_legs_x - leg_width - leg_width // 2, leg_y,
                            leg_width, leg_height))
        
        # 後ろ足（右）
        pygame.draw.ellipse(screen, self.color, 
                           (back_legs_x + leg_width // 2, leg_y,
                            leg_width, leg_height))
        
        # しっぽ（小さな円）- 体の後ろ側に表示
        tail_size = self.size // 4
        if self.looking_back:  # こちらを向いている時は左向き
            tail_x = self.x + body_width // 2
        else:  # そっぽを向いている時は右向き
            tail_x = self.x - body_width // 2
            
        tail_y = self.y
        pygame.draw.circle(screen, self.color, (int(tail_x), int(tail_y)), tail_size)
        
        # うさぎの状態表示
        if self.looking_back:  # こちらを向いている時
            status_text = "Looking at you!"
            font = pygame.font.SysFont(None, 20)
            text_surface = font.render(status_text, True, (255, 0, 0))
            screen.blit(text_surface, (self.x - text_surface.get_width() // 2, self.y - body_height - 20))
        else:  # そっぽを向いている時
            status_text = "Looking away"
            font = pygame.font.SysFont(None, 20)
            text_surface = font.render(status_text, True, (0, 128, 0))
            screen.blit(text_surface, (self.x - text_surface.get_width() // 2, self.y - body_height - 20))

    def get_position(self):
        """
        うさぎの位置を取得する
        
        Returns:
            tuple: (x, y) 座標のタプル
        """
        return (self.x, self.y)

    def is_looking_back(self):
        """
        うさぎが振り返っているかどうかを返す
        
        Returns:
            bool: 振り返っているならTrue、そうでなければFalse
        """
        return self.looking_back

    def get_mood(self):
        """
        うさぎの機嫌度を取得する
        
        Returns:
            int: 機嫌度
        """
        return self.mood
