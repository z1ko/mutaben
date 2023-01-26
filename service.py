
import re
import numpy as np
from generator import MBAGenerator
from bexpr import BExpr, evaluate_affine
from mutator import Mutator

# TODO: Trova un modo per inserirle dinamicamente
EXPRS = [
    BExpr("x",              lambda vars: vars[0]),
    BExpr("y",              lambda vars: vars[1]),
    BExpr("x & y",          lambda vars: vars[0] & vars[1]),
    BExpr("x | (~y)",       lambda vars: vars[0] | ~vars[1]),
    BExpr("x ^ y",          lambda vars: vars[0] ^ vars[1]),
    BExpr("(~x) & (~y)",    lambda vars: ~vars[0] & ~vars[1]),
    BExpr("~x",             lambda vars: ~vars[0]),
    BExpr("~y",             lambda vars: ~vars[1]),
    BExpr("(~x) ^ (~y)",    lambda vars: ~vars[0] ^ ~vars[1]),
    BExpr("1",              lambda vars: 1)
]


if __name__ == "__main__":
    mutator = Mutator(EXPRS)

    expr_text = input("Inserisci la combinazione affine di x e y da mutare:\n\n\t")
    count = int(input("\nQuante vuoi crearne? "))

    print("\nEspressione MBA generate:\n")
    for i in range(count):

        mba = mutator.rewrite(expr_text)
        print(mba.as_string())
