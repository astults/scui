import math
import unittest
from unittest.mock import Mock, MagicMock
from console.console_events import KeyPressEvent
from widgets.frame import Frame
from widgets.list_box import ListBox
from widgets.text_box import TextBox
from enum import Enum


class MockColor(Enum):
    BLACK = 0
    RED = 1
    GREEN = 2


class MockDisplay(object):
    def __init__(self):
        self.points_drawn = []
        self.text_drawn = []
        self.bg_colors_seen = set()
        self.text_colors_seen = set()
        self.max_x = 0
        self.max_y = 0
        self.min_x = 99999
        self.min_y = 99999

    def clear(self):
        pass

    def draw_point(self, x0, y0, color, pixel=""):
        self.max_x = max(self.max_x, x0)
        self.max_y = max(self.max_y, y0)
        self.min_x = min(self.min_x, x0)
        self.min_y = min(self.min_y, y0)

        self.points_drawn.append([x0, y0, color, None])

    def draw_text(self, x, y, text, fg_color, bg_color=None):
        self.max_x = max(self.max_x, x + len(text))
        self.max_y = max(self.max_y, y)
        self.min_x = min(self.min_x, x)
        self.min_y = min(self.min_y, y)

        self.bg_colors_seen.add(bg_color)
        self.text_colors_seen.add(fg_color)

        self.text_drawn.append([x, y, text, fg_color, bg_color])

    def draw_line(self, x0, y0, x1, y1, color):
        while(x0 <= x1):
            y = y0
            while (y <= y1):
                self.draw_point(x0, y, color)
                y += 1
            x0 += 1


class MockWidget(object):
    def __init__(self):
        self.width = 1
        self.height = 1
        self.was_draw_method_called = False

    def draw(self, display):
        self.was_draw_method_called = True


class FrameWidgetTests(unittest.TestCase):

    def setUp(self):
        self.any_width = 3
        self.any_height = 2
        self.any_color = MockColor.RED
        self.frame = Frame(self.any_width, self.any_height)

    def test_frame_draw(self):
        frame = self.frame
        display = MockDisplay()
        self.assertIsNotNone(frame)
        self.assertIsNotNone(display)
        expected_color = MockColor.BLACK
        frame.background_color = expected_color
        frame.border_enabled = False
        frame.draw(display)
        expected = []
        for x in range(0, self.any_width):
            for y in range(0, self.any_height):
                expected.append([x, y, expected_color, None])

        self.assertPointsDrawn(expected, display.points_drawn)

    def test_frame_title_draw(self):
        frame = self.frame
        any_title = "A"
        frame.title = any_title
        expected_title_text = " " + any_title + " "
        display = MockDisplay()
        frame.title_text_color = self.any_color
        frame.title_bg_color = self.any_color
        frame.draw(display)
        self.assertIn([0, 0,
                       expected_title_text,
                       self.any_color, self.any_color],
                      display.text_drawn)

    def test_frame_border_draw(self):
        frame = self.frame
        frame.border_enabled = True
        expected_color = MockColor.RED
        frame.border_color = expected_color
        display = MockDisplay()
        frame.draw_border(display)
        expected = []
        for x in range(0, self.any_width):
            expected.append([x, 0])
            expected.append([x, self.any_height - 1])

        for y in range(0, self.any_height):
            expected.append([0, y])
            expected.append([self.any_width - 1, y])

        for p in expected:
            self.add_color(p, expected_color)

        self.assertPointsDrawn(expected, display.points_drawn)

    def add_color(self, point, fg_color, bg_color=None):
        point.append(fg_color)
        point.append(bg_color)

    def test_resize_when_widget_added(self):
        w0_width = 2
        w0_height = 3
        w1_width = 5
        w1_height = 4
        w0 = Frame(w0_width, w0_height)
        w1 = Frame(w1_width, w1_height)
        frame = self.frame
        frame.add_widget(0, 0, w0)

        # add at the bottom right edge of w0

        frame.add_widget(w0.width, w0.height, w1)
        self.assertEqual(w0_width + w1_width, frame.width)
        self.assertEqual(w0_height + w1_height, frame.height)

    def test_draw_widgets(self):
        w0 = MockWidget()
        frame = self.frame
        frame.add_widget(0, 0, w0)
        display = display = MockDisplay()
        frame.draw(display)
        self.assertTrue(w0.was_draw_method_called,
                        "Draw method on widget was not called.")

    def assertPointsDrawn(self, expected_points, actual_points):
        self.assertEqual(len(expected_points), len(actual_points),
                         "Unequal count of points received.")
        for p in expected_points:
            self.assertTrue(p in actual_points,
                            "Missing %s in expected points." % str(p))

    def maplist(self, f, coll):
        return list(map(f, coll))


