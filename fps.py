import pygame


class Fps:
    """Counts the framerate"""

    def __init__(self):
        """
        Default constructor

        :param framerate: Maximum framerate.
        """
        self.second_accumulator = 0
        self.frame_accumulator = 0
        self.framerate = 0

    def get(self, clock):
        """
        Get the current framerate

        :returns: the current framerate (int)
        """
        self.second_accumulator += clock.get_time()
        self.frame_accumulator += 1
        if self.second_accumulator >= 1000:
            self.framerate = self.frame_accumulator
            self.second_accumulator = 0
            self.frame_accumulator = 0

        return self.framerate


fps = Fps()