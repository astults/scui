import unittest
from console.console_events import KeyPressEvent
from time import sleep
from console.event_listener import EventListener
from unittest.mock import Mock, MagicMock


class MockEvent(object):
    def __init__(self):
        pass


class MockConsoleInput(object):
    def __init__(self):
        self._events = []
        self._poll_count = 0
        self.exit_key_value = 113

    def set_next_input_code(self, c):
        e = MockEvent()
        e.key_code = c
        e.key_command = None
        e.key_char = chr(e.key_code)
        self.set_next_event(e)

    def set_next_event(self, e):
        self._events.append(e)
    
    def is_key_pressed(self):
        self._poll_count += 1
        if self._poll_count >= 2:
            return True
        return False

    def get_key_pressed(self):
        if len(self._events) == 0:
            self.set_next_input_code(self.exit_key_value)

        e = self._events.pop(0)
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

