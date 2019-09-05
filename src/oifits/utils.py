import datetime

import numpy as np


def _plurals(count):
    if count != 1:
        return "s"
    return ""


def _array_eq(a, b):
    """
    Test whether all the elements of two arrays are equal.

    Parameters
    ----------
    a : ~numpy.ndarray
    b : ~numpy.ndarray
    """
    try:
        return not (a != b).any()
    except:
        return not (a != b)


class _angpoint(float):
    """
    Convenience Class for representing angles.
    """

    def __init__(self, angle):
        self.angle = angle

    def __repr__(self):
        return "_angpoint(%s)" % self.angle.__repr__()

    def __str__(self):
        return "%g degrees" % (self.angle)

    def __eq__(self, other):
        return self.angle == other.angle

    def __ne__(self, other):
        return not self.__eq__(other)

    def asdms(self):
        """Return the value as a string in dms format,
        e.g. +25:30:22.55.  Useful for declination."""
        angle = self.angle
        if angle < 0:
            negative = True
            angle *= -1.0
        else:
            negative = False
        degrees = np.floor(angle)
        minutes = np.floor((angle - degrees) * 60.0)
        seconds = (angle - degrees - minutes / 60.0) * 3600.0
        try:
            if negative:
                return "-%02d:%02d:%05.2f" % (degrees, minutes, seconds)
            else:
                return "+%02d:%02d:%05.2f" % (degrees, minutes, seconds)
        except TypeError:
            return self.__repr__()

    def ashms(self):
        """Return the value as a string in hms format,
        e.g. 5:12:17.21.  Useful for right ascension."""
        angle = self.angle * 24.0 / 360.0

        hours = np.floor(angle)
        minutes = np.floor((angle - hours) * 60.0)
        seconds = (angle - hours - minutes / 60.0) * 3600.0
        try:
            return "%02d:%02d:%05.2f" % (hours, minutes, seconds)
        except TypeError:
            return self.__repr__()
