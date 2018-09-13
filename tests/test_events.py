import unittest
from console.console_events import KeyPressEvent
from time import sleep
from console.event_listener import EventListener
from unittest.mock import Mock, MagicMock

class MockEventGenerator(object):
    def __init__(self):
        pass

    def generate(self):
        pass

class MockConsoleInput(object):
    def __init__(self):
        self._input_codes = []
        self._poll_count = 0
        self.exit_key_value = 113

    def set_next_input_code(self, c):
        self._input_codes.append(c)

    def is_key_pressed(self):
        self._poll_count += 1
        if self._poll_count >= 2:
            return True
        return False

    def get_key_pressed(self):
        e = self._input_codes.pop(0)
        return e

class MockQueue(object):
    def __init__(self):
        self.items = []

    def put(self, item):
        self.items.append(item)


class EventListenerTest(unittest.TestCase):

    def setUp(self):
        self._enter_key_value = 13
        self._any_state = 1
        self._did_exit = False


    def test_can_listen_for_event(self):
        any_input_code = self._enter_key_value
        mock_input = MockConsoleInput()
        mock_input.set_next_input_code(any_input_code)
        mock_input.set_next_input_code(mock_input.exit_key_value)

        mock_queue = MockQueue()

        listener = EventListener(mock_input, mock_queue)
        listener.start()

        self.assertTrue(len(mock_queue.items) > 0)

