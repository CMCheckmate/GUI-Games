# Modules
import pygame
import math
import random
from time import time

# Initialising
pygame.init()

# Displaying screen
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

# Setting screen icon and title
icon = pygame.display.set_icon(pygame.image.load('Pictures/Tic Tac Toe icon.jpg'))
title = pygame.display.set_caption("Tic Tac Toe")

# Constants
# Colours
WHITE = (255, 255, 255)
GREY = (64, 64, 64)
BLACK = (0, 0, 0)


# Classes

# Button
class Button(object):
    def __init__(self, x, y, pages_show, normal_filename, hovered_filename, clicked_filename, is_draw=True):
        self.x = x
        self.y = y
        self.normal_image = pygame.image.load(normal_filename)
        self.hovered_image = pygame.image.load(hovered_filename)
        self.clicked_image = pygame.image.load(clicked_filename)
        self.width = self.normal_image.get_width()
        self.height = self.normal_image.get_height()
        self.pages_show = pages_show
        self.focused = False
        self.holding = False
        self.is_draw = is_draw

    def hover(self, page):
        if page in self.pages_show and self.is_draw:
            if self.x <= pygame.mouse.get_pos()[0] <= self.x + self.width and \
                    self.y <= pygame.mouse.get_pos()[1] <= self.y + self.height:
                return True

    def clicked(self, page, occurrence):
        if page in self.pages_show and self.is_draw:
            if "CLICKED" in occurrence:
                if self.hover(page):
                    self.focused = True
                    self.holding = True
                else:
                    self.focused = False

            if self.holding and "RELEASED" in occurrence:
                self.holding = False

                if self.hover(page):
                    return True

            return False

    def draw(self, page):
        if page in self.pages_show and self.is_draw:
            if self.holding:
                screen.blit(self.clicked_image, (self.x, self.y))
            elif self.hover(page):
                screen.blit(self.hovered_image, (self.x, self.y))
            else:
                screen.blit(self.normal_image, (self.x, self.y))


class Image(object):
    def __init__(self, x, y, pages_show, filename, is_draw=True):
        self.x = x
        self.y = y
        self.image = pygame.image.load(filename)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.pages_show = pages_show
        self.is_draw = is_draw

    def draw(self, page):
        if page in self.pages_show and self.is_draw:
            screen.blit(self.image, (self.x, self.y))


class Text(object):
    def __init__(self, x, y, type, colour, size, string, pages_show, is_draw=True, is_bold=False, is_italic=False):
        self.x = x
        self.y = y
        self.string = string
        self.font_size = size
        self.font_type = type
        self.font_colour = colour
        self.is_italic = is_italic
        self.is_bold = is_bold
        self.typography = pygame.font.SysFont(self.font_type, self.font_size, self.is_bold, self.is_italic)
        self.pages_show = pages_show
        self.is_draw = is_draw

    def generate_surface(self):
        self.typography = pygame.font.SysFont(self.font_type, self.font_size, self.is_bold, self.is_italic)
        surface = self.typography.render(self.string, 1, self.font_colour)

        return surface

    def draw(self, page):
        if self.is_draw and page in self.pages_show:
            screen.blit(self.generate_surface(), (self.x, self.y))


# Functions

# Get all events that happen while in game loop
def get_event():
    occurrence = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            occurrence.append("QUIT")

        if event.type == pygame.MOUSEBUTTONDOWN:
            occurrence.append("CLICKED")
        if event.type == pygame.MOUSEBUTTONUP:
            occurrence.append("RELEASED")

        if event.type == pygame.KEYDOWN:
            occurrence.append("TYPED")
            if event.key == pygame.K_RETURN:
                occurrence.append("ENTER")
            elif event.key == pygame.K_ESCAPE:
                occurrence.append("ESCAPE")
            elif event.key == pygame.K_BACKSPACE:
                occurrence.append("BACKSPACE")
            elif event.key != pygame.K_TAB:
                occurrence.append("LETTER")
                occurrence.append(event.unicode)

    return occurrence


# Blink cursor
def draw_blinking_cursor(cursor_image, tag, name):
    if tag.focused:
        if loop_count % 50 == 0:
            cursor_image.is_draw = False
        elif loop_count % 25 == 0:
            cursor_image.is_draw = True

        cursor_image.x = round(name.x + name.generate_surface().get_width())

        if cursor_image.is_draw:
            cursor_image.draw(screen_page)


# Enter username
def update_username(occurrence, tag, name, opponent):
    # Update username as typed
    if opponent[0] != "COMPUTER":
        if tag.focused and "TYPED" in occurrence:
            if "BACKSPACE" in occurrence:
                name.string = name.string[:-1]
            elif len(name.string) < 15 and "LETTER" in occurrence:
                name.string = name.string + occurrence[-1]

    # Set computer names
    else:
        name.string = opponent[1] + " Computer"

    # Align username in center of name tag
    name.x = round(tag.x + (tag.width - name.generate_surface().get_width()) / 2)


