import time
import random

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
        win: Window = None,
        seed: int | None = 10,
    ) -> None:
        self._cells: list[list[Cell]] = []
        self._x1 = x1 # top left corner of maze
        self._y1 = y1 # top left corner of maze
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self.__maze_corners = {"top_left" : (0, 0), "top_right" : (self._num_cols - 1, 0), "bottom_right" : (self._num_cols - 1, self._num_rows - 1), "bottom_left" : (0, self._num_rows - 1)}
        self._start_cell = self.__maze_corners["top_right"]
        self._end_cell = self.__maze_corners["bottom_left"]
        
        random.seed(seed)
        
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
        
    def _create_cells(self) -> None:
        # populate self._cells with a matrix of cells  (each top-level list is a column)
        self._cells = [[Cell(self._win) for row in range(self._num_rows)] for column in range(self._num_cols)]
        for i, column in enumerate(self._cells):
            for j in range(len(column)):
                self._draw_cell(i, j)
                
    def _draw_cell(self, i: int, j: int) -> None:
        if self._win is None:
            return
        
        top_left_x, top_left_y, bottom_right_x, bottom_right_y = self.get_cell_points(i, j)
        
        self._cells[i][j].draw(top_left_x, top_left_y, bottom_right_x, bottom_right_y)
        self._animate(0.01)

    def get_cell_points(self, i: int, j: int) -> tuple[int, int, int, int]:
        """return top left x, y, and bottom right x, y of the chosen cell"""
        top_left_x = self._x1 + (i * self._cell_size_x)
        top_left_y = self._y1 + (j * self._cell_size_y)
        bottom_right_x = top_left_x + self._cell_size_x
        bottom_right_y = top_left_y + self._cell_size_y
        return top_left_x, top_left_y, bottom_right_x, bottom_right_y
        
    def _animate(self, sec: float = 0.05) -> None:
        if self._win is None:
            return
        
        self._win.redraw()
        time.sleep(sec)
        
    def _break_entrance_and_exit(self) -> None:
        # remove top wall of top-left cell and bottom wall of bottom-right cell
        start_i, start_j = self._start_cell
        end_i, end_j = self._end_cell
        
        if start_j == 0:
            self._cells[start_i][start_j].has_top_wall = False
        else:
            self._cells[start_i][start_j].has_bottom_wall = False
        self._draw_cell(start_i, start_j)
        
        if end_j == 0:
            self._cells[end_i][end_j].has_top_wall = False
        else:
            self._cells[end_i][end_j].has_bottom_wall = False
        self._draw_cell(end_i, end_j)
    
    def _break_walls_r(self, i: int, j: int) -> None:
        curr_cell = self._cells[i][j]
        curr_cell.visited = True
        while True:
            to_visit = self._get_adjacent_cells(i, j)
                        
            if len(to_visit) == 0:
                curr_cell.draw(*self.get_cell_points(i, j))
                break
            
            # pick a random direction
            chosen_i, chosen_j = to_visit[random.randrange(0, len(to_visit))]
            
            # knock down walls between current cell and chosen cell
            chosen_cell = self._cells[chosen_i][chosen_j]
            # chosen cell on the left
            if chosen_i < i:
                curr_cell.has_left_wall = chosen_cell.has_right_wall = False
            # chosen cell above
            elif chosen_j < j:
                curr_cell.has_top_wall = chosen_cell.has_bottom_wall = False
            # chosen cell to the right
            elif chosen_i > i:
                curr_cell.has_right_wall = chosen_cell.has_left_wall = False
            # chosen cell below
            elif chosen_j > j:
                curr_cell.has_bottom_wall = chosen_cell.has_top_wall = False
                
            self._break_walls_r(chosen_i, chosen_j)

    def _get_adjacent_cells(self, i: int, j: int) -> list[tuple[int, int]]:
        to_visit: list[tuple[int, int]] = []
        adjacent_cells = [(i-1, j), (i, j-1), (i+1, j), (i, j+1)]
            
        for cell_i, cell_j in adjacent_cells:
            if 0 <= cell_i < self._num_cols and 0 <= cell_j < self._num_rows:
                if not self._cells[cell_i][cell_j].visited:
                    to_visit.append((cell_i, cell_j))
        return to_visit
            
    def _reset_cells_visited(self) -> None:
        for column in self._cells:
            for cell in column:
                cell.visited = False
                
    def solve(self) -> bool:
        return self._solve_r(*self._start_cell)
    
    def _solve_r(self, i: int, j: int) -> bool:
        self._animate()
        self._cells[i][j].visited = True
        if (i, j) == self._end_cell:
            return True
        cell = self._cells[i][j]
        
        adjacent_cells = self._get_adjacent_cells(i, j)
        # left i - 1, top j - 1, right i + 1, bottom j + 1
        for adj_i, adj_j in adjacent_cells:
            chosen_cell = self._cells[adj_i][adj_j]
            
            if chosen_cell.visited:
                continue
            if adj_i < i and cell.has_left_wall:
                continue
            if adj_j < j and cell.has_top_wall:
                continue
            if adj_i > i and cell.has_right_wall:
                continue
            if adj_j > j and cell.has_bottom_wall:
                continue
            
            cell.draw_move(chosen_cell)
            
            if self._solve_r(adj_i, adj_j):
                return True
            else:
                cell.draw_move(chosen_cell, undo=True)
                
        return False