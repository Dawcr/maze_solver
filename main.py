from graphics import Window, Line, Point


def main():
    win = Window(800, 600)
    win.draw_line(
        Line(
            Point(40, 100),
            Point(60, 0)
        ),
        "red"
    )
    win.wait_for_close()
    

if __name__ == "__main__":
    main()