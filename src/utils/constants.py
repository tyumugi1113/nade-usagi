"""
定数を定義するモジュール
"""

# ウィンドウ設定
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Rabbit Petting Game"  # 英語タイトルに変更
FPS = 60

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BACKGROUND_COLOR = (200, 230, 200)  # 薄い緑色の背景

# フォント設定
FONT_NAME = None  # デフォルトフォント
# 日本語フォントの候補（システムに存在するものを使用）
JAPANESE_FONTS = ['IPAGothic', 'IPAPGothic', 'MS Gothic', 'Yu Gothic', 'Noto Sans CJK JP', 'Meiryo', 'TakaoGothic']

# プレイヤー設定
PLAYER_SPEED = 3
PLAYER_SIZE = 30
PLAYER_COLOR = (50, 100, 200)  # より人間らしい青色に変更

# うさぎ設定
RABBIT_SIZE = 40
RABBIT_COLOR = (240, 240, 240)  # より白いウサギらしい色に変更
RABBIT_MOOD_MAX = 100  # 機嫌度の最大値
RABBIT_VIEW_ANGLE = 140  # うさぎの視野角（度）- 少し広げて120度から140度に変更
RABBIT_VIEW_DISTANCE = 200  # うさぎの視界距離
RABBIT_TURN_MIN_TIME = 3  # うさぎが振り返るまでの最小時間（秒）
RABBIT_TURN_MAX_TIME = 8  # うさぎが振り返るまでの最大時間（秒）
RABBIT_LOOKING_TIME = 2  # うさぎが振り返っている時間（秒）

# ゲーム設定
PETTING_DISTANCE = 50  # うさぎを撫でられる距離
MOOD_DECREASE = 15  # 発見されたときの機嫌度減少量（20から15に減少）

# シーン識別子
SCENE_TITLE = "title"
SCENE_GAME = "game"
SCENE_RESULT = "result"

# アセットパス
ASSETS_DIR = "assets"
IMAGES_DIR = f"{ASSETS_DIR}/images"
SOUNDS_DIR = f"{ASSETS_DIR}/sounds"

# ゲームテキスト（英語と日本語の両方を用意）
GAME_TEXTS = {
    "title": {
        "en": "Rabbit Petting Game",
        "ja": "うさぎを撫でろ！"
    },
    "start": {
        "en": "Click to Start",
        "ja": "クリックしてスタート"
    },
    "game_over": {
        "en": "Game Over",
        "ja": "ゲームオーバー"
    },
    "game_clear": {
        "en": "Game Clear!",
        "ja": "ゲームクリア！"
    },
    "found": {
        "en": "Found!",
        "ja": "見つかった！"
    },
    "rabbit_looking": {
        "en": "Rabbit is looking at you!",
        "ja": "うさぎがこちらを見ています！"
    },
    "petted": {
        "en": "You petted the rabbit!",
        "ja": "うさぎを撫でた！"
    },
    "mood": {
        "en": "Mood: ",
        "ja": "機嫌度: "
    },
    "click_to_title": {
        "en": "Click to return to title",
        "ja": "クリックしてタイトルに戻る"
    },
    "left_click": {
        "en": "Left Click: Move",
        "ja": "左クリック: 移動"
    },
    "right_click": {
        "en": "Right Click: Stop",
        "ja": "右クリック: 停止"
    },
    "clear_message": {
        "en": "You successfully petted the rabbit!",
        "ja": "うさぎを撫でることができました！"
    },
    "over_message": {
        "en": "The rabbit got upset...",
        "ja": "うさぎの機嫌を損ねてしまいました..."
    },
    "dont_move": {
        "en": "Don't move when rabbit is looking at you!",
        "ja": "うさぎがこちらを見ている時は動かないで！"
    },
    "move_ok": {
        "en": "You can move now!",
        "ja": "今なら動けます！"
    }
}

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BACKGROUND_COLOR = (200, 230, 200)  # 薄い緑色の背景

# プレイヤー設定
PLAYER_SPEED = 3
PLAYER_SIZE = 30
PLAYER_COLOR = (50, 100, 200)  # より人間らしい青色に変更

# うさぎ設定
RABBIT_SIZE = 40
RABBIT_COLOR = (240, 240, 240)  # より白いウサギらしい色に変更
RABBIT_MOOD_MAX = 100  # 機嫌度の最大値
RABBIT_VIEW_ANGLE = 140  # うさぎの視野角（度）- 少し広げて120度から140度に変更
RABBIT_VIEW_DISTANCE = 200  # うさぎの視界距離
RABBIT_TURN_MIN_TIME = 3  # うさぎが振り返るまでの最小時間（秒）
RABBIT_TURN_MAX_TIME = 8  # うさぎが振り返るまでの最大時間（秒）
RABBIT_LOOKING_TIME = 2  # うさぎが振り返っている時間（秒）

# ゲーム設定
PETTING_DISTANCE = 50  # うさぎを撫でられる距離
MOOD_DECREASE = 15  # 発見されたときの機嫌度減少量（20から15に減少）

# シーン識別子
SCENE_TITLE = "title"
SCENE_GAME = "game"
SCENE_RESULT = "result"

# アセットパス
ASSETS_DIR = "assets"
IMAGES_DIR = f"{ASSETS_DIR}/images"
SOUNDS_DIR = f"{ASSETS_DIR}/sounds"
