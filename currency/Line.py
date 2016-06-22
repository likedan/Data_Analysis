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

    def get_y(self, x):
        return float(x) * self.slope + self.intercept
    
    def get_x(self, y):
        return (float(y) - self.intercept) / self.slope

    def point_on_line(self, x, y, tolerance):
        x = float(x)
        y = float(y)
        if abs(y - self.get_y(x)) > tolerance:
            return False
        return True