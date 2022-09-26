import pygame as p
import chess
import os
from pygame.constants import MOUSEBUTTONDOWN

#Pygame constants
WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15

IMAGES = {}
#minimax constants
DEPTH = 5

#this puts all the pictures of the pieces into a dictionary called IMAGES
def load_images():
    pieces = ['bB', 'bK', 'bN', 'bP', 'bQ', 'bR', 'B', 'K', 'N', 'P', 'Q', 'R']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f'images/{piece}.png'), (SQ_SIZE, SQ_SIZE))


def main():
    os.listdir()
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    board = chess.Board()
    load_images()
    running = True
    sq_selected = [] # keeps track of square selected
    player_clicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #(x, y) of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                #if same square is selected, clears click que
                if len(sq_selected) > 0 and sq_selected[0] == (col+(row*8)):
                    sq_selected = []
                    player_clicks = []
                else: #this is when the first click has already been registered
                    sq_selected.append(col+row*8) 
                    player_clicks.append(sq_selected)
                    print('click registered')
                if len(player_clicks) == 2:
                    move = chess.Move(sq_selected[0], sq_selected[1])
                    if board.is_legal(move):
                        board.push(move)
                        sq_selected = []
                        player_clicks = []
                        print(board)
                    else:
                        print(f'move is invalid {sq_selected}')
                        sq_selected = []
                        player_clicks = []

        draw_gamestate(screen, board)
        clock.tick(MAX_FPS)
        p.display.flip()


def draw_gamestate(screen, board):
    draw_board(screen)
    draw_pieces(screen, board)

def draw_board(screen):
    colors = [p.Color("white"), p.Color('gray')]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

#changes chess.py piece to filename piece (B (white bishop) -> B, k (black king) -> bK)
def official_to_unofficial(official):
    if str(official).lower() == str(official):
        #piece is black
        return 'b'+str(official).upper()
    return str(official)

def draw_pieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            official_piece = board.piece_at(c+(r*8))
            file_piece = official_to_unofficial(official_piece)
            if file_piece != 'None':
                screen.blit(IMAGES[file_piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()