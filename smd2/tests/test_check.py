import check as c
import unittest


def is_positive(x):
    return x > 0


def is_even(x):
    return not x & 1


check_positive = c.lift(is_positive, 'Number has to be positive.')
check_even = c.lift(is_even, 'Number has to be even.')
check_evenpositive = c.compose(check_even, check_positive)


class TestCheck(unittest.TestCase):
    def test_return(self):
        x = c.return_(42)
        self.assertTrue(c.is_pass(x))
        self.assertEqual(x.value, 42)

    def test_lift(self):
        x = check_positive(-5)
        y = check_positive(5)
        self.assertTrue(c.is_fail(x))
        self.assertEqual(x.message, 'Number has to be positive.')
        self.assertTrue(c.is_pass(y))
        self.assertEqual(y.value, 5)

    def test_compose(self):
        x = check_evenpositive(1)
        y = check_evenpositive(2)
        z = check_evenpositive(-1)
        w = check_evenpositive(-2)

        self.assertTrue(c.is_fail(x))
        self.assertEqual(x.message, 'Number has to be even.')
        self.assertTrue(c.is_pass(y))
        self.assertEqual(y.value, 2)
        self.assertTrue(c.is_fail(z))
        self.assertEqual(z.message, 'Number has to be even.')
        self.assertTrue(c.is_fail(w))
        self.assertEqual(w.message, 'Number has to be positive.')
