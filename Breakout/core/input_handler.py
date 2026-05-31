import pygame
from dataclasses import dataclass, field
from typing import Set


@dataclass
class InputSnapshot:
    keys_down: Set[int] = field(default_factory=set)
    keys_pressed: Set[int] = field(default_factory=set)   # apenas neste frame
    quit: bool = False
    mouse_x: int = 0


class InputHandler:
    def __init__(self) -> None:
        self._snapshot = InputSnapshot()

    def process(self) -> InputSnapshot:
        pressed_this_frame: Set[int] = set()
        quit_flag = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_flag = True
            elif event.type == pygame.KEYDOWN:
                pressed_this_frame.add(event.key)

        keys = pygame.key.get_pressed()
        held: Set[int] = {k for k in range(len(keys)) if keys[k]}
        mouse_x, _ = pygame.mouse.get_pos()

        self._snapshot = InputSnapshot(
            keys_down=held,
            keys_pressed=pressed_this_frame,
            quit=quit_flag,
            mouse_x=mouse_x,
        )
        return self._snapshot

    @property
    def snapshot(self) -> InputSnapshot:
        return self._snapshot
