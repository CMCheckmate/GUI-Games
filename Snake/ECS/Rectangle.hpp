#pragma once

#include "../Game.hpp"
#include <SDL2/SDL.h>

class Rectangle {
public:
    Rectangle(float x, float y, float width, float height, SDL_Color colour) : rect({x, y, width, height}), colour(colour) {}

    virtual void setCoords(float x, float y) {
        this->rect.x = x;
        this->rect.y = y;
    }

    virtual void setSize(float width, float height) {
        this->rect.w = width;
        this->rect.h = height;
    }

    void render() {
        Game::setDrawColour(this->colour);
        SDL_RenderFillRectF(Game::renderer, &this->rect);
    }

    virtual SDL_Color getColour() const { return this->colour; }

    virtual SDL_FRect getRect() const { return this->rect; }
    
private:
    SDL_Color colour;
    SDL_FRect rect;
};