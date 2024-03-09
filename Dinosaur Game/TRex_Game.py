# Importing modules needed
import pygame
import warnings
from random import *

# Note: coordinates of objects are located on the left top corner

# Initialise program
pygame.init()

# Create game screen
screenwidth = 1283
screenheight = 665
screen = pygame.display.set_mode((screenwidth, screenheight))


# Classes
# Background
class Sheet(object):
    def __init__(self, x, width):
        self.x = x
        self.y = 115
        self.x_vel = 40
        self.y_vel = 0
        self.width = width
        self.height = 410


class Base(object):
    def __init__(self, x, x_vel):
        self.x = x
        self.y = 410
        self.platform_y = 429
        self.x_vel = x_vel
        self.y_vel = 0
        self.width = 4808
        self.height = 255
        self.excess_height = 19

        # Animations
        self.day_animations = pygame.image.load('Pictures/base-daytime(Dinosaur Game).jpg')
        self.night_animations = pygame.image.load('Pictures/base-nighttime(Dinosaur Game).jpg')


class Air(object):
    def __init__(self, x, x_vel):
        self.x = x
        self.y = 0
        self.x_vel = x_vel
        self.y_vel = 0
        self.width = 4808
        self.height = 665

        # Animations
        self.day_animations = pygame.image.load('Pictures/Air-daytime(Dinosaur Game).jpg')
        self.night_animations = pygame.image.load('Pictures/Air-nighttime(Dinosaur Game).jpg')


class Planet(object):
    def __init__(self, x, x_vel):
        self.x = x
        self.y = 125
        self.x_vel = x_vel
        self.y_vel = 0
        self.width = 25
        self.height = 45

        # Animations
        self.animations = pygame.image.load('Pictures/Moon(Dinosaur Game).jpg')


# Sprites
# Dinosaur Character
class Dinosaur(object):
    def __init__(self, y, jump_vel, is_duck, is_jump, is_dead, leg_lifted):
        self.x = 225
        self.y = y
        self.x_vel = 0
        self.y_vel = 0
        self.jump_vel = jump_vel
        self.duck_vel = 36
        self.duck_midair = False
        self.stand_width = 40
        self.stand_height = 44
        self.duck_width = 56
        self.duck_height = 26
        self.is_jump = is_jump
        self.is_duck = is_duck
        self.is_dead = is_dead
        self.is_won = False
        self.leg_lifted = leg_lifted

        # Sound
        self.jump_sound = pygame.mixer.Sound('Sounds/Dinosaur_Jumping_Sound.wav')
        self.death_sound = pygame.mixer.Sound('Sounds/Dinosaur_Death_Sound.wav')

        # Animations (index number 0 means in daytime, 1 means in nighttime)
        self.left_standing_animations = [pygame.image.load('Pictures/T-Rex-left-jumping-daytime(Dinosaur Game).jpg'), pygame.image.load('Pictures/T-Rex-left-jumping-nighttime(Dinosaur Game).jpg')]
        self.right_standing_animations = [pygame.image.load('Pictures/T-Rex-right-jumping-daytime(Dinosaur Game).jpg'), pygame.image.load('Pictures/T-Rex-right-jumping-nighttime(Dinosaur Game).jpg')]
        self.left_duck_animations = [pygame.image.load('Pictures/T-Rex-left-ducking-daytime(Dinosaur Game).jpg'), pygame.image.load('Pictures/T-Rex-left-ducking-nighttime(Dinosaur Game).jpg')]
        self.right_duck_animations = [pygame.image.load('Pictures/T-Rex-right-ducking-daytime(Dinosaur Game).jpg'), pygame.image.load('Pictures/T-Rex-right-ducking-nighttime(Dinosaur Game).jpg')]
        self.jumping_animations = [pygame.image.load('Pictures/T-Rex-jumping-daytime(Dinosaur Game).jpg'), pygame.image.load('Pictures/T-Rex-jumping-nighttime(Dinosaur Game).jpg')]
        self.dead_animations = [pygame.image.load('Pictures/T-Rex-Dead-daytime(Dinosaur Game).jpg'), pygame.image.load('Pictures/T-Rex-Dead-nighttime(Dinosaur Game).jpg')]


