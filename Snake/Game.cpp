#include "Game.hpp"
#include "Label.hpp"
#include "ECS/Board.hpp"
#include "ECS/Food.hpp"
#include "ECS/Snake.hpp"
#include <SDL2/SDL_image.h>
#include <SDL2/SDL_ttf.h>
#include <time.h>
#include <iostream>
#include <sstream>
#include <vector>

const SDL_Color Game::BG_COLOUR = {0, 0, 0, 255};
const SDL_Color Game::FONT_COLOUR = {255, 255, 255, 255};
const std::string Game::TITLE = "Snake";
const std::string Game::ICON_PATH = "assets/imgs/snake.png";
const std::string Game::FONT_PATH = "assets/fonts/PublicPixel.ttf";
const int Game::RESOLUTION[2] = {700, 700};
const int Game::FRAME_DELAY = 1000 / 7;
const int STATE_SIZE = 48;
const int CONTROLS_SIZE = 12;
const int SCORE_SIZE = 12;
const float STATE_POS[2] = {0.5, 0.5}; // In ratio of window (centered)
const float CONTROLS_POS[2] = {0.5, 0.025};
const float SCORE_POS[2] = {0.5, 0.075};
const SDL_FRect BOARD_RECT = {0.1, 0.1, 0.8, 0.8}; // In ratio of window
const int SNAKE_INITIAL_POS[2][2] = {{0, 1}, {0, 0}}; // Initial snake chain positions based on grid coordinates
const int SNAKE_INITIAL_DIRECTION[2] = {0, 1}; // Initial snake chain direction (-1 for negative movement, 0 for no movement and 1 for positive movement)
const int FOOD_INITIAL_POS[2] = {1, 1};

SDL_Renderer *Game::renderer = nullptr;
SDL_Event Game::event = {};
std::stringstream ss;
Label *controlsLabel = nullptr;
Label *stateLabel = nullptr;
Label *scoreLabel = nullptr;
Board *board = nullptr;
Food *food = nullptr;
Snake *snakeHead = nullptr;
Snake *snakeTail = nullptr;

