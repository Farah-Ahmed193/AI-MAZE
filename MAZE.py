import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QLabel, QPushButton
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
import random


width, height = 10, 10
maze = [[0 for _ in range(width)] for _ in range(height)]
start = (0, 0)  
end = (9, 9) 
player_position = start
score = 0
time_elapsed = 0
time_limit = 60  
steps_taken = 0 

def generate_walls():
    global maze
    path_exists = False
    while not path_exists:
        maze = [[0 if random.random() > 0.4 else 1 for _ in range(width)] for _ in range(height)]
        maze[start[0]][start[1]] = 0
        maze[end[0]][end[1]] = 0
        path_exists = bool(astar(maze, start, end))

def astar(maze, start, end):

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
    open_list = [(start, [], 0)] 
    closed_set = set()  

    def heuristic(n, end):
        return abs(n[0] - end[0]) + abs(n[1] - end[1])  
    while open_list:

        open_list.sort(key=lambda x: x[2] + heuristic(x[0], end))  
        current, path, g_cost = open_list.pop(0) 

        if current == end: 
            return path + [end]  

        if current in closed_set:
            continue  

        closed_set.add(current)  

        for dx, dy in directions: 
            nx, ny = current[0] + dx, current[1] + dy  
            if 0 <= nx < height and 0 <= ny < width and maze[nx][ny] == 0 and (nx, ny) not in closed_set:
                new_g_cost = g_cost + 1
                open_list.append(((nx, ny), path + [current], new_g_cost)) 

    return [] 


class MazeSolver(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Maze Solver")
        self.setGeometry(200, 200, 600, 700)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)

        self.score_label = QLabel(f"Score: {score}", self)
        self.score_label.setFont(QFont("Arial", 20))
        self.score_label.setStyleSheet("color: blue; margin: 10px;")

        self.timer_label = QLabel(f"Time: {time_elapsed} s", self)
        self.timer_label.setFont(QFont("Arial", 20))
        self.timer_label.setStyleSheet("color: red; margin: 10px;")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.score_label)
        self.layout.addWidget(self.timer_label)
        self.layout.addWidget(self.view)

        self.setLayout(self.layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000) 

        self.setFocusPolicy(Qt.StrongFocus) 
        self.view.setFocusPolicy(Qt.NoFocus)
        self.setFocus() 

        self.generate_maze()

    def generate_maze(self):
        global maze, start, end, player_position, time_elapsed, score, steps_taken
        generate_walls()
        player_position = start
        time_elapsed = 0 
        score = 0
        steps_taken = 0 
        self.draw_maze()

    def draw_maze(self):
        self.scene.clear()
        block_size = 50
        for i in range(height):
            for j in range(width):
                color = Qt.white if maze[i][j] == 0 else Qt.black
                rect = QGraphicsRectItem(j * block_size, i * block_size, block_size, block_size)
                rect.setBrush(color)
                self.scene.addItem(rect)

        start_rect = QGraphicsRectItem(start[1] * block_size, start[0] * block_size, block_size, block_size)
        start_rect.setBrush(Qt.green)
        self.scene.addItem(start_rect)

        end_rect = QGraphicsRectItem(end[1] * block_size, end[0] * block_size, block_size, block_size)
        end_rect.setBrush(Qt.red)
        self.scene.addItem(end_rect)

        
        self.draw_player()

    def draw_player(self):
        
        block_size = 50
        rect = QGraphicsRectItem(player_position[1] * block_size, player_position[0] * block_size, block_size, block_size)
        rect.setBrush(Qt.blue)
        self.scene.addItem(rect)

    def keyPressEvent(self, event):
        global player_position, score, steps_taken
        dx, dy = 0, 0
        if event.key() == Qt.Key_Up:
            dx, dy = -1, 0
        elif event.key() == Qt.Key_Down:
            dx, dy = 1, 0
        elif event.key() == Qt.Key_Left:
            dx, dy = 0, -1
        elif event.key() == Qt.Key_Right:
            dx, dy = 0, 1

        new_x, new_y = player_position[0] + dx, player_position[1] + dy
        if 0 <= new_x < height and 0 <= new_y < width and maze[new_x][new_y] == 0:
            player_position = (new_x, new_y)
            steps_taken += 1
            score += 1
            self.draw_maze()
            self.score_label.setText(f"Score: {score}")

            if player_position == end:
                self.handle_game_end()

    def update_timer(self):
        global time_elapsed
        time_elapsed += 1
        self.timer_label.setText(f"Time: {time_elapsed} s")
        if time_elapsed >= time_limit:
            self.timer.stop()
            self.handle_game_end()

    def handle_game_end(self):
        global steps_taken
        optimal_path = astar(maze, start, end)
        optimal_steps = len(optimal_path) - 1 

        if steps_taken == optimal_steps:
            self.show_congratulations(steps_taken, optimal_steps)
        else:
            self.show_game_over(steps_taken, optimal_steps)

    def show_congratulations(self, steps_taken, optimal_steps):
        self.game_over_window = QWidget()
        self.game_over_window.setWindowTitle("Congratulations")
        self.game_over_window.setGeometry(400, 400, 300, 250)
        self.game_over_window.setStyleSheet("background-color: black;")

        layout = QVBoxLayout()

        message_text = f"Congratulations!\nYour Steps: {steps_taken} | Optimal Steps: {optimal_steps}"

        message_label = QLabel(message_text, self.game_over_window)
        message_label.setFont(QFont("Arial", 18))
        message_label.setStyleSheet("color: green; margin: 20px;")
        message_label.setAlignment(Qt.AlignCenter)

        restart_button = QPushButton("Try Again", self.game_over_window)
        restart_button.setFont(QFont("Arial", 18))
        restart_button.setStyleSheet("background-color: green; color: white; padding: 10px;")
        restart_button.clicked.connect(self.restart_game)

        layout.addWidget(message_label)
        layout.addWidget(restart_button)

        self.game_over_window.setLayout(layout)
        self.game_over_window.show()

    def show_game_over(self, steps_taken, optimal_steps):
        self.game_over_window = QWidget()
        self.game_over_window.setWindowTitle("Game Over")
        self.game_over_window.setGeometry(400, 400, 500, 200)
        self.game_over_window.setStyleSheet("background-color: black;")

        layout = QVBoxLayout()

        message_text = f"Your Steps: {steps_taken} | Optimal Steps: {optimal_steps}"

        message_label = QLabel(message_text, self.game_over_window)
        message_label.setFont(QFont("Arial", 18))
        message_label.setStyleSheet("color: red; margin: 20px;")
        message_label.setAlignment(Qt.AlignCenter)

        restart_button = QPushButton("Try Again", self.game_over_window)
        restart_button.setFont(QFont("Arial", 18))
        restart_button.setStyleSheet("background-color: green; color: white; padding: 10px;")
        restart_button.clicked.connect(self.restart_game)

        layout.addWidget(message_label)
        layout.addWidget(restart_button)

        self.game_over_window.setLayout(layout)
        self.game_over_window.show()

    def restart_game(self):
        self.game_over_window.close()
        self.generate_maze()
        self.timer.start(1000)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MazeSolver()
    window.show()
    sys.exit(app.exec_())
