from .base_widget import Widget

class WidgetDecorator(Widget):
    def __init__(self, component):
        super(WidgetDecorator, self).__init__()
        self.component = component

    def draw(self, display):
        if self.component is None:
            return
        self.component.draw(display)

    def set_height(self, height):
        self.height = height

        if self.component is None:
            return

        self.component.set_height(height)

    def set_width(self, width):
        self.width = width

        if self.component is None:
            return

        self.component.set_width(width)