# Choose profile_picture option
def choose_profile_picture_option(player):
    if switch_arrow_button.clicked(screen_page, events):
        try:
            if player[0] == "PLAYER":
                player[1] = PLAYER_OPTIONS[PLAYER_OPTIONS.index(player[1]) + 1]
            elif player[0] == "COMPUTER":
                player[1] = COMPUTER_OPTIONS[COMPUTER_OPTIONS.index(player[1]) + 1]
        except IndexError:
            if player[0] == "PLAYER":
                player[1] = PLAYER_OPTIONS[0]
            elif player[0] == "COMPUTER":
                player[1] = COMPUTER_OPTIONS[0]

    return player[1]


# Choose player
def choose_player_options(player, player_choice_1_text, player_choice_2_text, name):
    if choosing_bar_2_button.clicked(screen_page, events):
        choosing_bar_2_button.is_draw = False
        player_choice_2_text.is_draw = False

        player[0] = player_choice_2_text.string

        player_choice_1_text.string, player_choice_2_text.string = player[0], player_choice_1_text.string

        if player[0] == "PLAYER" and player[1] != PLAYER_OPTIONS[0]:
            player[1] = PLAYER_OPTIONS[0]

            name.string = ""
        elif player[0] == "COMPUTER" and player[1] != COMPUTER_OPTIONS[0]:
            player[1] = COMPUTER_OPTIONS[0]

    return player


# Choose page to show
def choose_page(previous_page):
    global start_time

    if home_button.clicked(screen_page, events) and screen_page == "INGAME" and not confirm_exit_image.is_draw:
        confirm_exit_image.is_draw = True
        confirm_button.is_draw = True
        cancel_button.is_draw = True
        for pos in position_buttons:
            pos.is_draw = False

    if profile_frame_button_1.clicked(screen_page, events):
        return "PLAYERCHOOSING 1"
    elif profile_frame_button_2.clicked(screen_page, events):
        return "PLAYERCHOOSING 2"
    elif SFX_button.clicked(screen_page, events) and not confirm_exit_image.is_draw:
        return "SFX"
    elif game_won is not None and screen_page != "SFX" and start_time == math.inf:
        return "VICTORY"
    elif play_button.clicked(screen_page, events):
        if username_text_1.string == "" or username_text_2.string == "":
            no_name_image.is_draw = True
            start_time = time()
        else:
            return "INGAME"
    elif confirm_button.clicked(screen_page, events):
        confirm_exit_image.is_draw = False
        confirm_button.is_draw = False
        cancel_button.is_draw = False
        return "HOMEPAGE"
    elif home_button.clicked(screen_page, events) and screen_page != "INGAME":
        return "HOMEPAGE"
    elif return_button.clicked(screen_page, events):
        return previous_page

    return "SAME"


# Choose profile to blit
def choose_profile_image(player):
    profile_picture = ""
    if player[0] == "PLAYER":
        if player[1] == "Default":
            profile_picture = default_player_image
        elif player[1] == "Blocky":
            profile_picture = blocky_player_image
        elif player[1] == "Stick Figure":
            profile_picture = stick_figure_player_image
    elif player[0] == "COMPUTER":
        if player[1] == "Easy":
            profile_picture = easy_computer_image
        elif player[1] == "Medium":
            profile_picture = medium_computer_image
        elif player[1] == "Hard":
            profile_picture = hard_computer_image

    return profile_picture.image


# Player choosing screen function
def player_choosing_screen(player, profile_image, player_choice_1_text, player_choice_2_text,
                           profile_picture_option_text, name):
    profile_image.image = choose_profile_image(player)

    player = choose_player_options(player, player_choice_1_text, player_choice_2_text, name)
    player[1] = choose_profile_picture_option(player)

    profile_picture_option_text.string = player[1]
    profile_picture_option_text.x = \
        round((screen_width - profile_picture_option_text.generate_surface().get_width()) / 2)

    player_choice_1_text.x = \
        round(((choosing_bar_1_button.width + scrolling_bar_button.width -
                player_choice_1_text.generate_surface().get_width()) / 2) + choosing_bar_1_button.x)
    player_choice_2_text.x = \
        round(((choosing_bar_1_button.width + scrolling_bar_button.width -
                player_choice_2_text.generate_surface().get_width()) / 2) + choosing_bar_1_button.x)

    if not choosing_bar_2_button.is_draw:
        if scrolling_bar_button.clicked(screen_page, events):
            choosing_bar_2_button.is_draw = True
            player_choice_2_text.is_draw = True
    else:
        if scrolling_bar_button.clicked(screen_page, events):
            choosing_bar_2_button.is_draw = False
            player_choice_2_text.is_draw = False

    if not scrolling_bar_button.focused and not choosing_bar_2_button.focused:
        choosing_bar_2_button.is_draw = False
        player_choice_2_text.is_draw = False


# Determine volume
def determine_volume():
    global muted, volume_level

    if volume_icon_button.clicked(screen_page, events) or check_box_button.clicked(screen_page, events):
        if muted:
            volume_level = 4
            muted = False
        else:
            volume_level = 0
            muted = True
    elif volume_level > 0 and muted:
        muted = False
    elif volume_level == 0:
        muted = True

    if muted:
        mute_line_image.is_draw = True
        check_image.is_draw = False
    else:
        check_image.is_draw = True
        mute_line_image.is_draw = False

    indicator_distance = 119
    if volume_bar_button.clicked(screen_page, events) and volume_bar_button.hover(screen_page):
        volume_level = math.floor((pygame.mouse.get_pos()[0] - volume_bar_button.x) / indicator_distance)
    indicator_pos = 517
    volume_indicator_image.x = indicator_pos + indicator_distance * volume_level

    # Set volume according to ratio of available volumes
    pygame.mixer.music.set_volume((volume_level / 4))


