from widgets.widget_decorator import WidgetDecorator
from .common import Color


class Frame(WidgetDecorator):
    def __init__(self, width=0, height=0):
        super(Frame, self).__init__(None)
        self.width = width
        self.height = height
        self.title = ""
        self.title_text_color = Color.GREEN
        self.pinned_widgets = []

    def pinned_widget(self, x, y, widget):
        return [x, y, widget]

    def add_widget(self, x, y, widget):
        self.width = x + max(self.width, widget.width)
        self.height = y + max(self.height, widget.height)

        item = self.pinned_widget(x, y, widget)
        self.pinned_widgets.append(item)

    def draw(self, display):
        for x in range(0, self.width):
            for y in range(0, self.height):
                color = self.background_color
                if not self.enabled:
                    color = self.background_color_when_disabled
                display.draw_point(x, y, color)

        self.draw_border(display)
        self.draw_title(display)
        for pinned_widget in self.pinned_widgets:
            x, y, widget = pinned_widget
            widget.draw(display)
