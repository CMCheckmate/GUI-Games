# Modules
# GUI
from tkinter import *
from tkinter import messagebox
from tkinter import font
# Other
from copy import deepcopy

# Constants
# GUI
TITLE = "PyChess"
ICON_PATH = "Images/Icons/PyChess.ico"
SCREEN_GEOMETRY = (1280, 720)  # Index 0 for horizontal length and index 1 for vertical length
# Mouse
DRAG = "<B1-Motion>"
CLICK = '<Button-1>'
# Colours
WHITE = "#ffffff"
LIGHT_GREY = "#dbdbdb"
DARK_GREY = "#4d4e5c"
LIGHT_BROWN = "#f6ebbe"
DARK_BROWN = "#7d5a3c"
SELECTED_LIGHT_BROWN = "#aba573"
SELECTED_DARK_BROWN = "#4b280a"
# Board
BOARD_LENGTH = 560
SQUARE_LENGTH = 70
NUM_TOTAL_SQUARES = 64
NUM_SIDE_SQUARES = 8
COLUMN_NOTATIONS = (("a", "b", "c", "d", "e", "f", "g", "h"),  # Index 0 for normal order
                    ("h", "g", "f", "e", "d", "c", "b", "a"))  # Index 1 for reverse order
ROW_NOTATIONS = (("1", "2", "3", "4", "5", "6", "7", "8"),  # Same as above
                 ("8", "7", "6", "5", "4", "3", "2", "1"))
# Image path
PAWN_IMG_PATH = ("Images/Pictures/White Pawn.png",  # Index 0 for black piece display
                 "Images/Pictures/Black Pawn.png")  # Index 1 for white piece display
KNIGHT_IMG_PATH = ("Images/Pictures/White Knight.png",  # Same as above
                   "Images/Pictures/Black Knight.png")
BISHOP_IMG_PATH = ("Images/Pictures/White Bishop.png",  # Same as above
                   "Images/Pictures/Black Bishop.png")
ROOK_IMG_PATH = ("Images/Pictures/White Rook.png",  # Same as above
                 "Images/Pictures/Black Rook.png")
QUEEN_IMG_PATH = ("Images/Pictures/White Queen.png",  # Same as above
                  "Images/Pictures/Black Queen.png")
KING_IMG_PATH = ("Images/Pictures/White King.png",  # Same as above
                 "Images/Pictures/Black King.png")
# Pieces
QUEEN = "QUEEN"
KING = "KING"
PAWN = "PAWN"
KNIGHT = "KNIGHT"
BISHOP = "BISHOP"
ROOK = "ROOK"
# Movement
MOVE = "MOVE"
CAPTURE = "CAPTURE"
EN_PASSANT = "EN-PASSANT"
KING_SIDE_CASTLING = "O-O"
QUEEN_SIDE_CASTLING = "O-O-O"
PROMOTION = "PROMOTE"
# Game
EMPTY = "BLANK"
WHITE_SIDE = "White"
BLACK_SIDE = "Black"
PLAYING = "Ongoing"
CHECKMATE = "Checkmate"
RESIGN = "Resignation"
TIMEOUT = "Timeout"
DRAW = "Draw"
STALEMATE = "Stalemate" + DRAW
REPETITION = "Repetition" + DRAW
INSUFFICIENT_MATERIAL = "Insufficient material" + DRAW
FIFTY_MOVE_RULE = "Fifty-move rule" + DRAW
DRAW_MOVE_NUM = 100  # Game moves counted per movement of piece, thus number of moves to draw is doubled from 50 to 100
MAX_TIME_UNITS = [59, 59, 9]  # Maximum of 59 minutes, 59 seconds and 9 deciseconds
DELAY = 100

# Screen settings
WIN = Tk()
WIN.title(TITLE)
WIN.iconbitmap(ICON_PATH)
WIN.geometry(f"{SCREEN_GEOMETRY[0]}x{SCREEN_GEOMETRY[1]}")
WIN.config(bg=DARK_GREY)

# Variables
current_turn = WHITE_SIDE
game_state = PLAYING
viewing_side = WHITE_SIDE
initial_time = [5, 0, 0]  # 1st index represents number of minutes, followed by number of seconds and then deciseconds
checked = None
promoting = False
chosen_piece = None


# Functions
def exit():
    """
    Creates confirmation window, click on 'Ok' to quit program and 'Cancel' to close confirmation window

    Uses imported tkinter message box method

    :return: None (type=NoneType)
    """

    # Confirmation message box/window
    if messagebox.askokcancel("Quit", "Exit PyChess?"):
        WIN.destroy()


def selected_square(mouse_x, mouse_y):
    """
    Finds square in chess board where mouse pointer is located in

    Uses mouse coordinate locator from tkinter bindings and square dictionary to check coordinates

    :param mouse_x: x(horizontal) position of mouse in board canvas
    :param mouse_y: y(vertical) position of mouse in board canvas

    :return: square_notation (type=string)
    """

    # Board canvas boundaries
    if mouse_x <= 0:  # Exceeds minimum board length
        mouse_x = 0
    elif mouse_x >= BOARD_LENGTH:  # Exceeds maximum board length
        mouse_x = BOARD_LENGTH
    if mouse_y <= 0:  # Exceeds minimum board height
        mouse_y = 0
    elif mouse_y >= BOARD_LENGTH:  # Exceeds maximum board height
        mouse_y = BOARD_LENGTH

    # Square coordinates
    for square_notation, square_info in board_squares.items():
        # Individual square coordinate
        square_coords = square_info[0]
        # Square boundary
        x_min, x_max = square_coords[0], square_coords[0] + SQUARE_LENGTH
        y_min, y_max = square_coords[1], square_coords[1] + SQUARE_LENGTH

        # Mouse pointer in boundary
        if x_min <= mouse_x <= x_max and y_min <= mouse_y <= y_max:
            # Square notation of mouse pointer location
            return square_notation


def set_board():
    """
    Creates all square displays on board canvas in alternating colours
    Stores square coordinates on canvas(anchor=NW) and created square displays in a dictionary
    Sets click event for all squares

    Uses tkinter canvas functions to draw and display squares and bindings to set click events

    :return: squares (type=dict)
    """

    # Initialise data
    square_info = {}
    square_count = -1
    square_colour = LIGHT_BROWN

    # Squares from white's viewing perspective
    if viewing_side == WHITE_SIDE:
        # Square grid loop
        for column_index in range(NUM_SIDE_SQUARES):
            for row_index in range(NUM_SIDE_SQUARES):

                # Square information
                square_notation = COLUMN_NOTATIONS[0][column_index] + ROW_NOTATIONS[1][row_index]
                square_coord_x, square_coord_y = column_index * SQUARE_LENGTH, row_index * SQUARE_LENGTH
                square_count += 1

                # Alternate colour
                if square_count % NUM_SIDE_SQUARES != 0:
                    if square_colour == LIGHT_BROWN:
                        square_colour = DARK_BROWN
                    else:
                        square_colour = LIGHT_BROWN
                # Square display
                drawn_square = Board.create_rectangle(square_coord_x, square_coord_y,
                                                      square_coord_x + SQUARE_LENGTH, square_coord_y + SQUARE_LENGTH,
                                                      fill=square_colour, outline="")
                Board.lower(drawn_square)

                # Square dictionary (index 0 for coordinate tuple and index 1 for square display)
                square_info[square_notation] = [(square_coord_x, square_coord_y), drawn_square]

    # Same as above for opposite viewing perspective
    else:

        for column_index in range(NUM_SIDE_SQUARES):
            for row_index in range(NUM_SIDE_SQUARES):

                square_notation = COLUMN_NOTATIONS[1][column_index] + ROW_NOTATIONS[0][row_index]
                square_coord_x, square_coord_y = column_index * SQUARE_LENGTH, row_index * SQUARE_LENGTH
                square_count += 1

                if square_count % NUM_SIDE_SQUARES != 0:
                    if square_colour == LIGHT_BROWN:
                        square_colour = DARK_BROWN
                    else:
                        square_colour = LIGHT_BROWN

                drawn_square = Board.create_rectangle(square_coord_x, square_coord_y,
                                                      square_coord_x + SQUARE_LENGTH, square_coord_y + SQUARE_LENGTH,
                                                      fill=square_colour, outline="")
                Board.lower(drawn_square)

                square_info[square_notation] = ((square_coord_x, square_coord_y), drawn_square)

    # Square dictionary
    return square_info