# Objects
# Obstacle attributes
class Obstacle(object):
    def __init__(self, x, y, x_vel, object):
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.y_vel = 0
        self.is_draw = object


# Cactus attributes
class Spike(object):
    def __init__(self, width, height, size):
        self.width = width
        self.height = height
        self.width_small_solo = 15
        self.width_small_duo = 32
        self.width_small_trio = 49
        self.width_tall_solo = 23
        self.width_tall_duo = 48
        self.width_tall_quadruple = 73
        self.height_small = 33
        self.height_tall = 46
        self.size = size
        # Animations
        self.day_animations = [pygame.image.load('Pictures/Cactus-Small-Solo-daytime.jpg'), pygame.image.load('Pictures/Cactus-Small-Duo-daytime.jpg'), pygame.image.load('Pictures/Cactus-Small-Trio-daytime.jpg'), pygame.image.load('Pictures/Cactus-Tall-Solo-daytime.jpg'), pygame.image.load('Pictures/Cactus-Tall-Duo-daytime.jpg'), pygame.image.load('Pictures/Cactus-Tall-Quadruple-daytime.jpg')]
        self.night_animations = [pygame.image.load('Pictures/Cactus-Small-Solo-nighttime.jpg'), pygame.image.load('Pictures/Cactus-Small-Duo-nighttime.jpg'), pygame.image.load('Pictures/Cactus-Small-Trio-nighttime.jpg'), pygame.image.load('Pictures/Cactus-Tall-Solo-nighttime.jpg'), pygame.image.load('Pictures/Cactus-Tall-Duo-nighttime.jpg'), pygame.image.load('Pictures/Cactus-Tall-Quadruple-nighttime.jpg')]


# Pterodactyl attributes
class Pterosaur(object):
    def __init__(self, flap_direction, position):
        self.y_bottom = 393
        self.y_middle = 360
        self.y_top = 335
        self.flap_direction = flap_direction
        self.width = 42
        self.height = 36
        self.position = position
        # Animations
        self.down_flap_animations = [pygame.image.load('Pictures/Pterodactyl-down-daytime(Dinosaur Game).jpg'), pygame.image.load('Pictures/Pterodactyl-down-nighttime(Dinosaur Game).jpg')]
        self.up_flap_animations = [pygame.image.load('Pictures/Pterodactyl-up-daytime(Dinosaur Game).jpg'), pygame.image.load('Pictures/Pterodactyl-up-nighttime(Dinosaur Game).jpg')]


# Functions
# Receives all events and returns event type
def event_checker():
    # Event list
    events = []
    # Non key events
    for event in pygame.event.get():
        # Exit ('x' pressed)
        if event.type == pygame.QUIT:
            events.append("QUIT")
        # Reset pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            if TRex.is_dead or TRex.is_won:
                if 665 <= pygame.mouse.get_pos()[0] <= 699 and 285 <= pygame.mouse.get_pos()[1] <= 315:
                    events.append("RESET")

    # Key events
    key = pygame.key.get_pressed()
    # Either Up or Down is pressed (cannot be pressed simultaneously)
    if key[pygame.K_UP]:
        events.append("UP")
    elif key[pygame.K_DOWN]:
        events.append("DOWN")

    if key[pygame.K_SPACE]:
        events.append("PAUSE")

    return events


def pause(interval):
    if "PAUSE" in event_checker():
        # Delay so game is not un paused straight away
        pygame.time.delay(200)

        # Blit pause screen
        if interval == "Day":
            pause_screen = Pause_font.render("GAME PAUSED", 1, (83, 83, 83))
        else:
            pause_screen = Pause_font.render("GAME PAUSED", 1, (255, 255, 255))
        screen.blit(pause_screen, (635, 250))
        pygame.display.update()

        paused = True
        while paused:
            # check if quit is pressed, else check if un pause
            if "QUIT" in event_checker():
                return "QUIT"
            elif "PAUSE" in event_checker():
                paused = False

        # Delay so game is not paused straight away
        pygame.time.delay(200)


