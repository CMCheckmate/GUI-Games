"""This program creates an endless 2D shooter game.

The player is able to control their character with direction keys w, a, s and d
and can shoot projectiles when screen clicked in the direction of the cursor.
Different types of enemies will spawn in increasing numbers per wave and attack
the player through collision or projectiles, which will decrease the player's
health. Each projectile shot by the player will damage the enemies and kill
them when their health drops to 0. The game will end when the player dies and
the highest wave reached will be recorded.
"""

# Imports
import tkinter as tk
from tkinter import messagebox
import os
import winsound
import random
import math


# Classes
class GUI:
    """Game's GUI system."""

    # Constants
    WINDOW = tk.Tk()
    WIDTH = WINDOW.winfo_screenwidth()
    HEIGHT = WINDOW.winfo_screenheight()
    _GAME_AUDIO = "Assets/Audio/Game.wav"
    _ICON_IMAGE = tk.PhotoImage(file="Assets/Images/Ataxia.png")
    _MENU_IMAGE = tk.PhotoImage(file="Assets/Images/Background.png")
    COLOURS = {"White": "#FFFFFF", "Red": "#E60B0B", "Green": "#48D44D",
               "Light Gray": "#949494", "Dark Gray": "#212121",
               "Black": "#000000"}
    _TEXT_INFO = {  # Text dictionary for text based page objects
        "Title": {"Text": "Ataxia", "Font": ("OCR A Extended", 150, "bold"),
                  "Fill": COLOURS["Dark Gray"], "Highlight": COLOURS["White"],
                  "Position": (WIDTH / 3, HEIGHT / 2.5)},
        "Help": {"Text": "Help", "Font": ("OCR A Extended", 50, "bold"),
                 "Fill": COLOURS["Dark Gray"], "Highlight": COLOURS["White"],
                 "Position": (WIDTH / 3, HEIGHT / 1.5)},
        "Instruction": {
            "Text": "Ataxia—The lack of muscle control or coordination of "
                    "voluntary movements.\n"
                    "\nHello user. Welcome to Ataxia. "
                    "\nDodge and shoot incoming enemies from endless waves. "
                    "\nThey will damage you upon collision. "
                    "\nYou will find different enemies with different stats."
                    "\nYou can damage these enemies by shooting at them. "
                    "\nHave fun and happy clicking!\n"
                    "\nMovement Keys: Up—W\n"
                    "                Left—A\n"
                    "                Down—S\n"
                    "                Right—D\n"
                    "\n         Shoot: MOUSE1 (Left Click)",
                    "Font": ("OCR A Extended", 20, "bold"),
                    "Fill": COLOURS["Dark Gray"],
                    "Position": (WIDTH / 2, HEIGHT / 2)},
        "Highscore": {"Text": "Highest Wave: ",
                      "Font": ("OCR A Extended", 20, "bold"),
                      "Fill": COLOURS["Dark Gray"],
                      "Position": (WIDTH * 2 / 3, 30)},
        "Wave": {"Text": "Current Wave: ",
                 "Font": ("OCR A Extended", 20, "bold"),
                 "Fill": COLOURS["Dark Gray"],
                 "Position": (WIDTH * 2 / 3, 60)},
        "Counter": {"Text": "Enemies left: ",
                    "Font": ("OCR A Extended", 20, "bold"),
                    "Fill": COLOURS["Dark Gray"],
                    "Position": (WIDTH * 2 / 3, 90)},
        "Health": {"Text": "Health: ",
                   "Font": ("OCR A Extended", 20, "bold"),
                   "Fill": COLOURS["Dark Gray"],
                   "Position": (150, 20)},
        "Timer": {"Text": "Wave starting in: ", "Font": ("OCR A Extended", 30),
                  "Fill": COLOURS["Dark Gray"],
                  "Position": (WIDTH / 2, HEIGHT / 2)},
        "Restart": {"Text": "Restart", "Font": ("OCR A Extended", 50, "bold"),
                    "Fill": COLOURS["Dark Gray"],
                    "Highlight": COLOURS["White"],
                    "Position": (WIDTH / 2, HEIGHT / 2)},
        "Game Over": {"Text": "Game Over",
                      "Font": ("OCR A Extended", 50, "bold"),
                      "Fill": COLOURS["Dark Gray"],
                      "Position": (WIDTH / 2, HEIGHT / 3)},
        "Pause": {"Text": "Paused", "Font": ("OCR A Extended", 50, "bold"),
                  "Fill": COLOURS["Dark Gray"],
                  "Position": (WIDTH / 2, HEIGHT / 3)}}
    _ICON_INFO = {  # Icon image dictionary for image/icon based page objects
        "Audio": {"Image": [tk.PhotoImage(file="Assets/Images/Unmuted.png"),
                            tk.PhotoImage(file="Assets/Images/Muted.png")],
                  "Position": (WIDTH - 145, 55)},
        "Home": {"Image": tk.PhotoImage(file="Assets/Images/Home.png"),
                 "Position": (WIDTH - 55, 55)},
        "Pause": {"Image": [tk.PhotoImage(file="Assets/Images/Pause.png"),
                            tk.PhotoImage(file="Assets/Images/Play.png")],
                  "Position": (WIDTH - 55, 145)}}
    _HEALTH_BAR_INFO = {
        "Fill": {"Container": COLOURS["Red"], "Current": COLOURS["Green"]},
        "Outline": COLOURS["Dark Gray"], "Border": 3,
        "Dimension": (20, 40, WIDTH / 2, 60)}
    _WAVE_DELAY = 5  # Seconds before next wave begins
    _INITIAL_SPAWN_AMOUNT = 5  # Enemy first wave spawn amount
    _SPAWN_INCREASE = 1  # Enemy increase per wave
    _UNIQUE_WAVE_INTERVAL = 10  # Unique enemy wave cycle interval
    _SPAWN_INTERVAL = round(1000 * 1)  # Enemy spawn interval
    FRAME_INTERVAL = round(1000 / 60)

    def __init__(self):
        """Create GUI variables/attributes, pages and start game."""
        # Attributes
        self._game_over = tk.BooleanVar()
        self._wave_over = tk.BooleanVar()
        self._paused = tk.BooleanVar()
        self._audio = tk.BooleanVar()
        self._high_score = tk.IntVar()
        self._wave_number = tk.IntVar()
        self._enemies_left = tk.IntVar()
        self._required_enemies = tk.IntVar()  # Enemies to generate in wave
        self._delay_timer = tk.IntVar()  # Seconds remaining in delay timer
        self._player_health = tk.DoubleVar()
        self._pages = {"Menu": self._start_page(),
                       "Instructions": self._instruction_page(),
                       "Game": self._game_page()}
        self._player = Player(self._pages["Game"], *Player.SPAWN_POS)
        self._enemies = []
        self._projectiles = []
        self._current_page = None

        # Player shooting bind
        self.WINDOW.bind("<Button-1>",
                         lambda event: self._player_shoot(event.x, event.y))

        # Start GUI
        self._initiate()

    @staticmethod
    def get_trace_vel(object_x, object_y, trace_x, trace_y, speed):
        """Calculate velocities of tracing object.

        param object_x: Horizontal coordinates of object to move
        param object_y: Vertical coordinates of object to move
        param trace_x: Horizontal coordinates of object to trace
        param trace_y: Vertical coordinates of object to trace
        param speed: Maximum speed of object
        Returns: x_velocity, y_velocity (type=tuple)
        """
        # Calculate angle of elevation/decent of object to given position
        horizontal_distance = object_x - trace_x
        vertical_distance = object_y - trace_y
        if horizontal_distance == 0:
            angle = math.pi / 2
        else:
            angle = math.atan(abs(vertical_distance / horizontal_distance))

        # Calculate resultant velocity components with trigonometry
        if horizontal_distance < 0:
            x_velocity = speed * math.cos(angle)
        else:
            x_velocity = -speed * math.cos(angle)
        if vertical_distance < 0:
            y_velocity = speed * math.sin(angle)
        else:
            y_velocity = -speed * math.sin(angle)

        return x_velocity, y_velocity

    def _start_page(self):
        """Create and configure main page frame and objects.

        Returns: start_page (type=tk.Canvas)
        """
        # Container
        start_page = tk.Canvas(
            self.WINDOW, width=self.WIDTH, height=self.HEIGHT,
            bg=self.COLOURS["Light Gray"], highlightthickness=0)
        # Background
        start_page.create_image(self.WIDTH / 2, self.HEIGHT / 2,
                                image=self._MENU_IMAGE)

        # Objects
        # Play button
        play_button = start_page.create_text(
            self._TEXT_INFO["Title"]["Position"],
            text=self._TEXT_INFO["Title"]["Text"],
            font=self._TEXT_INFO["Title"]["Font"],
            fill=self._TEXT_INFO["Title"]["Fill"])
        # Hover/Click styling
        start_page.tag_bind(
            play_button, "<Enter>", lambda *_: start_page.itemconfigure(
                play_button, fill=self._TEXT_INFO["Title"]["Highlight"]))
        start_page.tag_bind(
            play_button, "<Leave>", lambda *_: start_page.itemconfigure(
                play_button, fill=self._TEXT_INFO["Title"]["Fill"]))
        # Setup game
        start_page.tag_bind(play_button, "<ButtonRelease-1>",
                            lambda *_: self._setup_game())

        # Help button
        help_button = start_page.create_text(
            self._TEXT_INFO["Help"]["Position"],
            text=self._TEXT_INFO["Help"]["Text"],
            font=self._TEXT_INFO["Help"]["Font"],
            fill=self._TEXT_INFO["Help"]["Fill"])
        # Hover/Click styling
        start_page.tag_bind(
            help_button, "<Enter>", lambda *_: start_page.itemconfigure(
                help_button, fill=self._TEXT_INFO["Help"]["Highlight"]))
        start_page.tag_bind(
            help_button, "<Leave>", lambda *_: start_page.itemconfigure(
                help_button, fill=self._TEXT_INFO["Help"]["Fill"]))
        # Set link to instruction page
        start_page.tag_bind(help_button, "<ButtonRelease-1>",
                            lambda *_: self._set_page("Instructions"))

        return start_page

    def _instruction_page(self):
        """Create and configure instruction page frame and objects.

        Returns: instruction_page (type=tk.Canvas)
        """
        # Container
        instruction_page = tk.Canvas(
            self.WINDOW, width=self.WIDTH, height=self.HEIGHT,
            bg=self.COLOURS["Light Gray"], highlightthickness=0)
        # Background
        instruction_page.create_image(self.WIDTH / 2, self.HEIGHT / 2,
                                      image=self._MENU_IMAGE)

        # Objects
        # Instruction text
        instruction_page.create_text(
            *self._TEXT_INFO["Instruction"]["Position"],
            text=self._TEXT_INFO["Instruction"]["Text"],
            font=self._TEXT_INFO["Instruction"]["Font"],
            fill=self._TEXT_INFO["Instruction"]["Fill"])

        # Home button
        home_button = instruction_page.create_image(
            *self._ICON_INFO["Home"]["Position"],
            image=self._ICON_INFO["Home"]["Image"])
        # Set link to menu page
        instruction_page.tag_bind(home_button, "<ButtonRelease-1>",
                                  lambda *_: self._set_page("Menu"))

        return instruction_page

    def _game_page(self):
        """Create and configure game page frame and objects.

        Returns: game_page (type=tk.Canvas)
        """
        # Container
        game_page = tk.Canvas(
            self.WINDOW, width=self.WIDTH, height=self.HEIGHT,
            bg=self.COLOURS["Light Gray"], highlightthickness=0)

        # Objects
        # High score text
        high_score_text = game_page.create_text(
            *self._TEXT_INFO["Highscore"]["Position"],
            text=self._TEXT_INFO["Highscore"]["Text"],
            font=self._TEXT_INFO["Highscore"]["Font"],
            fill=self._TEXT_INFO["Highscore"]["Fill"])
        # Update the highest wave label
        self._high_score.trace("w", lambda *_: game_page.itemconfigure(
            high_score_text, text=f"Highest wave: {self._high_score.get()}"))

        # Wave number text
        wave_text = game_page.create_text(
            *self._TEXT_INFO["Wave"]["Position"],
            text=self._TEXT_INFO["Wave"]["Text"],
            font=self._TEXT_INFO["Wave"]["Font"],
            fill=self._TEXT_INFO["Wave"]["Fill"])
        # Update current wave label
        self._wave_number.trace("w", lambda *_: game_page.itemconfigure(
            wave_text, text=f"Current wave: {self._wave_number.get()}"))

        # Enemy counter text
        enemy_counter_text = game_page.create_text(
            *self._TEXT_INFO["Counter"]["Position"],
            text=self._TEXT_INFO["Counter"]["Text"],
            font=self._TEXT_INFO["Counter"]["Font"],
            fill=self._TEXT_INFO["Counter"]["Fill"])
        # Update enemies left label
        self._enemies_left.trace("w", lambda *_: game_page.itemconfigure(
            enemy_counter_text,
            text=f"Enemies left: {self._enemies_left.get()}"))

        # Player health text
        health_text = game_page.create_text(
            *self._TEXT_INFO["Health"]["Position"],
            text=self._TEXT_INFO["Health"]["Text"],
            font=self._TEXT_INFO["Health"]["Font"],
            fill=self._TEXT_INFO["Health"]["Fill"])
        # Update health amount
        self._player_health.trace("w", lambda *_: game_page.itemconfigure(
            health_text,
            text=f"Health: {math.ceil(self._player_health.get())}/"
                 f"{Player.SPAWN_HEALTH}"))

        # Player health bar
        health_container = game_page.create_rectangle(
            *self._HEALTH_BAR_INFO["Dimension"],
            width=self._HEALTH_BAR_INFO["Border"],
            outline=self._HEALTH_BAR_INFO["Outline"],
            fill=self._HEALTH_BAR_INFO["Fill"]["Container"])
        health_bar = game_page.create_rectangle(
            *self._HEALTH_BAR_INFO["Dimension"],
            width=self._HEALTH_BAR_INFO["Border"],
            outline=self._HEALTH_BAR_INFO["Outline"],
            fill=self._HEALTH_BAR_INFO["Fill"]["Current"])
        # Update health bar
        self._player_health.trace("w", lambda *_: self._set_health_bar(
            health_container, health_bar, Player.SPAWN_HEALTH,
            self._player_health.get()))

        # Delay timer text
        delay_text = game_page.create_text(
            *self._TEXT_INFO["Timer"]["Position"],
            text=self._TEXT_INFO["Timer"]["Text"],
            font=self._TEXT_INFO["Timer"]["Font"],
            fill=self._TEXT_INFO["Timer"]["Fill"])
        # Update and hide timer until wave over
        self._delay_timer.trace("w", lambda *_: game_page.itemconfigure(
            delay_text, text=f"Wave starts in {self._delay_timer.get()}"))
        self._wave_over.trace("w", lambda *_: game_page.itemconfigure(
            delay_text, state="normal") if self._wave_over.get()
            else game_page.itemconfigure(delay_text, state="hidden"))

        # Paused text
        paused_text = game_page.create_text(
            *self._TEXT_INFO["Pause"]["Position"],
            text=self._TEXT_INFO["Pause"]["Text"],
            font=self._TEXT_INFO["Pause"]["Font"],
            fill=self._TEXT_INFO["Pause"]["Fill"])
        # Hide text until game paused
        self._paused.trace("w", lambda *_: game_page.itemconfigure(
            paused_text, state="normal") if self._paused.get()
            else game_page.itemconfigure(paused_text, state="hidden"))

        # Game over text
        game_over_text = game_page.create_text(
            *self._TEXT_INFO["Game Over"]["Position"],
            text=self._TEXT_INFO["Game Over"]["Text"],
            font=self._TEXT_INFO["Game Over"]["Font"],
            fill=self._TEXT_INFO["Game Over"]["Fill"])
        # Hide text until game over
        self._game_over.trace("w", lambda *_: game_page.itemconfigure(
            game_over_text, state="normal") if self._game_over.get()
            else game_page.itemconfigure(game_over_text, state="hidden"))

        # Restart button
        restart_button = game_page.create_text(
            *self._TEXT_INFO["Restart"]["Position"],
            text=self._TEXT_INFO["Restart"]["Text"],
            font=self._TEXT_INFO["Restart"]["Font"],
            fill=self._TEXT_INFO["Restart"]["Fill"])
        # Hover/Click styling
        game_page.tag_bind(
            restart_button, "<Enter>", lambda *_: game_page.itemconfigure(
                restart_button, fill=self._TEXT_INFO["Restart"]["Highlight"]))
        game_page.tag_bind(
            restart_button, "<Leave>", lambda *_: game_page.itemconfigure(
                restart_button, fill=self._TEXT_INFO["Restart"]["Fill"]))
        # Reset game
        game_page.tag_bind(restart_button, "<ButtonRelease-1>",
                           lambda *_: self._setup_game())
        # Hide button until game over and all enemies in wave spawned
        self._game_over.trace("w", lambda *_: game_page.itemconfigure(
            restart_button, state="normal") if self._game_over.get()
            else game_page.itemconfigure(restart_button, state="hidden"))

        # Audio/music button
        audio_button = game_page.create_image(
            *self._ICON_INFO["Audio"]["Position"],
            image=self._ICON_INFO["Audio"]["Image"][0])
        game_page.tag_bind(audio_button, "<ButtonRelease-1>",
                           lambda *_: self._set_audio())
        # Alternate mute/unmuted images when pressed
        self._audio.trace("w", lambda *_: game_page.itemconfigure(
            audio_button, image=self._ICON_INFO["Audio"]["Image"][0])
            if self._audio.get() else game_page.itemconfigure(
            audio_button, image=self._ICON_INFO["Audio"]["Image"][1]))

        # Home button
        home_button = game_page.create_image(
            *self._ICON_INFO["Home"]["Position"],
            image=self._ICON_INFO["Home"]["Image"])
        # Exit with confirmation
        game_page.tag_bind(
            home_button, "<ButtonRelease-1>",
            lambda *_: self._exit_game() if messagebox.askokcancel(
                "Home", "Exit to menu? Current progress will not be saved.")
            else None)
        # Hide button during waves or until game over
        self._game_over.trace("w", lambda *_: game_page.itemconfigure(
            home_button, state="normal") if self._game_over.get()
            else game_page.itemconfigure(home_button, state="hidden"))
        self._wave_over.trace("w", lambda *_: game_page.itemconfigure(
            home_button, state="normal") if self._wave_over.get()
            else game_page.itemconfigure(home_button, state="hidden"))

        # Pause/play button
        pause_button = game_page.create_image(
            *self._ICON_INFO["Pause"]["Position"],
            image=self._ICON_INFO["Pause"]["Image"][0])
        game_page.tag_bind(pause_button, "<ButtonRelease-1>",
                           lambda *_: self._paused.set(not self._paused.get())
                           if self._wave_over.get() else None)
        # Alternate pause/play image when pressed
        self._paused.trace("w", lambda *_: game_page.itemconfigure(
            pause_button, image=self._ICON_INFO["Pause"]["Image"][1])
            if self._paused.get() else game_page.itemconfigure(
            pause_button, image=self._ICON_INFO["Pause"]["Image"][0]))
        # Hide button during waves
        self._wave_over.trace("w", lambda *_: game_page.itemconfigure(
            pause_button, state="normal") if self._wave_over.get()
            else game_page.itemconfigure(pause_button, state="hidden"))

        return game_page

    def _set_page(self, page):
        """Set current screen to given page frame.

        param page: Page to change to
        Returns: None
        """
        # Clear current page
        if self._current_page:
            self._pages[self._current_page].grid_forget()
        self._current_page = page

        # Set new page
        self._pages[page].grid_propagate(False)
        self._pages[page].grid()
        self._pages[page].focus()

    def _setup_game(self):
        """Setup/reset game.

        Returns: None
        """
        # Reset game state variables
        self._game_over.set(False)
        self._wave_over.set(False)
        self._paused.set(False)
        self._audio.set(False)
        self._wave_number.set(0)
        self._enemies_left.set(0)
        self._delay_timer.set(0)
        self._required_enemies.set(0)

        # Remove projectiles
        for projectile in self._projectiles:
            projectile.remove()
        self._projectiles = []

        # Remove enemies
        for enemy in self._enemies:
            enemy.health = 0
            enemy.remove()
        self._enemies = []

        # Reset player
        # Position
        self._player.x, self._player.y = Player.SPAWN_POS
        self._pages["Game"].moveto(
            self._player.image, self._player.x - Player.WIDTH / 2,
            self._player.y - Player.HEIGHT / 2)
        self._pages["Game"].moveto(
            self._player.health_container, self._player.x - Player.WIDTH / 2,
            self._player.y - Player.HEIGHT / 2 -
            Player.HEALTH_BAR_INFO["Padding"] -
            Player.HEALTH_BAR_INFO["Height"])
        self._pages["Game"].moveto(
            self._player.health_bar,
            *self._pages["Game"].coords(self._player.health_container)[:2])
        self._player.lower()
        # Heath
        self._player.health = Player.SPAWN_HEALTH
        self._set_health_bar(
            self._player.health_container, self._player.health_bar,
            Player.SPAWN_HEALTH, self._player.health)

        # Play audio
        self._set_audio()

        # Set current page to game canvas
        self._set_page("Game")

    def _exit_game(self):
        """Handle events after player exits game page.

        Returns: None
        """
        # Reset game
        self._setup_game()

        # Stop audio
        self._set_audio()

        # Reset page to menu
        self._set_page("Menu")

    def _set_audio(self):
        """Play/Stop game background soundtrack.

        Returns: None
        """
        # Check if under Windows environment
        if os.name == "nt":
            # Check for game and audio state
            if self._audio.get() or self._game_over.get():
                # Stop music
                winsound.PlaySound(None, winsound.SND_PURGE)
                self._audio.set(False)
            else:
                # Play music
                winsound.PlaySound(self._GAME_AUDIO,
                                   winsound.SND_ASYNC + winsound.SND_LOOP +
                                   winsound.SND_FILENAME)
                self._audio.set(True)

    def _set_delay_timer(self):
        """Update countdown timer for wave delay.

        Returns: None
        """
        if not self._game_over.get():
            # Setup timer
            time_left = self._delay_timer.get()
            if time_left == 0:
                self._delay_timer.set(self._WAVE_DELAY)

            # Reduce timer time
            elif not self._paused.get():
                self._delay_timer.set(time_left - 1)

            # Loop timer every 1 second (1000 milliseconds)
            if self._delay_timer.get() > 0:
                self.WINDOW.after(1000, self._set_delay_timer)

    def _set_health_bar(self, container, bar, max_health, health):
        """Update given health bar.

        param container: Health bar of initial health
        param bar: Current health bar
        param max_health: Initial amount of health
        param health: Amount of current health
        Returns: None
        """
        # Current health bar position
        # (Interpreter unable to comprehend list)
        bar_rect = self._pages["Game"].coords(container)

        # Calculate updated length of health bar based on current health
        bar_rect[2] = bar_rect[0] + \
            (bar_rect[2] - bar_rect[0]) * (health / max_health)

        # Set new health bar position
        self._pages["Game"].coords(bar, *bar_rect)

    def _generate_enemy(self, unique_type=None):
        """Generate increasingly difficult enemies based on waves.

        Unique enemy waves only spawn with one type of enemy. These enemies
        will only appear after the first unique wave of its type passes.

        param unique_type: Whether wave will consist of only a unique enemy
        Returns: None
        """
        # Check number of enemies left to spawn for current wave
        enemy_num = self._required_enemies.get()
        if not self._game_over.get() and enemy_num > 0:
            # Check for unique enemy waves
            if unique_type is None:
                # Randomise enemy type based on weighted chance
                enemy_spawn = {}
                enemy_types = Enemy.get_types()
                for _class in enemy_types:
                    # Include enemy type if introduced before
                    if self._wave_number.get() > _class.SPAWN_WAVE:
                        enemy_spawn[_class] = _class.CHANCE
                enemy_type = random.choices(
                    list(enemy_spawn.keys()),
                    weights=list(enemy_spawn.values()))[0]
            else:
                enemy_type = unique_type

            # Set game canvas boundaries and randomise spawning side
            # (Top, bottom, right or left)
            x_boundaries = (-enemy_type.WIDTH / 2,
                            self.WIDTH + enemy_type.WIDTH / 2)
            y_boundaries = (-enemy_type.HEIGHT / 2,
                            self.HEIGHT + enemy_type.HEIGHT / 2)
            anchor_boundaries = random.choice((x_boundaries, y_boundaries))
            anchor_side = random.choice(anchor_boundaries)

            # Randomise for position of enemy that does not block other enemies
            overlapped = True
            while overlapped:
                # Set enemy position
                if anchor_boundaries == x_boundaries:
                    enemy_x = anchor_side
                    enemy_y = random.randrange(self.HEIGHT)
                else:
                    enemy_y = anchor_side
                    enemy_x = random.randrange(self.WIDTH)

                # Check if position overlaps with existing enemies
                overlapped = False
                enemy_rect = [enemy_x - enemy_type.WIDTH / 2,
                              enemy_y - enemy_type.HEIGHT / 2,
                              enemy_x + enemy_type.WIDTH / 2,
                              enemy_y + enemy_type.WIDTH / 2]
                for image in self._pages["Game"].find_overlapping(*enemy_rect):
                    if "Enemy" in self._pages["Game"].gettags(image):
                        overlapped = True

                if not overlapped:
                    # Create enemy
                    new_enemy = enemy_type(self._pages["Game"], enemy_x,
                                           enemy_y)
                    self._enemies.append(new_enemy)

                    # Lower player image under enemy
                    self._player.lower()

            # Loop until all enemies in wave are spawned
            required_enemies = enemy_num - 1
            self._required_enemies.set(required_enemies)
            if required_enemies > 0:
                self.WINDOW.after(self._SPAWN_INTERVAL,
                                  self._generate_enemy, unique_type)

    def _enemy_collision(self, enemy, move_x=False, move_y=False):
        """Handle collision events for enemies with player or other enemies.

        param enemy: Current enemy to check collisions
        param move_x: Whether horizontally moved enemy is checked
        param move_y: Whether vertically moved enemy is checked
        Returns: state (type=string)
        """
        # Set enemy states
        blocked = False
        attacking = False
        if not move_x:
            enemy_x = enemy.x
        else:
            enemy_x = move_x
        if not move_y:
            enemy_y = enemy.y
        else:
            enemy_y = move_y

        # Get images that collide with enemy
        enemy_rect = [enemy_x - enemy.WIDTH / 2,
                      enemy_y - enemy.HEIGHT / 2,
                      enemy_x + enemy.WIDTH / 2,
                      enemy_y + enemy.HEIGHT / 2]
        overlapped_images = self._pages["Game"].find_overlapping(
            *enemy_rect)
        for image in overlapped_images:
            image_tags = self._pages["Game"].gettags(image)
            # Attack player when overlapped
            if "Player" in image_tags:
                attacking = True
            # Blocked by other enemies or player
            if ("Enemy" in image_tags and image != enemy.image) \
                    or enemy.attacking:
                blocked = True

        # Update enemy states
        enemy.attacking = attacking
        if move_x:
            enemy.x_blocked = blocked
        if move_y:
            enemy.y_blocked = blocked

    def _projectile_collision(self, projectile):
        """Check for projectile collision with enemies.

        param projectile: Projectile to check collision
        Returns: None
        """
        if not self._game_over.get():
            # Get images that collide with projectile
            overlapped_images = self._pages["Game"].find_overlapping(
                projectile.x - Projectile.WIDTH / 2,
                projectile.y - Projectile.WIDTH / 2,
                projectile.x + Projectile.WIDTH / 2,
                projectile.y + Projectile.HEIGHT / 2)

            # Enemy collision for player projectile
            if projectile.side == "Player":
                for enemy in self._enemies:
                    if enemy.image in overlapped_images:
                        # Damage enemy and remove projectile
                        enemy.health = max(0,
                                           enemy.health - projectile.damage)
                        projectile.active = False
            # Player collision for enemy projectile
            else:
                if self._player.image in overlapped_images:
                    # Damage player and remove projectile
                    self._player.health = max(
                        0, self._player.health - projectile.damage)
                    projectile.active = False

    def _player_shoot(self, destination_x, destination_y):
        """Create and add projectile to list when shooting.

        param destination_x: Horizontal position of projectile to move to
        param destination_y: Vertical position of projectile to move to
        Returns: None
        """
        # Check if game over or paused
        if not self._game_over.get() and not self._paused.get():
            # Calculate projectile velocity based on direction clicked
            projectile_x_velocity, projectile_y_velocity = self.get_trace_vel(
                self._player.x, self._player.y, destination_x, destination_y,
                Player.PROJECTILE_SPEED)

            # Create projectile
            self._projectiles.append(Projectile(
                self._pages["Game"], self._player.x, self._player.y,
                projectile_x_velocity, projectile_y_velocity,
                Player.DAMAGE, "Player"))

    def _loop(self):
        """Run game loop.

        Returns: None
        """
        # Game Page
        if self._current_page == "Game":
            if not self._paused.get():
                if not self._game_over.get():
                    # Waves
                    # Delay next wave once current wave completed
                    wave_number = self._wave_number.get()
                    if self._required_enemies.get() == 0 and \
                        self._enemies_left.get() == 0 \
                            and not self._wave_over.get() and wave_number != 0:
                        self._wave_over.set(True)
                        self._set_delay_timer()

                    # Check if wave over and delay timer finished
                    if (self._wave_over.get() and
                            self._delay_timer.get() == 0) or wave_number == 0:
                        self._wave_over.set(False)

                        # Update wave number and high score
                        next_wave_number = wave_number + 1
                        self._wave_number.set(next_wave_number)
                        if self._high_score.get() < next_wave_number:
                            self._high_score.set(next_wave_number)

                        # Generate enemies
                        # Check for unique enemy waves
                        unique_enemy = None
                        enemy_amount = 0
                        enemy_types = Enemy.get_types()
                        for _type in enemy_types:
                            if next_wave_number % \
                                self._UNIQUE_WAVE_INTERVAL == \
                                    _type.SPAWN_WAVE:
                                unique_enemy = _type
                                enemy_amount = _type.SPAWN_INCREASE * \
                                    (next_wave_number //
                                     self._UNIQUE_WAVE_INTERVAL + 1)
                        # Calculate amount of enemies to spawn
                        if unique_enemy is None:
                            enemy_amount = self._INITIAL_SPAWN_AMOUNT + \
                                self._SPAWN_INCREASE * wave_number

                        # Set and spawn enemies
                        self._required_enemies.set(enemy_amount)
                        self._enemies_left.set(enemy_amount)
                        self._generate_enemy(unique_type=unique_enemy)

                    # Enemies
                    for enemy in self._enemies:
                        # Check if enemy still alive
                        if enemy.health > 0:
                            # Damage player if attacking
                            if enemy.attacking:
                                self._player.health = max(
                                    0, self._player.health - enemy.damage)

                            # Set velocity components
                            enemy.set_trace_vel(
                                self._player.x, self._player.y,
                                self._player.x_velocity,
                                self._player.y_velocity)

                            # Check collisions
                            # (simulate movement to check if blocked)
                            # Horizontal
                            moved_x = enemy.x + enemy.x_velocity
                            self._enemy_collision(enemy, move_x=moved_x)
                            # Vertical
                            moved_y = enemy.y + enemy.y_velocity
                            self._enemy_collision(enemy, move_y=moved_y)

                            # Move images and update health bar
                            enemy.move()
                            self._set_health_bar(
                                enemy.health_container, enemy.health_bar,
                                enemy.max_health, enemy.health, )
                        else:
                            # Remove enemy
                            enemy.remove()
                            self._enemies.remove(enemy)

                            # Update enemy counter
                            enemies_left = self._enemies_left.get()
                            enemies_left -= 1

                            # Create children for splitter enemy
                            if enemy.__class__ in \
                                    [Splitter] + Splitter.__subclasses__():
                                enemy.split()
                                for child in enemy.children:
                                    self._enemies.append(child)
                                    enemies_left += 1
                            self._enemies_left.set(enemies_left)

                        # Projectiles
                        # Add new ranger projectiles to list
                        if enemy.__class__ in [Ranger] + \
                                Ranger.__subclasses__():
                            for projectile in enemy.projectiles:
                                if not projectile.active:
                                    enemy.projectiles.remove(projectile)
                                elif projectile not in self._projectiles:
                                    self._projectiles.append(projectile)
                    for projectile in self._projectiles:
                        if projectile.active:
                            projectile.move()

                            # Check for projectile collisions
                            self._projectile_collision(projectile)
                        else:
                            # Remove projectile
                            projectile.remove()
                            self._projectiles.remove(projectile)

                    # Player
                    # Move images and update health bar
                    self._player.move()
                    self._set_health_bar(
                        self._player.health_container, self._player.health_bar,
                        Player.SPAWN_HEALTH, self._player.health)

                    # End game upon player death
                    self._player_health.set(self._player.health)
                    if self._player.health <= 0:
                        self._game_over.set(True)

                        # Stop audio after game ends
                        self._set_audio()

                # Remove any key input once game over or out of focus
                if (self._game_over.get() or
                    self._pages["Game"].focus_get() is None) and \
                        self._player.keys_pressed:
                    self._player.keys_pressed = []
                    self._player.x_velocity = 0
                    self._player.y_velocity = 0

        # Game loop
        self.WINDOW.after(self.FRAME_INTERVAL, self._loop)

    def _initiate(self):
        """Initiate GUI system.

        Returns: None
        """
        # Set window configurations
        self.WINDOW.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.WINDOW.title(self._TEXT_INFO["Title"]["Text"])
        self.WINDOW.iconphoto(False, self._ICON_IMAGE)
        self.WINDOW.resizable(False, False)
        self.WINDOW.state("zoomed")
        self.WINDOW.protocol(
            "WM_DELETE_WINDOW",
            lambda: self.WINDOW.destroy()
            if messagebox.askokcancel(
                "Quit", "Exit? Any current progress will not be saved.")
            else None)

        # Set starting page
        self._set_page("Menu")

        # Start game loops
        self._loop()
        self.WINDOW.mainloop()


