#!/bin/python3

import math
import sys

# sys.argv[0]   # prints test.py
# sys.argv[1]   # prints var1 

if len(sys.argv) == 2:
    theta = float(sys.argv[1])
    adjacent_leg = 140
elif len(sys.argv) > 2:
    theta = float(sys.argv[1])
    adjacent_leg = float(sys.argv[2])
else:
    theta = 38
    adjacent_leg = 140

# see also: https://docs.python.org/3/library/argparse.html

def width_on_stove(theta, adj):

    alpha_degree = theta / 2
    alpha_radian = alpha_degree * math.pi / 180

    hypothenuse = adjacent_leg / math.cos(alpha_radian)
    opposite_leg = math.sin(alpha_radian) * hypothenuse

    light_width = opposite_leg * 2

    print(f'Lichtkegellänge auf Herd mit {alpha_degree}° Abstrahlwinkel = {light_width} cm')
    return(light_width)


# -- Abstand Herd zur Lampe
width_on_stove(theta, adj=adjacent_leg)


# adjacent_leg = 140
# # -- 36°
# degrees = 36
# width = width_on_stove(degrees, adjacent_leg)
#
# # -- 38°
# degrees = 38
# width = width_on_stove(degrees, adjacent_leg)
#
# # -- 40°
# degrees = 40
# width = width_on_stove(degrees, adjacent_leg)