void Game::init() {
    // Initialise SDL
    if (!SDL_Init(SDL_INIT_EVERYTHING) == 0) {
        std::cout << "Failed to initialize SDL: " << SDL_GetError() << std::endl;
        return;
    }

    // Create game window
    this->window = SDL_CreateWindow(this->title.c_str(), SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, this->resolution[0], this->resolution[1], SDL_WINDOW_RESIZABLE);
    if (!this->window) {
        std::cout << "Failed to create window: " << SDL_GetError() << std::endl;
        return;
    }

    // Set game icon
    SDL_Surface *favicon = IMG_Load(this->iconPath.c_str());
    if (!favicon) {
        std::cout << "Failed to load icon at: " << this->iconPath << std::endl;
        return;
    }
    SDL_SetWindowIcon(this->window, favicon);
    SDL_FreeSurface(favicon);

    // Create surface renderer
    renderer = SDL_CreateRenderer(this->window, -1, SDL_RENDERER_ACCELERATED);
    if (!renderer) {
        std::cout << "Failed to create renderer: " << SDL_GetError() << std::endl;
        return;
    }

    // Initialise Fonts
    if (!TTF_Init() == 0) {
        std::cout << "Failed to initialize SDL_ttf: " << TTF_GetError() << std::endl;
        return;
    }
    // Labels
    controlsLabel = new Label("Move: WASD/Arrows    Pause/Play/Restart: Spacebar", this->fontPath, this->resolution[0] * CONTROLS_POS[0], this->resolution[1] * CONTROLS_POS[1], CONTROLS_SIZE, this->fontColour);
    stateLabel = new Label("Paused", this->fontPath, this->resolution[0] * STATE_POS[0], this->resolution[1] * STATE_POS[1], STATE_SIZE, this->fontColour);
    if (!controlsLabel->getFont()) {
        std::cout << "Failed to load font: " << this->fontPath << std::endl;
    }

    // Set board
    board = new Board(this->resolution[0] * BOARD_RECT.x, this->resolution[1] * BOARD_RECT.y,
                      this->resolution[0] * BOARD_RECT.w, this->resolution[1] * BOARD_RECT.h);
    
    // Create snake
    snakeHead = new Snake(SNAKE_INITIAL_POS[0][0], SNAKE_INITIAL_POS[0][1],
                          board->getRect().x + SNAKE_INITIAL_POS[0][0] * board->getGridLength()[0],
                          board->getRect().y + SNAKE_INITIAL_POS[0][1] * board->getGridLength()[1],
                          board->getGridLength()[0], board->getGridLength()[1],
                          board->getGridLength()[0], board->getGridLength()[1],
                          SNAKE_INITIAL_DIRECTION[0], SNAKE_INITIAL_DIRECTION[1]);
    snakeTail = new Snake(snakeHead, SNAKE_INITIAL_POS[1][0] - SNAKE_INITIAL_POS[0][0], SNAKE_INITIAL_POS[1][1] - SNAKE_INITIAL_POS[0][1]);
    for (const int* snakePos : SNAKE_INITIAL_POS) {
        board->setGrid(snakePos[0], snakePos[1], Snake::VALUE);
    }

    // Create food
    food = new Food(FOOD_INITIAL_POS[0], FOOD_INITIAL_POS[1], 
                    board->getRect().x + FOOD_INITIAL_POS[0] * board->getGridLength()[0], 
                    board->getRect().y + FOOD_INITIAL_POS[1] * board->getGridLength()[1],
                    board->getGridLength()[0], board->getGridLength()[1]);
    board->setGrid(FOOD_INITIAL_POS[0], FOOD_INITIAL_POS[1], Food::VALUE);

    // Initialise game state
    srand(time(NULL));
    this->paused = false;
    this->gameOver = false;
    this->active = true;
    this->frameClock = SDL_GetTicks();
    this->direction[0] = SNAKE_INITIAL_DIRECTION[0];
    this->direction[1] = SNAKE_INITIAL_DIRECTION[1];

    // Setting score
    this->score = 0;
    this->highScore = score;
    ss.str(std::string());
    ss << "Score: " << this->score << "    Highscore: " << this->highScore;
    scoreLabel = new Label(ss.str(), this->fontPath, this->resolution[0] * SCORE_POS[0], this->resolution[1] * SCORE_POS[1], SCORE_SIZE, this->fontColour);
}

void Game::reset() {
    // Reset game states
    this->score = 0;
    this->paused = false;
    this->gameOver = false;
    this->direction[0] = SNAKE_INITIAL_DIRECTION[0];
    this->direction[1] = SNAKE_INITIAL_DIRECTION[1];

    // Labels
    ss.str(std::string());
    ss << "Score: " << this->score << "    Highscore: " << this->highScore;
    scoreLabel->setText(ss.str());
    stateLabel->setText("Paused");

    // Clear grid
    board->clear();

    // Food
    std::pair<float, float> foodPos = board->gridToCoordinate(FOOD_INITIAL_POS[0], FOOD_INITIAL_POS[1]);
    food->setCoords(foodPos.first, foodPos.second);
    food->setPosition(FOOD_INITIAL_POS[0], FOOD_INITIAL_POS[1]);
    board->setGrid(FOOD_INITIAL_POS[0], FOOD_INITIAL_POS[1], Food::VALUE);

    // Snake head
    std::pair<float, float> snakePos = board->gridToCoordinate(SNAKE_INITIAL_POS[0][0], SNAKE_INITIAL_POS[0][1]);
    snakeHead->setCoords(snakePos.first, snakePos.second);
    snakeHead->setPosition(SNAKE_INITIAL_POS[0][0], SNAKE_INITIAL_POS[0][1]);
    snakeHead->setDirection(SNAKE_INITIAL_DIRECTION[0], SNAKE_INITIAL_DIRECTION[1]);
    // Snake tail
    snakePos = board->gridToCoordinate(SNAKE_INITIAL_POS[1][0], SNAKE_INITIAL_POS[1][1]);
    snakeTail->setCoords(snakePos.first, snakePos.second);
    snakeTail->setPosition(SNAKE_INITIAL_POS[1][0], SNAKE_INITIAL_POS[1][1]);
    snakeTail->setDirection(SNAKE_INITIAL_DIRECTION[0], SNAKE_INITIAL_DIRECTION[1]);
    snakeTail->setPrevious(snakeHead);
    for (const int *snakePos : SNAKE_INITIAL_POS) {
        board->setGrid(snakePos[0], snakePos[1], Snake::VALUE);
    }
}

