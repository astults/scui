from queue import Queue
from threading import Thread
from time import sleep
from console.display import MsConsoleDisplay
from console.event_listener import EventListener
from console.console_events import KeyboardInput, KeyCommands


class DisplayWindow(object):
    def __init__(self, display):
        self.x = 0
        self.y = 0
        self._display = display

    def draw_point(self, x0, y0, color, pixel=" "):
        self._display.draw_point(self.x + x0, self.y + y0, color, pixel)

    def draw_text(self, x, y, text, color, bg_color=None):
        self._display.draw_text(self.x + x, self.y + y, text, color, bg_color)

    def draw_line(self, x0, y0, x1, y1, color):
        self._display.draw_line(self.x + x0, self.y + y0,
                                self.x + x1, self.y + y1,
                                color)

    def clear(self):
        self._display.clear()


class App(object):
    def __init__(self, input_source=KeyboardInput(),
                 display=MsConsoleDisplay()):
        self.widgets = []
        self._cancel_event_polling = False
        self._event_queue = Queue()
        self._event_listener = EventListener(input_source, self._event_queue)
        self.event_poll_thread = None

        self._display = display
        self._should_exit = False
        self._gui_refresh_in_seconds = 0.01
        self._widget_in_focus = None
        self.focused_widget = None
        self._next_widget_id = 0

    def inc_widget_id(self):
        self._next_widget_id += 1

    def add_widget(self, widget, x=0, y=0):
        widget.x = x
        widget.y = y
        widget.id = self._next_widget_id
        self.inc_widget_id()
        self.widgets.append(widget)
        self.set_focus(widget)

    def set_focus(self, w):
        self._widget_in_focus = w
        self.focused_widget = w

    def start(self):
        self._start_event_polling()
        self._run_gui()

    def _start_event_polling(self):
        """Start event-polling"""
        self.event_poll_thread = Thread(target=self._event_listener.start)
        # close poll if main application exits
        self.event_poll_thread.setDaemon(True)
        self.event_poll_thread.start()

    def draw_widget(self, w):
        display_window = DisplayWindow(self._display)
        display_window.x = w.x
        display_window.y = w.y
        w.draw(display_window)

    def _run_gui(self):
        self._display.clear()
        for widget in self.widgets:
            self.draw_widget(widget)

        while True:
            while not self._event_queue.empty():
                event = self._event_queue.get()
                self.exit_event(event)
                self.tab_event(event)
                if self.focused_widget is not None:
                    self.focused_widget.handle_event(event)
                    if self.focused_widget.is_dirty:
                        self.draw_widget(self.focused_widget)
                        self.focused_widget.is_dirty = False
                for w in self.widgets:
                    if w.is_dirty:
                        self.draw_widget(w)
                        w.is_dirty = False
                if self._should_exit:
                    self.event_poll_thread.join()
                    # self._display.clear()
                    return
            sleep(self._gui_refresh_in_seconds)

    def exit_event(self, event):
        if (event.key_code == self._event_listener.exit_key_value):
            self._should_exit = True

    def tab_event(self, event):
        if (event.key_command == KeyCommands.TAB):
            self.select_next_widget()

    def select_next_widget(self):
        current_id = self.focused_widget.id
        if current_id >= len(self.widgets) - 1:
            self.focused_widget = self.widgets[0]
        else:
            self.focused_widget = self.widgets[current_id + 1]
