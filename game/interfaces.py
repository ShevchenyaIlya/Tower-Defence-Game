from abc import ABCMeta, abstractmethod


class ILocation:
    @abstractmethod
    def get_position(self):
        """Bring the location of object in window"""
        pass


class IMovable:
    @abstractmethod
    def move(self):
        """Realizes in classes that have ability to change position by moving"""
        pass


class IUpgradable:
    @abstractmethod
    def upgrade(self):
        """Change basic behavior of object throw upgraiding it"""
        pass
