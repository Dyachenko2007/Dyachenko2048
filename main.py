import pygame
import random

pygame.init()

screen = pygame.display.set_mode([1000, 800])
pygame.display.set_caption('Михаил Андреевич 💝')
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 28)

board_values = [[0 for _ in range(4)] for _ in range(4)]
game_over = False
spawn_new = True
init_count = 0
direction = ''
score = 0
file = open('high_score', 'r')
init_high = int(file.readline())
file.close()
high_score = init_high


# 2048 game color library
colors = {0: (176, 226, 255),
          2: (135, 206, 250),
          4: (32, 178, 170),
          8: (84, 255, 159),
          16: (78, 238, 148),
          32: (67, 205, 128),
          64: (0, 205, 102),
          128: (0, 139, 69),
          256: (173, 255, 47),
          512: (255, 236, 139),
          1024: (238, 220, 130),
          2048: (205, 190, 112),
          'light text': (249, 246, 242),
          'dark text': (0, 0, 0),
          'other': (0, 0, 0),
          'bg': (187, 173, 160)}


# draw game over and restart text
def draw_over():
    pygame.draw.rect(screen, 'black', [50, 50, 500, 150], 0, 10)
    game_over_text1 = font.render('Игра окончена!', True, 'white')
    game_over_text2 = font.render('Press Enter to Restart', True, 'white')
    screen.blit(game_over_text1, (130, 65))
    screen.blit(game_over_text2, (70, 105))


# take your turn based on direction
def take_turn(direc, board):
    global score
    merged = [[False for _ in range(4)] for _ in range(4)]
    if direc == 'UP':
        for i in range(4):
            for j in range(4):
                shift = 0
                if i > 0:
                    for q in range(i):
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[i - shift][j] = board[i][j]
                        board[i][j] = 0
                    if board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift][j] \
                            and not merged[i - shift - 1][j]:
                        board[i - shift - 1][j] *= 2
                        score += board[i - shift - 1][j]
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True

    elif direc == 'DOWN':
        for i in range(3):
            for j in range(4):
                shift = 0
                for q in range(i + 1):
                    if board[3 - q][j] == 0:
                        shift += 1
                if shift > 0:
                    board[2 - i + shift][j] = board[2 - i][j]
                    board[2 - i][j] = 0
                if 3 - i + shift <= 3:
                    if board[2 - i + shift][j] == board[3 - i + shift][j] and not merged[3 - i + shift][j] \
                            and not merged[2 - i + shift][j]:
                        board[3 - i + shift][j] *= 2
                        score += board[3 - i + shift][j]
                        board[2 - i + shift][j] = 0
                        merged[3 - i + shift][j] = True

    elif direc == 'LEFT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][j - shift] = board[i][j]
                    board[i][j] = 0
                if board[i][j - shift] == board[i][j - shift - 1] and not merged[i][j - shift - 1] \
                        and not merged[i][j - shift]:
                    board[i][j - shift - 1] *= 2
                    score += board[i][j - shift - 1]
                    board[i][j - shift] = 0
                    merged[i][j - shift - 1] = True

    elif direc == 'RIGHT':
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][3 - q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][3 - j + shift] = board[i][3 - j]
                    board[i][3 - j] = 0
                if 4 - j + shift <= 3:
                    if board[i][4 - j + shift] == board[i][3 - j + shift] and not merged[i][4 - j + shift] \
                            and not merged[i][3 - j + shift]:
                        board[i][4 - j + shift] *= 2
                        score += board[i][4 - j + shift]
                        board[i][3 - j + shift] = 0
                        merged[i][4 - j + shift] = True
    return board


# spawn in new pieces randomly when turns start
def new_pieces(board):
    count = 0
    full = False
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count < 1:
        full = True
    return board, full


# draw background for the board
def draw_board():
    pygame.draw.rect(screen, colors['bg'], [0, 0, 400, 400], 0, 10)
    score_text = font.render(f'Score: {score}', True, 'black')
    high_score_text = font.render(f'High Score: {high_score}', True, 'black')
    screen.blit(score_text, (500, 200))
    screen.blit(high_score_text, (500, 250))
    pass


# draw tiles for game
def draw_pieces(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value > 8:
                value_color = colors['light text']
            else:
                value_color = colors['dark text']
            if value <= 2048:
                color = colors[value]
            else:
                color = colors['other']
            pygame.draw.rect(screen, color, [j * 95 + 20, i * 95 + 20, 75, 75], 0, 5)
            if value > 0:
                value_len = len(str(value))
                font = pygame.font.Font('freesansbold.ttf', 48 - (5 * value_len))
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))
                screen.blit(value_text, text_rect)
                pygame.draw.rect(screen, 'black', [j * 95 + 20, i * 95 + 20, 75, 75], 2, 5)


button1 = pygame.Rect(250, 250, 500, 100)  # Создаем прямоугольник для первой кнопки
button2 = pygame.Rect(250, 450, 500, 100)  # Создаем прямоугольник для второй кнопки
button3 = pygame.Rect(250, 650, 500, 100)


def draw_title(text):
    font = pygame.font.Font(None, 150)  # Выбираем шрифт для текста
    text = font.render(text, 1, (0, 0, 0))  # Создаем объект текста
    screen.blit(text, (250, 100))  # Отрисовываем текст на экране



def draw_button(button, text):
    pygame.draw.rect(screen, (0, 255, 0), button)  # Отрисовываем прямоугольник кнопки
    font = pygame.font.Font(None, 36)  # Выбираем шрифт для текста
    text = font.render(text, 24, (0, 0, 0))  # Создаем объект текста
    screen.blit(text, button.move(10, 10))  # Отрисовываем текст на кнопке



def start_screen():
    run = True
    while run:
        screen.fill('gray')
        draw_title("Игра 2048")
        draw_button(button1, "Начать игру")
        draw_button(button2, "Показать лучший результат")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button1.collidepoint(mouse_pos):
                    main_game()  # Запуск основной игры
                elif button2.collidepoint(mouse_pos):
                    show_high_score()  # Показать лучший результат

        pygame.display.flip()

    pygame.quit()


def show_high_score():
    pass

def main_game():
    board_values = [[0 for _ in range(4)] for _ in range(4)]
    game_over = False
    spawn_new = True
    init_count = 0
    direction = ''
    score = 0
    file = open('high_score', 'r')
    init_high = int(file.readline())
    file.close()
    high_score = init_high
    run = True
    while run:
        timer.tick(fps)
        screen.fill('gray')
        draw_board()
        draw_pieces(board_values)
        if spawn_new or init_count < 2:
            board_values, game_over = new_pieces(board_values)
            spawn_new = False
            init_count += 1
        if direction != '':
            board_values = take_turn(direction, board_values)
            direction = ''
            spawn_new = True
        if game_over:
            draw_over()
            if high_score > init_high:
                file = open('high_score', 'w')
                file.write(f'{high_score}')
                file.close()
                init_high = high_score

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    direction = 'UP'
                elif event.key == pygame.K_DOWN:
                    direction = 'DOWN'
                elif event.key == pygame.K_LEFT:
                    direction = 'LEFT'
                elif event.key == pygame.K_RIGHT:
                    direction = 'RIGHT'

                if game_over:
                    if event.key == pygame.K_RETURN:
                        board_values = [[0 for _ in range(4)] for _ in range(4)]
                        spawn_new = True
                        init_count = 0
                        score = 0
                        direction = ''
                        game_over = False

        if score > high_score:
            high_score = score


        pygame.display.flip()


if __name__ == '__main__':
    start_screen()
