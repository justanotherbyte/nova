from __future__ import annotations

from uuid import uuid4
from typing import (
    TYPE_CHECKING,
    Callable,
    TypeVar
)

if TYPE_CHECKING:
    from state.ui import UIState
    from components.view import View


class LayoutInfo:
    def __init__(
        self,
        orientation: str,
        padding: float,
        spacing: float
    ):
        self.orientation = orientation
        self.padding = padding
        self.spacing = spacing

class UIBase:
    def __init__(self, state: UIState):
        self.state = state
        self.item_id = str(uuid4())

        self._view: View | None = None

    def __eq__(self, __o: object) -> bool:
        try:
            return __o.item_id == self.item_id
        except AttributeError:
            return False

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} "
            f"item_id={self.item_id!r}>"
        )

    @property
    def view(self) -> View:
        self._view

    def set_view(self, view: View):
        self._view = view


T = TypeVar("T", bound=UIBase)
UICallable = Callable[[T], None]