class Player:
    """Main player class."""

    _IMAGE = tk.PhotoImage(file="Assets/Images/Player.png")
    WIDTH = _IMAGE.width()
    HEIGHT = _IMAGE.height()
    HEALTH_BAR_INFO = {"Width": WIDTH, "Height": 10, "Padding": 10,
                       "Fill": {"Container": GUI.COLOURS["Red"],
                                "Current": GUI.COLOURS["Green"]},
                       "Border": 3, "Outline": GUI.COLOURS["Dark Gray"]}
    SPAWN_POS = (GUI.WIDTH / 2, GUI.HEIGHT / 2)
    SPAWN_HEALTH = 100
    DAMAGE = 1
    PROJECTILE_SPEED = 30  # Speed in pixels per frame
    SPEED = 10
    _DIAGONAL_SPEED = SPEED / math.sqrt(2)  # Speed when moving diagonally
    _X_DIRECTION_KEYS = ("a", "d")
    _Y_DIRECTION_KEYS = ("w", "s")

    def __init__(self, canvas, x, y):
        """Create player variables, display images and bind to movement."""
        self._canvas = canvas
        self.x = x
        self.y = y
        self.x_velocity = 0
        self.y_velocity = 0
        self.health = self.SPAWN_HEALTH
        self.keys_pressed = []

        # Images
        self.image = self._canvas.create_image(
            self.x, self.y, image=self._IMAGE, tag="Player")
        self.health_container = self._canvas.create_rectangle(
            self.x - self.HEALTH_BAR_INFO["Width"] / 2,
            self.y - self.HEIGHT / 2 - self.HEALTH_BAR_INFO["Padding"] -
            self.HEALTH_BAR_INFO["Height"],
            self.x + self.HEALTH_BAR_INFO["Width"] / 2 -
            self.HEALTH_BAR_INFO["Border"],
            self.y - self.HEIGHT / 2 - self.HEALTH_BAR_INFO["Padding"],
            width=self.HEALTH_BAR_INFO["Border"],
            fill=self.HEALTH_BAR_INFO["Fill"]["Container"],
            outline=self.HEALTH_BAR_INFO["Outline"])
        self.health_bar = self._canvas.create_rectangle(
            *self._canvas.coords(self.health_container),
            width=self.HEALTH_BAR_INFO["Border"],
            fill=self.HEALTH_BAR_INFO["Fill"]["Current"],
            outline=self.HEALTH_BAR_INFO["Outline"])

        # Movement binds
        self._canvas.master.bind("<KeyPress>", lambda event, pressed=True:
                                 self._direction_event(event, pressed))
        self._canvas.master.bind("<KeyRelease>", lambda event, pressed=False:
                                 self._direction_event(event, pressed))

    def lower(self):
        """Lower order of player images.

        Returns: None
        """
        self._canvas.lower(self.image)
        self._canvas.lower(self.health_bar)
        self._canvas.lower(self.health_container)

    def _direction_event(self, event, pressed):
        """Handle direction key press movement of player.

        param event: Keyboard event list
        param pressed: Keyboard pressed or released
        Returns: None
        """
        # Check for direction keys pressed
        key_pressed = event.keysym
        if key_pressed in self._X_DIRECTION_KEYS + self._Y_DIRECTION_KEYS:
            x_stop = False
            y_stop = False

            # Add/remove key from current key press stack
            if pressed:
                if key_pressed not in self.keys_pressed:
                    self.keys_pressed.append(key_pressed)
            else:
                if key_pressed in self.keys_pressed:
                    self.keys_pressed.remove(key_pressed)
                if key_pressed in self._X_DIRECTION_KEYS:
                    x_stop = True
                else:
                    y_stop = True

            # Set velocities based on direction keys pressed (assume diagonal)
            x_velocity_set = False
            y_velocity_set = False
            for key in self.keys_pressed:
                # Horizontal
                if (not x_velocity_set or x_stop) and \
                        key in self._X_DIRECTION_KEYS:
                    x_stop = False
                    x_velocity_set = True
                    if key == self._X_DIRECTION_KEYS[0]:
                        self.x_velocity = -self._DIAGONAL_SPEED
                    elif key == self._X_DIRECTION_KEYS[1]:
                        self.x_velocity = self._DIAGONAL_SPEED

                # Vertical
                if (not y_velocity_set or y_stop) and \
                        key in self._Y_DIRECTION_KEYS:
                    y_stop = False
                    y_velocity_set = True
                    if key == self._Y_DIRECTION_KEYS[0]:
                        self.y_velocity = -self._DIAGONAL_SPEED
                    elif key == self._Y_DIRECTION_KEYS[1]:
                        self.y_velocity = self._DIAGONAL_SPEED

            # Reset movement upon direction key release
            if not pressed:
                if x_stop:
                    self.x_velocity = 0
                elif y_stop:
                    self.y_velocity = 0

            # Set speed to maximum for single direction movement
            if self.x_velocity != 0 and self.y_velocity == 0:
                self.x_velocity = math.copysign(self.SPEED, self.x_velocity)
            elif self.y_velocity != 0 and self.x_velocity == 0:
                self.y_velocity = math.copysign(self.SPEED, self.y_velocity)

    def move(self):
        """Move player based on current horizontal and vertical velocities.

        Returns: None
        """
        # Move within game canvas
        # Horizontal
        if self.x_velocity != 0:
            moved_x = self.x + self.x_velocity
            if moved_x < self.WIDTH / 2:
                moved_x = self.WIDTH / 2
            elif moved_x > GUI.WIDTH - self.WIDTH / 2:
                moved_x = GUI.WIDTH - self.WIDTH / 2
            if self.x == moved_x:
                self.x_velocity = 0
            else:
                self.x = moved_x

        # Vertical
        if self.y_velocity != 0:
            moved_y = self.y + self.y_velocity
            if moved_y < self.HEIGHT / 2:
                moved_y = self.HEIGHT / 2
            elif moved_y > GUI.HEIGHT - self.HEIGHT / 2:
                moved_y = GUI.HEIGHT - self.HEIGHT / 2
            if self.y == moved_y:
                self.y_velocity = 0
            else:
                self.y = moved_y

        # Check if player blocked or stopped moving
        if self.x_velocity != 0 or self.y_velocity != 0:
            # Move images
            self._canvas.moveto(self.image, self.x - self.WIDTH / 2,
                                self.y - self.HEIGHT / 2)
            self._canvas.moveto(
                self.health_container, self.x - self.WIDTH / 2,
                self.y - self.HEIGHT / 2 - self.HEALTH_BAR_INFO["Padding"] -
                self.HEALTH_BAR_INFO["Height"])
            self._canvas.moveto(
                self.health_bar,
                *self._canvas.coords(self.health_container)[:2])


