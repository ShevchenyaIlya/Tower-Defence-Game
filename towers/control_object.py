from abc import ABC, abstractmethod


class ButtonObject(ABC):
    def __init__(self):
        self.width = 0
        self.height = 0
        self.icon = 0

    @abstractmethod
    def update(self):
        """Update condition, behavior, position"""

    @abstractmethod
    def draw(self, window):
        """Draw button object"""

    @abstractmethod
    def click(self, x, y):
        """Behavior after clicking button"""


class MenuObject(ABC):
    def __init__(self):
        self.width = 0
        self.height = 0
        self.bg = None
        self.buttons = []

    @abstractmethod
    def draw(self, window):
        """Draw menu with other object placing in menu"""

    @abstractmethod
    def add_btn(self, img, name):
        """Add buttons for the menu"""

    @abstractmethod
    def get_clicked(self, x, y):
        """If menu is active, return clicked button"""