# Reset Game Settings
def reset_game(fully):
    global game_won, match_won, game_num, board_positions_list, player_turn, added

    if fully:
        game_won = None
        game_num = None

        player_1[2] = 0
        player_2[2] = 0
        user_1_score.string = 0
        user_2_score.string = 0
        player_turn = None
    else:
        player_turn = random.choice(["1", "2"])

    match_won = None
    added = False
    board_positions_list = ["", "", "", "", "", "", "", "", ""]


# Draw choose player screen
def draw_choose_player_screen(player_text_image, profile_image, profile_picture_option_text, player_choice_1_text, player_choice_2_text):

    return_button.draw(screen_page)

    player_text_image.draw(screen_page)

    screen.blit(pygame.transform.scale
                (profile_image.image, ((profile_image.width * 2), (profile_image.height * 2))), (521, 153))

    screen.blit(pygame.transform.scale
                (profile_frame_button_1.normal_image,
                 (profile_frame_button_1.width * 2, profile_frame_button_1.height * 2)), (499, 125))

    profile_picture_option_text.draw(screen_page)

    switch_arrow_button.draw(screen_page)

    player_choosing_bar_image.draw(screen_page)

    scrolling_bar_button.draw(screen_page)

    choosing_bar_1_button.draw(screen_page)
    choosing_bar_2_button.draw(screen_page)

    player_choice_1_text.draw(screen_page)
    player_choice_2_text.draw(screen_page)


# Draw SFX screen
def draw_sfx_screen():
    return_button.draw(screen_page)

    music_text_image.draw(screen_page)

    music_credits.draw(screen_page)

    check_box_button.draw(screen_page)

    volume_bar_button.draw(screen_page)

    volume_indicator_image.draw(screen_page)

    volume_icon_button.draw(screen_page)

    mute_line_image.draw(screen_page)

    check_image.draw(screen_page)


# Draw homepage
def draw_home_screen():
    background_addition_image.draw(screen_page)

    title_image.draw(screen_page)

    VS_text_image.draw(screen_page)

    SFX_button.draw(screen_page)

    # Name message
    no_name_image.draw(screen_page)

    # Player 1
    player_1_tag_image.draw(screen_page)

    profile_image_1.draw(screen_page)
    profile_frame_button_1.draw(screen_page)

    name_tag_button_1.draw(screen_page)

    name_tag_button_1.clicked(screen_page, events)

    draw_blinking_cursor(cursor_image_1, name_tag_button_1, username_text_1)

    username_text_1.draw(screen_page)

    # Player 2
    player_2_tag_image.draw(screen_page)

    profile_image_2.draw(screen_page)
    profile_frame_button_2.draw(screen_page)

    name_tag_button_2.draw(screen_page)

    name_tag_button_2.clicked(screen_page, events)

    draw_blinking_cursor(cursor_image_2, name_tag_button_2, username_text_2)

    username_text_2.draw(screen_page)

    play_button.draw(screen_page)


# Draw Game screen
def draw_in_game_screen(pos_list, games, turn):
    home_button.draw(screen_page)

    SFX_button.draw(screen_page)

    if match_won == 1:
        player_1_win_text_image.draw(screen_page)
    elif match_won == -1:
        player_2_win_text_image.draw(screen_page)
    elif match_won == 0:
        draw_text_image.draw(screen_page)
    elif turn == "1":
        player_1_turn_text_image.draw(screen_page)
    elif turn == "2":
        player_2_turn_text_image.draw(screen_page)
    else:
        Score_text_image.draw(screen_page)

    screen.blit(user_1_score.generate_surface(),
                (269 + round((625 - 269 - user_1_score.generate_surface().get_width()) / 2), user_1_score.y))
    screen.blit(user_2_score.generate_surface(),
                (662 + round((1016 - 662 - user_2_score.generate_surface().get_width()) / 2), user_2_score.y))

    dash_text_image.draw(screen_page)

    screen.blit(profile_image_1.image, (136, 44))
    screen.blit(profile_image_2.image, (1016, 44))

    screen.blit(profile_frame_button_1.normal_image, (125, 30))
    screen.blit(profile_frame_button_2.normal_image, (1005, 30))

    screen.blit(name_tag_button_1.normal_image, (110, 188))
    screen.blit(name_tag_button_2.normal_image, (990, 188))

    screen.blit(player_1_tag_image.image, (182, 0))
    screen.blit(player_2_tag_image.image, (1052, 0))

    screen.blit(username_text_1.generate_surface(),
                (round(110 + (name_tag_button_1.width - username_text_1.generate_surface().get_width()) / 2), 200))
    screen.blit(username_text_2.generate_surface(),
                (round(990 + (name_tag_button_2.width - username_text_2.generate_surface().get_width()) / 2), 200))

    game_board_image.draw(screen_page)

    # Display pieces according to pos list
    for square_index in range(len(pos_list)):
        piece_pos = (BOARD_POSITIONS[square_index][0] + 15, BOARD_POSITIONS[square_index][1] + 15)
        if pos_list[square_index] == "O":
            screen.blit(blue_piece_image.image, piece_pos)
        elif pos_list[square_index] == "X":
            screen.blit(red_piece_image.image, piece_pos)

    # Game Settings
    if games is None:
        game_settings_image.draw(screen_page)
        games_3.draw(screen_page)
        games_10_button.draw(screen_page)
        games_20_button.draw(screen_page)

    # Confirm quit image
    confirm_exit_image.draw(screen_page)
    confirm_button.draw(screen_page)
    cancel_button.draw(screen_page)


