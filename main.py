import sys

from app import App
from console.display import MsConsoleDisplay
from widgets.list_box import ListBox
from widgets.text_box import TextBox
from widgets.frame import Frame


def main(args):
    display = MsConsoleDisplay()
    display.clear()
    width = 80
    height = 26
    enclosing_frame = Frame(width, height)
    enclosing_frame.set_width(width)
    enclosing_frame.set_title("The Sample Application")
    enclosing_frame.border_enabled = True
    text_box = TextBox()
    text_box.set_width(60)
    text_box.text = "This is a description of the application"
    list_box = ListBox()
    list_box.set_title("Menu")
    list_box.set_width(20)
    list_box.left_padding = 3
    list_box.top_padding = 2
    list_box.add_lines(["Option 1", "Option 2", "Option 3"])
    app = App()
    app.add_widget(enclosing_frame, 0, 0)
    app.add_widget(text_box, 2, 2)
    app.add_widget(list_box, 2, 4 + text_box.height)
    app.set_focus(list_box)
    app.start()


if __name__ == "__main__":
    main(sys.argv[1:])
