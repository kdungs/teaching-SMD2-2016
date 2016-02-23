from . import check as c

from functools import partial
import numpy as np


def is_matrix(m):
    return type(m) is np.matrix


def same_shape(m, n):
    return m.shape == n.shape


def matrix_same(m, n):
    return np.allclose(m, n)


def make_matrix_checker(result):
    return c.compose_many(
        c.lift(is_matrix, 'Input has to be a numpy matrix.'),
        c.lift(partial(same_shape, result),
               'Matrix should have dimension {}.'.format(result.shape)),
        c.lift(partial(matrix_same, result),
               'Numbers are not close to expected result.'))


CHECKERS = {
    '1.1': make_matrix_checker(np.matrix([[0.04, -0.016], [-0.016, 0.01]]))
}


def check_solution(assignment, value):
    checker = CHECKERS.get(assignment)
    if checker is None:
        return 'There is no such assignment.'
    r = checker(value)
    if c.is_fail(r):
        return 'There was a problem with your solution: {}'.format(r.message)
    return 'Correct!'
