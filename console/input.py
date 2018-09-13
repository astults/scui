import os
import msvcrt

class MsConsoleInput(object):
    def __init__(self):
        pass

    def is_key_pressed(self):
        return self.is_key_hit()

    def get_key_pressed(self):
        return ord(self.getch())

    def getch(self):
        return msvcrt.getwch()

    def is_key_hit(self):
        return msvcrt.kbhit()
