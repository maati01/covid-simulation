from time import sleep

import arcade

from GUI.gui import GUI

PATH_TO_BINARY_ARRAY = "data/binary_array.npy"


class Engine:
    def __init__(self):
        self.is_running = True
        self.gui = GUI(PATH_TO_BINARY_ARRAY)
        arcade.run()
