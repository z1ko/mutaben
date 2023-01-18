
import unittest as ut
import numpy as np

from mba import *

# Test boolean expression used in the generator
EXPRS = [
    BExpr("x",       lambda vars: vars[0]),
    BExpr("y",       lambda vars: vars[1]),
    BExpr("x & y",   lambda vars: vars[0] & vars[1]),
    BExpr("x | ~y",  lambda vars: vars[0] | ~vars[1]),
    BExpr("x ^ y",   lambda vars: vars[0] ^ vars[1]),
    BExpr("~x & ~y", lambda vars: ~vars[0] & ~vars[1]),
    BExpr("~x",      lambda vars: ~vars[0]),
    BExpr("~y",      lambda vars: ~vars[1]),
    BExpr("~x ^ ~y", lambda vars: ~vars[0] ^ ~vars[1]),
    BExpr("1",       lambda vars: 1)
]

class TestMBAGenerator(ut.TestCase):
    def test_zero_identities(self):
        
        GEN_MAX_COEFF = 100000
        GEN_MBA_COUNT = 10
        RNG_STO_COUNT = 100
        RNG_MAX_INPUT = 10000
        
        generator = Generator(EXPRS)
        for identity in generator.identities(max_coeff=GEN_MAX_COEFF, count=GEN_MBA_COUNT, check_identity=False):
            self.assertTrue(identity.is_zero_identity())

            # Controllo stocastico con valori interi
            for _ in range(RNG_STO_COUNT):
                vars = np.random.randint(RNG_MAX_INPUT, size=2)
                self.assertEqual(0, identity.evaluate(vars))


if __name__ == "__main__":
    ut.main()