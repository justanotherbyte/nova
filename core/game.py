import threading
import sys
import tkinter

import pygame
import requests

from state.ui import UIState
from ui.components.button import Button


_root = tkinter.Tk()
width, height = _root.winfo_screenwidth(), _root.winfo_screenheight()
_root.destroy()

class GameCore:
    SCREEN_WIDTH = width
    SCREEN_HEIGHT = height
    DEFAULT_FPS = 60

    def __init__(self):
        pygame.init()
        
        self._ev = threading.Event()
        self._ev.clear()

        self._clock = pygame.time.Clock()
        self.__fps = self.DEFAULT_FPS

        screen_size = (self.SCREEN_WIDTH, self.SCREEN_WIDTH)
        self.screen = pygame.display.set_mode(screen_size)
        
        pygame.display.set_caption("Game")
        
        self.screen.fill((220, 220, 220))

        self._http = requests.Session()

        # state
        self._ui_state = UIState(self)

        game_icon = pygame.image.load("assets/images/icon_round.png").convert()
        pygame.display.set_icon(game_icon)

    def _handle_event(self, event: pygame.event.Event):
        _type = event.type
        if _type == pygame.QUIT:
            self._ev.set()

    def run(self):
        while not self._ev.is_set():
            self._clock.tick(self.__fps)
            pygame.display.update()

            events = pygame.event.get()
            for event in events:
                self._handle_event(event)

        pygame.quit()
        sys.exit(0)