def draw_victory_screen(game_finished):
    SFX_button.draw(screen_page)

    restart_button.draw(screen_page)
    menu_button.draw(screen_page)

    victory_image.draw(screen_page)
    confetti_image.draw(screen_page)

    screen.blit(final_score_text.generate_surface(),
                (round((screen_width - final_score_text.generate_surface().get_width()) / 2), final_score_text.y))

    if game_finished == "1":
        p1_victory_image.draw(screen_page)

        screen.blit(profile_image_1.image, (579, 154))
        screen.blit(profile_frame_button_1.normal_image, (568, 140))
        screen.blit(username_text_1.generate_surface(),
                    (round((screen_width - username_text_1.generate_surface().get_width()) / 2), 115))
    elif game_finished == "2":
        p2_victory_image.draw(screen_page)

        screen.blit(profile_image_2.image, (579, 154))
        screen.blit(profile_frame_button_2.normal_image, (568, 140))
        screen.blit(username_text_2.generate_surface(),
                    (round((screen_width - username_text_2.generate_surface().get_width()) / 2), 115))
    elif game_finished == "0":
        tie_image.draw(screen_page)
        clash_image.draw(screen_page)


# Game functions
def eval_pos(pos_list):
    for win_pos in WIN_LIST:
        if pos_list[win_pos[0]] == "O" and pos_list[win_pos[1]] == "O" and pos_list[win_pos[2]] == "O":
            return 1
        elif pos_list[win_pos[0]] == "X" and pos_list[win_pos[1]] == "X" and pos_list[win_pos[2]] == "X":
            return -1

    for pos in pos_list:
        if pos == "":
            return None

    return 0


def easy_comp_move(pos_list):
    possible_moves = []
    for position in range(len(pos_list)):
        if pos_list[position] == "":
            possible_moves.append(position + 1)

    return random.choice(possible_moves)


def medium_comp_move(pos_list, player):
    if player[3] == "X":
        opponent_piece = "O"
    else:
        opponent_piece = "X"

    # Take win
    for line in WIN_LIST:
        piece_count = 0
        empty_pos = None
        for index in line:
            if pos_list[index] == player[3]:
                piece_count += 1
            elif pos_list[index] == "":
                empty_pos = index

        if piece_count == 2 and empty_pos is not None:
            return empty_pos + 1

    for line in WIN_LIST:
        piece_count = 0
        empty_pos = None
        for index in line:
            if pos_list[index] == opponent_piece:
                piece_count += 1
            elif pos_list[index] == "":
                empty_pos = index

        if piece_count == 2 and empty_pos is not None:
            return empty_pos + 1

    return easy_comp_move(pos_list)


def hard_comp_move(pos_list, turn, index_order, depth=0):
    best_move = None
    min_depth = math.inf

    current_eval = eval_pos(pos_list)
    if current_eval is not None:
        return [current_eval, min_depth], best_move
    elif turn == "1":
        max_score = -math.inf
        for possible_index in index_order:
            if pos_list[possible_index] == "":
                child_pos_list = pos_list[:]
                child_pos_list[possible_index] = "O"

                child_eval, child_depth = hard_comp_move(child_pos_list, "2", index_order, depth + 1)[0]
                if child_eval > max_score or (child_eval == max_score and child_depth <= min_depth):
                    max_score = child_eval
                    min_depth = child_depth
                    best_move = possible_index + 1

        return [[max_score, min_depth], best_move]
    elif turn == "2":
        min_score = math.inf
        for possible_index in index_order:
            if pos_list[possible_index] == "":
                child_pos_list = pos_list[:]
                child_pos_list[possible_index] = "X"

                child_eval, child_depth = hard_comp_move(child_pos_list, "1", index_order, depth + 1)[0]

                if child_eval < min_score or (child_eval == min_score and child_depth <= min_depth):
                    min_score = child_eval
                    min_depth = child_depth
                    best_move = possible_index + 1

        return [[min_score, min_depth], best_move]


# Class usage

# Buttons

