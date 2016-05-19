__author__ = 'zwan145'
from passive_mechanics import *


def average_stress_strain_elem(filename, component):
    # Read in strain data for optimised solution and evaluate averaged strain per element.
    passive_loop_index()
