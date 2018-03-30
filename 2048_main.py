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

    def init():
        gf.reset(ai_settings)
        gf.spawn(ai_settings, move_is_possible=True)
        gf.update_matrix(ai_settings)

        return 'Game'

    def not_game(state):
        if state == 'Win':
            pass

        if state == 'Gameover':
            gf.show_gameover(screen)
            gf.check_events(ai_settings)
            if ai_settings.reset == True:
                return 'Init'
            return 'Gameover'

    def game():



        gf.check_events(ai_settings)
        gf.drawSurface(screen, ai_settings, block_matrix)

        if ai_settings.reset == True:
            return 'Init'
        if ai_settings.gameover_check == True:
            return 'Gameover'
        if ai_settings.gamewin_check == True:
            gf.show_gamewin(screen)

        return 'Game'




    state_actions = {
        'Init': init,
        'Win': lambda: not_game('Win'),
        'Gameover': lambda: not_game('Gameover'),
        'Game': game
    }

    state = 'Init'


    while True:
        state = state_actions[state]()
        pygame.display.flip()







run_game()