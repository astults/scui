from .common import Color


class Widget(object):
    def __init__(self):
        self.width = 10
        self.height = 10
        self.enabled = True
        self.border_enabled = False
        self.border_color = Color.GREEN
        self.background_color = Color.BLACK
        self.title_text_color = Color.GREEN
        self.title_bg_color = Color.BLACK
        self.background_color_when_disabled = Color.GREEN
        self.is_dirty = False

    def handle_event(self, event):
        pass

    def draw(self, display):
        # self.parent_frame.draw(display)
        pass

    def draw_title(self, display):
        x = (self.width - len(self.title) - 2) // 2
        y = 0
        color = self.title_text_color
        bg_color = self.title_bg_color
        if self.title is "":
            text = ""
        else:
            text = " " + self.title + " "
        display.draw_text(x, y, text, color, bg_color)

    def draw_border(self, display):
        if not self.border_enabled:
            return
        color = self.border_color
        # top
        display.draw_line(0, 0, self.width - 1, 0, color)
        # bottom
        display.draw_line(0, self.height - 1,
                          self.width - 1, self.height - 1,
                          color)
        # left
        display.draw_line(0, 0, 0, self.height - 1, color)
        # right
        display.draw_line(self.width - 1, 0,
                          self.width - 1, self.height - 1,
                          color)
