from abc import abstractmethod


class Controller:
    @abstractmethod
    def on_key_press(self, key):
        pass

    @abstractmethod
    def on_mouse_press(self, pos):
        pass

    @abstractmethod
    def on_mouse_release(self, pos):
        pass

    @abstractmethod
    def on_mouse_move(self, pos):
        pass

    @abstractmethod
    def update(self, timepassed):
        pass

    @abstractmethod
    def draw(self, display):
        pass