def side_labels(square_info):
    """
    Creates column and row notation labels in first row(anchor=SE) and column(anchor=NW)
    Stores column and row notation labels in separate lists

    Uses tkinter canvas drawing and font method

    :param: square_info: Dictionary of square information on board

    :return: column_side_notation (type=list), row_side_notation (type=list)
    """

    # Label font
    label_font = font.Font(family='Courier', size=10, weight="bold")

    # Set columns and rows for perspective side
    if viewing_side == WHITE_SIDE:
        column_notations = COLUMN_NOTATIONS[0]
        row_notations = ROW_NOTATIONS[0]
    else:
        column_notations = COLUMN_NOTATIONS[1]
        row_notations = ROW_NOTATIONS[1]

    # Column labels
    col_labels = []
    for col_notation in column_notations:
        # Label square notation
        label_square_notation = col_notation + row_notations[0]

        # Alternate text and square colour
        label_square_color = Board.itemcget(square_info[label_square_notation][1], "fill")
        if label_square_color == LIGHT_BROWN:
            label_color = DARK_BROWN
        else:
            label_color = LIGHT_BROWN

        # Set label coordinates
        label_x = (square_info[label_square_notation][0][0] + SQUARE_LENGTH) - label_font.actual()["size"]
        label_y = (square_info[label_square_notation][0][1] + SQUARE_LENGTH) - label_font.actual()["size"]
        # Column label list
        col_labels.append(Board.create_text(label_x, label_y, text=col_notation, fill=label_color, font=label_font))

    # Same as above for row labels
    rw_labels = []
    for rw_notation in row_notations:

        label_square_notation = column_notations[0] + rw_notation

        label_square_color = Board.itemcget(square_info[label_square_notation][1], "fill")
        if label_square_color == LIGHT_BROWN:
            label_color = DARK_BROWN
        else:
            label_color = LIGHT_BROWN

        label_x = square_info[label_square_notation][0][0] + label_font.actual()["size"]
        label_y = square_info[label_square_notation][0][1] + label_font.actual()["size"]

        rw_labels.append(Board.create_text(label_x, label_y, text=rw_notation, fill=label_color, font=label_font))

    # Column label list and row label list
    return col_labels, rw_labels


def update_state(turn):
    """
    Updates state of current game
    Includes Ongoing match, drawn match and won match.

    Uses if statements to check for state and update score and messages accordingly

    :param: turn: side of next player to move

    :return: None (type=NoneType)
    """

    global game_state

    if game_state == PLAYING:
        game_end = True
        for name, piece in pieces.items():
            if turn in name:
                if len(piece.legal_moves()) != 0:
                    game_end = False
                    break

        if game_end:
            if checked == turn:
                game_state = CHECKMATE
            else:
                game_state = STALEMATE
        else:
            for pos in game_pos:
                if game_pos.count(pos) == 3:
                    game_state = REPETITION
                    break

            if game_state == PLAYING:
                if len(game_moves) >= DRAW_MOVE_NUM:
                    fifty_move_draw = True
                    final_fifty_moves = game_moves[len(game_moves) - DRAW_MOVE_NUM:len(game_moves)]
                    for piece, movement, move in final_fifty_moves:
                        if PAWN in piece or CAPTURE in movement:
                            fifty_move_draw = False
                            break
                    if fifty_move_draw:
                        game_state = FIFTY_MOVE_RULE

    if game_state == PLAYING or game_state == TIMEOUT:
        white_pieces = []
        black_pieces = []
        for name, piece in pieces.items():
            if WHITE_SIDE in name:
                white_pieces.append(piece)
            else:
                black_pieces.append(piece)

        white_insufficient = False
        if len(white_pieces) <= 2:
            white_insufficient = True
            for piece in white_pieces:
                if PAWN in piece.id or ROOK in piece.id or QUEEN in piece.id:
                    white_insufficient = False
                    break
        black_insufficient = False
        if len(black_pieces) <= 2:
            black_insufficient = True
            for piece in black_pieces:
                if PAWN in piece.id or ROOK in piece.id or QUEEN in piece.id:
                    black_insufficient = False
                    break

        if white_insufficient and black_insufficient:
            game_state = INSUFFICIENT_MATERIAL
        elif game_state == TIMEOUT:
            if turn == WHITE_SIDE and black_insufficient:
                game_state = f"{TIMEOUT},\n{INSUFFICIENT_MATERIAL}"
            elif turn == BLACK_SIDE and white_insufficient:
                game_state = f"{TIMEOUT},\n{INSUFFICIENT_MATERIAL}"

    if game_state == PLAYING:
        State_Text.config(text=f"Match in progress.\n\n- {turn} to move -")
    elif game_state == CHECKMATE or game_state == RESIGN or game_state == TIMEOUT:
        if turn == player_1["side"]:
            winning_player = player_2
        else:
            winning_player = player_1

        winning_player["points"] += 1
        State_Text.config(text="Game end, " + game_state + ".\n\n" + winning_player["side"] + " wins.\n" +
                               str(player_2["points"]) + " - " + str(player_1["points"]))

        Resign_Button.config(state=DISABLED)
    elif DRAW in game_state:
        player_1["points"] += 0.5
        player_2["points"] += 0.5
        State_Text.config(text=f"Game end.\nDraw by\n\n" + game_state.replace(DRAW, "") + ".\n" +
                               str(player_1["points"]) + " - " + str(player_2["points"]))

        Resign_Button.config(state=DISABLED)


def timer(turn, player):
    """
    Countdown timer system for both players where the game is over if either side runs out of time

    Uses recursion with the 'after' method to constantly reduce the displayed time on the sidebar timer.

    :param turn: side of player to move
    :param player: player to move's information
    :return: None (type=NoneType)
    """

    global game_state

    if current_turn == turn and game_state == PLAYING:
        time_display = player["time"]["display"]
        player_time = player["time"]["units"]

        time_label = ""
        for unit_index in range(0, len(player_time)):
            unit_time = str(player_time[unit_index])
            time_label += "0" * (len(str(MAX_TIME_UNITS[unit_index])) - len(unit_time)) + unit_time
            if unit_index != len(player_time) - 1:
                time_label += ":"
        time_display.config(text=time_label)

        timeout = True
        for unit in player_time:
            if unit > 0:
                timeout = False
                break
        if timeout:
            game_state = TIMEOUT

            update_state(current_turn)
        else:
            for unit_index in range(0, len(player_time) - 1):
                if player_time[unit_index] > 0 and player_time[unit_index + 1] == 0:
                    player_time[unit_index] -= 1
                    player_time[unit_index + 1] = MAX_TIME_UNITS[unit_index + 1] + 1

            player_time[-1] -= 1
            WIN.after(DELAY, timer, turn, player)


def flip_board():
    """
    Flips perspective side by changing notations of all squares on board
    Replaces previous square dictionary and label lists
    Deselects all pieces and move them to new square according to new square notation
    Redraws column and notation labels
    Flips player name, icon and time display for both sides

    Uses existing functions to reset and redraw pieces and labels

    :return: None (type=NoneType)
    """

    global viewing_side, board_squares, column_labels, row_labels

    # Change perspective side
    if viewing_side == WHITE_SIDE:
        viewing_side = BLACK_SIDE
    elif viewing_side == BLACK_SIDE:
        viewing_side = WHITE_SIDE

    # Flip time display
    player_1_time_display = player_1["time"]["display"]
    player_2_time_display = player_2["time"]["display"]
    player_1_time = player_1_time_display.cget("text")
    player_2_time = player_2_time_display.cget("text")
    player_1_time_display.config(text=player_2_time)
    player_2_time_display.config(text=player_1_time)
    player_1["time"]["display"] = player_2_time_display
    player_2["time"]["display"] = player_1_time_display
    # Flip name
    player_1_name = player_1["name display"].cget("text")
    player_2_name = player_2["name display"].cget("text")
    player_1["name display"].config(text=player_2_name)
    player_2["name display"].config(text=player_1_name)
    # Flip icon
    player_1_icon = player_1["icon display"].cget("image")
    player_2_icon = player_2["icon display"].cget("image")
    player_1["icon display"].config(image=player_2_icon)
    player_2["icon display"].config(image=player_1_icon)

    # Deselect pieces
    for piece in pieces.values():
        if piece.selection:
            piece_selection(piece.notation, select=False)

    # Replace square information dictionary
    for coord, square in board_squares.values():
        Board.delete(square)
    board_squares = set_board()

    # Delete and redraw notation labels
    for col_label in column_labels:
        Board.delete(col_label)
    for row_label in row_labels:
        Board.delete(row_label)
    column_labels, row_labels = side_labels(board_squares)

    # Move pieces to new squares
    for piece in pieces.values():
        piece_x, piece_y = board_squares[piece.notation][0]
        Board.moveto(piece.display, piece_x, piece_y)