class Enemy:
    """Default enemy class."""

    _IMAGES = {
        "Default": tk.PhotoImage(file="Assets/Images/Enemies/Default.png"),
        "Advanced": tk.PhotoImage(
            file="Assets/Images/Enemies/Default (Advanced).png")}
    WIDTH = _IMAGES["Default"].width()  # Images should have same dimensions
    HEIGHT = _IMAGES["Default"].height()
    _HEALTH_BAR_INFO = {"Width": WIDTH, "Height": 10, "Padding": 10,
                        "Fill": {"Container": GUI.COLOURS["Red"],
                                 "Current": GUI.COLOURS["Green"]},
                        "Border": 3, "Outline": GUI.COLOURS["Dark Gray"]}
    _TYPE_CHANCES = {"Default": 3, "Advanced": 1}
    _ADVANCED_MULTIPLIER = 1.2  # Multiplier to advanced enemy overall stats
    SPAWN_WAVE = 1  # Unique wave intervals to spawn (1, 11, 21, etc)
    SPAWN_INCREASE = 5  # Increase in amount per unique wave
    CHANCE = 1000  # Weight of chance to spawn
    _SPAWN_HEALTH = 5
    _DAMAGE = 10 / GUI.FRAME_INTERVAL  # Damage per frame
    _SPEED = 7  # Speed in pixels per frame

    def __init__(self, canvas, x, y):
        """Create enemy attributes and display enemy images."""
        self._canvas = canvas
        self.x = x
        self.y = y
        self.x_velocity = 0
        self.y_velocity = 0
        self.x_blocked = False
        self.y_blocked = False
        self.attacking = False

        # Stats
        self.advanced = random.choices(
            list(self._TYPE_CHANCES.keys()),
            weights=list(self._TYPE_CHANCES.values()))[0]
        self.max_health = self._SPAWN_HEALTH
        self.health = self._SPAWN_HEALTH
        self.damage = self._DAMAGE
        self._speed = self._SPEED
        if self.advanced == "Advanced":
            self.max_health *= self._ADVANCED_MULTIPLIER
            self.health *= self._ADVANCED_MULTIPLIER
            self.damage *= self._ADVANCED_MULTIPLIER
            self._speed *= self._ADVANCED_MULTIPLIER

        # Images
        self.image = self._canvas.create_image(
            self.x, self.y, image=self._IMAGES[self.advanced], tag="Enemy")
        self.health_container = self._canvas.create_rectangle(
                self.x - self._HEALTH_BAR_INFO["Width"] / 2,
                self.y - self.HEIGHT / 2 - self._HEALTH_BAR_INFO["Padding"] -
                self._HEALTH_BAR_INFO["Height"],
                self.x + self._HEALTH_BAR_INFO["Width"] / 2 -
                self._HEALTH_BAR_INFO["Border"],
                self.y - self.HEIGHT / 2 - self._HEALTH_BAR_INFO["Padding"],
                width=self._HEALTH_BAR_INFO["Border"],
                fill=self._HEALTH_BAR_INFO["Fill"]["Container"],
                outline=self._HEALTH_BAR_INFO["Outline"]
            )
        self.health_bar = self._canvas.create_rectangle(
                *self._canvas.coords(self.health_container),
                width=self._HEALTH_BAR_INFO["Border"],
                fill=self._HEALTH_BAR_INFO["Fill"]["Current"],
                outline=self._HEALTH_BAR_INFO["Outline"]
            )
        self._canvas.lower(self.image)
        self._canvas.lower(self.health_bar)
        self._canvas.lower(self.health_container)

    @staticmethod
    def get_types():
        """Get list of all enemy types including subclasses.

        Returns: enemy_types (type=list)
        """
        # Set enemy class types
        enemy_types = [Enemy]
        for enemy in Enemy.__subclasses__():
            enemy_types.append(enemy)
            # Include enemies with combined subclasses
            for sub_enemy in enemy.__subclasses__():
                if sub_enemy not in enemy_types:
                    enemy_types.append(sub_enemy)

        return enemy_types

    def remove(self):
        """Remove enemy after death.

        Returns: None
        """
        self._canvas.delete(self.image)
        self._canvas.delete(self.health_container)
        self._canvas.delete(self.health_bar)

    def set_trace_vel(self, player_x, player_y, player_x_vel, player_y_vel):
        """Find velocity components for enemy to trace player.

        Normal enemies use default tracing system in GUI class.
        Advanced enemies have a 'blocking' system that predicts the movement of
        the player and traces towards the predicted position.

        param player_x: Player's current vertical position
        param player_y: Player's current horizontal position
        param player_x_vel: Player's horizontal velocity
        param player_y_vel: Player's vertical velocity
        Returns: None
        """
        # Set player position
        predicted_x = player_x
        predicted_y = player_y

        # Check if advanced enemy is moving towards player
        if self.advanced == "Advanced" and \
                (player_x_vel * self.x_velocity > 0 or
                 player_y_vel * self.y_velocity > 0):
            # Advanced tracing
            # Calculate distance and time to reach player
            horizontal_distance = self.x - player_x
            vertical_distance = self.y - player_y
            distance = math.sqrt(
                horizontal_distance ** 2 + vertical_distance ** 2)
            time = distance / Player.SPEED

            # Calculate predicted player position within game canvas
            # Horizontal
            predicted_x = player_x + player_x_vel * time
            if predicted_x < Player.WIDTH / 2:
                predicted_x = Player.WIDTH / 2
            elif predicted_x > GUI.WIDTH - Player.WIDTH / 2:
                predicted_x = GUI.WIDTH - Player.WIDTH / 2
            # Vertical
            predicted_y = player_y + player_y_vel * time
            if predicted_y < Player.HEIGHT / 2:
                predicted_y = Player.HEIGHT / 2
            elif predicted_y > GUI.HEIGHT - Player.HEIGHT / 2:
                predicted_y = GUI.HEIGHT - Player.HEIGHT / 2

        # Calculate and set tracing velocities
        self.x_velocity, self.y_velocity = GUI.get_trace_vel(
            self.x, self.y, predicted_x, predicted_y, self._speed)

    def move(self):
        """Move enemy based on player position if not blocked.

        Returns: None
        """
        # Horizontal movement
        if not self.x_blocked:
            self.x += self.x_velocity

        # Vertical movement
        if not self.y_blocked:
            self.y += self.y_velocity

        # Move images
        if not self.x_blocked or not self.y_blocked:
            self._canvas.moveto(self.image, self.x - self.WIDTH / 2,
                                self.y - self.HEIGHT / 2)
            self._canvas.moveto(
                self.health_container, self.x - self.WIDTH / 2,
                self.y - self.HEIGHT / 2 - self._HEALTH_BAR_INFO["Padding"] -
                self._HEALTH_BAR_INFO["Height"])
            self._canvas.moveto(
                self.health_bar,
                *self._canvas.coords(self.health_container)[:2])


