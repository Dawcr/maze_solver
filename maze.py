import time

from graphics import Window
from cell import Cell


class Maze():
    def __init__(
        self,
        x1: int,
        y1: int,
        num_rows: int,
        num_cols: int,
        cell_size_x: int,
        cell_size_y: int,
        win: Window,
    ) -> None:
        self._x1 = x1 # top left corner of maze
        self._y1 = y1 # top left corner of maze
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells: list[list[Cell]] = []
        self._create_cells()
        
    def _create_cells(self) -> None:
        # populate self._cells with a matrix of cells  (each top-level list is a column)
        self._cells = [[Cell(self._win) for row in range(self._num_rows)] for column in range(self._num_cols)]
        for i, column in enumerate(self._cells):
            for j in range(len(column)):
                self._draw_cell(i, j)
                
    def _draw_cell(self, i: int, j: int) -> None:
        top_left_x = self._x1 + (i * self._cell_size_x)
        top_left_y = self._y1 + (j * self._cell_size_y)
        bottom_right_x = top_left_x + self._cell_size_x
        bottom_right_y = top_left_y + self._cell_size_y
        
        self._cells[i][j].draw(top_left_x, top_left_y, bottom_right_x, bottom_right_y)
        self._animate()
        
    def _animate(self) -> None:
        self._win.redraw()
        time.sleep(0.05)