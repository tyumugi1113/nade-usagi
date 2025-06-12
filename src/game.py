"""
ゲームのメインクラスを定義するモジュール
"""
import pygame
import sys
from src.utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, FPS, SCENE_TITLE, SCENE_GAME, SCENE_RESULT
from src.scenes.title_scene import TitleScene
from src.scenes.game_scene import GameScene
from src.scenes.result_scene import ResultScene


class Game:
    """
    ゲームのメインクラス
    """
    def __init__(self):
        """
        ゲームの初期化
        """
        pygame.init()
        
        # 日本語フォントの初期化に関する情報を表示
        print("Available system fonts:")
        available_fonts = pygame.font.get_fonts()
        print(f"Total fonts: {len(available_fonts)}")
        print(f"Sample fonts: {available_fonts[:10]}")
        
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_scene = None
        self.scenes = {}
        self._init_scenes()

    def _init_scenes(self):
        """
        シーンを初期化する
        """
        self.scenes = {
            SCENE_TITLE: TitleScene()
        }
        self.current_scene = SCENE_TITLE

    def run(self):
        """
        ゲームのメインループを実行する
        """
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # 経過時間（秒）
            
            # イベント処理
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                
                # 現在のシーンにイベントを渡す
                next_scene = self.scenes[self.current_scene].handle_event(event)
                if next_scene:
                    self._change_scene(next_scene)
            
            # シーンの更新
            next_scene = self.scenes[self.current_scene].update(dt)
            if next_scene:
                self._change_scene(next_scene)
            
            # 描画
            self.scenes[self.current_scene].draw(self.screen)
            pygame.display.flip()
        
        pygame.quit()
        sys.exit()

    def _change_scene(self, scene_name):
        """
        シーンを変更する
        
        Args:
            scene_name (str): 変更先のシーン名
        """
        print(f"Changing scene to: {scene_name}")
        
        # 常に新しいシーンインスタンスを作成
        if scene_name == SCENE_TITLE:
            self.scenes[SCENE_TITLE] = TitleScene()
        elif scene_name == SCENE_GAME:
            self.scenes[SCENE_GAME] = GameScene()
        elif scene_name == SCENE_RESULT and SCENE_GAME in self.scenes:
            # ゲームシーンからの情報を取得
            game_scene = self.scenes[SCENE_GAME]
            is_clear = game_scene.game_clear
            mood = game_scene.rabbit.get_mood()
            self.scenes[SCENE_RESULT] = ResultScene(is_clear, mood)
        
        self.current_scene = scene_name
