
import unittest as ut
import numpy as np
import sympy as sp

from generator import MBAGenerator
from bexpr import BExpr, evaluate_affine

# Test boolean expression used in the generator
EXPRS = [
    BExpr("x",       lambda vars:  vars[0]),
    BExpr("y",       lambda vars:  vars[1]),
    BExpr("x & y",   lambda vars:  vars[0] &  vars[1]),
    BExpr("x | ~y",  lambda vars:  vars[0] | ~vars[1]),
    BExpr("x ^ y",   lambda vars:  vars[0] ^  vars[1]),
    BExpr("~x & ~y", lambda vars: ~vars[0] & ~vars[1]),
    BExpr("~x",      lambda vars: ~vars[0]),
    BExpr("~y",      lambda vars: ~vars[1]),
    BExpr("~x ^ ~y", lambda vars: ~vars[0] ^ ~vars[1]),
    BExpr("1",       lambda vars: 1)
]

class TestLibrary(ut.TestCase):

    # Controlla che le identità generate siano corrette
    def test_generator_identities(self):
        
        GEN_MAX_COEFF = 100000
        GEN_MBA_COUNT = 10
        RNG_STO_COUNT = 100
        RNG_MAX_INPUT = 10000
        
        generator = MBAGenerator(EXPRS)
        for identity in generator.identities(max_coeff=GEN_MAX_COEFF, count=GEN_MBA_COUNT, check_identity=False):
            self.assertTrue(identity.is_zero_identity())

            # Controllo stocastico con valori interi
            for _ in range(RNG_STO_COUNT):
                vars = np.random.randint(RNG_MAX_INPUT, size=2)
                self.assertEqual(0, identity.evaluate(vars))


    # Controlla che le mutazioni siano corrette
    def test_generator_mutate(self):
        generator = MBAGenerator(EXPRS)

        expr = BExpr("...", lambda bits: (~bits[0] & ~bits[1]) | (bits[0] & bits[1]))
        for i in range(10):
            mba = generator.mutate(expr)
            self.assertTrue(mba.is_mutation(expr))


    # Controlla che le mutazioni di combinazioni lineari siano corrette
    def test_generator_mutate_linear(self):
        generator = MBAGenerator(EXPRS)
        terms = [
            (4, BExpr("", lambda vars:  vars[0] ^ ~vars[1])),
            (6, BExpr("", lambda vars: ~vars[0] |  vars[1])),
            (9, BExpr("", lambda vars: ~vars[0] & ~vars[1]))
        ]
    
        for i in range(100):
            mba = generator.mutate_affine(terms, 0)
            mba.print()

            vars = np.random.randint(0, 1001, size=2)
            self.assertTrue(mba.evaluate(vars) == evaluate_affine(vars, terms, 0))

    
    # Controllo mutazione su somme semplice di variabili
    def test_generator_mutate_linear_simple(self):
        generator = MBAGenerator(EXPRS)
        terms = [
            (1, BExpr("x", lambda vars: vars[0])),
            (1, BExpr("y", lambda vars: vars[1])),
        ]

        for i in range(100):
            mba = generator.mutate_affine(terms, 0)
            mba.print()

            vars = np.random.randint(0, 1001, size=2)
            self.assertTrue(mba.evaluate(vars) == vars[0] + vars[1])





if __name__ == "__main__":
    ut.main()