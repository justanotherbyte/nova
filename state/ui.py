from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from core.game import GameCore


class UIState:
    def __init__(self, core: GameCore):
        self._core = core
        self._displaying: dict[pygame.Surface, tuple[float, float]] = {}

    def register(
        self,
        surface: pygame.Surface,
        position: tuple[float, float],
        /,
        blit: bool = False
    ):
        self._displaying[surface] = position
        
        if blit:
            self._core.screen.blit(surface, position)
        