# Play
play_button = Button(525, 475, "HOMEPAGE", 'Pictures/Play Button.jpg', 'Pictures/Play Button (hovered).jpg', 'Pictures/Play Button (Clicked).jpg')
# SFX
SFX_button = Button(1145, 550, ("HOMEPAGE", "INGAME", "VICTORY"), "Pictures/Sfx Symbol.jpg", "Pictures/Sfx Symbol (hovered).jpg", "Pictures/Sfx Symbol (hovered).jpg")
# Checkbox in sfx
check_box_button = Button(727, 405, "SFX", "Pictures/checkbox.jpg", "Pictures/checkbox.jpg", "Pictures/checkbox.jpg")
# Volume bar
volume_bar_button = Button(500, 150, "SFX", "Pictures/volume amplitude.jpg", "Pictures/volume amplitude.jpg", "Pictures/volume amplitude.jpg")
# Volume icon buttons
volume_icon_button = Button(275, 107, "SFX", "Pictures/volume icon.jpg", "Pictures/volume icon (hovered).jpg", "Pictures/volume icon (hovered).jpg")
# Return
return_button = Button(50, 550, ("SFX", "PLAYERCHOOSING 1", "PLAYERCHOOSING 2", "EDITPROFILE 1", "EDITPROFILE 2"), "Pictures/return icon.jpg", "Pictures/return icon (hovered).jpg", "Pictures/return icon (hovered).jpg")
# Home
home_button = Button(50, 550, "INGAME", "Pictures/Home icon.jpg", "Pictures/Home icon (hovered).jpg", "Pictures/Home icon (hovered).jpg")
# Profile Image
profile_frame_button_1 = Button(349, 235, "HOMEPAGE", 'Pictures/Player profile picture frame.jpg', 'Pictures/Player profile picture frame (hovered).jpg', 'Pictures/Player profile picture frame (hovered).jpg')
profile_frame_button_2 = Button(793, 235, "HOMEPAGE", 'Pictures/Player profile picture frame.jpg', 'Pictures/Player profile picture frame (hovered).jpg', 'Pictures/Player profile picture frame (hovered).jpg')
# Name tag
name_tag_button_1 = Button(333, 393, "HOMEPAGE", 'Pictures/Player name tag.jpg', 'Pictures/Player name tag.jpg', 'Pictures/Player name tag.jpg')
name_tag_button_2 = Button(777, 393, "HOMEPAGE", 'Pictures/Player name tag.jpg', 'Pictures/Player name tag.jpg', 'Pictures/Player name tag.jpg')
# Switch arrow button
switch_arrow_button = Button(554, 488, ("PLAYERCHOOSING 1", "PLAYERCHOOSING 2"), "Pictures/switch arrow.jpg", "Pictures/switch arrow (hovered).jpg", "Pictures/switch arrow (hovered).jpg")
# Choosing bar button
scrolling_bar_button = Button(778, 579, ("PLAYERCHOOSING 1", "PLAYERCHOOSING 2"), "Pictures/choosing bar button.jpg", "Pictures/choosing bar button (hovered).jpg", "Pictures/choosing bar button (hovered).jpg")
# Choosing bar options buttons
choosing_bar_1_button = Button(465, 577, ("PLAYERCHOOSING 1", "PLAYERCHOOSING 2"), "Pictures/choosing bar options.jpg", "Pictures/choosing bar options.jpg", "Pictures/choosing bar options.jpg")
choosing_bar_2_button = Button(465, 621, ("PLAYERCHOOSING 1", "PLAYERCHOOSING 2"), "Pictures/choosing bar options.jpg", "Pictures/choosing bar options.jpg", "Pictures/choosing bar options.jpg", False)
# Game Setting buttons
games_3 = Button(749, 321, "INGAME", "Pictures/Game Settings button.jpg", "Pictures/Game Settings button (hovered).jpg", "Pictures/Game Settings button.jpg")
games_10_button = Button(749, 423, "INGAME", "Pictures/Game Settings button.jpg", "Pictures/Game Settings button (hovered).jpg", "Pictures/Game Settings button.jpg")
games_20_button = Button(749, 522, "INGAME", "Pictures/Game Settings button.jpg", "Pictures/Game Settings button (hovered).jpg", "Pictures/Game Settings button.jpg")
# Restart/exit buttons
restart_button = Button(309, 195, "VICTORY", "Pictures/Restart Button.jpg", "Pictures/Restart Button (hovered).jpg", "Pictures/Restart Button (hovered).jpg")
menu_button = Button(832, 195, "VICTORY", "Pictures/Menu Button.jpg", "Pictures/Menu Button (hovered).jpg", "Pictures/Menu Button (hovered).jpg")
# Confirm and cancel buttons
confirm_button = Button(522, 425, ["HOMEPAGE", "INGAME"], "Pictures/confirm button.jpg", "Pictures/confirm button (hovered).jpg", "Pictures/confirm button (hovered).jpg", False)
cancel_button = Button(685, 425, ["HOMEPAGE", "INGAME"], "Pictures/cancel button.jpg", "Pictures/cancel button (hovered).jpg", "Pictures/cancel button (hovered).jpg", False)


