from time import sleep

import arcade

from GUI.gui import GUI


class Engine:
    def __init__(self):
        self.is_running = True
        self.gui = GUI("data/map.png")
        arcade.run()

