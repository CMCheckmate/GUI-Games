"""
A game of endless pong.

Both sides each have a paddle that can move to bounce a ball to the other side.
Round is won when ball reaches the opposite side border of the player.
Ball bounces off top and bottom border and resets at centre.
"""

# Imports
import tkinter as tk
import random


# Classes
class GUI:
    """Create the canvas and objects on canvas to begin game."""

    # Constants
    _ASSET_DIR = "Assets"
    _IMAGE_DIR = "Images"
    _FONT_DIR = "Fonts"
    COLOURS = {"WHITE": "#FFFFFF", "BLACK": "#000000"}
    _TITLE = "Pong"
    WIDTH = 800
    HEIGHT = 600
    FRAME_INTERVAL = round(1000 / 60)

    def __init__(self):
        """Create canvas and window."""
        self._window = tk.Tk()
        self.canvas = tk.Canvas(self._window,
                                width=GUI.WIDTH, height=GUI.HEIGHT,
                                bg=GUI.COLOURS["BLACK"], highlightthickness=0)
        self.paddle_1 = Paddle(*Paddle.DEFAULT_POSITION[1], self.canvas, 1)
        self.paddle_2 = Paddle(*Paddle.DEFAULT_POSITION[2], self.canvas, 2)
        self.ball = Ball(*Ball.DEFAULT_POSITION, self.canvas)
        self.score_1 = tk.StringVar()
        self.score_2 = tk.StringVar()

    def _check_collisions(self):
        """
        Check collisions of ball with paddle.

        :param paddle_1_pos: Tuple of coordinates of player 1's paddle
        :param paddle_2_pos: Tuple of coordinates of player 2's paddle
        :return:
        """
        # Define edges
        paddle_1_side = (self.paddle_1.x + Paddle.WIDTH, self.paddle_1.y,
                         self.paddle_1.x + Paddle.WIDTH,
                         self.paddle_1.y + Paddle.HEIGHT)
        paddle_1_top = (self.paddle_1.x, self.paddle_1.y,
                        self.paddle_1.x + Paddle.WIDTH, self.paddle_1.y)
        paddle_1_bottom = (self.paddle_1.x, self.paddle_1.y + Paddle.HEIGHT,
                           self.paddle_1.x + Paddle.WIDTH,
                           self.paddle_1.y + Paddle.HEIGHT)
        paddle_2_side = (self.paddle_2.x, self.paddle_2.y,
                         self.paddle_2.x, self.paddle_2.y + Paddle.HEIGHT)
        paddle_2_top = (self.paddle_2.x, self.paddle_2.y,
                        self.paddle_2.x + Paddle.WIDTH, self.paddle_2.y)
        paddle_2_bottom = (self.paddle_2.x, self.paddle_2.y + Paddle.HEIGHT,
                           self.paddle_2.x + Paddle.WIDTH,
                           self.paddle_2.y + Paddle.HEIGHT)

        # Collisions
        collisions = []
        # Side
        if self.ball.image in self.canvas.find_overlapping(*paddle_1_side):
            collisions.append("Left")
        elif self.ball.image in self.canvas.find_overlapping(*paddle_2_side):
            collisions.append("Right")
        # Top
        if self.ball.image in self.canvas.find_overlapping(*paddle_1_top) or \
                self.ball.image in self.canvas.find_overlapping(*paddle_2_top):
            collisions.append("Top")
        elif self.ball.image in \
                self.canvas.find_overlapping(*paddle_1_bottom) or \
                self.ball.image in \
                self.canvas.find_overlapping(*paddle_2_bottom):
            collisions.append("Bottom")

        return collisions

    def _loop(self):
        """
        Game loop events.

        :return: None
        """
        # Collisions
        collisions = self._check_collisions()
        # Horizontal
        if "Left" in collisions:
            self.ball.x_velocity = abs(self.ball.x_velocity)
        elif "Right" in collisions:
            self.ball.x_velocity = -abs(self.ball.x_velocity)
        # Vertical
        if "Top" in collisions:
            self.ball.y_velocity = -abs(self.ball.y_velocity)
        elif "Bottom" in collisions:
            self.ball.y_velocity = abs(self.ball.y_velocity)

        # Object movement
        self.ball.move()
        self.paddle_1.move()
        self.paddle_2.move()

        # Point scored
        if self.ball.scored:
            # Update score
            if self.ball.scored == 1:
                score_1 = int(self.score_1.get())
                self.score_1.set(score_1 + 1)
            elif self.ball.scored == 2:
                score_2 = int(self.score_2.get())
                self.score_2.set(score_2 + 1)

            # Reset objects
            self.ball.reset()
            self.paddle_1.reset()
            self.paddle_2.reset()

        # Loop
        self.canvas.after(GUI.FRAME_INTERVAL, self._loop)

    def initiate(self):
        """Initiate and run game."""
        # Window
        self._window.title(GUI._TITLE)
        self._window.geometry(f"{GUI.WIDTH}x{GUI.HEIGHT}")
        self._window.protocol("WM_DELETE_WINDOW", exit)

        # Background
        # Central line
        line_width = round(GUI.WIDTH / 150)
        line_dash = round(GUI.HEIGHT / 40)
        line_coordinates = (GUI.WIDTH / 2, 0, GUI.WIDTH / 2, GUI.HEIGHT)
        self.canvas.create_line(*line_coordinates, width=line_width,
                                fill=GUI.COLOURS["WHITE"], dash=line_dash)
        # Score
        score_font = ("OCR A Extended",
                      round(0.5 * (GUI.WIDTH + GUI.HEIGHT) / 20))
        score_padding = (GUI.WIDTH / 10, GUI.HEIGHT / 10)
        score_1_text = self.canvas.create_text(
            (GUI.WIDTH / 2) - score_padding[0], score_padding[1],
            fill=GUI.COLOURS["WHITE"], font=score_font)
        score_2_text = self.canvas.create_text(
            (GUI.WIDTH / 2) + score_padding[0], score_padding[1],
            fill=GUI.COLOURS["WHITE"], font=score_font)
        self.score_1.trace("w", lambda *_: self.canvas.itemconfig(
            score_1_text, text=str(self.score_1.get())))
        self.score_2.trace("w", lambda *_: self.canvas.itemconfig(
            score_2_text, text=str(self.score_2.get())))
        self.score_1.set(0)
        self.score_2.set(0)

        self.canvas.pack()
        self.canvas.focus_set()

        # GUI loop
        self._loop()
        self._window.mainloop()


