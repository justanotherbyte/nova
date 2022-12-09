from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

from ..base import UIBase

if TYPE_CHECKING:
    from state.ui import UIState
    from .view import View
    from ..base import UICallable


class Button(UIBase):
    def __init__(self, state: UIState):
        super().__init__(state)


def button(text: str):
    def decorator(func: UICallable[Button]):
        func.__ui_info__ = {
            "text": text,
            "cls": Button
        }
        print("From decorator", func.__name__)
        return func

    return decorator