def resign():
    """
    Updates game state to RESIGN to end game

    Uses global game_state variable

    :return: None (type=NoneType)
    """

    global game_state

    game_state = RESIGN

    # Call state updater
    update_state(current_turn)


def piece_selection(piece_square, select):
    """
    Selects current piece's occupied square by changing its colour if selecting
    Deselects current piece by reverting the piece's previously selected square colour if deselecting

    Uses tkinter item config method on canvas items

    :param piece_square: Notation for original square of the piece to select/deselect
    :param select: Determines whether to select/deselect a piece

    :return: None (type=NoneType)
    """

    global chosen_piece

    # Selection
    if select:
        # Darken piece's occupied square colour
        if Board.itemcget(board_squares[piece_square][1], "fill") == LIGHT_BROWN:
            selected_color = SELECTED_LIGHT_BROWN
        else:
            selected_color = SELECTED_DARK_BROWN
        Board.itemconfig(board_squares[piece_square][1], fill=selected_color)

    # Deselection
    else:
        # Revert selected square color
        if Board.itemcget(board_squares[piece_square][1], "fill") == SELECTED_LIGHT_BROWN:
            original_color = LIGHT_BROWN
        else:
            original_color = DARK_BROWN
        Board.itemconfigure(board_squares[piece_square][1], fill=original_color)

        # Reset movement and selection variables
        chosen_piece.selection = False
        chosen_piece.movement = None
        chosen_piece = None


def start_promotion(promoted_pawn, destination_square, movement_type):
    # noinspection PyGlobalUndefined
    global promoting, queen_img, rook_img, knight_img, bishop_img  # Tkinter image garbage recycling prevention

    if promoted_pawn is not None:
        promoting = True

        # Option Frame
        option_frame = Board.create_rectangle(235, 130, 325, 430, fill=LIGHT_GREY)

        # Option images
        if promoted_pawn.side == WHITE_SIDE:
            img_index = 0
        else:
            img_index = 1
        queen_img = PhotoImage(file=QUEEN_IMG_PATH[img_index])
        rook_img = PhotoImage(file=ROOK_IMG_PATH[img_index])
        knight_img = PhotoImage(file=KNIGHT_IMG_PATH[img_index])
        bishop_img = PhotoImage(file=BISHOP_IMG_PATH[img_index])

        # Option list
        promotion_options = [[Board.create_image(280, 175, image=queen_img), QUEEN],
                             [Board.create_image(280, 245, image=rook_img), ROOK],
                             [Board.create_image(280, 315, image=knight_img), KNIGHT],
                             [Board.create_image(280, 385, image=bishop_img), BISHOP]]

        # Set button events for options
        for option_img, option_type in promotion_options:
            Board.tag_bind(option_img, CLICK,
                           lambda event, pawn=promoted_pawn, promoted_type=option_type,
                                  frame=option_frame, promote_options=eval(str(promotion_options)),
                                  destination=destination_square,
                                  movement=movement_type:
                           end_promotion(pawn, promoted_type, frame, promote_options, destination, movement))


def end_promotion(pawn, promoted_type, frame, promote_options, destination, move_type):
    global promoting

    if pawn is not None:
        promoting = False

        # Remove promotion GUI options
        Board.delete(frame)
        for option_img, option_type in promote_options:
            Board.delete(option_img)

        # Delete pawn
        Board.delete(pawn.display)

        # Update game information
        update_move_info(pawn, destination, move_type, promoted_piece=promoted_type)


def detect_check(board_values, piece_list, checked_side):
    """
    Checks if the current side is under check from the opponent
    Explores all possible opponent moves and returns True if an enemy piece is able to capture the king
    Returns False if all enemy pieces are unable to capture the king, indicating the current side is not in check

    :param: board_values: Dictionary of piece value in each square
    :param: piece_dict: Dictionary of enemy pieces
    :param: current_side: Possibly checked side

    :return: True/False (type=boolean)
    """

    # Get all enemy pieces
    for name, piece in piece_list.items():
        if checked_side not in name:

            # Check all possible moves of enemy pieces
            for possible_move, possible_move_type in piece.possible_moves(board_values, False):

                # Capture of king detected (current side in check)
                if KING in board_values[possible_move]:
                    return True
    # False for no possible capture of king
    return False


def move_piece(board_values, piece_list, moving_piece, destination, movement_type, promote_type=None):
    """
    Moves piece from current square to destination square
    Allows simulation of move where only board square information is changed
    Updates board position list, current turn and game move list for normal moves

    :param board_values: dictionary of square values in the board
    :param piece_list: List of all pieces on board
    :param moving_piece: piece that performs current move
    :param destination: final/chosen destination of piece
    :param movement_type: type of move played (includes EN_PASSANT, PROMOTION, CASTLING, CAPTURES an MOVE)
    :param promote_type: chosen piece type for pawn to promote into in the case of promotion

    :return: destination_square_value (type=string/class)
    """

    # Castling
    # King side castling
    if KING_SIDE_CASTLING in movement_type:
        # Move king side rook
        rook_origin = f"h{moving_piece.notation[1]}"
        rook_destination = f"f{moving_piece.notation[1]}"
        board_values[rook_destination] = board_values[rook_origin]

        # Clear rook square
        board_values[rook_origin] = EMPTY

    # Queen side castling
    elif QUEEN_SIDE_CASTLING in movement_type:
        # Move queen side rook
        rook_origin = f"a{moving_piece.notation[1]}"
        rook_destination = f"d{moving_piece.notation[1]}"
        board_values[rook_destination] = board_values[rook_origin]

        # Clear rook square
        board_values[rook_origin] = EMPTY

    # En passant
    elif EN_PASSANT in movement_type:
        # Manually move captured pawn back one square
        board_values[destination] = board_values[destination[0] + moving_piece.notation[1]]

        # Clear captured pawn square
        board_values[destination[0] + moving_piece.notation[1]] = EMPTY

    # Capture
    destination_square_value = board_values[destination]
    if CAPTURE in movement_type:
        captured_piece = destination_square_value

        # Remove piece from dictionary of pieces
        del piece_list[captured_piece]

    # Promotion
    if PROMOTION in movement_type and promote_type is not None:
        # Remove promoted pawn
        promoted_pawn = board_values[moving_piece.notation]
        del piece_list[promoted_pawn]

        # Get total amount of promoted type pieces
        num_piece = 0
        for name, piece in piece_list.items():
            if promote_type in name:
                num_piece += 1

        # Create new promoted piece
        new_piece = None
        if promote_type == QUEEN:
            new_piece = Queen(moving_piece.side, num_piece + 1, destination)
        elif promote_type == ROOK:
            new_piece = Rook(moving_piece.side, num_piece + 1, destination)
        elif promote_type == BISHOP:
            new_piece = Bishop(moving_piece.side, num_piece + 1, destination)
        elif promote_type == KNIGHT:
            new_piece = Knight(moving_piece.side, num_piece + 1, destination)

        if new_piece is not None:
            piece_list[new_piece.id] = new_piece
            board_values[moving_piece.notation] = new_piece.id

    # Update new square with piece value
    board_values[destination] = board_values[moving_piece.notation]
    # Clear original square
    board_values[moving_piece.notation] = EMPTY


