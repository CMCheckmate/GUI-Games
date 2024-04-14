#pragma once

#include <SDL2/SDL.h>
#include <SDL2/SDL_mixer.h>
#include <string>

class Game {
public:
    static const SDL_Color BG_COLOUR;
    static const SDL_Color FONT_COLOUR;
    static const std::string TITLE;
    static const std::string ICON_PATH;
    static const std::string FONT_PATH;
    static const int RESOLUTION[2];
    static const int FRAME_DELAY;
    
    static SDL_Renderer *renderer;
    static SDL_Event event;

    Game(int width = RESOLUTION[0], int height = RESOLUTION[1], std::string title = TITLE, SDL_Color bgColour = BG_COLOUR,
         std::string iconPath = ICON_PATH, std::string fontPath = FONT_PATH, SDL_Color fontColour = FONT_COLOUR)
        : title(title), bgColour(bgColour), iconPath(iconPath), fontPath(fontPath), fontColour(fontColour), bgMusicPath(bgMusicPath),
          resolution{width, height}, window(nullptr), frameClock(0), active(false) {}

    static void setDrawColour(SDL_Colour colour) {
        SDL_SetRenderDrawColor(renderer, colour.r, colour.g, colour.b, colour.a);
    }

    void init();

    void reset();

    void update();

    void render();

    void stop();

    bool isActive() const { return this->active; }

private:
    const std::string title;
    const SDL_Color bgColour;
    const std::string iconPath;
    const std::string fontPath;
    const SDL_Color fontColour;
    const std::string bgMusicPath;
    SDL_Window *window;
    Uint32 frameClock;
    int resolution[2];
    int direction[2];
    int score;
    int highScore;
    bool paused;
    bool gameOver;
    bool active;
};