from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Callable,
    Any
)

import pygame

if TYPE_CHECKING:
    from core.game import GameCore
    from ui.base import UIBase


RenderPipelineT = tuple[Callable, tuple[Any], dict[str, Any]]

class UIState:
    def __init__(self, core: GameCore):
        self._core = core
        self._loop_pipelines: list[tuple[pygame.Surface, RenderPipelineT]] = []

        self._component_rects: dict[UIBase, pygame.Rect] = {}
        self._component_callbacks: dict[UIBase, Callable[[UIBase]]] = {}

    def register(
        self,
        item: UIBase,
        pipeline: RenderPipelineT,
        callback: Callable[..., None],
        *,
        surface: pygame.Surface | None = None
    ):
        surface = surface or self._core.screen
        rect = self._process_pipeline(pipeline, surface)

        self._component_rects[item] = rect
        self._component_callbacks[item] = callback


    def _process_pipeline(self, pipeline: RenderPipelineT, surface: pygame.Surface) -> pygame.Rect:
        func, args, kwargs = pipeline
        rect = func(surface, *args, **kwargs)
        return rect
        
    def _process_loop(self):
        # render all pipelines
        for pair in self._loop_pipelines:
            surface, pipeline = pair
            self._process_pipeline(pipeline, surface)

    def user_clicked(self):
        x, y = pygame.mouse.get_pos()
        for item, rect in self._component_rects.items():
            if rect.collidepoint(x, y):
                # clicked when mouse is over button
                callback = self._component_callbacks[item]
                callback(item.view, item)
                
    def mouse_moved(self):
        x, y = pygame.mouse.get_pos()
        for item, rect in self._component_rects.items():
            if rect.collidepoint(x, y):
                # hovering
                hover_color = item.props.get("hover_color")
                # not all components will have this property
                if hover_color is not None:
                    ... # render new color