def convert_to_notation(piece_type, origin, destination, move_type, promoted_piece):
    move_notation = ""

    # First letter (indicates piece that moved)
    if piece_type == KNIGHT:
        move_notation = "N"
    elif piece_type != PAWN:
        move_notation = piece_type[0]

    # Check if other pieces of the same type can perform the move
    moved_piece = square_values[origin]
    move = [destination, move_type]
    common_move = False
    same_in_row = False
    same_in_column = False
    for name, piece in pieces.items():
        # Correct piece type
        if current_turn in name and piece_type in name and moved_piece != name:

            # Check same row/column and add row/column indicator if needed
            if move in piece.legal_moves():
                common_move = True

                if origin[1] == piece.notation[1]:
                    same_in_row = True
                if origin[0] == piece.notation[0]:
                    same_in_column = True

    if common_move:
        if same_in_row and same_in_column:
            move_notation += origin
        elif same_in_column:
            move_notation += origin[1]
        else:
            move_notation += origin[0]

    # Capture if present
    if CAPTURE in move_type:
        if PAWN in piece_type:
            move_notation += origin[0]
        move_notation += "x"
    # Add destination
    move_notation += destination

    # Promotion if present
    if promoted_piece is not None:
        if promoted_piece == KNIGHT:
            piece_symbol = "N"
        else:
            piece_symbol = promoted_piece[0]
        move_notation += f"={piece_symbol}"

    return move_notation


def update_move_info(moving_piece, destination, movement, promoted_piece=None):
    global current_turn, checked

    if moving_piece is not None:
        move_notation = convert_to_notation(moving_piece.type, moving_piece.notation, destination,
                                            movement, promoted_piece)

        # Update position dictionary
        move_piece(square_values, pieces, moving_piece, destination, movement, promote_type=promoted_piece)

        # Update game record
        game_moves.append([square_values[destination], [moving_piece.notation, destination], movement, move_notation])
        game_pos.append(square_values.copy())

        # New piece notation
        moving_piece.notation = destination

        if detect_check(square_values, pieces, moving_piece.enemy_side):
            checkmate = True
            for name, piece in pieces.items():
                if moving_piece.enemy_side in name:
                    if len(piece.legal_moves()) > 0:
                        checkmate = False
                        break

            if checkmate:
                move_notation += "#"
            else:
                move_notation += "+"
            game_moves[-1][-1] = move_notation

        # Update move box
        Moves_Box.config(state=NORMAL)
        spaces = " " * (7 - len(move_notation))
        if len(game_moves) % 2 != 0:
            if len(game_moves) != 1:
                move_num = len(game_moves) - 1
            else:
                move_num = len(game_moves)
            move_num = " " * (3 - len(str(move_num))) + str(move_num)
            Moves_Box.insert(END, f"{move_num}. {move_notation}{spaces}|")
        else:
            Moves_Box.insert(END, f"{spaces}{move_notation}\n")
        Moves_Box.config(state=DISABLED)

        # Update player turn and set off timer for next player
        if current_turn == WHITE_SIDE:
            current_turn = BLACK_SIDE
            timer(current_turn, player_1)
        else:
            current_turn = WHITE_SIDE
            timer(current_turn, player_2)

        # Update checking and game status
        if detect_check(square_values, pieces, current_turn):
            checked = current_turn
        else:
            checked = None

        update_state(current_turn)


def set_piece(event):
    """
    Moves piece according to chosen location with 'move_piece()' function
    Updates game information and movement variables
    Updates whether or not after the current move the opponent is under check
    Resets piece back to original square if an illegal move is made
    Deselects pieces after movement or when they are clicked right after selection

    :param event: Contains mouse position information in the 'event.x' and 'event.y' attributes

    :return: None (type=NoneType)
    """

    # Move/Set piece when chosen
    if chosen_piece is not None and game_state == PLAYING:
        # Set variables
        moved = False
        legal = False
        move_types = []

        # Set origin and destination
        origin = chosen_piece.notation
        chosen_square = selected_square(event.x, event.y)
        # Check if piece moved away from original square
        if chosen_square != origin:
            moved = True
            # Check legality and get movement type of chosen move
            for move, move_types in chosen_piece.legal_moves():
                if move == chosen_square:
                    legal = True
                    break
            # Reset piece position if illegal move is made
            if not legal:
                chosen_square = origin

        # Move piece display to destination square on board
        destination_x, destination_y = board_squares[chosen_square][0]
        Board.moveto(chosen_piece.display, destination_x, destination_y)

        # Update game information if valid move is made
        if legal:
            # Save new square original occupant
            new_square_value = square_values[chosen_square]
            if CAPTURE in move_types:
                # Update correct original occupant for en-passant captures
                if EN_PASSANT in move_types:
                    new_square_value = square_values[f"{chosen_square[0]}{origin[1]}"]

                # Delete captured piece displays
                new_square_value = pieces[new_square_value]
                Board.delete(new_square_value.display)

            # Move rook display after castling
            elif KING_SIDE_CASTLING in move_types:
                king_side_rook = pieces[ROOK + chosen_piece.side + "2"]
                # Move rook
                moved_square = f"f{origin[1]}"
                destination_x, destination_y = board_squares[moved_square][0]
                Board.moveto(king_side_rook.display, destination_x, destination_y)

                # Update location
                king_side_rook.notation = moved_square

            # Same for queen side rook
            elif QUEEN_SIDE_CASTLING in move_types:
                queen_side_rook = pieces[ROOK + chosen_piece.side + "1"]

                moved_square = f"d{origin[1]}"
                destination_x, destination_y = board_squares[moved_square][0]
                Board.moveto(queen_side_rook.display, destination_x, destination_y)

                queen_side_rook.notation = moved_square

            # Promote pawn
            if PROMOTION in move_types:
                # Display promotion GUI
                start_promotion(chosen_piece, chosen_square, move_types)
            else:
                # Update game information for move
                update_move_info(chosen_piece, chosen_square, move_types)

        # Deselect after movement
        if moved or not chosen_piece.selection:
            piece_selection(origin, select=False)


# GUI elements
# Frames
# Left info box (Player info)
Player_Frame = Frame(WIN, width=260, height=560, bg=WHITE)
Player_Frame.grid(column=0, row=0, sticky=W, padx=50, pady=70)
Top_Player = Frame(Player_Frame, width=250, height=75, bg=LIGHT_GREY)
Top_Player.grid(column=0, row=0, sticky=N, padx=10, pady=10)
P1_Icon = PhotoImage(file="Images/Pictures/Player.png")
Top_Player_Icon = Label(Top_Player, image=P1_Icon)
Top_Player_Icon.grid(column=0, row=0)
Top_Player_Name = Label(Top_Player, width=20, text="Player 2", font=("Helvetica", 12), bg=LIGHT_GREY)
Top_Player_Name.grid(column=1, row=0)
Bottom_Player = Frame(Player_Frame, width=250, height=75, bg=LIGHT_GREY)
Bottom_Player.grid(column=0, row=2, sticky=S, padx=10, pady=10)
P2_Icon = PhotoImage(file="Images/Pictures/Player.png")
Bottom_Player_Icon = Label(Bottom_Player, image=P2_Icon)
Bottom_Player_Icon.grid(column=0, row=0)
Bottom_Player_Name = Label(Bottom_Player, width=20, text="Player 1", font=("Helvetica", 12), bg=LIGHT_GREY)
Bottom_Player_Name.grid(column=1, row=0)
Game_State = Frame(Player_Frame, width=250, height=370, bg=LIGHT_GREY)
Game_State.grid(column=0, row=1)
State_Text = Label(Game_State, text="Match in progress.\n- White to Move -", font=("Montserrat", 15), bg=LIGHT_GREY)
State_Text.grid(column=0, row=0, columnspan=3)
resign_img = PhotoImage(file="Images/Pictures/Resign.png")
Resign_Button = Button(Game_State, image=resign_img, relief=SUNKEN, borderwidth=0,
                       bg=LIGHT_GREY, activebackground=LIGHT_GREY, command=lambda: resign())
Resign_Button.grid(column=1, row=1)
flip_img = PhotoImage(file="Images/Pictures/Flip.png")
Flip_Board_Button = Button(Game_State, image=flip_img, relief=SUNKEN, borderwidth=0,
                           bg=LIGHT_GREY, activebackground=LIGHT_GREY, command=flip_board)
