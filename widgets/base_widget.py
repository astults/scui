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
        self.background_color_when_disabled = Color.GREEN
        self.is_dirty = False

    def handle_event(self, event):
        pass

    def draw(self, display):
        # self.parent_frame.draw(display)
        pass

    def draw_title(self, display):
        x = self.width // 2
        y = 0
        color = self.title_text_color
        display.draw_text(x, y, self.title, color)

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
