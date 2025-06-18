# Fruit Catcher Game

A simple Python game built with Pygame where you catch falling fruits with a basket.

## How to Play

- Use **LEFT** and **RIGHT** arrow keys to move your basket
- Catch falling apples to gain points (1 point per apple)
- You have 3 lives - you lose a life each time a fruit hits the ground
- Game ends after losing all 3 lives
- Press **SPACE** to restart after game over
- Press **ESC** to quit from the game over screen

## Installation

1. Make sure you have Python installed
2. Install Pygame:
   ```bash
   pip install pygame
   ```
   Or install from requirements file:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Game

```bash
python fruit_catcher.py
```

## Game Features

- **Balanced Gameplay**: Optimized speeds and timing for human players
- **Wider Basket**: Easier to catch fruits with improved collision detection
- **Progressive Difficulty**: Game gets gradually harder as you play
- **Forgiving Collision**: Slightly expanded catch area for better gameplay
- **Smooth Movement**: Responsive basket controls
- **Visual Design**: Red apples with green stems and brown basket
- **Level System**: Shows current difficulty level

## Game Balance Improvements

- **Faster Basket Movement**: 50% faster basket speed for better control
- **Slower Fruit Speed**: Reduced fruit falling speed for easier catching
- **Wider Basket**: 25% larger basket for improved catch rate
- **Better Collision**: Expanded collision area for more forgiving gameplay
- **Less Frequent Spawning**: More time between fruit drops initially
- **Progressive Challenge**: Difficulty increases gradually over time

## Controls

- **LEFT Arrow**: Move basket left
- **RIGHT Arrow**: Move basket right
- **SPACE**: Restart game (on game over screen)
- **ESC**: Quit game (on game over screen)
- **X button**: Close game window

Enjoy catching those fruits!
