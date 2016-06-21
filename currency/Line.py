from DefaultVariables import *
import os, sys, os
import datetime

class Line:
    def __init__(self, x1, y1, x2, y2):
        if x1 == x2:
            raise Exception("two point of same x")
        x1 = float(x1)
        x2 = float(x2)
        y1 = float(y1)
        y2 = float(y2)
        self.slope = (y2-y1) / (x2-x1)
        self.intercept = y1 - self.slope * x1

    def point_on_line(self, x, y, tolerance):
        if abs(y - (self.slope * x + self.intercept)) > tolerance:
            return False
        return True