Flip_Board_Button.grid(column=0, row=1)
# Frame settings
Top_Player.columnconfigure(0, weight=5)
Top_Player.columnconfigure(1, weight=1)
Top_Player.rowconfigure(0, weight=1)
Top_Player.grid_propagate(False)
Bottom_Player.columnconfigure(0, weight=5)
Bottom_Player.columnconfigure(1, weight=1)
Bottom_Player.rowconfigure(0, weight=1)
Bottom_Player.grid_propagate(False)
Game_State.columnconfigure(0, weight=1)
Game_State.columnconfigure(1, weight=1)
Game_State.rowconfigure(0, weight=3)
Game_State.rowconfigure(1, weight=1)
Game_State.grid_propagate(False)
# Right info box (Game info)
Game_Info_Frame = Frame(WIN, width=260, height=560, bg=WHITE)
Game_Info_Frame.grid(column=2, row=0, sticky=E, padx=50, pady=70)
Top_Time = Frame(Game_Info_Frame, width=240, height=104, bg=LIGHT_GREY)
Top_Time.grid(column=0, row=0, sticky=N, padx=10, pady=10)
Top_Time_Count = Label(Top_Time, font=("ocr a extended", 40), bg=LIGHT_GREY)
Top_Time_Count.place(x=120, y=52, anchor="center")
Bottom_Time = Frame(Game_Info_Frame, width=240, height=104, bg=LIGHT_GREY)
Bottom_Time.grid(column=0, row=3, sticky=S, padx=10, pady=10)
Bottom_Time_Count = Label(Bottom_Time, font=("ocr a extended", 40), bg=LIGHT_GREY)
Bottom_Time_Count.place(x=120, y=52, anchor="center")
Move_Title = Frame(Game_Info_Frame, width=240, height=30, bg=LIGHT_GREY)
Move_Title.grid(column=0, row=1)
side_title = Label(Move_Title, text=" WHITE    BLACK", font=("Montserrat", 15), bg=LIGHT_GREY)
side_title.pack()
Move_Title.propagate(False)
Move_List = Frame(Game_Info_Frame, width=240, height=282, bg=LIGHT_GREY)
Move_List.grid(column=0, row=2, padx=10)
scroll = Scrollbar(Move_List)
scroll.pack(side=RIGHT, fill=Y)
Moves_Box = Text(Move_List, wrap=NONE, width=240, height=312, bg=LIGHT_GREY, font=("courier", 12),
                 borderwidth=0, yscrollcommand=scroll.set)
Moves_Box.pack()
Moves_Box.config(state=DISABLED)
scroll.config(command=Moves_Box.yview)
Move_List.propagate(False)
Game_Info_Frame.grid_propagate(False)
# Game/Board
Board_Frame = Frame(WIN, width=BOARD_LENGTH, height=BOARD_LENGTH)
Board_Frame.grid(column=1, row=0)

# Canvas (Game board)
Board = Canvas(Board_Frame, width=BOARD_LENGTH, height=BOARD_LENGTH, highlightthickness=0)
# Set piece release event
Board.bind("<ButtonRelease-1>", set_piece)
Board.pack()


# Classes
class Pieces:
    """
    Creates and displays pieces
    Allows selection of created pieces
    Moves created pieces via dragging
    """

    # Attributes
    def __init__(self, type, side, number, img_path, piece_notation):
        # Identifiers
        self.type = type
        self.side = side
        self.counter = number
        self.id = f"{self.type}{self.side}{self.counter}"
        # Notation and coordinates
        self.notation = piece_notation
        self.coordinate = board_squares[self.notation][0]
        # Movement
        self.movement = None
        self.selection = False
        # Display and dimensions
        self.img = PhotoImage(file=img_path)
        self.display = self.create()
        self.width = self.img.width()
        self.height = self.img.height()
        # Other
        self.enemy_side = BLACK_SIDE if self.side == WHITE_SIDE else WHITE_SIDE
        self.column_notations = COLUMN_NOTATIONS[0] if self.side == WHITE_SIDE else COLUMN_NOTATIONS[1]
        self.row_notations = ROW_NOTATIONS[0] if self.side == WHITE_SIDE else ROW_NOTATIONS[1]

    def create(self):
        """
        Sets and returns image of piece in centre of starting notation square
        Adds piece to square value dictionary
        Binds click and drag events for piece movement

        :return: piece_display (type='Tkinter canvas item')
        """

        # Create image on board canvas centred in each square
        piece_display = Board.create_image(
            self.coordinate[0] + (SQUARE_LENGTH / 2), self.coordinate[1] + (SQUARE_LENGTH / 2), image=self.img)

        # Update piece in square value dictionary
        square_values[self.notation] = self.id

        # Set movement events
        # Click
        Board.tag_bind(piece_display, CLICK, self.select)
        # Drag
        Board.tag_bind(piece_display, DRAG, self.drag)

        # Created piece display on canvas
        return piece_display

    def drag(self, event):
        """
        Moves piece according to mouse position
        Piece will stick to board boundaries when mouse is moved beyond the board

        :param event: Event information from binding (mouse location derived from 'event.x' and 'event.y'

        :return: None (type=NoneType)
        """

        # Allow piece selection/movement during the piece's side's turn and not under promotion
        if current_turn == self.side and not promoting and game_state == PLAYING:
            # Set boundaries
            # x-position
            if event.x <= 0:
                event.x = 0
            elif event.x >= BOARD_LENGTH:
                event.x = BOARD_LENGTH
            # y-position
            if event.y <= 0:
                event.y = 0
            elif event.y >= BOARD_LENGTH:
                event.y = BOARD_LENGTH

            # Update movement attributes
            self.movement = DRAG
            self.coordinate = (event.x - (self.width / 2), event.y - (self.height / 2))

            # Move and anchor piece at mouse pointer
            Board.moveto(self.display, self.coordinate[0], self.coordinate[1])

    def select(self, event):
        """
        Selects current piece by changing piece's square color and updating selection and movement piece attributes
        Sets selection attribute of piece to false if piece originally selected and clicked again
        Deselects all previously selected pieces if current piece is selected

        :param event: Event information from binding

        :return: event (type=Binding information)
        """

        global chosen_piece

        # Allow piece selection/movement during the piece's side's turn and piece not under promotion
        if current_turn == self.side and not promoting and game_state == PLAYING:
            # Select piece if not selected or same side with previously selected piece
            if chosen_piece != self and \
                    (chosen_piece is None or chosen_piece.side == self.side or self.movement == DRAG):
                # Select piece's square
                piece_selection(self.notation, select=True)
                # Deselect all previously selected pieces
                for name, piece in pieces.items():
                    if self.side in name and piece.selection:
                        piece_selection(piece.notation, select=False)

                # Update attributes
                self.movement = CLICK
                self.selection = True
                chosen_piece = self

                # Lift image to first order (prevent other pieces from overlapping it)
                Board.lift(self.display)

            # Update selection if piece already selected
            elif chosen_piece == self:
                self.selection = False

        # Event information from binding (parameter usage)
        return event

    def legal_moves(self):
        """
        Discards possible moves that lead to a capture of the king on the next move
        Returns list of all legal moves of the chosen/moving piece

        :return: moves (type=list)
        """

        # Get possible moves of selected piece
        possible_moves = self.possible_moves(square_values)

        # Check all moves
        for move, move_type in possible_moves.copy():
            if KING_SIDE_CASTLING not in move_type and QUEEN_SIDE_CASTLING not in move_type:
                move_info = [move, move_type]

                # Simulate move
                square_values_copy = deepcopy(square_values)
                pieces_copy = pieces.copy()
                move_piece(square_values_copy, pieces_copy, self, move, move_type)

                # Check all possible moves of enemy pieces after current move
                if detect_check(square_values_copy, pieces_copy, self.side):
                    possible_moves.remove(move_info)

        # List of legal moves
        return possible_moves


