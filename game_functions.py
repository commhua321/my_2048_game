import pygame
import random
import sys
import numpy

def check_events(ai_settings):

    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings)

def check_keydown_events(event, ai_settings):

    if event.key == pygame.K_RIGHT:
        invert_matrix(ai_settings)
        update_matrix(ai_settings)
        invert_matrix(ai_settings)
    elif event.key == pygame.K_LEFT:
        update_matrix(ai_settings)
    elif event.key == pygame.K_UP:
        inver_rotate_matrix(ai_settings)
        update_matrix(ai_settings)
        rotate_matrix(ai_settings)
    elif event.key == pygame.K_DOWN:
        rotate_matrix(ai_settings)
        update_matrix(ai_settings)
        inver_rotate_matrix(ai_settings)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_r:
        ai_settings.reset = True

def update_matrix(ai_settings):

    #2. 以左移為基礎

    #3. [4040] -> [4400] 把所有元素放一邊整理更新，並判斷是否可移動
    temp_matrix = ai_settings.matrix.copy()
    tighten_row(ai_settings)
    #4. [4400] -> [8000]

    #判斷是否可移動
    move_is_possible = True
    if (temp_matrix == merge_row(ai_settings)).all():
        move_is_possible = False
    #5. 計算0的所有index加入至zerolist
    get_zerolist(ai_settings)
    #6. spawn一個數出來
    spawn(ai_settings, move_is_possible)
    ai_settings.gamewin_check = gamewin_check(ai_settings)
    ai_settings.gameover_check = gameover_check(ai_settings)

def inver_rotate_matrix(ai_settings):

    invert_matrix(ai_settings)
    ai_settings.matrix = numpy.transpose(ai_settings.matrix)
    return ai_settings.matrix

def rotate_matrix(ai_settings):

    ai_settings.matrix = numpy.transpose(ai_settings.matrix)
    invert_matrix(ai_settings)
    return ai_settings.matrix

def invert_matrix(ai_settings):

    for i in range(4):
        rowlist = list(ai_settings.matrix[i])
        newrowlist = [val for val in rowlist[::-1]]
        ai_settings.matrix[i] = newrowlist
    return ai_settings.matrix

def tighten_row(ai_settings):

    for i in range(4):
        rowlist = list(ai_settings.matrix[i])
        newrowlist = [val for val in rowlist if val != 0]
        while len(newrowlist) < 4:
            newrowlist.append(0)
        ai_settings.matrix[i] = newrowlist
    return ai_settings.matrix

def merge_row(ai_settings):

    for i in range(4):
        rowlist = list(ai_settings.matrix[i])
        current_num = 1
        end_num = 4 - rowlist.count(0)
        while current_num < end_num:
            if rowlist[current_num - 1] == rowlist[current_num]:
                rowlist[current_num - 1] *= 2
                ai_settings.score += rowlist[current_num - 1]
                rowlist[current_num : ] = rowlist[current_num + 1 : ]
                rowlist.append(0)
            current_num += 1
        ai_settings.matrix[i] = rowlist
    return ai_settings.matrix

def get_zerolist(ai_settings):

    ai_settings.zerolist = []
    for i in range(4):
        rowlist = list(ai_settings.matrix[i])
        current_num = 0
        while current_num < 4:
            if rowlist[current_num] == 0:
                ai_settings.zerolist.append((i, current_num))
            current_num += 1
    return ai_settings.zerolist

def spawn(ai_settings, move_is_possible):

    if move_is_possible == True:
        newnumber = 4 if random.randint(1, 100) > 89 else 2
        if ai_settings.zerolist == []:
            i = random.randint(0, 3)
            j = random.randint(0, 3)
        else:
            (i, j) = random.sample(ai_settings.zerolist, 1)[0]
        ai_settings.matrix[i][j] = newnumber
    return ai_settings.matrix

def show_score(screen, ai_settings):

    rounded_score = int(ai_settings.score)
    score_str = "{:,}".format(rounded_score)
    score_image = ai_settings.scorefont.render(score_str, True, (255, 127, 0), ai_settings.titlecolor)
    score_rect = score_image.get_rect()
    score_rect.right = ai_settings.screen_width
    score_rect.top = 85
    screen.blit(score_image, score_rect)

def drawSurface(screen, ai_settings, block_matrix):

    pygame.draw.rect(screen, ai_settings.titlecolor, ai_settings.titlerect)
    font_title = pygame.font.SysFont("stxingkai", 48)
    font_score = pygame.font.SysFont("stxingkai", 48)
    screen.blit(font_title.render("HuaGer`s 2048", True, (128,42,42)), (145,10))
    screen.blit(font_score.render("score", True, (255, 127, 0)), (440, 45))
    show_score(screen, ai_settings)
    for row in range(4):
        for column in range(4):
            blocknumber = ai_settings.matrix[row][column]
            color = block_matrix.color[blocknumber]
            numsize = block_matrix.numsize[blocknumber]
            drawBlock(screen, block_matrix, row, column, color, blocknumber, numsize)

def drawBlock(screen, block_matrix, row, column, color, blocknumber, numsize):

    font = pygame.font.SysFont("stxingkai", numsize)
    rect_x = column * block_matrix.width + (column + 1) * block_matrix.gap
    rect_y = row * block_matrix.height + 120 + (row + 1) * block_matrix.gap
    pygame.draw.rect(screen, color, (rect_x, rect_y, 120, 120))
    if blocknumber != 0:
        font_width, font_height = font.size(str(int(blocknumber)))
        screen.blit(font.render(str(int(blocknumber)), True, (0, 0, 0)), (rect_x + (120 - font_width) / 2, rect_y + (120 - font_height) / 2))

def reset(ai_settings):

    ai_settings.score = 0
    ai_settings.matrix = numpy.zeros([4, 4])
    ai_settings.zerolist = []
    ai_settings.reset = False
    ai_settings.gameover_check = False
    ai_settings.gamewin_check = False

def gameover_check(ai_settings):

    for i in range(4):
        for j in range(3):
            if ai_settings.matrix[i][j] == ai_settings.matrix[i][j + 1]:
                return False
            if ai_settings.matrix[i][j] == 0 or ai_settings.matrix[i][j + 1] == 0:
                return False
    for i in range(4):
        for j in range(3):
            if ai_settings.matrix[j][i] == ai_settings.matrix[j + 1][i]:
                return False
            if ai_settings.matrix[j][i] == 0 or ai_settings.matrix[j + 1][i] == 0:
                return False
    return True

def show_gameover(screen):

    font_gameover = pygame.font.SysFont("stxingkai", 50)
    screen.blit(font_gameover.render("you are lose! GG~~~", True, (128, 42, 42)), (45, 50))
    screen.blit(font_gameover.render("press r to restart", True, (128, 42, 42)), (45, 75))

def show_gamewin(screen):

    font_gamewin = pygame.font.SysFont("stxingkai", 30)
    screen.blit(font_gamewin.render("you got 2048", True, (128, 42, 42)), (45, 50))
    screen.blit(font_gamewin.render("HuaGer victory!! you are awesome! ", True, (128, 42, 42)), (45, 75))

def gamewin_check(ai_settings):

    for i in range(4):
        for j in range(4):
            if ai_settings.matrix[i][j] == 2048:
                return True
    return False

def show_info(screen):

    font_info = pygame.font.SysFont("stxingkai", 30)
    screen.blit(font_info.render("press q to quit", True, (128, 42, 42)), (45, 50))
    screen.blit(font_info.render("press r to restart", True, (128, 42, 42)), (45, 75))