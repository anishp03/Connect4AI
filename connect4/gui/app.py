import pygame
import json
from pathlib import Path


from connect4.ai import predictColumn
from connect4.logic.logic import (
    ROWS,
    COLUMNS,
    EMPTY,
    PLAYER1,
    PLAYER2,
    empty_board,
    valid_move,
    place_piece,
    game_status,
)
rows = ROWS
columns = COLUMNS
score_file = Path(__file__).resolve().parents[1] / "scores.json"

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
    current_player = PLAYER1
    result_msg = ""
    scores = load_scores()
    player1_score = scores["player1_score"]
    player2_score = scores["player2_score"]
    draw_score = scores["draw_score"]
    start_button_rect = pygame.Rect(
        (width - button_width) // 2,
        top_margin + board_height + button_gap,
        button_width,
        button_height
    )

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos

                if start_button_rect.collidepoint(event.pos):
                    if not game_started:
                        board = empty_board()
                        game_started = True
                        current_player = PLAYER1
                        result_msg = ""
                    else:
                        board = empty_board()
                        game_started = False
                        player2_score += 1
                        save_scores(player2_score, player1_score, draw_score)
                        result_msg = "Player Forfeited AI Wins!"

                elif game_started and click_on_board(mouse_x, mouse_y):
                    column = get_column(mouse_x)
                    if column is not None and valid_move(board, column):
                        place_piece(board, column, current_player)
                        status = game_status(board)

                        if status == "player1_win":
                            player1_score += 1
                            save_scores(player1_score, player2_score, draw_score)
                            result_msg = "Humans Win!"
                            game_started = False
                        elif status == "player2_win":
                            player2_score += 1
                            save_scores(player1_score, player2_score, draw_score)
                            result_msg = "AI Wins!"
                            game_started = False
                        elif status == "draw":
                            draw_score += 1
                            save_scores(player1_score, player2_score, draw_score)
                            result_msg = "Draw!"
                            game_started = False
                        else :
                            current_player = PLAYER2
                            aiColumn = predictColumn(board)

                            if aiColumn is not None and valid_move(board, aiColumn):
                                place_piece(board, aiColumn, PLAYER2)
                                status = game_status(board)

                                if status == "player2_win":
                                    player2_score += 1
                                    save_scores(player1_score, player2_score, draw_score)
                                    result_msg = "AI Wins!"
                                    game_started = False
                                elif status == "draw":
                                    draw_score += 1
                                    save_scores(player1_score, player2_score, draw_score)
                                    result_msg = "Draw!"
                                    game_started = False
                                else:
                                    current_player = PLAYER1

        screen.fill(background)
        draw_turn_text(screen, font, game_started, current_player, result_msg)
        draw_board(screen, board)
        draw_start_button(screen, font, start_button_rect, game_started)
        draw_scoreboard(screen, font, player1_score, player2_score, draw_score)
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

            if value == EMPTY:
                color = empty_slot
            elif value == PLAYER1:
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
    label = "Start Game" if not game_started else "Forfeit Game"
    label_surface = font.render(label, True, text)

    label_x = button_rect.centerx - label_surface.get_width() // 2
    label_y = button_rect.centery - label_surface.get_height() // 2
    screen.blit(label_surface, (label_x, label_y))

def draw_turn_text(screen, font, game_started, current_player, result_msg):
    if game_started:
        label = "Human's turn!" if current_player == PLAYER1 else "AI's turn!"
        color = player1_slot if current_player == PLAYER1 else player2_slot
    else :
        if result_msg:
            label = result_msg
            if result_msg == "Humans Win!":
                color = player1_slot
            elif result_msg == "AI Wins!":
                color = player2_slot
            else :
                color = subtext
        else :
            label = "Press Start Game!"
            color = subtext

    label_surface = font.render(label, True, color)
    x = (width - label_surface.get_width()) // 2
    y = 60
    screen.blit(label_surface, (x, y))

def click_on_board(mouse_x, mouse_y):
    board_x = (width - board_width) // 2
    board_y = top_margin

    return (
        board_x <= mouse_x < board_x + board_width
        and
        board_y <= mouse_y < board_y + board_height
    )

def get_column(mouse_x):
    board_x = (width - board_width) // 2
    relative_x = mouse_x - board_x - board_padding

    if relative_x < 0:
        return None

    column = relative_x // cell_size

    if 0 <= column < columns:
        return int(column)
    return None

def draw_scoreboard(screen, font, player1_score, player2_score, draw_score):
    label = f"Humans: {player1_score} | AI: {player2_score} | Draws: {draw_score}"
    label_surface = font.render(label, True, text)
    x = (width - label_surface.get_width()) // 2
    y = 100
    screen.blit(label_surface, (x, y))

def load_scores():
    if not score_file.exists():
        return {
            "player1_score": 0,
            "player2_score": 0,
            "draw_score": 0,
        }
    with(open(score_file, "r") as file):
        return json.load(file)

def save_scores(player1_score, player2_score, draw_score):
    scores = {
        "player1_score": player1_score,
        "player2_score": player2_score,
        "draw_score": draw_score,
    }
    with(open(score_file, "w")) as file:
        json.dump(scores, file)