class Ball:
    """Create ball and set velocity."""

    # Constants
    _DIAMETER = round(0.5 * (GUI.WIDTH + GUI.HEIGHT) / 50)
    DEFAULT_POSITION = ((GUI.WIDTH / 2) - (_DIAMETER / 2),
                        (GUI.HEIGHT / 2) - (_DIAMETER / 2))
    _SPEED_RANGE = {"x": (round((GUI.WIDTH / 10) / GUI.FRAME_INTERVAL),
                          round((GUI.WIDTH / 6) / GUI.FRAME_INTERVAL)),
                    "y": (round((GUI.HEIGHT / 10) / GUI.FRAME_INTERVAL),
                          round((GUI.HEIGHT / 6) / GUI.FRAME_INTERVAL))}

    def __init__(self, x, y, canvas):
        """Set ball position on canvas."""
        self.x = x
        self.y = y
        self.canvas = canvas
        self.image = self.canvas.create_oval(self.x, self.y,
                                             self.x + Ball._DIAMETER,
                                             self.y + Ball._DIAMETER,
                                             fill=GUI.COLOURS["WHITE"])
        self.x_velocity = random.choice((-1, 1)) * \
            random.randrange(*Ball._SPEED_RANGE["x"])
        self.y_velocity = random.choice((-1, 1)) * \
            random.randrange(*Ball._SPEED_RANGE["y"])
        self.scored = None

    def reset(self):
        """
        Reset ball after point scored.

        :return: None
        """
        # Reset attributes
        self.x_velocity = random.choice((-1, 1)) * \
            random.randrange(*Ball._SPEED_RANGE["x"])
        self.y_velocity = random.choice((-1, 1)) * \
            random.randrange(*Ball._SPEED_RANGE["y"])
        self.scored = None

        # Replace at default
        movement = (Ball.DEFAULT_POSITION[0] - self.x,
                    Ball.DEFAULT_POSITION[1] - self.y)
        self.canvas.move(self.image, *movement)
        self.x, self.y = Ball.DEFAULT_POSITION

    def move(self):
        """
        Move and bounce ball according to collisions and current speed.

        :return: None
        """
        # Horizontal
        moved_x = self.x + self.x_velocity
        if 0 < moved_x < GUI.WIDTH - Ball._DIAMETER:
            self.canvas.move(self.image, self.x_velocity, 0)
        elif moved_x > GUI.WIDTH - Ball._DIAMETER:
            moved_x = GUI.WIDTH - Ball._DIAMETER
            self.scored = 1
        elif moved_x < 0:
            moved_x = 0
            self.scored = 2
        self.x = moved_x

        # Vertical
        moved_y = self.y + self.y_velocity
        if 0 < moved_y < GUI.HEIGHT - Ball._DIAMETER:
            self.canvas.move(self.image, 0, self.y_velocity)
        elif moved_y < 0:
            moved_y = 0
            self.y_velocity = -self.y_velocity
        elif moved_y > GUI.HEIGHT - Ball._DIAMETER:
            moved_y = GUI.HEIGHT - Ball._DIAMETER
            self.y_velocity = -self.y_velocity
        self.y = moved_y


