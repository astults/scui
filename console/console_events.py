import os
import msvcrt
from enum import Enum
from console.input import MsConsoleInput

class KeyTag(Enum):
    PRINT = 0
    CONTROL = 1

class KeyCommands(Enum):
    NEWLINE = 0
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    

class KeyPressEvent(object):
   
    def __init__(self, key_code, key_command):
        self.key_code = key_code
        self.key_command = key_command
        self.tag = self.set_tag(self.key_code)
        self.key_char = None
        if self.tag == KeyTag.PRINT:
            self.key_char = chr(self.key_code)

    def set_tag(self, key_code):
        if 32 <= key_code <= 126:
            return KeyTag.PRINT
        if key_code == 8:
            return KeyTag.PRINT
        return KeyTag.CONTROL



class KeyboardInput(object):
    CAR_RETURN = 13
    NEWLINE = 10
    ARROW_BASE = 224
    ARROW_UP = 72
    ARROW_DOWN = 80
    
    def __init__(self, inp=MsConsoleInput()):
        self._input = inp

    def is_key_down(self):
        return self._input.is_key_pressed()

    def is_key_pressed(self):
        return self._input.is_key_pressed()

    def get_key_pressed(self):
        key_ord = self._input.get_key_pressed()
        command = None
        if key_ord == KeyboardInput.ARROW_BASE:
            key_ord_two = self._input.get_key_pressed()
            command = self.to_command(key_ord, key_ord_two)
        else:
            command = self.to_command(key_ord)
        return KeyPressEvent(key_ord, command)
            
    def to_command(self, k0, k1=None):
        if k0 == KeyboardInput.ARROW_BASE:
            if k1 == KeyboardInput.ARROW_UP:
                return KeyCommands.UP
            if k1 == KeyboardInput.ARROW_DOWN:
                return KeyCommands.DOWN

        if k0 == KeyboardInput.CAR_RETURN:
            return KeyCommands.NEWLINE

        if k1 == KeyboardInput.NEWLINE:
            return KeyCommands.NEWLINE
        return None
