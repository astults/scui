import unittest

from app import App
from tests.test_events import MockConsoleInput
from tests.test_widgets import MockDisplay
from widgets.text_box import TextBox


class MockTextWidget(object):
    def __init__(self):
        self.draw_counts = 0
        self.is_dirty = False

    def draw(self, display):
        self.draw_counts += 1

    def handle_event(self, event):
        pass


class AppTest(unittest.TestCase):
    def setUp(self):
        pass

    def get_initialized_mock_input(self):
        any_input_code = 13
        mock_input = MockConsoleInput()
        mock_input.set_next_input_code(any_input_code)
        mock_input.set_next_input_code(mock_input.exit_key_value)
        return mock_input

    def test_app_refreshes(self):
        mock_input = self.get_initialized_mock_input()
        app = App(input_source=mock_input)
        any_widget = MockTextWidget()
        app.add_widget(any_widget)
        app.start()

        expected_draw_counts = 1
        self.assertEqual(expected_draw_counts, any_widget.draw_counts)

    def test_app_can_position_widgets(self):
        mock_input = self.get_initialized_mock_input()
        any_widget = TextBox()
        any_pos_x = 5
        any_pos_y = 10
        display = MockDisplay()
        app = App(mock_input, display)
        app.add_widget(any_widget, any_pos_x, any_pos_y)
        app.start()
        self.assertEqual(any_pos_x, display.min_x)
        self.assertTrue(any_pos_y, display.min_y)