class King(Pieces):
    """
    Subclass from 'Pieces' class
    Sets image for king
    Sets possible moves for king
    """

    # Attributes
    def __init__(self, side, number, piece_notation):
        # Set image depending on which side the piece belongs to
        self.img_path = "Images/Pictures/White King.png" if side == WHITE_SIDE else "Images/Pictures/Black King.png"

        # Call to parent class (Piece)
        super().__init__(KING, side, number, self.img_path, piece_notation)

    # Possible moves
    def possible_moves(self, board_values, castle=True):
        """
        Calculates all possible moves of the king in the current position
        May include illegal moves that may result in king being captured
        Returns a list of possible moves with the move and the move type as an element

        :param castle: Set to 'False' to prevent recursion error in 'detect_check()' function
        :param board_values: Dictionary of each square value of each square notation in the board

        :return: possible_moves (type=list)
        """

        # Set move list
        possible_moves = []

        # Column and row index in list
        column_list_index = self.column_notations.index(self.notation[0])
        row_list_index = self.row_notations.index(self.notation[1])

        # Neighbour columns
        for col in range(column_list_index - 1, column_list_index + 2):
            # Confirm columns in board
            if 0 <= col <= NUM_SIDE_SQUARES - 1:

                # Neighbour rows
                for rw in range(row_list_index - 1, row_list_index + 2):
                    # Confirm rows in board
                    if 0 <= rw <= NUM_SIDE_SQUARES - 1:

                        # Possible notation to neighbour square
                        possible_move = self.column_notations[col] + self.row_notations[rw]

                        # Set movement type
                        move_types = [MOVE]
                        square_value = board_values[possible_move]
                        if self.enemy_side in square_value:
                            move_types = [MOVE, CAPTURE]

                        # Prevent capture of own piece
                        if self.side not in square_value:
                            possible_moves.append([possible_move, move_types])

        # Castling
        # Possible when not in check and castling squares are not occupied/attacked
        # The king and the moving rook must not have moved before in the game
        # King side castling
        # Swap between king and rook where king moves two steps towards the rook that moves to the left of the king
        # Queen side castling
        # Swap between king and rook where king moves three steps towards the rook that moves to the right of the king

        king_side_castle = True
        queen_side_castle = True
        if castle:
            # King not under check
            if detect_check(square_values, pieces, self.side):
                king_side_castle = False
                queen_side_castle = False
            else:
                for piece, movement, move_type, move in game_moves:
                    # No king move
                    if KING + self.side in piece or (not king_side_castle and not queen_side_castle):
                        king_side_castle = False
                        queen_side_castle = False
                        break
                    # No Rook moves
                    if piece == ROOK + self.side + "2":
                        king_side_castle = False
                    if piece == ROOK + self.side + "1":
                        queen_side_castle = False
        else:
            king_side_castle = False
            queen_side_castle = False

        # Castling moves not blocked/attacked
        if king_side_castle:
            castling_squares = [f"f{self.row_notations[0]}", f"g{self.row_notations[0]}"]
            for square in castling_squares:
                if board_values[square] == EMPTY:
                    # Simulate move
                    square_values_copy = deepcopy(square_values)
                    pieces_copy = pieces.copy()
                    move_piece(square_values_copy, pieces_copy, self, square, MOVE)

                    # Castling not allowed if square is attacked
                    if detect_check(square_values_copy, pieces_copy, self.side):
                        king_side_castle = False
                        break
                else:
                    king_side_castle = False
                    break
        if queen_side_castle:
            castling_squares = [f"d{self.row_notations[0]}", f"c{self.row_notations[0]}"]
            for square in castling_squares:
                if board_values[square] == EMPTY:
                    # Simulate move
                    square_values_copy = deepcopy(square_values)
                    pieces_copy = pieces.copy()
                    move_piece(square_values_copy, pieces_copy, self, square, MOVE)

                    # Castling not allowed if square is attacked
                    if detect_check(square_values_copy, pieces_copy, self.side):
                        king_side_castle = False
                        break
                else:
                    queen_side_castle = False
                    break
        # Add castle moves if above conditions matched
        if king_side_castle:
            king_move = f"g{self.row_notations[0]}"
            move_types = [KING_SIDE_CASTLING]
            possible_moves.append([king_move, move_types])
        if queen_side_castle:
            king_move = f"c{self.row_notations[0]}"
            move_types = [QUEEN_SIDE_CASTLING]
            possible_moves.append([king_move, move_types])

        # List of all possible moves
        return possible_moves


class Queen(Pieces):
    """
    Subclass from 'Pieces' class
    Sets image for queens
    Sets possible moves for queens
    """

    # Attributes
    def __init__(self, side, number, piece_notation):
        # Set image depending on which side the piece belongs to
        self.img_path = "Images/Pictures/White Queen.png" if side == WHITE_SIDE else "Images/Pictures/Black Queen.png"

        # Call to parent class (Piece)
        super().__init__(QUEEN, side, number, self.img_path, piece_notation)

    # Possible moves
    def possible_moves(self, board_values, *_):
        """
        Calculates all possible moves of the chosen queen in the current position
        May include illegal moves that may result in king being captured
        Returns a list of possible moves with the move and the move type as an element

        :param board_values: Dictionary of each square value of each square notation in the board

        :return: possible_moves (type=list)
        """

        # Set move list
        possible_moves = []

        # Opposite column and row list
        if self.side == WHITE_SIDE:
            opposite_column_notations = COLUMN_NOTATIONS[1]
            opposite_row_notations = ROW_NOTATIONS[1]
        else:
            opposite_column_notations = COLUMN_NOTATIONS[0]
            opposite_row_notations = ROW_NOTATIONS[0]
        # Column and row index in list
        column_list_index = self.column_notations.index(self.notation[0])
        row_list_index = self.row_notations.index(self.notation[1])

        # Vertical and horizontal lines
        line_dict = {"North Row": self.row_notations[row_list_index + 1:],
                     "South Row": opposite_row_notations[NUM_SIDE_SQUARES - row_list_index:],
                     "West Column": opposite_column_notations[NUM_SIDE_SQUARES - column_list_index:],
                     "East Column": self.column_notations[column_list_index + 1:]}
        # Diagonals
        diagonal_dict = {"North West": [],
                         "South West": [],
                         "North East": [],
                         "South East": []}
        for length in range(1, NUM_SIDE_SQUARES):
            # North West
            column_notation = column_list_index - length
            row_notation = row_list_index + length
            if 0 <= column_notation <= NUM_SIDE_SQUARES - 1 and 0 <= row_notation <= NUM_SIDE_SQUARES - 1:
                diagonal_dict["North West"].append(
                    self.column_notations[column_notation] + self.row_notations[row_notation])
            # South West
            column_notation = column_list_index - length
            row_notation = row_list_index - length
            if 0 <= column_notation <= NUM_SIDE_SQUARES - 1 and 0 <= row_notation <= NUM_SIDE_SQUARES - 1:
                diagonal_dict["South West"].append(
                    self.column_notations[column_notation] + self.row_notations[row_notation])
            # North East
            column_notation = column_list_index + length
            row_notation = row_list_index + length
            if 0 <= column_notation <= NUM_SIDE_SQUARES - 1 and 0 <= row_notation <= NUM_SIDE_SQUARES - 1:
                diagonal_dict["North East"].append(
                    self.column_notations[column_notation] + self.row_notations[row_notation])
            # South East
            column_notation = column_list_index + length
            row_notation = row_list_index - length
            if 0 <= column_notation <= NUM_SIDE_SQUARES - 1 and 0 <= row_notation <= NUM_SIDE_SQUARES - 1:
                diagonal_dict["South East"].append(
                    self.column_notations[column_notation] + self.row_notations[row_notation])

        # Vertical and horizontal movements
        for direction, line in line_dict.items():
            # Columns
            if "Column" in direction:
                for col in line:
                    # Vertical moves
                    possible_move = col + self.notation[1]

                    # Set movement type
                    move_types = [MOVE]
                    square_value = board_values[possible_move]
                    if self.enemy_side in square_value:
                        move_types = [MOVE, CAPTURE]

                    # Prevent capture of own piece
                    if self.side not in square_value:
                        possible_moves.append([possible_move, move_types])

                    # Stop line check if piece blocking
                    if square_value != EMPTY:
                        break
            # Rows (Same but for columns)
            elif "Row" in direction:
                for rw in line:
                    possible_move = self.notation[0] + rw

                    # Set movement type
                    move_types = [MOVE]
                    square_value = board_values[possible_move]
                    if self.enemy_side in square_value:
                        move_types = [MOVE, CAPTURE]

                    # Prevent capture of own piece
                    if self.side not in square_value:
                        possible_moves.append([possible_move, move_types])

                    if square_value != EMPTY:
                        break

        # Diagonal movements
        for direction, line in diagonal_dict.items():
            # Diagonal moves in each direction
            for move_notation in line:
                # Diagonal move
                possible_move = move_notation

                # Set movement type
                move_types = [MOVE]
                square_value = board_values[possible_move]
                if self.enemy_side in square_value:
                    move_types = [MOVE, CAPTURE]

                # Prevent capture of own piece
                if self.side not in square_value:
                    possible_moves.append([possible_move, move_types])

                # Stop line check if piece blocking
                if square_value != EMPTY:
                    break

        # List of all possible moves
        return possible_moves