class Assassin(Enemy):
    """Fast moving smaller enemy with less health and damage."""

    _IMAGES = {
        "Default": tk.PhotoImage(file="Assets/Images/Enemies/Assassin.png"),
        "Advanced": tk.PhotoImage(
            file="Assets/Images/Enemies/Assassin (Advanced).png")}
    WIDTH = _IMAGES["Default"].width()
    HEIGHT = _IMAGES["Default"].height()
    _HEALTH_BAR_INFO = {"Width": WIDTH, "Height": 10, "Padding": 10,
                        "Fill": {"Container": GUI.COLOURS["Red"],
                                 "Current": GUI.COLOURS["Green"]},
                        "Border": 3, "Outline": GUI.COLOURS["Dark Gray"]}
    SPAWN_WAVE = 2
    SPAWN_INCREASE = 7
    CHANCE = 250
    _SPAWN_HEALTH = 3
    _DAMAGE = 5 / GUI.FRAME_INTERVAL
    _SPEED = 9

    def __init__(self, canvas, x, y):
        """Set enemy attributes based on parent class."""
        super().__init__(canvas, x, y)


class Tank(Enemy):
    """Larger and slower enemy with more health and damage."""

    _IMAGES = {
        "Default": tk.PhotoImage(file="Assets/Images/Enemies/Tank.png"),
        "Advanced": tk.PhotoImage(
            file="Assets/Images/Enemies/Tank (Advanced).png")}
    WIDTH = _IMAGES["Default"].width()
    HEIGHT = _IMAGES["Default"].height()
    _HEALTH_BAR_INFO = {"Width": WIDTH, "Height": 10, "Padding": 10,
                        "Fill": {"Container": GUI.COLOURS["Red"],
                                 "Current": GUI.COLOURS["Green"]},
                        "Border": 3, "Outline": GUI.COLOURS["Dark Gray"]}
    SPAWN_WAVE = 3
    SPAWN_INCREASE = 4
    CHANCE = 300
    _SPAWN_HEALTH = 10
    _DAMAGE = 20 / GUI.FRAME_INTERVAL
    _SPEED = 6

    def __init__(self, canvas, x, y):
        """Set enemy attributes based on parent class."""
        super().__init__(canvas, x, y)


