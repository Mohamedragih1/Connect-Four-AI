from sre_parse import WHITESPACE
import numpy as np
import pygame
import sys
import math
from minmax import Minmax
from expected_minmax import ExpMinmax
from alpha_beta import PurMinmax
from heuristic import ROWS, COLS, PLAYER1, PLAYER2, find_score
import time

BLUE = (34, 0, 124)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
game_over = False
pygame.init()

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
info = 600
total_width = width + info

size = (total_width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

title_font = pygame.font.SysFont("Walbaum Display Heavy", 150)
text_font = pygame.font.SysFont("Times New Roman (Headings CS)", 80)
number_font = pygame.font.SysFont("Times New Roman (Headings CS)", 30)


def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
                int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE / 2) + SQUARESIZE), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE / 2) + SQUARESIZE), RADIUS)
    pygame.display.update()


def write_scores(score1, score2):
    pygame.draw.rect(screen, (0, 13, 77), (width, 0, info, height))
    title = title_font.render("Connect 4 ", 1, (255, 255, 255))
    screen.blit(title, (width + 50, SQUARESIZE - 40))
    text1 = text_font.render(f"Your Score: {score1}", 1, RED)
    screen.blit(text1, (width + 20, SQUARESIZE * 2 - 20))
    text2 = text_font.render(f"AI Score: {score2}", 1, YELLOW)
    screen.blit(text2, (width + 20, SQUARESIZE * 3 - 40))
    pygame.display.update()


def draw_nodes(best_score, scores):
    pygame.draw.circle(screen, (138, 43, 226), (width + info / 2, height / 2 + 70), RADIUS + 10)
    text = number_font.render("Max Node", 1, (255, 255, 255))
    screen.blit(text, (width + info / 2 + RADIUS + 20, height / 2 + 55))
    max_score = number_font.render(f"{best_score}", 1, (255, 255, 255))
    screen.blit(max_score, (width + info / 2 - 30, height / 2 + 60))
    lenght = len(scores)
    for i, score in enumerate(scores):
        pygame.draw.circle(screen, (138, 43, 226), (width + (i + 1) * info / lenght - 40, height / 2 + 200), RADIUS - 5)
        text = number_font.render(f"{score}", 1, (255, 255, 255))
        screen.blit(text, (width + (i + 1) * info / lenght - 70, height / 2 + 190))
    pygame.display.update()

k = 1
# ai = Minmax(k)
ai = PurMinmax(k)
# ai = ExpMinmax(k)

board = np.zeros((ROWS, COLS), dtype=int)
game_over = False
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect Four")
draw_board(board)
write_scores(0, 0)
pygame.display.update()


def gui():
    turn = 0
    global game_over
    best_score = 0
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if turn % 2 == 0:
                start_time = time.time()
                col = ai.get_best_move(board)
                end_time = time.time()
                row = ai.get_next_empty_row(board, col)
                scores = ai.scores
                nodes = ai.nodeExpansion
                scores = sorted(scores, reverse=True)[:7]  # Return the top 7 scores
                print(scores, nodes, end_time - start_time)
                board[row][col] = PLAYER2
                score1, score2 = find_score(board)
                write_scores(score2, score1)
                draw_board(board)
                print(board)
                draw_nodes(best_score, scores)
                best_score = max(scores)
                if len(ai.get_valid_moves(board)) == 0:
                    game_over = True
                if game_over:
                    pygame.time.wait(3000)
                    sys.exit()
                turn += 1
            else:
                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                    posx = event.pos[0]
                    if posx > width:
                        continue
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
                    pygame.draw.rect(screen, (0, 13, 77), (width, 0, SQUARESIZE / 2, SQUARESIZE))
                pygame.display.update()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx = event.pos[0]
                    if posx <= width:
                        col = int(math.floor(posx / SQUARESIZE))
                        row = ai.get_next_empty_row(board, col)
                        if row != -1:
                            board[row][col] = PLAYER1
                            score1, score2 = find_score(board)
                            write_scores(score2, score1)
                            draw_board(board)
                            if len(ai.get_valid_moves(board)) == 0:
                                game_over = True
                            if game_over:
                                pygame.time.wait(2000)
                                break
                            turn += 1
    pygame.draw.rect(screen, (0, 13, 77), (width, SQUARESIZE * 3 + 40, info, height))
    if score1 > score2:
        text = text_font.render("AI Win ;(", 1, YELLOW)
        screen.blit(text, (width + info / 3, SQUARESIZE * 5))
    else:
        text = text_font.render("You Win !!!!", 1, RED)
        screen.blit(text, (width + info / 3, SQUARESIZE * 5))
    pygame.display.update()
    pygame.time.wait(5000)


gui()