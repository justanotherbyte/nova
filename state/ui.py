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
        self._pipelines: dict[UIBase, RenderPipelineT] = {}

        self._component_rects: dict[UIBase, pygame.Rect] = {}
        self._component_callbacks: dict[UIBase, Callable[[UIBase], None]] = {}

        self._hot_items: list[UIBase] = [] # items are considered "hot" when they need to be passed
        # into the item arg in _process_pipeline

    def register(
        self,
        item: UIBase,
        pipeline: RenderPipelineT,
        callback: Callable[..., None],
        *,
        surface: pygame.Surface | None = None
    ):
        surface = surface or self._core.screen # type: ignore
        rect = self._process_pipeline(pipeline, surface) # type: ignore

        self._component_rects[item] = rect
        self._component_callbacks[item] = callback
        self._pipelines[item] = pipeline

    def _process_pipeline(self, pipeline: RenderPipelineT, surface: pygame.Surface, item: UIBase | None = None) -> pygame.Rect:
        if item is not None:
            pipeline = item.render()
        func, args, kwargs = pipeline
        rect = func(surface, *args, **kwargs)
        return rect
        
    def _process_loop(self):
        # render all pipelines
        for item, pipeline in self._pipelines.items():
            if item in self._hot_items:
                self._process_pipeline(pipeline, self._core.screen, item) # type: ignore
            else:
                self._process_pipeline(pipeline, self._core.screen) # type: ignore

    def user_clicked(self):
        x, y = pygame.mouse.get_pos()
        for item, rect in self._component_rects.items():
            if rect.collidepoint(x, y):
                # clicked when mouse is over button
                callback = self._component_callbacks[item]
                callback(item.view, item) # type: ignore
                
    def mouse_moved(self):
        # print("mouse moved")
        x, y = pygame.mouse.get_pos()
        for item, rect in self._component_rects.items():
            if rect.collidepoint(x, y):
                # hovering
                self._hot_items.append(item)
                item.register_action("hovering", True)
            else:
                try:
                    self._hot_items.remove(item)
                except ValueError:
                    pass
                item.register_action("hovering", False)
