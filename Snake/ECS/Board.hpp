#pragma once

#include "Rectangle.hpp"
#include <SDL2/SDL.h>
#include <vector>

class Board : public Rectangle {
public:
    static const SDL_Color COLOUR;
    static const int GRID_SIZE[2];
    static const int EMPTY;

    Board(float x, float y, float width, float height, int gridX = GRID_SIZE[0], int gridY = GRID_SIZE[1], SDL_Color colour = COLOUR)
        : Rectangle(x, y, width, height, colour), gridSize{gridX, gridY}, gridLength{width / gridX, height / gridY} {
        grid.resize(gridX, std::vector<int>(gridY, 0));
    }

    void clear() {
        for (int x = 0; x < this->gridSize[0]; ++x) {
            for (int y = 0; y < this->gridSize[1]; ++y) {
                grid[x][y] = EMPTY;
            }
        }
    }

    std::vector<std::pair<int, int>> getEmptySpaces() const {
        std::vector<std::pair<int, int>> emptySpaces;
        // Grid loop
        for (int x = 0; x < this->gridSize[0]; ++x) {
            for (int y = 0; y < this->gridSize[1]; ++y) {
                // Empty space
                if (this->grid[x][y] == EMPTY) {
                    emptySpaces.emplace_back(std::make_pair(x, y));
                }
            }
        }
        return emptySpaces;
    }

    std::pair<float, float> gridToCoordinate(int x, int y) {
        return std::make_pair(this->getRect().x + x * this->gridLength[0], this->getRect().y + y * this->gridLength[1]);
    }

    void setSize(float width, float height) override {
        Rectangle::setSize(width, height);
        gridLength[0] = width / gridSize[0];
        gridLength[1] = height / gridSize[1];
    }

    void setGrid(int x, int y, int value) { this->grid[x][y] = value; }

    int getGridVal(int x, int y) const { return this->grid[x][y]; }

    const int* getGridSize() const { return this->gridSize; }

    const float *getGridLength() const { return this->gridLength; }

    std::vector<std::vector<int>> getGrid() const { return this->grid; }

private:
    const int gridSize[2];
    float gridLength[2];
    std::vector<std::vector<int>> grid;
};

const SDL_Color Board::COLOUR = {64, 64, 64, 255};
const int Board::GRID_SIZE[2] = {20, 20};
const int Board::EMPTY = 0;