class Rook(Pieces):
    """
    Subclass from 'Pieces' class
    Sets image for rooks
    Sets possible moves for rooks
    """

    # Attributes
    def __init__(self, side, number, piece_notation):
        # Set image depending on which side the piece belongs to
        self.img_path = "Images/Pictures/White Rook.png" if side == WHITE_SIDE else "Images/Pictures/Black Rook.png"

        # Call to parent class (Piece)
        super().__init__(ROOK, side, number, self.img_path, piece_notation)

    # Possible moves
    def possible_moves(self, board_values, *_):
        """
        Calculates all possible moves of the chosen rook in the current position
        May include illegal moves that may result in king being captured
        Returns a list of possible moves with the move and the move type as an element

        :param board_values: Dictionary of each square value of each square notation in the board

        :return: possible_moves (type=list)
        """

        # Set move list
        possible_moves = []

        # Opposite column and row list
        if self.side == WHITE_SIDE:
            opposite_column_notations = COLUMN_NOTATIONS[1]
            opposite_row_notations = ROW_NOTATIONS[1]
        else:
            opposite_column_notations = COLUMN_NOTATIONS[0]
            opposite_row_notations = ROW_NOTATIONS[0]
        # Column and row index in list
        column_list_index = self.column_notations.index(self.notation[0])
        row_list_index = self.row_notations.index(self.notation[1])

        # Vertical and horizontal lines
        line_dict = {"North Row": self.row_notations[row_list_index + 1:],
                     "South Row": opposite_row_notations[NUM_SIDE_SQUARES - row_list_index:],
                     "West Column": opposite_column_notations[NUM_SIDE_SQUARES - column_list_index:],
                     "East Column": self.column_notations[column_list_index + 1:]}

        # Vertical and horizontal movements
        for direction, line in line_dict.items():
            # Columns
            if "Column" in direction:
                for col in line:
                    # Vertical moves
                    possible_move = col + self.notation[1]

                    # Set movement type
                    move_types = [MOVE]
                    square_value = board_values[possible_move]
                    if self.enemy_side in square_value:
                        move_types = [MOVE, CAPTURE]

                    # Prevent capture of own piece
                    if self.side not in square_value:
                        possible_moves.append([possible_move, move_types])

                    # Stop line check if piece blocking
                    if square_value != EMPTY:
                        break
            # Rows (Same but for columns)
            elif "Row" in direction:
                for rw in line:
                    possible_move = self.notation[0] + rw

                    # Set movement type
                    move_types = [MOVE]
                    square_value = board_values[possible_move]
                    if self.enemy_side in square_value:
                        move_types = [MOVE, CAPTURE]

                    # Prevent capture of own piece
                    if self.side not in square_value:
                        possible_moves.append([possible_move, move_types])

                    if square_value != EMPTY:
                        break

        # List of all possible moves
        return possible_moves


class Bishop(Pieces):
    """
    Subclass from 'Pieces' class
    Sets image for bishops
    Sets possible moves for bishops
    """

    # Attributes
    def __init__(self, side, number, piece_notation):
        # Set image depending on which side the piece belongs to
        self.img_path = "Images/Pictures/White Bishop.png" if side == WHITE_SIDE else "Images/Pictures/Black Bishop.png"

        # Call to parent class (Piece)
        super().__init__(BISHOP, side, number, self.img_path, piece_notation)

    # Possible moves
    def possible_moves(self, board_values, *_):
        """
        Calculates all possible moves of the chosen bishop in the current position
        May include illegal moves that may result in king being captured
        Returns a list of possible moves with the move and the move type as an element

        :param board_values: Dictionary of each square value of each square notation in the board

        :return: possible_moves (type=list)
        """

        # Set move list
        possible_moves = []

        # Column and row index in list
        column_list_index = self.column_notations.index(self.notation[0])
        row_list_index = self.row_notations.index(self.notation[1])

        # Diagonals
        diagonal_dict = {"North West": [],
                         "South West": [],
                         "North East": [],
                         "South East": []}
        for length in range(1, NUM_SIDE_SQUARES):
            # North West
            column_notation = column_list_index - length
            row_notation = row_list_index + length
            if 0 <= column_notation <= NUM_SIDE_SQUARES - 1 and 0 <= row_notation <= NUM_SIDE_SQUARES - 1:
                diagonal_dict["North West"].append(
                    self.column_notations[column_notation] + self.row_notations[row_notation])
            # South West
            column_notation = column_list_index - length
            row_notation = row_list_index - length
            if 0 <= column_notation <= NUM_SIDE_SQUARES - 1 and 0 <= row_notation <= NUM_SIDE_SQUARES - 1:
                diagonal_dict["South West"].append(
                    self.column_notations[column_notation] + self.row_notations[row_notation])
            # North East
            column_notation = column_list_index + length
            row_notation = row_list_index + length
            if 0 <= column_notation <= NUM_SIDE_SQUARES - 1 and 0 <= row_notation <= NUM_SIDE_SQUARES - 1:
                diagonal_dict["North East"].append(
                    self.column_notations[column_notation] + self.row_notations[row_notation])
            # South East
            column_notation = column_list_index + length
            row_notation = row_list_index - length
            if 0 <= column_notation <= NUM_SIDE_SQUARES - 1 and 0 <= row_notation <= NUM_SIDE_SQUARES - 1:
                diagonal_dict["South East"].append(
                    self.column_notations[column_notation] + self.row_notations[row_notation])

        # Diagonal movements
        for direction, line in diagonal_dict.items():
            # Diagonal moves in each direction
            for move_notation in line:
                # Diagonal move
                possible_move = move_notation

                # Set movement type
                move_types = [MOVE]
                square_value = board_values[possible_move]
                if self.enemy_side in square_value:
                    move_types = [MOVE, CAPTURE]

                # Prevent capture of own piece
                if self.side not in square_value:
                    possible_moves.append([possible_move, move_types])

                # Stop line check if piece blocking
                if square_value != EMPTY:
                    break

        # List of all possible moves
        return possible_moves


class Knight(Pieces):
    """
    Subclass from piece
    Sets image for knights
    Sets possible moves for knights
    """

    # Attributes
    def __init__(self, side, number, piece_notation):
        # Set image depending on which side the piece belongs to
        self.img_path = "Images/Pictures/White Knight.png" if side == WHITE_SIDE else "Images/Pictures/Black Knight.png"

        # Call to parent class (Piece)
        super().__init__(KNIGHT, side, number, self.img_path, piece_notation)

    # Possible moves of piece
    def possible_moves(self, board_values, *_):
        """
        Calculates all possible moves of the chosen knight in the current position
        May include illegal moves that may result in king being captured
        Returns a list of possible moves with the move and the move type as an element

        :param board_values: Dictionary of each square value of each square notation in the board

        :return: possible_moves (type=list)
        """

        # Set move list
        possible_moves = []

        # Column and row index in list
        column_list_index = self.column_notations.index(self.notation[0])
        row_list_index = self.row_notations.index(self.notation[1])

        # Knights only move 2 squares or 1 squares vertically or horizontally
        movement_lengths = [-2, -1, 1, 2]
        for length in movement_lengths:
            column_notation_index = column_list_index + length
            # Valid column
            if 0 <= column_notation_index <= NUM_SIDE_SQUARES - 1:
                # Determine row movement based on column movement
                if length > 0:
                    row_notation_index_1 = row_list_index + (3 - length)
                    row_notation_index_2 = row_list_index - (3 - length)
                else:
                    row_notation_index_1 = row_list_index + (3 + length)
                    row_notation_index_2 = row_list_index - (3 + length)

                # Valid row
                if 0 <= row_notation_index_1 <= NUM_SIDE_SQUARES - 1:
                    possible_move_1 = \
                        self.column_notations[column_notation_index] + self.row_notations[row_notation_index_1]

                    # Set movement type
                    move_types = [MOVE]
                    square_value = board_values[possible_move_1]
                    if self.enemy_side in square_value:
                        move_types = [MOVE, CAPTURE]

                    # Prevent capture of own piece
                    if self.side not in square_value:
                        possible_moves.append([possible_move_1, move_types])

                if 0 <= row_notation_index_2 <= NUM_SIDE_SQUARES - 1:
                    possible_move_2 = \
                        self.column_notations[column_notation_index] + self.row_notations[row_notation_index_2]

                    # Set movement type
                    move_types = [MOVE]
                    square_value = board_values[possible_move_2]
                    if self.enemy_side in square_value:
                        move_types = [MOVE, CAPTURE]

                    # Prevent capture of own piece
                    if self.side not in square_value:
                        possible_moves.append([possible_move_2, move_types])

        # List of all possible moves
        return possible_moves


