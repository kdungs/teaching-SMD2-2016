""" Define a Check monad and corresponding functions.
"""
from functools import (reduce, partial)


class Check:
    """ This super class is not really necessary but helps make the structure
        clear.

        data Check a = Pass a | Fail Message
    """
    pass


class Pass(Check):
    def __init__(self, value):
        self.value = value


class Fail(Check):
    def __init__(self, message):
        self.message = message


def is_(t, x):
    """ Check whether the type of a given x is a given type t.
    """
    return type(x) is t


is_check = partial(is_, Check)
is_pass = partial(is_, Pass)
is_fail = partial(is_, Fail)


def return_(x):
    """ Monadic return for the Check monad.
        return :: a -> m a

        return = Pass
    """
    return Pass(x)


def bind(f):
    """ Monadic bind for the Check monad.
        (>>=) :: m a -> (a -> m b) -> m b

        Fail x >>= f = Fail x
        Pass x >>= f = f x
    """
    def bind_impl(x):
        if is_fail(x):
            return x
        if is_pass(x):
            return f(x.value)
        raise ValueError('Check has to be of type Pass | Fail.')

    return bind_impl


def compose(f, g):
    """ Kleisli composition of two (Check-)monadic functions f and g.
        (>=>) :: (a -> m b) -> (b -> m c) -> (a -> m c)
    """
    def compose_impl(x):
        return bind(g)(f(x))

    return compose_impl


def compose_many(*fs):
    """ Reduces a variable number of functions with composition.
        Same as repeatedly calling `compose` on pairs.
    """
    return reduce(compose, fs)


def lift(f, message):
    """ Lifts a boolean function into the realm of the Check monad.
        lift :: (a -> bool) -> (a -> Check a)
    """
    def lift_impl(x):
        if f(x):
            return return_(x)
        return Fail(message)

    return lift_impl
