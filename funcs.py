import numpy as np
import math
def distance(pt1,pt2):
    p1 = np.array(pt1)
    p2 = np.array(pt2)
    p3 = p2 - p1
    p4 = math.hypot(p3[0], p3[1])
    return p4