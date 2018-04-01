import pygame
from blockmatrix import BlockMatrix
from settings import Settings
import game_functions as gf

def run_game():

    pygame.init()
    block_matrix = BlockMatrix()
    ai_settings = Settings(block_matrix)
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height + 120))
    screen.fill((100, 100, 100))
    clock = pygame.time.Clock()

    def init():
        #遊戲初始重置，所有參數初始並且產生兩個隨機數
        gf.reset(ai_settings)
        gf.spawn(ai_settings, move_is_possible=True)
        gf.update_matrix(ai_settings)
        return 'Game'

    def not_game(state):
        #目前只有設定遊戲結束時是否重置或結束遊戲
        if state == 'Win':
            pass
        if state == 'Gameover':
            gf.show_gameover(screen)
            gf.check_events(ai_settings)
            if ai_settings.reset == True:
                return 'Init'
            return 'Gameover'

    def game():
        #遊戲中，用戶按鍵檢測，是否下一步，以及贏或輸
        gf.check_events(ai_settings)
        gf.drawSurface(screen, ai_settings, block_matrix)

        if ai_settings.reset == True:
            return 'Init'
        if ai_settings.gameover_check == True:
            return 'Gameover'
        if ai_settings.gamewin_check == True:
            gf.show_gamewin(screen)
        return 'Game'

    #有限狀態機四種要素，並用狀態轉移函數描述將轉移到哪個狀態
    #這些函數名存在字典裡，方便循環中的調用
    state_actions = {
        'Init': init,
        'Win': lambda: not_game('Win'),
        'Gameover': lambda: not_game('Gameover'),
        'Game': game
    }
    state = 'Init'


    while True:
        #狀態機開始循環
        clock.tick(60)
        state = state_actions[state]()
        pygame.display.flip()

run_game()