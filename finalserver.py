#screen size

WIDTH = 600
HEIGHT = 600

ROWS = 3
COLS = 3
SQSIZE = WIDTH //COLS
LINE_WIDTH =15
#colors
#BG_COLOR = (28,170,156)
BG_COLOR = (186,90,155)

LINE_COLOR = (23,145,135)


CIRC_COLOR = (239,231,200)
CROSS_COLOR=(66,66,66)
#circle
RADIUS = (SQSIZE//4)
CIRC_WIDTH = 15
#cross
CROSS_WIDTH =20
OFFSET=50




import copy
import random
import time
import sys
import pygame
import numpy as np
import socket
import threading



#for pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('TIC TAC AND TOE')
screen.fill(BG_COLOR)


class communicate:
    def __init__(self):
        self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        self.turn = "X"
        self.you = "X"
        self.opponent = "0"
        self.winner = None
        self.game_over = False
        self.counter = 0

    def host_game(self, host, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(1)
        client, addr = server.accept()
        self.you = "X"
        self.opponent = "0"
        self.handle_connection(client)
        server.close()

    def connect_to_game(self, host, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        self.you = "0"
        self.opponent = "X"
        self.handle_connection(client)

    def handle_connection(self, client):
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)
        # horizontal
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    row = pos[1] // SQSIZE
                    col = pos[0] // SQSIZE
                    move = str(row)+","+str(col)
                    print("\n\n"+ move)
                    if self.turn == self.you:
                        if self.check_valid_move(move.split(',')):
                            client.send(move.encode('utf-8'))
                            self.apply_move(move.split(','), self.you)
                            self.draw_fig(row,col)
                            pygame.display.update()
                            self.turn = self.opponent
                        else:
                            print("invalid move!")

            if self.turn != self.you:
                data = client.recv(1024)
                if not data:
                    break
                else:
                    opponentsmove = data.decode('utf-8').split(",")
                    print(opponentsmove, self.opponent)
                    self.apply_move(opponentsmove, self.opponent)
                    #time.sleep(1)
                    self.draw_fig(int(opponentsmove[0]), int(opponentsmove[1]))
                    pygame.display.update()
                    self.turn = self.you
            pygame.display.update()
        time.sleep(5)
        client.close()



    def check_valid_move(self, move):
        if self.board[int(move[0])][int(move[1])] == " ":
            return True


    def check_if_won(self):
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != " ":
                self.winner = self.board[row][0]
                self.game_over = True
                return True
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != " ":
                self.winner = self.board[0][col]
                self.game_over = True
                return True
        if ((self.board[0][0] == self.board[1][1] == self.board[2][2] != " ") or (
                self.board[2][0] == self.board[1][1] == self.board[0][2] != " ")):
            self.winner = self.board[1][1]
            self.game_over = True
            return True
        return False

    def draw_fig(self, row, col):
        if self.turn == "X":
            # \
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
            # /
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

        elif self.turn == "0":
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)

    def apply_move(self, move, player):
        if self.game_over:
            return
        self.counter += 1
        self.board[int(move[0])][int(move[1])] = player
        print(self.board)
        if self.check_if_won():
            if self.winner == self.you:
                print("you win!")
                time.sleep(4)
                exit()
            elif self.winner == self.opponent:
                print("you lose!")
                time.sleep(4)
                exit()
        else:
            if self.counter == 9:
                print("tie")
                time.sleep(4)
                exit()



game = communicate()
game.host_game("localhost", 9999)