class Pawn(Pieces):
    """
    Subclass from 'Pieces' class
    Sets image for pawns
    Sets possible moves for pawns
    """

    # Attributes
    def __init__(self, side, number, piece_notation):
        # Set image depending on which side the piece belongs to
        self.img_path = "Images/Pictures/White Pawn.png" if side == WHITE_SIDE else "Images/Pictures/Black Pawn.png"

        # Call to parent class (Piece)
        super().__init__(PAWN, side, number, self.img_path, piece_notation)

    # Possible moves of piece
    def possible_moves(self, board_values, *_):
        """
        Calculates all possible moves of the chosen pawn in the current position
        May include illegal moves that may result in king being captured
        Returns a list of possible moves with the move and the move type as an element

        :param board_values: Dictionary of each square value of each square notation in the board

        :return: possible_moves (type=list)
        """

        # Set move list
        possible_moves = []

        # Column and row index in list
        column_list_index = self.column_notations.index(self.notation[0])
        row_list_index = self.row_notations.index(self.notation[1])

        move_types = [MOVE]
        # Move one step
        possible_move_notation_1 = self.notation[0] + self.row_notations[row_list_index + 1]
        # Add move if no piece blocking
        if board_values[possible_move_notation_1] == EMPTY:
            # Set promotion move type if pawn reaches back rank
            if possible_move_notation_1[1] == self.row_notations[-1]:
                move_types = [MOVE, PROMOTION]

            possible_moves.append([possible_move_notation_1, move_types])

        # Move two steps if pawn has yet to move (still at starting rank)
        move_types = [MOVE]
        if self.notation[1] == self.row_notations[1] and possible_moves:
            possible_move_notation_2 = self.notation[0] + self.row_notations[row_list_index + 2]
            # Add move if no piece blocking
            if board_values[possible_move_notation_2] == EMPTY:
                possible_moves.append([possible_move_notation_2, move_types])

        # Captures
        move_types = [MOVE, CAPTURE]
        # Diagonal right
        # Check if diagonal square in board
        capture_notation_index_1 = column_list_index + 1
        if 0 <= capture_notation_index_1 <= NUM_SIDE_SQUARES - 1:
            possible_capture_notation_1 = self.column_notations[capture_notation_index_1] + \
                                          possible_move_notation_1[1]
            # Add move if enemy piece is there
            if self.enemy_side in board_values[possible_capture_notation_1]:
                # Set promotion move type if pawn reaches back rank
                if possible_move_notation_1[1] == self.row_notations[-1]:
                    move_types = [MOVE, CAPTURE, PROMOTION]

                possible_moves.append([possible_capture_notation_1, move_types])

        move_types = [MOVE, CAPTURE]
        # Diagonal left (Same as above)
        capture_notation_index_2 = column_list_index - 1
        if 0 <= capture_notation_index_2 <= NUM_SIDE_SQUARES - 1:
            possible_capture_notation_2 = self.column_notations[capture_notation_index_2] + \
                                          possible_move_notation_1[1]

            if self.enemy_side in board_values[possible_capture_notation_2]:
                # Set promotion move type if pawn reaches back rank
                if possible_move_notation_1[1] == self.row_notations[-1]:
                    move_types = [MOVE, CAPTURE, PROMOTION]

                possible_moves.append([possible_capture_notation_2, move_types])

        # En passant
        move_types = [MOVE, CAPTURE, EN_PASSANT]
        # Allows enemy pawn that had just moved two steps up to land beside a pawn to be captured by that pawn as
        # if it had only moved one step
        if game_moves:
            last_piece, last_movement, last_move_type, last_move = game_moves[-1]
            # Last move is pawn and chosen pawn is at 5th rank from viewing perspective
            if PAWN in last_piece and self.notation[1] == self.row_notations[4]:
                # Enemy pawn just moved two steps last move
                piece_origin, piece_destination = last_movement
                if int(piece_destination[1]) - int(piece_origin[1]) in (-2, 2):
                    # Enemy pawn beside current pawn
                    piece_column_index = self.column_notations.index(piece_destination[0])
                    if piece_column_index == capture_notation_index_1 or \
                            piece_column_index == capture_notation_index_2:
                        en_passant_notation = piece_destination[0] + possible_move_notation_1[1]
                        possible_moves.append([en_passant_notation, move_types])

        # List of all possible moves
        return possible_moves


# Dictionaries
board_squares = set_board()
square_values = {}
for notation in board_squares.keys():
    square_values[notation] = EMPTY
# Pieces
pieces = {KING + WHITE_SIDE + "1": King(WHITE_SIDE, "1", "e1"),
          KING + BLACK_SIDE + "1": King(BLACK_SIDE, "1", "e8"),
          QUEEN + WHITE_SIDE + "1": Queen(WHITE_SIDE, "1", "d1"),
          QUEEN + BLACK_SIDE + "1": Queen(BLACK_SIDE, "1", "d8"),
          ROOK + WHITE_SIDE + "1": Rook(WHITE_SIDE, "1", "a1"),
          ROOK + WHITE_SIDE + "2": Rook(WHITE_SIDE, "2", "h1"),
          ROOK + BLACK_SIDE + "1": Rook(BLACK_SIDE, "1", "a8"),
          ROOK + BLACK_SIDE + "2": Rook(BLACK_SIDE, "2", "h8"),
          BISHOP + WHITE_SIDE + "1": Bishop(WHITE_SIDE, "1", "c1"),
          BISHOP + WHITE_SIDE + "2": Bishop(WHITE_SIDE, "2", "f1"),
          BISHOP + BLACK_SIDE + "1": Bishop(BLACK_SIDE, "1", "c8"),
          BISHOP + BLACK_SIDE + "2": Bishop(BLACK_SIDE, "2", "f8"),
          KNIGHT + WHITE_SIDE + "1": Knight(WHITE_SIDE, "1", "b1"),
          KNIGHT + WHITE_SIDE + "2": Knight(WHITE_SIDE, "2", "g1"),
          KNIGHT + BLACK_SIDE + "1": Knight(BLACK_SIDE, "1", "b8"),
          KNIGHT + BLACK_SIDE + "2": Knight(BLACK_SIDE, "2", "g8")}
for pawn_count in range(1, 9):
    pieces[PAWN + WHITE_SIDE + str(pawn_count)] = \
        Pawn(WHITE_SIDE, str(pawn_count), COLUMN_NOTATIONS[0][pawn_count - 1] + ROW_NOTATIONS[0][1])
    pieces[PAWN + BLACK_SIDE + str(pawn_count)] = \
        Pawn(BLACK_SIDE, str(pawn_count), COLUMN_NOTATIONS[1][pawn_count - 1] + ROW_NOTATIONS[1][1])
# Player data
player_1 = {"name display": Bottom_Player_Name,
            "icon display": Bottom_Player_Icon,
            "side": BLACK_SIDE,
            "points": 0,
            "time": {"display": Top_Time_Count, "units": initial_time.copy()}}
player_2 = {"name display": Top_Player_Name,
            "icon display": Top_Player_Icon,
            "side": WHITE_SIDE,
            "points": 0,
            "time": {"display": Bottom_Time_Count, "units": initial_time.copy()}}

# Lists
game_moves = []
game_pos = [square_values.copy()]
column_labels, row_labels = side_labels(board_squares)

# Main program
if __name__ == "__main__":
    # Code

    # Set timer
    initial_time = ""
    for unit_count in range(0, len(player_2["time"]["units"])):
        time_unit = str(player_2["time"]["units"][unit_count])
        initial_time += "0" * (len(str(MAX_TIME_UNITS[unit_count])) - len(time_unit)) + time_unit
        if unit_count != len(player_2["time"]["units"]) - 1:
            initial_time += ":"
    player_2["time"]["display"].config(text=initial_time)
    initial_time = ""
    for unit_count in range(0, len(player_1["time"]["units"])):
        time_unit = str(player_1["time"]["units"][unit_count])
        initial_time += "0" * (len(str(MAX_TIME_UNITS[unit_count])) - len(time_unit)) + time_unit
        if unit_count != len(player_1["time"]["units"]) - 1:
            initial_time += ":"
    player_1["time"]["display"].config(text=initial_time)

    # Exit confirmation
    WIN.protocol("WM_DELETE_WINDOW", exit)

    # Initiate GUI
    WIN.mainloop()