class Paddle:
    """Create paddle and set velocity."""

    # Constants
    WIDTH = GUI.WIDTH / 50
    HEIGHT = GUI.HEIGHT / 8
    _SPEED = (GUI.HEIGHT / 5) / GUI.FRAME_INTERVAL
    _DIRECTION_KEYS = {1: ("w", "s"), 2: ("Up", "Down")}
    DEFAULT_POSITION = {1: (GUI.WIDTH / 80, (GUI.HEIGHT / 2) - (HEIGHT / 2)),
                        2: (GUI.WIDTH - (GUI.WIDTH / 80) - WIDTH,
                            (GUI.HEIGHT / 2) - (HEIGHT / 2))}

    def __init__(self, x, y, canvas, id_):
        """Set coordinates and place paddle on canvas."""
        self.x = x
        self.y = y
        self._id = id_
        self.canvas = canvas
        self._image = self.canvas.create_rectangle(self.x, self.y,
                                                   self.x + Paddle.WIDTH,
                                                   self.y + Paddle.HEIGHT,
                                                   fill=GUI.COLOURS["WHITE"])
        self._velocity = 0

        # Events
        self.canvas.bind("<KeyPress>",
                         lambda event, pressed=True: self._direction_event(
                             event, pressed), add="+")
        self.canvas.bind("<KeyRelease>",
                         lambda event, pressed=False: self._direction_event(
                             event, pressed), add="+")

    def reset(self):
        """
        Reset paddle after point scored.

        :return: None
        """
        # Reset attributes
        self._velocity = 0

        # Replace at default
        movement = Paddle.DEFAULT_POSITION[self._id][1] - self.y
        self.canvas.move(self._image, 0, movement)
        self.x, self.y = Paddle.DEFAULT_POSITION[self._id]

    def _direction_event(self, event, pressed):
        """
        Convert keyboard events to direction for paddle.

        :param event: Keyboard event object
        :param pressed: Keyboard pressed or released
        :return: None
        """
        key_pressed = event.keysym
        if pressed:
            # Direction
            if key_pressed == Paddle._DIRECTION_KEYS[self._id][0]:
                self._velocity = -Paddle._SPEED
            elif key_pressed == Paddle._DIRECTION_KEYS[self._id][1]:
                self._velocity = Paddle._SPEED
        else:
            # Reset
            if key_pressed in Paddle._DIRECTION_KEYS[self._id]:
                self._velocity = 0

    def move(self):
        """
        Move paddle according to current direction.

        :return: None
        """
        # Movement
        if self._velocity != 0:
            moved_y = self.y + self._velocity
            if 0 < moved_y < GUI.HEIGHT - Paddle.HEIGHT:
                self.canvas.move(self._image, 0, self._velocity)
            else:
                if moved_y < 0:
                    moved_y = 0
                if moved_y > GUI.HEIGHT - Paddle.HEIGHT:
                    moved_y = GUI.HEIGHT - Paddle.HEIGHT
                self.canvas.moveto(self._image, self.x, moved_y)
            self.y = moved_y


# Main
if __name__ == "__main__":
    GUI().initiate()
