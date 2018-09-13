import sys

from app import App
from console.display import MsConsoleDisplay
from console.event_listener import EventListener
from console.input import MsConsoleInput
from widgets.frame import Frame
from widgets.list_box import ListBox
from widgets.text_box import TextBox
from widgets.common import Color
from time import sleep

def main(args):
    display = MsConsoleDisplay()
    display.clear()
    #frame.border_enabled = True
    #frame.width = 20
    # listBox = ListBox(frame)
    # listBox.border_color = Color.GREEN
    # listBox.width = 30
    # any_line = "This is a test of a decently sized long line."
    # any_other_line = "Yet another line that is too long"
    # listBox.add_line(any_line)
    # listBox.add_line(any_other_line)
    # listBox.border_enabled = True
    # listBox.auto_resize = True
    # listBox.draw(display)
    text_box = TextBox()
    text_box.text = "Hello there good fellow!"


    list_box = ListBox()
    list_box.width = 20
    any_line = "Hello this is a test"
    another_line = "Goodbye tests!"
    list_box.add_line(any_line)
    list_box.add_line(another_line)
    #
    #console_input = MsConsoleInput()
    app = App()
    app.add_widget(list_box, 20, 5)
    app.add_widget(text_box, 0, 0)
    app.start()



if __name__ == "__main__":
    main(sys.argv[1:])