class TextBoxWidgetTests(unittest.TestCase):
    def setUp(self):
        self.any_width = 3
        self.any_height = 2
        self.frame = Frame(self.any_width, self.any_height)
        self.any_color = [0, 0, 0, 0]
        self.offset = 4
        self.text_box = TextBox()

    def test_can_initialize(self):
        text_box = TextBox()
        expected = "This is a test"
        text_box.text = expected
        display = MockDisplay()
        text_box.draw(display)
        actual = [t[2] for t in display.text_drawn]
        for c in expected:
            self.assertIn(c, actual)

    def test_disable_text_box_fills_in_background(self):
        self.text_box.text = "Hello World"
        self.text_box.disable()
        display = MockDisplay()
        self.text_box.draw(display)
        expected_color = self.text_box.background_color_when_disabled
        self.assertIn(expected_color, display.bg_colors_seen)

    def test_text_wraps(self):
        text_box = TextBox()
        text_box.width = 20
        expected = "This is a line that should wrap"
        text_box.text = expected
        display = MockDisplay()
        text_box.draw(display)
        self.assertLess(display.max_x, text_box.width)

    def test_text_remains_inbounds(self):
        pass

    def test_can_accept_user_input(self):
        text_box = TextBox()
        input_code_for_letter_a = 97
        expected_text = "a"
        key_event = KeyPressEvent(input_code_for_letter_a)
        text_box.on_key_press(key_event)

        self.assertEqual(expected_text, text_box.text)


class ListBoxWidgetTests(unittest.TestCase):
    def setUp(self):
        self.any_width = 3
        self.any_height = 2
        self.frame = Frame(self.any_width, self.any_height)
        self.any_color = [0, 0, 0, 0]
        self.offset = 4
        self.list_box = ListBox()
        self._test_value = False
        self.item_selected = None

    def test_draw_of_list_contents(self):
        new_line = "Test Line 1"
        self.frame.width = len(new_line) + self.offset
        listBox = self.list_box
        listBox.width = 20
        listBox.max_line_length = 20
        listBox.add_line(new_line)
        display = MockDisplay()
        listBox.draw(display)
        expected = new_line
        actual = [t[2] for t in display.text_drawn]
        self.assertIn(expected, actual)

    def test_vertical_resize_on_new_line(self):
        listBox = self.list_box
        empty_height = listBox.height
        lines = ["Foo", "Bar", "FooBar"]
        listBox.add_lines(lines)
        listBox.draw(Mock())
        self.assertTrue(empty_height < listBox.height)

    def test_draw_of_border(self):
        listBox = self.list_box
        listBox.set_width(20)
        listBox.set_height(10)
        display = MockDisplay()
        listBox.max_line_length = listBox.width
        any_line = "This is a test of a decently sized long line."
        listBox.add_line(any_line)
        listBox.draw(display)
        self.assertLessEqual(display.max_x, listBox.width,
                             "Drew beyond border")
        self.assertEqual(0, display.min_x)
        self.assertEqual(0, display.min_y)
        self.assertEqual(listBox.width, display.max_x + 1)
        self.assertEqual(listBox.height, display.max_y + 1)

    def test_auto_resize(self):
        listBox = self.list_box
        listBox.auto_resize = True
        n_lines_to_add = listBox.height + 5
        multi_line_line = "This is a line that will span multiple lines."
        while (n_lines_to_add > 0):
            listBox.add_line(multi_line_line)
            n_lines_to_add -= 1

        pre_resize_height = listBox.height

        display = MockDisplay()
        listBox.draw(display)
        self.assertLess(pre_resize_height, listBox.height)

    def test_select_list_item_fires_event(self):
        listBox = self.list_box
        listBox.auto_resize = True
        lines = ["Test", "Line", "Here"]
        listBox.add_lines(lines)
        any_item_index = 0
        listBox.call_back = self.list_box_select_callback
        listBox.select(any_item_index)
        self.assertIsNotNone(self.item_selected)

    def test_select_list_item_highlights_entry(self):
        listBox = self.list_box
        listBox.auto_resize = True
        lines = ["Test", "Line", "Here"]
        listBox.add_lines(lines)
        display = MockDisplay()
        listBox.draw(display)
        any_item_index = 1
        listBox.call_back = self.toggle_value
        listBox.select(any_item_index)
        listBox.draw(display)
        list_box_highlight_color = listBox.text_highlight_color
        self.assertIn(list_box_highlight_color, display.text_colors_seen)

    def assertSubset(self, subset, container):
        for item in subset:
            self.assertIn(item, container, "Missing item from subset.")

    def toggle_value(self, event):
        self._test_value = not self._test_value

    def list_box_select_callback(self, event):
        self.item_selected = event


if __name__ == '__main__':
    unittest.main()
