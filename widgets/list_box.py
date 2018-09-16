from random import randint
from widgets.widget_decorator import WidgetDecorator
from .frame import Frame
from .text_box import TextBox
from .common import Color
from console.console_events import KeyCommands


class ListBoxItem(object):
    def __init__(self, text):
        self.width = 10
        self.text = text
        self.text_color = Color.GREEN
        self.background_color = Color.BLACK
        self.highlight = False
        self.highlight_bg_color = Color.GREEN
        self.highlight_text_color = Color.BLACK
        self.id = 0
        self.x = 0
        self.y = 0

    def draw(self, display):
        truncated_text = self.text[:self.width]
        text_color = self.__text_color()
        bg_color = self.__bg_color()
        display.draw_text(self.x, self.y, truncated_text, text_color, bg_color)

    def __text_color(self):
        if self.highlight:
            return self.highlight_text_color
        return self.text_color

    def __bg_color(self):
        if self.highlight:
            return self.highlight_bg_color
        return self.background_color


class ListBox(WidgetDecorator):
    def __init__(self):
        self._frame = Frame()
        self._frame.border_enabled = True
        self._text_box = TextBox()

        super(ListBox, self).__init__(self._text_box)
        self._lines = []
        self._line_number_prefix = "[%d.]"
        self._items = []
        self.top_padding = 1
        self.left_padding = 2
        self.right_padding = 2
        self.bottom_padding = 3
        self.width = 10
        self.height = self.top_padding
        self.auto_resize = True
        self.text_color = Color.GREEN
        self.text_highlight_color = Color.BLUE
        self.call_back = None
        self._selected_item = None
        self._id_counter = 0

    def add_line(self, line):
        """Push line to bottom of list"""
        item = ListBoxItem(line)
        item.id = self._id_counter
        self._items.append(item)
        self._id_counter += 1

    def add_lines(self, lines):
        for line in lines:
            self.add_line(line)

    def wrap_line(self, line, max_line_length):
        lines = []
        i, j = 0, max_line_length
        while i <= len(line):
            lines.append(line[i:j])
            i, j = j, j + max_line_length
        return lines

    def indent(self, s, n):
        i = 0
        while i < n:
            s = " " + s
            i += 1
        return s

    def draw(self, display):
        n = len(self._items)
        height_with_items = n + self.top_padding + self.bottom_padding
        if (height_with_items > self.height):
            self.set_height(height_with_items)

        super(ListBox, self).draw(display)

        x, y = [self.left_padding, self.top_padding]
        for item in self._items:
            item.x = x
            item.y = y
            item.width = self.width - self.right_padding
            item.highlight_text_color = self.text_highlight_color
            item.draw(display)
            y += 1

    def on_select(self, item):
        self.clear_highlighting()
        self.highlight_item(item)
        self._selected_item = item
        if self.call_back:
            self.call_back(item)

    def select(self, item_index):
        item = self._items[item_index]
        self.on_select(item)

    def highlight_item(self, item):
        item.highlight = True

    def remove_highlight_item(self, item):
        item.highlight = False

    def clear_highlighting(self):
        for item in self._items:
            self.remove_highlight_item(item)

    def get_key_command(self, event):
        return event.key_command

    def get_last_index(self):
        return len(self._items) - 1
        
    def handle_event(self, event):
        command = self.get_key_command(event)
        if command is None:
            return

        n = len(self._items)
        selected = self._selected_item
        
        if command == KeyCommands.UP:
            if selected is None:
                self.select(0)
            elif selected.id > 0:
                self.select(selected.id - 1)
        elif command == KeyCommands.DOWN:
            if selected is None:
                self.select(n-1)
            elif selected.id < (n-1):
                self.select(selected.id + 1)

        self.is_dirty = True
        return