# Images
# Backgrounds
main_background_image = Image(0, 0, ("HOMEPAGE", "SFX", "PLAYERCHOOSING 1", "PLAYERCHOOSING 2", "INGAME", "VICTORY"), "Pictures/GUI background.jpg")
background_addition_image = Image(0, 0, "HOMEPAGE", "Pictures/background addition.jpg")
# Game Setting page
game_settings_image = Image(375, 175, "INGAME", "Pictures/Game Settings.jpg")
# Title
title_image = Image(356, 47, "HOMEPAGE", 'Pictures/Title.jpg')
# VS text
VS_text_image = Image(596, 300, "HOMEPAGE", 'Pictures/VS text.jpg')
# Score text
Score_text_image = Image(523, 20, "INGAME", "Pictures/Score text.jpg")
# Player 1 and 2 tags
player_1_tag_image = Image(403, 200, "HOMEPAGE", "Pictures/player 1 tag.jpg")
player_2_tag_image = Image(840, 200, "HOMEPAGE", "Pictures/player 2 tag.jpg")
# Player 1 turn text
player_1_turn_text_image = Image(409, 30, "INGAME", "Pictures/p1_turn.jpg")
# Player 2 turn text
player_2_turn_text_image = Image(403, 30, "INGAME", "Pictures/p2_turn.jpg")
# Player 1 win text
player_1_win_text_image = Image(506, 20, "INGAME", "Pictures/p1 match win.jpg")
# Player 2 win text
player_2_win_text_image = Image(495, 20, "INGAME", "Pictures/p2 match win.jpg")
# Draw text
draw_text_image = Image(533, 20, "INGAME", "Pictures/Draw text.jpg")
# Dash text
dash_text_image = Image(625, 131, "INGAME", "Pictures/Dash text.jpg")
# Board
game_board_image = Image(402, 192, "INGAME", "Pictures/Tic Tac Toe Board.jpg")
# Red X
red_piece_image = Image(417, 207, "INGAME", "Pictures/Red X.jpg")
# Blue O
blue_piece_image = Image(417, 207, "INGAME", "Pictures/Blue O.jpg")
# Check
check_image = Image(737, 425, "SFX", "Pictures/check.jpg")
# Mute text
music_text_image = Image(200, 405, "SFX", "Pictures/Music text.jpg")
# Mute line
mute_line_image = Image(275, 107, "SFX", "Pictures/mute line.jpg")
# Music credits
music_credits = Image(350, 615, "SFX", "Pictures/credits.jpg")
# Volume indicator
volume_indicator_image = Image(517, 167, "SFX", "Pictures/volume indicator.jpg")
# Player text
Player_1_text_image = Image(461, 37, "PLAYERCHOOSING 1", "Pictures/player 1 text.jpg")
Player_2_text_image = Image(461, 37, "PLAYERCHOOSING 2", "Pictures/player 2 text.jpg")
# Profile Images
# Players
default_player_image = Image(521, 153, ("PLAYERCHOOSING 1", "PLAYERCHOOSING 2"), "Pictures/Player profile picture (default).jpg")
blocky_player_image = Image(521, 153, ("PLAYERCHOOSING 1", "PLAYERCHOOSING 2"), "Pictures/Player profile picture (block).jpg")
stick_figure_player_image = Image(521, 153, ("PLAYERCHOOSING 1", "PLAYERCHOOSING 2"), "Pictures/Player profile picture (stick figure).jpg")
# Computers
easy_computer_image = Image(521, 153, ("PLAYERCHOOSING 1", "PLAYERCHOOSING 2"), "Pictures/Computer profile picture (easy).jpg")
medium_computer_image = Image(521, 153, ("PLAYERCHOOSING 1", "PLAYERCHOOSING 2"), "Pictures/Computer profile picture (medium).jpg")
hard_computer_image = Image(521, 153, ("PLAYERCHOOSING 1", "PLAYERCHOOSING 2"), "Pictures/Computer profile picture (hard).jpg")
# Confirmed profile image
profile_image_1 = Image(360, 249, "HOMEPAGE", "Pictures/Player profile picture (default).jpg")
profile_image_2 = Image(804, 249, "HOMEPAGE", 'Pictures/Player profile picture (default).jpg')
# Cursors
cursor_image_1 = Image(339, 400, "HOMEPAGE", 'Pictures/Blinking name tag cursor.jpg')
cursor_image_2 = Image(783, 400, "HOMEPAGE", 'Pictures/Blinking name tag cursor.jpg')
# Player choosing bar
player_choosing_bar_image = Image(453, 563, ("PLAYERCHOOSING 1", "PLAYERCHOOSING 2"), "Pictures/player choosing bar.jpg")
# Victory screen and text
victory_image = Image(509, 320, "VICTORY", "Pictures/Victory.jpg")
confetti_image = Image(95, 250, "VICTORY", "Pictures/Confetti.jpg")
p1_victory_image = Image(384, 20, "VICTORY", "Pictures/P1 Wins.jpg")
p2_victory_image = Image(370, 20, "VICTORY", "Pictures/P2 Wins.jpg")
tie_image = Image(577, 20, "VICTORY", "Pictures/Tie.jpg")
clash_image = Image(530, 100, "VICTORY", "Pictures/tie clash.jpg")
# Confirm exits screen
confirm_exit_image = Image(430, 220, ["HOMEPAGE", "INGAME"], "Pictures/confirm exit.jpg", False)
# Confirm name input image
no_name_image = Image(394, 620, "HOMEPAGE", "Pictures/name message.jpg", False)

# Text

