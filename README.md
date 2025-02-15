Maze Solver Game
Python
PyQt5
License

A PyQt5-based maze navigation game where players race against time to find the optimal path from start to finish. Features procedural maze generation, real-time scoring, and A* pathfinding visualization.

Table of Contents
Features

Installation

How to Play

Game Mechanics

Screenshots

License

Features
🎮 Interactive GUI built with PyQt5

🧩 Procedural maze generation with guaranteed solvable paths

⏳ 60-second time limit challenge

📈 Scoring system comparing player steps vs optimal path

🏃 Real-time player movement with arrow keys

📊 A algorithm integration* for optimal path calculation

🎉 Win/lose screens with performance metrics

Installation
Clone the repository:

bash
Copy
git clone https://github.com/yourusername/maze-solver-game.git
cd maze-solver-game
Install dependencies:

bash
Copy
pip install PyQt5
Run the game:

bash
Copy
python maze_solver.py
How to Play
Controls: Use arrow keys (↑ ↓ ← →) to move the blue player

Objective: Reach the red exit before time runs out

Scoring: Each move deducts points - fewer steps = higher score!

Challenge: Try to match the optimal A* path length

Time Limit: 60 seconds per attempt

Game Mechanics
🧱 Mazes are 10x10 grids with random wall placement (40% wall density)

🔍 A* algorithm ensures solvability during generation

⭐ Score calculation: 100 - (player_steps - optimal_steps)

🕒 Game ends if:

Player reaches exit (win)

Time expires (lose)

Player matches optimal path (special win message)
