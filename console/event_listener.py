from time import sleep
from collections import defaultdict
from console.console_events import KeyPressEvent

class EventListener(object):
    def __init__(self, input_source, event_queue):
        self.input_source = input_source
        self._sleep_in_secs = 0.01
        self.exit_key_value = 113
        self._event_queue = event_queue
        self._should_exit = False

    def start(self):
        while True:
            self.step_forward()
            if self._should_exit:
                #self._event_queue.task_done()
                return
            sleep(self._sleep_in_secs)

    def step_forward(self):
        if self.input_source.is_key_pressed():
            scan_code = self.input_source.get_key_pressed()
            if self._is_exit_code(scan_code):
                self._should_exit = True
            self.on_keyboard_event(scan_code)

    def _is_exit_code(self, scan_code):
        return scan_code == self.exit_key_value

    def on_keyboard_event(self, scan_code):
        event = KeyPressEvent(scan_code)
        self._event_queue.put(event)