class Ranger(Enemy):
    """Ranged enemy that shoots at player."""

    _IMAGES = {
        "Default": tk.PhotoImage(file="Assets/Images/Enemies/Ranger.png"),
        "Advanced": tk.PhotoImage(
            file="Assets/Images/Enemies/Ranger (Advanced).png")}
    WIDTH = _IMAGES["Default"].width()
    HEIGHT = _IMAGES["Default"].height()
    _HEALTH_BAR_INFO = {"Width": WIDTH, "Height": 10, "Padding": 10,
                        "Fill": {"Container": GUI.COLOURS["Red"],
                                 "Current": GUI.COLOURS["Green"]},
                        "Border": 3, "Outline": GUI.COLOURS["Dark Gray"]}
    SPAWN_WAVE = 5
    SPAWN_INCREASE = 3
    CHANCE = 150
    _SPAWN_HEALTH = 5
    _DAMAGE = 10 / GUI.FRAME_INTERVAL
    _SPEED = 5
    _PROJECTILE_DAMAGE = 5
    _PROJECTILE_SPEED = 20
    _PROJECTILE_NUM = 6  # Number of projectiles per shot
    _PROJECTILE_INTERVAL = 1 * 1000  # Shoot period in milliseconds

    def __init__(self, canvas, x, y):
        """Set enemy attributes based on parent class and shooting loop."""
        super().__init__(canvas, x, y)

        # Projectile stats
        self._projectile_damage = self._PROJECTILE_DAMAGE
        self._projectile_speed = self._PROJECTILE_SPEED
        if self.advanced:
            self._projectile_damage *= self._ADVANCED_MULTIPLIER
            self._projectile_speed *= self._ADVANCED_MULTIPLIER
        self.projectiles = []

        self._shoot()

    def _shoot(self):
        """Shoots projectiles evenly from centre of enemy image.

        Returns: None
        """
        if self.health > 0:
            for projectile_num in range(self._PROJECTILE_NUM):
                # Calculate angle and velocity components of bullet from centre
                angle = 2 * math.pi * projectile_num / self._PROJECTILE_NUM
                projectile_x_vel = self._projectile_speed * math.cos(angle)
                projectile_y_vel = self._projectile_speed * math.sin(angle)

                # Create projectile
                self.projectiles.append(Projectile(
                    self._canvas, self.x, self.y, projectile_x_vel,
                    projectile_y_vel, self._PROJECTILE_DAMAGE, "Enemy"))

            # Loop until enemy removed
            GUI.WINDOW.after(self._PROJECTILE_INTERVAL, self._shoot)


