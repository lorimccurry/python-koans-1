#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Triangle Project Code.

# Triangle analyzes the lengths of the sides of a triangle
# (represented by a, b and c) and returns the type of triangle.
#
# It returns:
#   'equilateral'  if all sides are equal
#   'isosceles'    if exactly 2 sides are equal
#   'scalene'      if no sides are equal
#
# The tests for this method can be found in
#   about_triangle_project.py
# and
#   about_triangle_project_2.py
#
def triangle(a, b, c):
    triangle_list = sorted([a, b, c])
    triangle_set = set(triangle_list)
    if triangle_list[0] <= 0:
        raise TriangleError('All sides of a triangle should be greater than 0.')

    if triangle_list[2] >= triangle_list[0] + triangle_list[1]:
        raise TriangleError('The sum of any two sides should be greater than the third one.')

    if len(triangle_set) == 1:
        return 'equilateral'
    elif len(triangle_set) == 2:
        return 'isosceles'
    else:
        return 'scalene'

# Error class used in part 2.  No need to change this code.
class TriangleError(Exception):
    pass