def start_screen(begin_jumped, begin):
    # Set proportions of trex (unable to duck thus standing)
    TRex.width = TRex.stand_width
    TRex.height = TRex.stand_height

    # Detect and call jump function
    if "UP" in event_checker() and not TRex.is_jump:
        begin_jumped = True
        TRex.is_jump = True
        # Play jump sound
        TRex.jump_sound.play()
    # Jump function
    trex_jump()

    # Reset variables when sprite reaches ground again
    trex_variable_reset()

    # move Cover1 and Cover2 away after sprite jumps to begin game
    if begin_jumped:
        Cover1.x += Cover1.x_vel
        Cover2.x -= Cover2.x_vel

    # Displaying main screen
    display_screen(time)

    # Blit start screen words
    if not begin_jumped:
        start_screen_1 = Start_Screen1_font.render("TREX GAME", 1, (83, 83, 83))
        start_screen_2 = Start_Screen2_font.render("--------------- Jump to Begin ---------------", 1, (83, 83, 83))

        screen.blit(start_screen_1, (635, 200))
        screen.blit(start_screen_2, (600, 270))

    # Update screen
    pygame.display.update()

    if Cover1.x >= screenwidth and Cover2.x <= -Cover2.width:
        begin = False

    return [begin_jumped, begin]


def game_over_screen(interval):
    # Printing GameOver statement and restart button
    if interval == "Day":
        if TRex.is_dead:
            game_over_text = GameOver_font.render("GAME LOST", 1, (83, 83, 83))
        else:
            game_over_text = GameOver_font.render("GAME WON", 1, (83, 83, 83))
        screen.blit(pygame.image.load('Pictures/Reset-Button-daytime(Dinosaur Game).jpg'), (665, 285))
    else:
        if TRex.is_dead:
            game_over_text = GameOver_font.render("GAME LOST", 1, (255, 255, 255))
        else:
            game_over_text = GameOver_font.render("GAME WON", 1, (255, 255, 255))
        screen.blit(pygame.image.load('Pictures/Reset-Button-nighttime(Dinosaur Game).jpg'), (665, 285))
    screen.blit(game_over_text, (635, 250))
    pygame.display.update()


# Displaying score function
def scoreboard(points):
    if len(str(points)) == 1 and points != 0:
        text = "0000" + str(points)
    elif len(str(points)) == 2:
        text = "000" + str(points)
    elif len(str(points)) == 3:
        text = "00" + str(points)
    elif len(str(points)) == 4:
        text = "0" + str(points)
    elif len(str(points)) == 5:
        text = str(points)
    elif points >= 99999:
        text = "99999"
    else:
        text = "00000"
    return text


def choose_and_update(points, last_object, object, cactus, pterodactyl):
    # Choosing the next object (pterodactyl or cactus) when object disappears from screen
    if object.x <= -Cactus_1.width_tall_quadruple:
        # Choose either an object is created or nothing is shown
        is_obstacle = randrange(1, 3)
        if is_obstacle == 1:
            # Setting new current_object through randomising
            # increase chance of pterodactyl if last object was pterodactyl
            if last_object.is_draw == "Pterodactyl":
                object_picker = randrange(1, 4)
            else:
                object_picker = randrange(1, 9)
            # Pterodactyl (1 in 4 chance if last object was cactus, 2 in 3 chance if last object was pterodactyl)
            if object_picker <= 2 and points >= 700:
                # Update new object.is_draw
                object.is_draw = "Pterodactyl"
                # Randomise for position of pterodactyl
                pterodactyl.position = randrange(1, 4)

            # Cactus (3 in 4 chance if last object was cactus, 1 in 3 chance if last object was pterodactyl)
            else:
                # Update new object.is_draw
                object.is_draw = "Cactus"
                # Choose type of cactus (1-6)
                cactus.size = randrange(1, 7)
        else:
            # Update object.is_draw to blank if no objects are chosen
            object.is_draw = "Blank"


def set_object_y(object, cactus, pterodactyl):
    if object.is_draw == "Cactus":
        object.y = Ground.platform_y - cactus.height
    elif object.is_draw == "Pterodactyl":
        if pterodactyl.position == 1:
            object.y = pterodactyl.y_bottom
        elif pterodactyl.position == 2:
            object.y = pterodactyl.y_middle
        else:
            object.y = pterodactyl.y_top
    else:
        object.y = 429


