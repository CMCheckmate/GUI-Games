#pragma once

#include "Rectangle.hpp"
#include <SDL2/SDL.h>

class Food : public Rectangle {
public:
    static const SDL_Color COLOUR;
    static const int VALUE;

    Food(int xGrid, int yGrid, float x, float y, float width, float height, SDL_Color colour = COLOUR)
        : Rectangle(x, y, width, height, colour), position{xGrid, yGrid} {}

    void setPosition(int x, int y) {
        this->position[0] = x;
        this->position[1] = y;
    }
    
    const int* getPosition() const { return this->position; }

private:
    int position[2];
};

const SDL_Color Food::COLOUR = {255, 0, 0, 255};
const int Food::VALUE = 1;
