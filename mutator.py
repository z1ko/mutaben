
import re
import numpy as np
from generator import MBAGenerator
from bexpr import BExpr, evaluate_affine

class Mutator:
    def __init__(self, exprs) -> None:
        self.generator = MBAGenerator(exprs)

        # TODO: Make more versatile
        self.x = BExpr("x", lambda vars: vars[0])
        self.y = BExpr("y", lambda vars: vars[1])


    # Returns a muated version of the affine expr. provided
    # works only for x and y
    def rewrite(self, expr_string: str) -> str:

        vars = { }
        offset = 0

        expr_string = expr_string.strip().replace(" ", "")
        matches = re.findall("([+-]*)([0-9]*)([a-z]{0,1})", expr_string)        
        for i in range(len(matches) - 1):
            m_sign, m_coef, m_var = matches[i]

            # Skip empty matches
            if m_sign == '' and m_coef == '' and m_var == '':
                continue

            sign = 1 if m_sign != '-' else -1
            coef = 1 if m_coef == ''  else int(m_coef)

            # Offset
            if m_var == '':
                offset += sign * coef
                continue

            if not m_var in vars:
                vars[m_var] = 0
        
            vars[m_var] += sign * coef

        terms = [
            (vars['x'], self.x),
            (vars['y'], self.y)
        ]

        mba = self.generator.mutate_affine(terms, offset)
        return mba

