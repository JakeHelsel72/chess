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
    load_images()
    
    #global vars
    screen = p.display.set_mode((WIDTH+100, HEIGHT+100))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    board = chess.Board()
    board_offset_x = board_offset_y = 100
    flip_board = False
    running = True
    sq_selected = [] # keeps track of square selected
    player_clicks = [] #keeps track of where the player has clicked

    while running:
        for e in p.event.get():
            if e.type == p.QUIT: #when the x of the window is pressed,
                running = False #stops running 
            elif e.type == p.K_f: #when Key "f" is pressed,
                flip_board = not flip_board #changes to opposite
            elif e.type == p.MOUSEBUTTONDOWN: #when mouse is pressed,
                location = p.mouse.get_pos() # gets (x, y) tuple of mouse position
                print(f"{location=}") #prints "location"s value to console
                col = (location[0] - board_offset_x)//SQ_SIZE #converts x to number of square from the left it is
                row = (location[1] - board_offset_y)//SQ_SIZE #converts y to number of square from the top it is
                if len(sq_selected) > 0 and sq_selected[0] == (col+(row*8)): #if same square is selected, 
                    sq_selected = [] #clears click queue
                    player_clicks = []
                else: #distinct square is chosen,
                    sq_selected.append(col+row*8) #figure out chess import's square number
                    player_clicks.append(sq_selected)
                    print('click registered')
                if len(player_clicks) == 2: #when two squares are selected,
                    print(f'{sq_selected=}')
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

        draw_gamestate(screen, board, board_offset_x, board_offset_y)
        myfont = p.font.SysFont("monospace", 20)
        BLACK = (0, 0, 0)
        label = myfont.render("press f to flip board", 1, BLACK)
        screen.blit(label, (20, 10))
        clock.tick(MAX_FPS)
        p.display.flip()


def draw_gamestate(screen, board, x=0, y=0):
    draw_board(screen, x, y)
    draw_pieces(screen, board, x, y)

def draw_board(screen, x=0, y=0):
    #x and y are offset
    colors = [p.Color("white"), p.Color('gray')]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE+x, r*SQ_SIZE+y, SQ_SIZE, SQ_SIZE))

#changes chess.py piece to filename piece (B (white bishop) -> B, k (black king) -> bK)
def official_to_unofficial(official):
    if str(official).lower() == str(official):
        #piece is black
        return 'b'+str(official).upper()
    return str(official)

def draw_pieces(screen, board, x=0, y=0):
    #x and y are offset
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            official_piece = board.piece_at(c+(r*8))
            file_piece = official_to_unofficial(official_piece)
            if file_piece != 'None':
                screen.blit(IMAGES[file_piece], p.Rect(c*SQ_SIZE+x, r*SQ_SIZE+y, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()