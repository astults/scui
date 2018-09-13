from widgets.widget_decorator import WidgetDecorator
from .frame import Frame
from .base_widget import Widget
from .common import TextUtils
from .common import Color

class TextBox(WidgetDecorator):
    def __init__(self):
        default_width = 20
        default_height = 10
        self.frame = Frame(default_width, default_height)
        self.frame.border_enabled = True
        super(TextBox, self).__init__(self.frame)
        self.text = ""
        self.text_color = Color.GREEN
        self.left_padding = 2
        self.right_padding = 2
        self.top_padding = 2
        self._cursor_pos = [self.left_padding, self.top_padding]
        self._cursor_index = 0
        self._redraw_frame = True
        self._backspace = chr(8)
        self._newline = chr(13)
        self.width = default_width
        self.height = default_height

    def draw(self, display):
        if self._redraw_frame:
            super(TextBox, self).draw(display)
            self._cursor_index = 0
            self._redraw_frame = False

        i = self._cursor_index
        j = 0
        new_text = ""
        while i < len(self.text):
            x, y = self._cursor_pos
            c = self.text[i]

            if c == self._backspace:
                self.dec_cursor_pos()
                x, y = self._cursor_pos
                empty_space = " "
                c = empty_space
            elif TextUtils.is_newline(c):
                self.newline_cursor_pos()
                x,y = self._cursor_pos
                new_text += c
                c = ""
                j += 1
            else:
                self.inc_cursor_pos()
                new_text += c
                j += 1

            display.draw_text(x, y, c, self.text_color, self.background_color)
            i += 1

        self._cursor_index = i
        if j > 0:
            self._cursor_index = j
            self.text = new_text

    def inc_cursor_pos(self):
        x, y = self._cursor_pos
        x += 1
        if x >= (self.width - self.right_padding):
            x = self.left_padding
            y += 1
        self._cursor_pos = [x, y]

    def dec_cursor_pos(self):
        x, y = self._cursor_pos
        x -= 1
        if x < self.left_padding:
            x = self.width - self.right_padding - 1
            y -= 1
        if y < self.top_padding:
            y = self.top_padding
        self._cursor_pos = [x, y]

    def newline_cursor_pos(self):
        x, y = self._cursor_pos
        x = self.left_padding
        y += 1
        self._cursor_pos = [x,y]

    def add_char_to_text(self, char):
        self.text += char

    def on_key_press(self, key_event):
        if key_event.key_char is not None:
            self.add_char_to_text(key_event.key_char)

        self.is_dirty = True

    def handle_event(self, event):
        self.on_key_press(event)