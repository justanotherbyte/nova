from __future__ import annotations

from typing import (
    TYPE_CHECKING,
    Callable,
    Any
)

import pygame

from ..base import UIBase

if TYPE_CHECKING:
    from state.ui import UIState
    from ..base import UICallable


class Button(UIBase):
    def __init__(self, state: UIState, callback: Callable[["Button"], None], props: dict[str, Any]):
        super().__init__(state, callback, props)

    def render(self, position: tuple[float, float] | None = None):
        if position is not None:
            self.register_pos(position)
        else:
            position = self.previous_position
        
        hover = self.actions.get("hovering", False)
        hover_color = self.props["hover_color"]

        props = self.props
        size_x, size_y = props["size"]
        color = props["color"]

        if hover is True:
            color = hover_color

        border_radius = props["border_radius"]

        assert position is not None

        x, y = position
        pipeline = (
            pygame.draw.rect,
            (
                color,
                pygame.Rect(x, y, size_x, size_y)
            ),
            {"border_radius": border_radius}
        )
        if hover is False:
            self.state.register(
                self,
                pipeline, # type: ignore
                self.callback
            )
        return pipeline

def button(
    *,
    text: str,
    size: tuple[float, float],
    color: tuple[int, int, int],
    border_radius: int = -1,
    hover_color: tuple[int, int, int] | None = None
):
    def decorator(func: UICallable[Button]):
        func.__ui_info__ = {
            "cls": Button,
            "callback": func,
            "props": {
                "text": text,
                "size": size,
                "color": color,
                "border_radius": border_radius,
                "hover_color": hover_color or color
            }
        }
        return func

    return decorator

# @ui.button("Hello there")
# def method(self, button: Button):
#   ## callback