import sys

from app import App
from console.display import MsConsoleDisplay
from widgets.list_box import ListBox
from widgets.text_box import TextBox


def main(args):
    display = MsConsoleDisplay()
    display.clear()
    text_box = TextBox()
    text_box.text = "Hello there good fellow!"
    text_box.title = "Test"
    text_box.disable()
    list_box = ListBox()
    list_box.width = 20
    any_line = "Hello this is a test"
    another_line = "Goodbye tests!"
    list_box.add_line(any_line)
    list_box.add_line(another_line)
    app = App()
    app.add_widget(list_box, 20, 5)
    app.add_widget(text_box, 0, 0)
    app.start()


if __name__ == "__main__":
    main(sys.argv[1:])