class Splitter(Enemy):
    """Enemy that splits into smaller enemies upon death."""

    _IMAGES = {
        "Default": tk.PhotoImage(file="Assets/Images/Enemies/Splitter.png"),
        "Advanced": tk.PhotoImage(
            file="Assets/Images/Enemies/Splitter (Advanced).png")}
    WIDTH = _IMAGES["Default"].width()
    HEIGHT = _IMAGES["Default"].height()
    _HEALTH_BAR_INFO = {"Width": WIDTH, "Height": 10, "Padding": 10,
                        "Fill": {"Container": GUI.COLOURS["Red"],
                                 "Current": GUI.COLOURS["Green"]},
                        "Border": 3, "Outline": GUI.COLOURS["Dark Gray"]}
    SPAWN_WAVE = 7
    SPAWN_INCREASE = 3
    CHANCE = 150
    _SPAWN_HEALTH = 8
    _DAMAGE = 15 / GUI.FRAME_INTERVAL
    _SPEED = 4
    _CHILD = Assassin

    def __init__(self, canvas, x, y):
        """Set enemy attributes based on parent class."""
        super().__init__(canvas, x, y)

        self.children = []

    def split(self):
        """Create two enemies from centre of enemy image.

        Returns: None
        """
        # Create child enemies
        children = [self._CHILD(self._canvas, self.x - self._CHILD.WIDTH / 2,
                                self.y),
                    self._CHILD(self._canvas, self.x + self._CHILD.WIDTH / 2,
                                self.y)]
        for child in children:
            self.children.append(child)


