from graphics import Window, Line, Point


class Cell():
    def __init__(self, win: Window) -> None:
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None # top-left corner
        self._x2 = None # bottom-right corner
        self._y1 = None # top-left corner
        self._y2 = None # bottom-right corner
        self._win: Window = win
        
    def draw(self, x1: int, y1: int, x2: int, y2: int, fill_color: str = "black") -> None:
        self.set_corners(x1, y1, x2, y2)
        
        top_left = Point(self._x1, self._y1)
        bottom_right = Point(self._x2, self._y2)
        top_right = Point(self._x2, self._y1)
        bottom_left = Point(self._x1, self._y2)
        
        if self.has_left_wall:
            line_left = Line(bottom_left, top_left)
            self._win.draw_line(line_left, fill_color)
        if self.has_top_wall:
            line_top = Line(top_left, top_right)
            self._win.draw_line(line_top, fill_color)
        if self.has_right_wall:
            line_right = Line(top_right, bottom_right)
            self._win.draw_line(line_right, fill_color)
        if self.has_bottom_wall:
            line_bottom = Line(bottom_right, bottom_left)
            self._win.draw_line(line_bottom, fill_color)
            
    def set_corners(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2