# Username
username_text_1 = Text(340, 405, "consolas", BLACK, 20, "", "HOMEPAGE")
username_text_2 = Text(784, 405, "consolas", BLACK, 20, "", "HOMEPAGE")
# User score
user_1_score = Text(481, 100, "consolas", GREY, 75, "0", "INGAME")
user_2_score = Text(717, 100, "consolas", GREY, 75, "0", "INGAME")
# Player choice
player_1_choice_1_text = Text(470, 578, "Arial", GREY, 40, "PLAYER", ("PLAYERCHOOSING 1", "PLAYERCHOOSING 2"), True, True)
player_1_choice_2_text = Text(470, 622, "Arial", GREY, 40, "COMPUTER", ("PLAYERCHOOSING 1", "PLAYERCHOOSING 2"), False, True)
player_2_choice_1_text = Text(470, 578, "Arial", GREY, 40, "PLAYER", ("PLAYERCHOOSING 1", "PLAYERCHOOSING 2"), True, True)
player_2_choice_2_text = Text(470, 622, "Arial", GREY, 40, "COMPUTER", ("PLAYERCHOOSING 1", "PLAYERCHOOSING 2"), False, True)
# Profile picture option
profile_picture_1_option_text = Text(643, 415, "arialblack", GREY, 50, "Default", ("PLAYERCHOOSING 1", "PLAYERCHOOSING 2"))
profile_picture_2_option_text = Text(643, 415, "arialblack", GREY, 50, "Default", ("PLAYERCHOOSING 1", "PLAYERCHOOSING 2"))
# Final score
final_score_text = Text(640, 294, "consolas", GREY, 25, f"{user_1_score.string} - {user_2_score.string}", "VICTORY")

# Music/Sounds

# Background music
pygame.mixer.music.load('Music and Sounds/Game music.wav')

# Match win
win_sound = pygame.mixer.Sound('Music and Sounds/game win.wav')
# Match Loss
loss_sound = pygame.mixer.Sound('Music and Sounds/game loss.wav')
# Draw
draw_sound = pygame.mixer.Sound('Music and Sounds/game drawn.wav')


# Constants
PLAYER_OPTIONS = ["Default", "Blocky", "Stick Figure"]
COMPUTER_OPTIONS = ["Easy", "Medium", "Hard"]
# Coordinates within each square to be place each piece
BOARD_POSITIONS = [[397, 185], [565, 185], [735, 185],
                   [397, 355], [565, 355], [735, 355],
                   [397, 520], [565, 520], [735, 520]]

# Variables
loop_count = 0
start_time = math.inf
place_time = math.inf
time_set = False
added = False

last_page = None
new_page = "SAME"
screen_page = "HOMEPAGE"

game_num = None

match_won = None
game_won = None

player_1 = ["PLAYER", "Default", 0, "O"]
player_2 = ["PLAYER", "Default", 0, "X"]

player_turn = None

board_positions_list = ["", "", "", "", "", "", "", "", ""]
WIN_LIST = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

# Board position buttons
position_buttons = []
for position_index in range(len(board_positions_list)):
    position_buttons.append(Button(BOARD_POSITIONS[position_index][0], BOARD_POSITIONS[position_index][1],
                                   ["INGAME"], "Pictures/Button placeholder.jpg", "Pictures/Button placeholder.jpg",
                                   "Pictures/Button placeholder.jpg"))

muted = False
volume_level = 4

# Start music
pygame.mixer.music.play(-1)