class Boss(Ranger, Splitter):
    """Boss enemy with combined abilities as above and overall high stats."""

    _IMAGES = {
        "Default": tk.PhotoImage(file="Assets/Images/Enemies/Boss.png"),
        "Advanced": tk.PhotoImage(
            file="Assets/Images/Enemies/Boss (Advanced).png")}
    WIDTH = _IMAGES["Default"].width()
    HEIGHT = _IMAGES["Default"].height()
    _HEALTH_BAR_INFO = {"Width": WIDTH, "Height": 10, "Padding": 10,
                        "Fill": {"Container": GUI.COLOURS["Red"],
                                 "Current": GUI.COLOURS["Green"]},
                        "Border": 3, "Outline": GUI.COLOURS["Dark Gray"]}
    SPAWN_WAVE = 9
    SPAWN_INCREASE = 1
    CHANCE = 5
    _SPAWN_HEALTH = 40
    _DAMAGE = 50 / GUI.FRAME_INTERVAL
    _SPEED = 3
    _CHILD = Enemy
    _PROJECTILE_DAMAGE = 10
    _PROJECTILE_SPEED = 15
    _PROJECTILE_NUM = 16
    _PROJECTILE_INTERVAL = 2 * 1000

    def __init__(self, canvas, x, y):
        """Create enemy attributes based on parent classes."""
        super().__init__(canvas, x, y)


