#include "Game.hpp"

const int FRAME_DELAY = 1000 / 120;

int main(int argc, char* argv[]) {
    Uint32 frameClock;
    
    // Game instansiation
    Game *game = new Game();
    game->init();

    while (game->isActive()) {
        frameClock = SDL_GetTicks();

        // Game actions
        game->update();
        game->render();

        // Set frame rate
        frameClock = SDL_GetTicks() - frameClock;
        if (frameClock < FRAME_DELAY) {
            SDL_Delay(FRAME_DELAY - frameClock);
        }
    }

    game->stop();
}