# Main game loop
in_game = True
while in_game:
    # Track number of loops
    loop_count += 1

    # Store events
    events = get_event()

    # Quit if window is closed
    if "QUIT" in events:
        in_game = False

    # Update for page to show
    if new_page != "SAME":
        last_page = screen_page
        screen_page = new_page
    new_page = choose_page(last_page)

    # Clear screen and display background
    screen.fill(WHITE)
    main_background_image.draw(screen_page)

    # Homepage settings
    if screen_page == "HOMEPAGE":
        reset_game(True)

        if username_text_1.string != "" and username_text_2.string != "":
            no_name_image.is_draw = False
        elif time() - start_time >= 2:
            no_name_image.is_draw = False
            start_time = math.inf

        # Update username for players
        update_username(events, name_tag_button_1, username_text_1, player_1)
        update_username(events, name_tag_button_2, username_text_2, player_2)

        # Draw Home screen
        draw_home_screen()

    # Player choosing screen settings
    # Player choosing screen 1
    elif screen_page == "PLAYERCHOOSING 1":
        player_choosing_screen(player_1, profile_image_1, player_1_choice_1_text, player_1_choice_2_text, profile_picture_1_option_text, username_text_1)

        draw_choose_player_screen(Player_1_text_image, profile_image_1, profile_picture_1_option_text, player_1_choice_1_text, player_1_choice_2_text)

    # Player choosing screen 2
    elif screen_page == "PLAYERCHOOSING 2":
        player_choosing_screen(player_2, profile_image_2, player_2_choice_1_text, player_2_choice_2_text, profile_picture_2_option_text, username_text_2)

        draw_choose_player_screen(Player_2_text_image, profile_image_2, profile_picture_2_option_text, player_2_choice_1_text, player_2_choice_2_text)

    # Sfx screen settings
    elif screen_page == "SFX":
        determine_volume()

        draw_sfx_screen()
    # Game screen settings
    elif screen_page == "INGAME":
        if confirm_button.clicked(screen_page, events) or cancel_button.clicked(screen_page, events):
            confirm_exit_image.is_draw = False
            confirm_button.is_draw = False
            cancel_button.is_draw = False

        if not confirm_exit_image.is_draw:
            for button in position_buttons:
                button.is_draw = True

        # Set amount of games
        if games_3.clicked(screen_page, events):
            game_num = 3
            player_turn = str(random.randint(1, 2))
        elif games_10_button.clicked(screen_page, events):
            game_num = 10
            player_turn = str(random.randint(1, 2))
        elif games_20_button.clicked(screen_page, events):
            game_num = 20
            player_turn = str(random.randint(1, 2))

        games_3.is_draw = False if game_num is not None or confirm_exit_image.is_draw else True
        games_10_button.is_draw = False if game_num is not None or confirm_exit_image.is_draw else True
        games_20_button.is_draw = False if game_num is not None or confirm_exit_image.is_draw else True

        # Enter pieces
        if game_num is not None and match_won is None:
            if player_turn == "1":
                if player_1[0] == "COMPUTER":
                    if not time_set:
                        place_time = time()
                        time_set = True
                    if time() - place_time >= 1:
                        if player_1[1] == "Easy":
                            board_positions_list[easy_comp_move(board_positions_list) - 1] = "O"
                        elif player_1[1] == "Medium":
                            board_positions_list[medium_comp_move(board_positions_list, player_1) - 1] = "O"
                        elif player_1[1] == "Hard":
                            board_positions_list[hard_comp_move(board_positions_list, "1", random.sample([0, 1, 2, 3, 4, 5, 6, 7, 8], 9))[1] - 1] = "O"
                        place_time = math.inf
                        time_set = False
                        player_turn = "2"
                else:
                    for button_index in range(len(position_buttons)):
                        if position_buttons[button_index].clicked(screen_page, events) \
                                and board_positions_list[button_index] == "":
                            board_positions_list[button_index] = "O"
                            player_turn = "2"
            elif player_turn == "2":
                if player_2[0] == "COMPUTER":
                    if not time_set:
                        place_time = time()
                        time_set = True
                    if time() - place_time >= 1:
                        if player_2[1] == "Easy":
                            board_positions_list[easy_comp_move(board_positions_list) - 1] = "X"
                        elif player_2[1] == "Medium":
                            board_positions_list[medium_comp_move(board_positions_list, player_2) - 1] = "X"
                        elif player_2[1] == "Hard":
                            board_positions_list[hard_comp_move(board_positions_list, "2", random.sample([0, 1, 2, 3, 4, 5, 6, 7, 8], 9))[1] - 1] = "X"
                        place_time = math.inf
                        time_set = False
                        player_turn = "1"
                else:
                    for button_index in range(len(position_buttons)):
                        if position_buttons[button_index].clicked(screen_page, events) \
                                and board_positions_list[button_index] == "":
                            board_positions_list[button_index] = "X"
                            player_turn = "1"

        match_won = eval_pos(board_positions_list)

        if not added:
            if match_won == 1:
                if player_1[2] < 998.5:
                    player_1[2] += 1.0
                added = True
                start_time = time()
            elif match_won == -1:
                if player_2[2] < 998.5:
                    player_2[2] += 1.0
                added = True
                start_time = time()
            elif match_won == 0:
                if player_1[2] < 999:
                    player_1[2] += 0.5
                if player_2[2] < 999:
                    player_2[2] += 0.5
                added = True
                start_time = time()

        if time() - start_time >= 1.5:
            if game_won is None:
                reset_game(False)
            elif game_won == "0":
                pygame.mixer.Sound.play(draw_sound)
            elif player_1[0] == "COMPUTER" and player_2[0] == "COMPUTER" and game_won:
                pygame.mixer.Sound.play(win_sound)
            elif player_1[0] == "COMPUTER" and game_won == "1":
                pygame.mixer.Sound.play(loss_sound)
            elif player_2[0] == "COMPUTER" and game_won == "2":
                pygame.mixer.Sound.play(loss_sound)
            else:
                pygame.mixer.Sound.play(win_sound)

            start_time = math.inf

        user_1_score.string = str(float(player_1[2]))
        user_2_score.string = str(float(player_2[2]))

        if float(user_1_score.string) + float(user_2_score.string) == game_num:
            if float(user_1_score.string) > float(user_2_score.string):
                game_won = "1"
            elif float(user_2_score.string) > float(user_1_score.string):
                game_won = "2"
            elif float(user_2_score.string) == float(user_2_score.string):
                game_won = "0"

        draw_in_game_screen(board_positions_list, game_num, player_turn)
    elif screen_page == "VICTORY":
        final_score_text.string = f"{user_1_score.string} - {user_2_score.string}"

        if restart_button.clicked(screen_page, events):
            reset_game(True)

            new_page = "INGAME"
        elif menu_button.clicked(screen_page, events):
            reset_game(True)

            new_page = "HOMEPAGE"

        draw_victory_screen(game_won)

    # Update game frame
    pygame.display.update()

# Exit game
pygame.quit()