class Projectile:
    """Projectiles/bullets shot from player and enemies."""

    _IMAGES = {
        "Player": tk.PhotoImage(file="Assets/Images/Bullet (Player).png"),
        "Enemy": tk.PhotoImage(file="Assets/Images/Bullet (Enemy).png")}
    WIDTH = _IMAGES["Player"].width()  # Images should have same dimensions
    HEIGHT = _IMAGES["Player"].height()

    def __init__(self, canvas, x, y, x_velocity, y_velocity, damage, side):
        """Create projectile attributes and display projectile image."""
        self._canvas = canvas
        self.x = x
        self.y = y
        self._x_velocity = x_velocity
        self._y_velocity = y_velocity
        self.damage = damage
        self.side = side  # Owner of projectile (Player or Enemy)
        self.active = True

        # Images
        self.image = self._canvas.create_image(
            self.x, self.y, image=Projectile._IMAGES[self.side])
        self._canvas.lower(self.image)

    def remove(self):
        """Remove projectile image.

        Returns: None
        """
        self._canvas.delete(self.image)

    def move(self):
        """Move projectile within game canvas based on velocity.

        Return: None
        """
        # Check if projectile in game canvas
        if self.x + self.WIDTH < 0 or self.x > GUI.WIDTH or \
                self.y + self.HEIGHT < 0 or self.y > GUI.HEIGHT:
            self.active = False
        else:
            # Move images
            self.x += self._x_velocity
            self.y += self._y_velocity
            self._canvas.moveto(
                self.image, self.x - self.WIDTH / 2,
                self.y - self.HEIGHT / 2)


# Start program
if __name__ == "__main__":
    GUI()