def obstacle_position_reset():
    # Cactus (Longest Cactus length if chosen)
    if Object_1.x <= -Cactus_1.width_tall_quadruple:
        Object_1.x = 1284
    if Object_2.x <= -Cactus_2.width_tall_quadruple:
        Object_2.x = 1284
    if Object_3.x <= -Cactus_3.width_tall_quadruple:
        Object_3.x = 1284
    if Object_4.x <= -Cactus_4.width_tall_quadruple:
        Object_4.x = 1284


def collision_checker(object, cactus, pterodactyl):
    # Sprite death
    # Cactus (Left Top is impossible to collide with a cactus)
    if object.is_draw == "Cactus":
        # TRex Corner 2
        if object.x <= TRex.x + TRex.width <= object.x + cactus.width and object.y <= TRex.y <= object.y + cactus.height:
            return True
        # TRex Corner 3 (Left Quarter(because leg is located at quarter of width)
        if object.x <= TRex.x + (TRex.width / 4) <= object.x + cactus.width and object.y <= TRex.y + TRex.height <= object.y + cactus.height:
            return True
        # TRex Corner 4 (Right Quarter(because leg is located a quarter width from TRex + TRex.width)
        if object.x <= TRex.x + ((3 * TRex.width) / 4) <= object.x + cactus.width and object.y <= TRex.y + TRex.height <= object.y + cactus.height:
            return True

    # Pterodactyl
    if object.is_draw == "Pterodactyl":
        # TRex Corner 1 (Left Middle(because left top is air, and TRex tail is in middle of left side))
        if object.x <= TRex.x <= object.x + pterodactyl.width and object.y <= TRex.y + (TRex.width / 2) <= object.y + pterodactyl.height:
            return True
        # TRex Corner 2 (Right top)
        if object.x <= TRex.x + TRex.width <= object.x + pterodactyl.width and object.y <= TRex.y <= object.y + pterodactyl.height:
            return True
        # TRex Corner 3 (Left Quarter(because leg is located at quarter of width)
        if object.x <= TRex.x + (TRex.width / 4) <= object.x + pterodactyl.width and object.y <= TRex.y + TRex.height <= object.y + pterodactyl.height:
            return True
        # TRex Corner 4 (Right Quarter(because leg is located a quarter width from TRex + TRex.width)
        if object.x <= TRex.x + ((3 * TRex.width) / 4) <= object.x + pterodactyl.width and object.y <= TRex.y + TRex.height <= object.y + pterodactyl.height:
            return True


def change_cactus_proportions(cactus):
    # Changing cactus width and height according to type of cactus
    if cactus.size == 1:
        cactus.width = cactus.width_small_solo
        cactus.height = cactus.height_small
    elif cactus.size == 2:
        cactus.width = cactus.width_small_duo
        cactus.height = cactus.height_small
    elif cactus.size == 3:
        cactus.width = cactus.width_small_trio
        cactus.height = cactus.height_small
    elif cactus.size == 4:
        cactus.width = cactus.width_tall_solo
        cactus.height = cactus.height_tall
    elif cactus.size == 5:
        cactus.width = cactus.width_tall_duo
        cactus.height = cactus.height_tall
    else:
        cactus.width = cactus.width_tall_quadruple
        cactus.height = cactus.height_tall


def trex_jump():
    # Jump mechanics
    if TRex.is_jump:
        # Setting y_vel of TRex and changing y position of TRex to display jumping
        TRex.y_vel = TRex.jump_vel
        TRex.y -= TRex.y_vel
        # Changing acceleration of TRex as jumping, as if affected by gravity
        TRex.jump_vel -= 2


def trex_duck():
    # Duck mechanics
    if TRex.is_duck:
        # Determine whether TRex is in air or on ground
        if TRex.y < Ground.platform_y - TRex.duck_height:
            TRex.duck_midair = True
    # Only if TRex is in air, increase y_vel to make it fall down
    if TRex.duck_midair:
        TRex.y_vel = TRex.duck_vel
        TRex.y += TRex.y_vel