void Game::update() {
    // Events
    SDL_PollEvent(&event);

    switch (event.type) {
        // Quit game
        case SDL_QUIT:
            this->active = false;
            break;
        case SDL_KEYDOWN:
            if (!this->paused) {
                // Horizontal movement
                if (snakeHead->getDirection()[0] == 0) {
                    if (event.key.keysym.sym == SDLK_a || event.key.keysym.sym == SDLK_LEFT) {
                        this->direction[0] = -1;
                        this->direction[1] = 0;
                    }
                    else if (event.key.keysym.sym == SDLK_d || event.key.keysym.sym == SDLK_RIGHT) {
                        this->direction[0] = 1;
                        this->direction[1] = 0;
                    }
                // Vertical movement
                } else if (snakeHead->getDirection()[1] == 0) {
                    if (event.key.keysym.sym == SDLK_w || event.key.keysym.sym == SDLK_UP) {
                        this->direction[0] = 0;
                        this->direction[1] = -1;
                    }
                    else if (event.key.keysym.sym == SDLK_s || event.key.keysym.sym == SDLK_DOWN) {
                        this->direction[0] = 0;
                        this->direction[1] = 1;
                    }
                }
            }

            // Pause/Unpause/Restart
            if (event.key.keysym.sym == SDLK_SPACE) {
                this->frameClock = SDL_GetTicks();

                if (this->gameOver) {
                    this->reset();
                } else {
                    this->paused = !this->paused;
                }
            }
            break;
        case SDL_WINDOWEVENT:
            // Window resize
            if (event.window.event == SDL_WINDOWEVENT_RESIZED) {
                int originalWidth = this->resolution[0];
                SDL_GetWindowSize(window, &this->resolution[0], &this->resolution[1]);
                // Labels
                float fontRatio = static_cast<float>(this->resolution[0]) / originalWidth;
                stateLabel->setPosition(this->resolution[0] * STATE_POS[0], this->resolution[1] * STATE_POS[1]);
                stateLabel->setSize(stateLabel->getFontSize() * fontRatio);
                controlsLabel->setPosition(this->resolution[0] * CONTROLS_POS[0], this->resolution[1] * CONTROLS_POS[1]);
                controlsLabel->setSize(controlsLabel->getFontSize() * fontRatio);
                scoreLabel->setPosition(this->resolution[0] * SCORE_POS[0], this->resolution[1] * SCORE_POS[1]);
                scoreLabel->setSize(scoreLabel->getFontSize() * fontRatio);
                // Board
                board->setCoords(this->resolution[0] * BOARD_RECT.x, this->resolution[1] * BOARD_RECT.y);
                board->setSize(this->resolution[0] * BOARD_RECT.w, this->resolution[1] * BOARD_RECT.h);
                // Food
                std::pair<float, float> foodPos = board->gridToCoordinate(food->getPosition()[0], food->getPosition()[1]);
                food->setCoords(foodPos.first, foodPos.second);
                food->setSize(board->getGridLength()[0], board->getGridLength()[1]);
                // Snake
                Snake *snake = snakeTail;
                while (snake) {
                    std::pair<float, float> snakePos = board->gridToCoordinate(snake->getPosition()[0], snake->getPosition()[1]);
                    snake->setCoords(snakePos.first, snakePos.second);
                    snake->setSize(board->getGridLength()[0], board->getGridLength()[1]);
                    snake->setSpeed(board->getGridLength()[0], board->getGridLength()[1]);
                    snake = snake->getPrevious();
                }
            }
            break;
        default:
            break;
    }

    // Set game frame rate
    if (SDL_GetTicks() - this->frameClock > Game::FRAME_DELAY && !this->paused && !this->gameOver) {
        this->frameClock = SDL_GetTicks();

        // Check wall collision
        snakeHead->setDirection(this->direction[0], this->direction[1]);
        int snakeHeadPos[2] = {snakeHead->getPosition()[0] + this->direction[0], snakeHead->getPosition()[1] + this->direction[1]};
        if (0 <= snakeHeadPos[0] && snakeHeadPos[0] < board->getGridSize()[0] && 0 <= snakeHeadPos[1] && snakeHeadPos[1] < board->getGridSize()[1]) {
            // Check self collision
            int snakeHeadPosVal = board->getGridVal(snakeHeadPos[0], snakeHeadPos[1]);
            if (snakeHeadPosVal != Snake::VALUE) {
                // Set head
                board->setGrid(snakeHeadPos[0], snakeHeadPos[1], Snake::VALUE);

                // Move snake from tail to head
                Snake *snake = snakeTail;
                while (snake) {
                    // Food eaten
                    if (snakeHeadPosVal == Food::VALUE) {
                        if (snake == snakeTail) {
                            // Lengthen tail
                            snakeTail = new Snake(snake, 0, 0);
                        } else if (snake == snakeHead) {
                            // Spawn new food
                            std::vector<std::pair<int, int>> emptySpaces = board->getEmptySpaces();
                            if (emptySpaces.size() > 1) {
                                int foodIndex;
                                do {
                                    foodIndex = rand() % (emptySpaces.size() - 1);
                                } while (board->getGridVal(emptySpaces[foodIndex].first, emptySpaces[foodIndex].second) != Board::EMPTY);
                                food = new Food(emptySpaces[foodIndex].first, emptySpaces[foodIndex].second,
                                                board->getRect().x + emptySpaces[foodIndex].first * board->getGridLength()[0],
                                                board->getRect().y + emptySpaces[foodIndex].second * board->getGridLength()[1],
                                                board->getGridLength()[0], board->getGridLength()[1]);

                                board->setGrid(emptySpaces[foodIndex].first, emptySpaces[foodIndex].second, Food::VALUE);
                            }
                            // Update score
                            ++this->score;
                            ss.str(std::string());
                            ss << "Score: " << this->score << "    Highscore: " << this->highScore;
                            scoreLabel->setText(ss.str());
                        }
                    } else if (snake == snakeTail) {
                        // Clear tail
                        board->setGrid(snake->getPosition()[0], snake->getPosition()[1], Board::EMPTY);
                    }

                    snake->move();

                    // Update snake chain
                    Snake *prevSnake = snake->getPrevious();
                    if (prevSnake) {
                        snake->setDirection(prevSnake->getDirection()[0], prevSnake->getDirection()[1]);
                    }
                    snake = prevSnake;
                }
            } else {
                this->gameOver = true;
            }
        } else  {
            this->gameOver = true;
        }

        // Game over
        if (this->gameOver) {
            if (this->score > this->highScore) {
                this->highScore = this->score;
                ss.str(std::string());
                ss << "Score: " << this->score << "    Highscore: " << this->highScore;
                scoreLabel->setText(ss.str());
            }
            stateLabel->setText("Game Over");
        }
    }
}

void Game::render() {
    SDL_RenderClear(this->renderer);

    // Rendering objects
    if (board) {
        board->render();
    }
    if (food) {
        food->render();
    }
    Snake *snake = snakeTail;
    while (snake) {
        snake->render();
        snake = snake->getPrevious();
    } 
    // Labels
    if (controlsLabel) {
        controlsLabel->render();
    }
    if (scoreLabel) {
        scoreLabel->render();
    }
    if (stateLabel && (this->paused || this->gameOver)) {
        stateLabel->render();
    }

    // Set background colour
    Game::setDrawColour(this->bgColour);

    SDL_RenderPresent(this->renderer);
}

void Game::stop() {
    // Clean up display
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(this->window);

    SDL_Quit();
}