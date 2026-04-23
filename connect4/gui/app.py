import pygame

rows = 6
columns = 7
cell_size = 90
cell_radius = 30
top_margin = 150
side_margin = 40
bottom_margin = 25

button_width = 200
button_height = 50
button_gap = 20

board_padding = 20
board_width = (columns * cell_size) + (board_padding * 2)
board_height = (rows * cell_size) + (board_padding * 2)

width = board_width + (side_margin * 2)
height = top_margin + board_height + button_gap + button_height + bottom_margin

board_color = (48, 105, 212)
background = (24, 28, 36)
text = (245, 247, 250)
subtext = (180, 188, 200)
empty_slot = (18, 22, 30)
player1_slot = (231, 76, 60)
player2_slot = (241, 196, 15)

def run() -> None:
    pygame.init()
    pygame.display.set_caption("Connect 4")
    screen = pygame.display.set_mode((width, height))
    font = pygame.font.SysFont("Avenir Next", 20, bold=True)

    board = empty_board()
    game_started = False
    start_button_rect = pygame.Rect((width - button_width) // 2, top_margin + board_height + button_gap, button_width, button_height)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button_rect.collidepoint(event.pos):
                    if not game_started:
                        board = empty_board()
                        game_started = True
                    else:
                        board = empty_board()
                        game_started = False
                       # player_forfeit()

        screen.fill(background)
        draw_board(screen, board)
        draw_start_button(screen, font, start_button_rect, game_started)
        pygame.display.flip()

    pygame.quit()

def draw_board(screen, board):
    board_width = (columns * cell_size) + (board_padding * 2)
    board_height = (rows * cell_size) + (board_padding * 2)

    board_x = (width - board_width) // 2
    board_y = top_margin

    board_rect = pygame.Rect(board_x, board_y, board_width, board_height)

    pygame.draw.rect(screen, board_color, board_rect, border_radius=24)

    for row in range(rows):
        for column in range(columns):
            x = board_x + board_padding + column * cell_size + cell_size // 2
            y = board_y + board_padding + row * cell_size + cell_size // 2
            value = board[row][column]

            if value == 0:
                color = empty_slot
            elif value == 1:
                color = player1_slot
            else:
                color = player2_slot

            pygame.draw.circle(screen, color, (x, y), cell_radius)

def draw_start_button(screen, font, button_rect, game_started):
    mouse_pos = pygame.mouse.get_pos()
    hovered = button_rect.collidepoint(mouse_pos)

    base_color = (185, 52, 52)
    hover_color = (210, 72, 72)
    button_color = hover_color if hovered else base_color

    pygame.draw.rect(screen, button_color, button_rect, border_radius=15)
    label = "Start Game" if not game_started else "End Game"
    label_surface = font.render(label, True, text)

    label_x = button_rect.centerx - label_surface.get_width() // 2
    label_y = button_rect.centery - label_surface.get_height() // 2
    screen.blit(label_surface, (label_x, label_y))

def empty_board():
    board = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ]
    return board