def trex_variable_reset():
    if TRex.y >= Ground.platform_y - TRex.height:
        # Resetting position of TRex if it has overshot the boundaries
        TRex.y = Ground.platform_y - TRex.height
        # Resetting jumping and ducking variables
        TRex.is_jump = False
        TRex.jump_vel = 18
        TRex.duck_midair = False


# Drawing pterodactyl object function
def draw_pterodactyl(interval, object, pterodactyl):
    # Alternate between Pterodactyl flap animations to generate flapping effect
    if loop_count % 5 == 0:
        pterodactyl.flap_direction = "Down"
    if loop_count % 10 == 0:
        pterodactyl.flap_direction = "Up"

    # Day time
    if interval == "Day":
        if pterodactyl.flap_direction == "Down":
            screen.blit(pterodactyl.down_flap_animations[0], (object.x, object.y))
        else:
            screen.blit(pterodactyl.up_flap_animations[0], (object.x, object.y))
    # Night time
    else:
        if pterodactyl.flap_direction == "Down":
            screen.blit(pterodactyl.down_flap_animations[1], (object.x, object.y))
        else:
            screen.blit(pterodactyl.up_flap_animations[1], (object.x, object.y))


# Drawing cactus object function
def draw_cactus(interval, object, cactus):
    # Determining which type of cactus is chosen
    if cactus.size == 1:
        # Blitting the cactus
        if interval == "Day":
            screen.blit(cactus.day_animations[0], (object.x, object.y))
        else:
            screen.blit(cactus.night_animations[0], (object.x, object.y))
    # Same for below for entire if current_object == "Cactus" block
    elif cactus.size == 2:
        if interval == "Day":
            screen.blit(cactus.day_animations[1], (object.x, object.y))
        else:
            screen.blit(cactus.night_animations[1], (object.x, object.y))
    elif cactus.size == 3:
        if interval == "Day":
            screen.blit(cactus.day_animations[2], (object.x, object.y))
        else:
            screen.blit(cactus.night_animations[2], (object.x, object.y))
    elif cactus.size == 4:
        if interval == "Day":
            screen.blit(cactus.day_animations[3], (object.x, object.y))
        else:
            screen.blit(cactus.night_animations[3], (object.x, object.y))
    elif cactus.size == 5:
        if interval == "Day":
            screen.blit(cactus.day_animations[4], (object.x, object.y))
        else:
            screen.blit(cactus.night_animations[4], (object.x, object.y))
    else:
        if interval == "Day":
            screen.blit(cactus.day_animations[5], (object.x, object.y))
        else:
            screen.blit(cactus.night_animations[5], (object.x, object.y))


def draw_sprite(interval):
    # Filling sprite frame according to time
    # Dead
    if TRex.is_dead:
        if TRex.is_duck:
            if interval == "Day":
                screen.blit(TRex.dead_animations[0], (TRex.x - (TRex.stand_width - TRex.duck_width), TRex.y - (TRex.stand_height - TRex.duck_height)))
            else:
                screen.blit(TRex.dead_animations[1], (TRex.x - (TRex.stand_width - TRex.duck_width), TRex.y - (TRex.stand_height - TRex.duck_height)))
        else:
            if interval == "Day":
                screen.blit(TRex.dead_animations[0], (TRex.x, TRex.y))
            else:
                screen.blit(TRex.dead_animations[1], (TRex.x, TRex.y))
    # Jump or if in start screen
    elif TRex.is_jump or start:
        if interval == "Day":
            screen.blit(TRex.jumping_animations[0], (TRex.x, TRex.y))
        else:
            screen.blit(TRex.jumping_animations[1], (TRex.x, TRex.y))
    else:
        # Alternating moving scenes for crouching and running
        if loop_count % 3 == 0:
            TRex.leg_lifted = "Right"
        if loop_count % 6 == 0:
            TRex.leg_lifted = "Left"
        # Crouching
        if TRex.is_duck:
            if TRex.leg_lifted == "Right":
                if interval == "Day":
                    screen.blit(TRex.right_duck_animations[0], (TRex.x, TRex.y))
                else:
                    screen.blit(TRex.right_duck_animations[1], (TRex.x, TRex.y))
            else:
                if interval == "Day":
                    screen.blit(TRex.left_duck_animations[0], (TRex.x, TRex.y))
                else:
                    screen.blit(TRex.left_duck_animations[1], (TRex.x, TRex.y))
        # Running
        else:
            if TRex.leg_lifted == "Right":
                if interval == "Day":
                    screen.blit(TRex.right_standing_animations[0], (TRex.x, TRex.y))
                else:
                    screen.blit(TRex.right_standing_animations[1], (TRex.x, TRex.y))
            else:
                if interval == "Day":
                    screen.blit(TRex.left_standing_animations[0], (TRex.x, TRex.y))
                else:
                    screen.blit(TRex.left_standing_animations[1], (TRex.x, TRex.y))


