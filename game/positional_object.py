from abc import ABC, abstractmethod


class PositionalObject(ABC):
    @abstractmethod
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.img = None

    @abstractmethod
    def draw(self, window):
        """Draw positional object"""

    @abstractmethod
    def collide(self, instance):
        """Behavior in collision of different positional objects"""
