from abc import ABCMeta, abstractmethod


class ILocation(metaclass=ABCMeta):
    @abstractmethod
    def get_position(self):
        """Bring the location of object in window"""
        pass
