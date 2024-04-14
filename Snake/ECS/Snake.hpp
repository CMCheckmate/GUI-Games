#pragma once

#include "Rectangle.hpp"
#include <SDL2/SDL.h>

class Snake : public Rectangle {
public:
    static const SDL_Color COLOUR;
    static const int VALUE;

    Snake(Snake *previous, int xDir, int yDir) // Direction from previous snake chain
        : Rectangle(previous->getRect().x + xDir * previous->getSpeed()[0], previous->getRect().y + yDir * previous->getSpeed()[1],
                    previous->getRect().w, previous->getRect().h, previous->getColour()),
          position{previous->getPosition()[0] + xDir, previous->getPosition()[1] + yDir}, speed{previous->getSpeed()[0], 
          previous->getSpeed()[1]}, direction{previous->getDirection()[0], previous->getDirection()[1]}, previous(previous) {}
    Snake(int gridX, int gridY, float x, float y, float width, float height, float xspeed, float yspeed, int xDir, int yDir, SDL_Color colour = COLOUR)
        : Rectangle(x, y, width, height, colour), position{gridX, gridY}, speed{xspeed, yspeed}, direction{xDir, yDir}, previous(nullptr) {}

    void move() {
        SDL_FRect rect = this->getRect();
        if (this->direction[0] != 0) {
            this->position[0] += this->direction[0];
            this->setCoords(rect.x + this->direction[0] * this->speed[0], rect.y);
        }
        if (this->direction[1] != 0) {
            this->position[1] += this->direction[1];
            this->setCoords(rect.x, rect.y + this->direction[1] * this->speed[1]);
        }
    }

    void setPrevious(Snake *snake) {
        this->previous = snake;
    }

    void setPosition(int x, int y) {
        this->position[0] = x;
        this->position[1] = y;
    }

    void setDirection(int xDir, int yDir) {
        this->direction[0] = xDir;
        this->direction[1] = yDir;
    }

    void setSpeed(float xspeed, float yspeed) {
        this->speed[0] = xspeed;
        this->speed[1] = yspeed;
    }

    const int* getPosition() const { return this->position; }

    const float* getSpeed() const { return this->speed; }

    const int* getDirection() const { return this->direction; }

    Snake* getPrevious() const { return this->previous; }

private:
    Snake *previous;
    float speed[2];
    int direction[2];
    int position[2];
};

const SDL_Color Snake::COLOUR = {0, 255, 0, 255};
const int Snake::VALUE = 2;
