import sys
import random

from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PySide6.QtGui import QPen, QBrush
from PySide6.QtCore import Qt, QTimer

CELL_SIZE = 20
GRID_WIDTH = 20
GRID_HEIGTH = 15

class SnakeGame(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setScene(QGraphicsScene(self))
        self.setSceneRect(0,0,CELL_SIZE*GRID_WIDTH, CELL_SIZE*GRID_HEIGTH)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)
        self.init_game()

    def init_game(self):
        self.direction = Qt.Key_Right
        self.snake = [(4,4),(4,5),(4,6)]
        self.food = self.new_food()
        self.timer.start(300)

    def update_game(self):
        head_x, head_y = self.snake[0]
        if self.direction == Qt.Key_Left:
            new_head = (head_x -1, head_y)
        elif self.direction == Qt.Key_Right:
            new_head = (head_x +1, head_y)
        elif self.direction == Qt.Key_Up:
            new_head = (head_x, head_y -1)
        elif self.direction == Qt.Key_Down:
            new_head = (head_x, head_y +1)

        if new_head in self.snake or new_head[0] < 0 or new_head[0] >= GRID_WIDTH or new_head[1] < 0 or new_head[1] >= GRID_HEIGTH:
            self.timer.stop()
            return

        self.snake.insert(0,new_head)

        if new_head == self.food:
            self.food = self.new_food()
        else:
            self.snake.pop()

        self.draw_game()

    def new_food(self):
        while True:
            x = random.randint(0,GRID_WIDTH-1)
            y = random.randint(0,GRID_HEIGTH-1)

            if (x,y) not in self.snake:
                return x,y

    def draw_game(self):
        self.scene().clear()

        for item in self.snake:
            x, y = item
            self.scene().addRect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE, QPen(Qt.black), QBrush(Qt.red))

        fx, fy = self.food
        self.scene().addRect(fx*CELL_SIZE, fy*CELL_SIZE, CELL_SIZE, CELL_SIZE, QPen(Qt.black), QBrush(Qt.green))


    def keyPressEvent(self, event):
        key = event.key()
        if key in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down):
            if key == Qt.Key_Left and self.direction != Qt.Key_Right:
                self.direction = key
            elif key == Qt.Key_Right and self.direction != Qt.Key_Left:
                self.direction = key
            elif key == Qt.Key_Up and self.direction != Qt.Key_Down:
                self.direction = key
            elif key == Qt.Key_Down and self.direction != Qt.Key_Up:
                self.direction = key

def main():
    app = QApplication(sys.argv)
    game = SnakeGame()
    game.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()