# Display new screen frame function
def display_screen(interval):
    # Filling background frame according to time
    # Day time
    if interval == "Day":
        # Filling background frame according to time
        screen.blit(Sky.day_animations, (Sky.x, Sky.y))
        screen.blit(Ground.day_animations, (Ground.x, Ground.y))

        # Displaying scores according to time
        # Score
        score_text = Score_font.render(scoreboard(score), 1, (83, 83, 83))
        # High score
        high_score_text = High_score_font.render("HI " + scoreboard(high_score), 1, (83, 83, 83))

        # Displaying control menu according to time
        control_menu_text_1 = Control_Menu_font.render("UP = Jump", 1, (83, 83, 83))
        control_menu_text_2 = Control_Menu_font.render("DOWN = Duck", 1, (83, 83, 83))
        control_menu_text_3 = Control_Menu_font.render("SPACEBAR = Pause/Unpause", 1, (83, 83, 83))

    # Night time
    else:
        # Background
        screen.blit(Sky.night_animations, (Sky.x, Sky.y))
        screen.blit(Ground.night_animations, (Ground.x, Ground.y))
        screen.blit(Moon.animations, (Moon.x, Moon.y))

        # Displaying score according to time
        # Score
        score_text = Score_font.render(scoreboard(score), 1, (255, 255, 255))
        # High score
        high_score_text = High_score_font.render("HI " + scoreboard(high_score), 1, (255, 255, 255))

        # Displaying control menu according to time
        control_menu_text_1 = Control_Menu_font.render("UP = Jump", 1, (255, 255, 255))
        control_menu_text_2 = Control_Menu_font.render("DOWN = Duck", 1, (255, 255, 255))
        control_menu_text_3 = Control_Menu_font.render("SPACEBAR = Pause/Unpause", 1, (255, 255, 255))

    # Score
    screen.blit(score_text, (1200, 150))
    # High score
    screen.blit(high_score_text, (1075, 150))

    # Control menu
    screen.blit(control_menu_text_1, (30, 30))
    screen.blit(control_menu_text_2, (30, 60))
    screen.blit(control_menu_text_3, (30, 90))

    # Cover1
    pygame.draw.rect(screen, (255, 255, 255), (Cover1.x, Cover1.y, Cover1.width, Cover1.height))
    # Cover2
    pygame.draw.rect(screen, (255, 255, 255), (Cover2.x, Cover2.y, Cover2.width, Cover2.height))

    # Filling object frame according to time, and object type
    # Object 1
    if Object_1.is_draw == "Cactus":
        draw_cactus(time, Object_1, Cactus_1)
    elif Object_1.is_draw == "Pterodactyl":
        draw_pterodactyl(time, Object_1, Pterodactyl_1)
    # Object 2
    if Object_2.is_draw == "Cactus":
        draw_cactus(time, Object_2, Cactus_2)
    elif Object_2.is_draw == "Pterodactyl":
        draw_pterodactyl(time, Object_2, Pterodactyl_2)
    # Object 3
    if Object_3.is_draw == "Cactus":
        draw_cactus(time, Object_3, Cactus_3)
    elif Object_3.is_draw == "Pterodactyl":
        draw_pterodactyl(time, Object_3, Pterodactyl_3)
    # Object 4
    if Object_4.is_draw == "Cactus":
        draw_cactus(time, Object_4, Cactus_4)
    elif Object_4.is_draw == "Pterodactyl":
        draw_pterodactyl(time, Object_4, Pterodactyl_4)

    # Draw Sprite
    draw_sprite(time)


