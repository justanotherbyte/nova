import threading
import sys

import pygame
import requests

import ui
from state.ui import UIState


class GameCore:
    SCREEN_WIDTH = 0
    SCREEN_HEIGHT = 0
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
        elif _type == pygame.MOUSEBUTTONDOWN:
            self._ui_state.user_clicked()

    def run(self):
        ui_state = self._ui_state
        class TestView(ui.View):
            def __init__(self):
                layout = ui.LayoutInfo(
                    "vertical",
                    10
                )
                super().__init__(ui_state, layout)

            @ui.button(
                text="Hello",
                color=(255, 0, 0),
                size=(60, 30)
            )
            def btn_callback(self, btn):
                print("Clicked")

            @ui.button(
                text="Hello 2",
                color=(0, 0, 255),
                size=(60, 30)
            )
            def btn_callback_2(self, btn):
                print("Clicked, 2")

        view = TestView()
        view.render((30, 30))
            
        while not self._ev.is_set():
            self._clock.tick(self.__fps)
            pygame.display.update()

            events = pygame.event.get()
            for event in events:
                self._handle_event(event)

            self._ui_state._process_loop()

        pygame.quit()
        sys.exit(0)
