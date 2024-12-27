from graphics import Window, Line, Point


class Cell():
    def __init__(self, win: Window = None) -> None:
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = None # top-left corner
        self._x2 = None # bottom-right corner
        self._y1 = None # top-left corner
        self._y2 = None # bottom-right corner
        self._visited = False
        self._win = win
        
    def draw(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self.set_corners(x1, y1, x2, y2)
        
        if self._win is None:
            return
        
        top_left = Point(self._x1, self._y1)
        bottom_right = Point(self._x2, self._y2)
        top_right = Point(self._x2, self._y1)
        bottom_left = Point(self._x1, self._y2)
        
        line_left = Line(bottom_left, top_left)
        self._win.draw_line(line_left, "black" if self.has_left_wall else "white")
        line_top = Line(top_left, top_right)
        self._win.draw_line(line_top, "black" if self.has_top_wall else "white")
        line_right = Line(top_right, bottom_right)
        self._win.draw_line(line_right, "black" if self.has_right_wall else "white")
        line_bottom = Line(bottom_right, bottom_left)
        self._win.draw_line(line_bottom, "black" if self.has_bottom_wall else "white")
            
    def set_corners(self, x1: int, y1: int, x2: int, y2: int) -> None:
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        
    def get_center(self) -> Point:
        half_width = abs(self._x2 - self._x1) // 2
        half_height = abs(self._y2 - self._y1) // 2
        return Point(self._x1 + half_width, self._y1 + half_height) 
        
    def draw_move(self, to_cell: 'Cell', undo: bool = False) -> None:
        if self._win is None:
            return 
        
        color = "gray" if undo else "red"
        center_line = Line(self.get_center(), to_cell.get_center())
        # can probably avoid a lot of overhead by using less assignments and more primitive types but this is meant to be practice on readability
        self._win.draw_line(center_line, color)
        