# Text preferences
Start_Screen1_font = pygame.font.SysFont('Arial', 40, True)
Start_Screen2_font = pygame.font.SysFont('Arial', 20, True)
Control_Menu_font = pygame.font.SysFont('Arial', 20, True)
Pause_font = pygame.font.SysFont('Arial', 20, True)
Score_font = pygame.font.SysFont('Arial', 20, True)
High_score_font = pygame.font.SysFont('Arial', 20, True)
GameOver_font = pygame.font.SysFont('Arial', 20, True)

# Set high score initial high score(0)
high_score = 0

# Reset loop to play game again when a game is over
reset = True
while reset:
    # Class definitions

    # Background
    # Cover1
    Cover1 = Sheet(275, 1008)
    # Cover2
    Cover2 = Sheet(0, 200)
    # Ground
    Ground = Base(0, 8.5)
    # Air
    Sky = Air(0, 8.5)
    # Moon
    Moon = Planet(1283, 0.93)

    # Objects
    # Obstacles
    Object_1 = Obstacle(1284, 396, 8.5, "Cactus")
    Object_2 = Obstacle(1605, 429, 8.5, "Blank")
    Object_3 = Obstacle(1926, 396, 8.5, "Cactus")
    Object_4 = Obstacle(2247, 429, 8.5, "Blank")
    # Cactus character for each obstacle
    Cactus_1 = Spike(15, 33, 1)
    Cactus_2 = Spike(32, 33, 2)
    Cactus_3 = Spike(49, 33, 3)
    Cactus_4 = Spike(23, 46, 4)
    # Pterodactyl character for each obstacle
    Pterodactyl_1 = Pterosaur("Down", 1)
    Pterodactyl_2 = Pterosaur("Down", 2)
    Pterodactyl_3 = Pterosaur("Down", 3)
    Pterodactyl_4 = Pterosaur("Down", 1)

    # Sprite
    # TRex
    TRex = Dinosaur(385, 18, False, False, False, "Right")

    # Variables to define before game loop
    GameOver = False
    GameWon = False
    time = "Day"
    background_vel = 8.5
    score = 0
    loop_count = 0
    start = False
    initial_jumped = False

    # Main game loop
    while not GameOver:
        # Setting frame per second rate
        pygame.time.delay(7)

        # Filtering deprecation warning due to limited movements of sprites and objects if not ignored
        warnings.filterwarnings("ignore", category=DeprecationWarning)

        # Starting screen
        if loop_count == 0:
            start = True
            while start:
                # Start screen function
                start_variables = start_screen(initial_jumped, start)
                # Update start and initial_jumped variables
                start = start_variables[1]
                initial_jumped = start_variables[0]

                # Quit if pressed
                if "QUIT" in event_checker():
                    start = False
                    GameOver = True
                    reset = False

        # Increase score by 1 every 2 loops
        if loop_count % 2 == 0:
            score += 1
            # For every 100 points play sound
            if score % 100 == 0 and score != 0:
                point_sound = pygame.mixer.Sound('Sounds/Dinosaur_100_point_Sound.wav')
                point_sound.play()

        # Update loop_count
        loop_count += 1

        # Updating High score
        if score > high_score:
            high_score = score

        # Updating time variable
        if score % 700 == 0 and score != 0:
            time = "Night"
        if score % 1400 == 0:
            time = "Day"

        # Choosing object and updating it
        # Choose and update
        # Object.is_draw updated
        # If Cactus, Cactus.type updated
        # If Pterodactyl, Pterodactyl.position updated
        choose_and_update(score, Object_4, Object_1, Cactus_1, Pterodactyl_1)
        choose_and_update(score, Object_1, Object_2, Cactus_2, Pterodactyl_2)
        choose_and_update(score, Object_2, Object_3, Cactus_3, Pterodactyl_3)
        choose_and_update(score, Object_3, Object_4, Cactus_4, Pterodactyl_4)

        # Update proportions of cactus if object is cactus
        change_cactus_proportions(Cactus_1)
        change_cactus_proportions(Cactus_2)
        change_cactus_proportions(Cactus_3)
        change_cactus_proportions(Cactus_4)

        # Update y-coordinate of object (influenced by different object heights)
        set_object_y(Object_1, Cactus_1, Pterodactyl_1)
        set_object_y(Object_2, Cactus_2, Pterodactyl_2)
        set_object_y(Object_3, Cactus_3, Pterodactyl_3)
        set_object_y(Object_4, Cactus_4, Pterodactyl_4)

        # Setting new velocity for background and objects
        # Background
        Sky.x_vel = background_vel
        Ground.x_vel = background_vel
        # Objects
        Object_1.x_vel = background_vel
        Object_2.x_vel = background_vel
        Object_3.x_vel = background_vel
        Object_4.x_vel = background_vel

        # accelerate background movement to make game harder as each 500 points passes, until it reaches maximum velocity (34)
        if background_vel <= 34 and score % 700 == 0:
            # if background_vel is at 30, decrease acceleration by 10 times for better game play
            if background_vel <= 17:
                background_vel += 2.5
            elif background_vel <= 34:
                background_vel += 0.625
            else:
                background_vel = 34

        # Reset positions if positions are off screen
        # Background
        if Sky.x <= -Sky.width / 2 and Ground.x <= -Ground.width / 2:
            Sky.x = 0
            Ground.x = 0
        # Moon Position
        if time == "Day":
            Moon.x = 1283
        # Objects
        obstacle_position_reset()

        # Maintaining constant background and object movement (Moon velocity is constant)
        # Background
        Sky.x -= Sky.x_vel
        Ground.x -= Ground.x_vel
        if time == "Night":
            Moon.x -= Moon.x_vel
        # Objects
        Object_1.x -= Object_1.x_vel
        Object_2.x -= Object_2.x_vel
        Object_3.x -= Object_3.x_vel
        Object_4.x -= Object_3.x_vel

        # Setting sprite movement
        # Detect and call jump function
        if "UP" in event_checker() and not TRex.is_jump:
            TRex.is_jump = True
            # Play jump sound
            TRex.jump_sound.play()

        # Jump function
        trex_jump()

        # Detect and call duck function
        if "DOWN" in event_checker():
            TRex.is_duck = True
        else:
            TRex.is_duck = False
        trex_duck()

        # Setting proportions of sprite in actions
        if TRex.is_duck:
            # Set duck width
            TRex.width = TRex.duck_width
            TRex.height = TRex.duck_height
        else:
            # Set width when not ducking
            TRex.width = TRex.stand_width
            TRex.height = TRex.stand_height

        # Reset variables when sprite reaches ground again
        trex_variable_reset()

        # Check collisions
        if collision_checker(Object_1, Cactus_1, Pterodactyl_1) or collision_checker(Object_2, Cactus_2, Pterodactyl_2) or collision_checker(Object_3, Cactus_3, Pterodactyl_3) or collision_checker(Object_4, Cactus_4, Pterodactyl_4):
            TRex.is_dead = True
            # Play death sound
            TRex.death_sound.play()

        # Check whether score has reached maximum
        if score >= 99999:
            TRex.is_won = True

        # Generating new screen frame
        display_screen(time)

        # Updating game screen with new frame
        pygame.display.update()

        # Exit game if 'x' button is clicked
        if "QUIT" in event_checker():
            GameOver = True
            reset = False

        # Pause
        # quit if x is pressed while paused, else unpause
        if pause(time) == "QUIT":
            GameOver = True
            reset = False

        # Exit game if Sprite has died or score has reached maximum
        if TRex.is_dead or TRex.is_won:
            # Display game over screen
            game_over_screen(time)

            # Replay game
            ask_reset = False
            while not ask_reset:
                # Quit
                if "QUIT" in event_checker():
                    ask_reset = True
                    GameOver = True
                    reset = False
                # Reset pressed
                if "RESET" in event_checker():
                    ask_reset = True
                    GameOver = True

# End Program
pygame.quit()
