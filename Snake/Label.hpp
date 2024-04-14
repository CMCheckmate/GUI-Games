#pragma once

#include "Game.hpp"
#include <SDL2/SDL.h>
#include <SDL2/SDL_ttf.h>

class Label {
public:
    Label(std::string content, std::string fontSrc, float x, float y, int size, SDL_Colour colour) {
        this->font = TTF_OpenFont(fontSrc.c_str(), size);
        if (this->font) {
            this->fontSize = size;
            this->colour = colour;
            setText(content);
            setPosition(x, y);
        }
    }

    void setTexture() {
        SDL_DestroyTexture(this->texture);

        // Create new font texture from surface
        SDL_Surface *surface = TTF_RenderText_Solid(this->font, this->content.c_str(), this->colour);
        this->texture = SDL_CreateTextureFromSurface(Game::renderer, surface);
        SDL_FreeSurface(surface);

        // Get origin
        float origin[2] = {this->rect.x + this->rect.w / 2, this->rect.y + this->rect.h / 2};

        // Recalculate dimension
        int width, height;
        SDL_QueryTexture(this->texture, NULL, NULL, &width, &height);
        this->rect.w = width;
        this->rect.h = height;

        // Reset position
        setPosition(origin[0], origin[1]);
    }

    void setSize(int size) {
        this->fontSize = size;
        TTF_SetFontSize(this->font, size);

        setTexture();
    }

    void setPosition(float x, float y) {
        this->rect.x = x - this->rect.w / 2;
        this->rect.y = y - this->rect.h / 2;
    }

    void setText(std::string content) {
        this->content = content;

        setTexture();
    }

    void render() {
        SDL_RenderCopyF(Game::renderer, this->texture, NULL, &this->rect);
    }

    int getFontSize() const { return this->fontSize; }

    TTF_Font* getFont() const { return this->font; }
    
    SDL_FRect getRect() const { return this->rect; }

private:
    SDL_Texture *texture;
    SDL_FRect rect;
    TTF_Font *font;
    int fontSize;
    SDL_Color colour;
    std::string content;
};