from __future__ import annotations

from uuid import uuid4
from typing import (
    TYPE_CHECKING,
    Callable,
    TypeVar,
    Any
)

import pygame

if TYPE_CHECKING:
    from state.ui import UIState
    from components.view import View


class LayoutInfo:
    def __init__(
        self,
        orientation: str,
        spacing: float,
        /,
        padding: float = 0
    ):
        if orientation not in {"horizontal", "vertical"}:
            raise ValueError("orientation must be either 'horizontal' or 'vertical'")

        self.orientation = orientation
        self.padding = padding
        self.spacing = spacing
        
        self.__previous_pos: tuple[float, float] | None = None

    def correct(self, position: tuple[float, float], size: tuple[float, float]) -> tuple[float, float]:
        if self.__previous_pos is None:
            # first child, no change required
            self.__previous_pos = position
            return position

        orientation = self.orientation
        spacing = self.spacing

        self.__previous_pos = position

        pos_x, pos_y = position
        size_x, size_y = size
        
        if orientation == "horizontal":
            bottom_x = pos_x + size_x
            pos_x = bottom_x + spacing

        if orientation == "vertical":
            bottom_y = pos_y + size_y
            pos_y = bottom_y + spacing

        return (pos_x, pos_y)

    def clear(self):
        self.__previous_pos = None

        

class UIBase:
    def __init__(self, state: UIState, callback: Callable, props: dict[str, Any]):
        self.state = state
        self.callback = callback
        self.item_id = uuid4().hex
        self.props = props

        self.actions: dict[str, Any] = {}
        self.previous_position: tuple[float, float] | None = None

        self._view: View | None = None

    def register_action(self, action: str, value: Any):
        self.actions[action] = value
        # print(self.actions)

    def register_pos(self, pos: tuple[float, float]):
        self.previous_position = pos

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} "
            f"callback={self.callback!r} "
            f"item_id={self.item_id!r}>"
        )
    
    def __eq__(self, __o: object) -> bool:
        try:
            return __o.item_id == self.item_id # type: ignore
        except AttributeError:
            return False

    def __hash__(self) -> int:
        return hash(self.item_id)

    def render(self, position: tuple[float, float] | None = None):
        raise NotImplementedError

    @property
    def view(self) -> View | None:
        self._view

    def set_view(self, view: View):
        self._view = view


T = TypeVar("T", bound=UIBase)
UICallable = Callable[[T], None]
