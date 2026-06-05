from abc import ABC, abstractmethod


class MovementStrategy(ABC):

    @abstractmethod
    def move(self, enemy):
        pass
