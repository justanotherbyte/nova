from __future__ import annotations

import inspect
from typing import TYPE_CHECKING

import pygame

from ..base import UIBase, LayoutInfo

if TYPE_CHECKING:
    from state.ui import UIState


class View(UIBase):
    def __init__(self, state: UIState, layout: LayoutInfo):
        self._state = state

        self.children: list[UIBase] = []
        self.layout = layout

        for _, item in inspect.getmembers(self):
            ui_info = getattr(item, "__ui_info__", None)
            if ui_info is not None:
                _cls = ui_info["cls"]
                callback = ui_info["callback"]
                props = ui_info["props"]
                item = _cls(self._state, callback, props)
                self.add_item(item)

    def add_item(self, item: UIBase):
        if item in self.children:
            raise ValueError("Component already attached to view")
        
        item.set_view(self)
        self.children.append(item)

    def render(self, position: tuple[float, float]):
        for child in self.children:
            size = child.props["size"]
            pos = self.layout.correct(position, size)
            child.render(pos)

        self.layout.clear()
