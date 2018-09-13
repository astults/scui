import os
from .ColorIt import  Color as ColorIt
from widgets.common import Color
from ctypes import *
from enum import Enum

class COORD(Structure):
    pass

COORD._fields_ = [("X", c_short), ("Y", c_short)]

ColorConv = {Color.BLACK : ColorIt.BLACK,
             Color.GREEN : ColorIt.GREEN,
             Color.BLUE  : ColorIt.BLUE,
             Color.RED   : ColorIt.RED}



class MsConsoleDisplay(object):
    STD_OUTPUT_HANDLE = -11

    def __init__(self):
        self._handle= windll.kernel32.GetStdHandle(MsConsoleDisplay.STD_OUTPUT_HANDLE)
        self._max_y = 0

    def draw_point(self, x0, y0, color, pixel = " "):
        self.__print_at(x0, y0, pixel, color, None)

    def draw_text(self, x, y, text, color, bg_color = None):
        self.__print_at(x, y, text, color, bg_color)

    def draw_line(self, x0, y0, x1, y1, color):
        while(x0 <= x1):
            y = y0
            while (y <= y1):
                self.draw_point(x0, y, color, "*")
                y += 1
            x0 += 1

    def clear(self):
        os.system('cls')

    def __print_at(self, x, y, s, fg_color, bg_color):
        if bg_color is None:
            bg_color = fg_color
        fc = ColorConv[fg_color]
        bc = ColorConv[bg_color]
        s = ColorIt.It(s, fc, bc)
        self._max_y = max(y, self._max_y)
        windll.kernel32.SetConsoleCursorPosition(self._handle, COORD(x, y))
        c = s.encode("windows-1252")
        windll.kernel32.WriteConsoleA(self._handle, c_char_p(c), len(c), None, None)
        windll.kernel32.SetConsoleCursorPosition(self._handle, COORD(0, self._max_y + 1))