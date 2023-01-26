
import re
import numpy as np
from generator import MBAGenerator
from bexpr import BExpr, evaluate_affine

# TODO: Trova un modo per inserirle dinamicamente
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

x = BExpr("x", lambda vars: vars[0])
y = BExpr("y", lambda vars: vars[1])

regex_1 = "([+-]*)([0-9]*)([a-z]{0,1})"
regex_2 = "([+-]*[0-9]*)(?:\*)*([a-z]+)"

if __name__ == "__main__":

    linear_comb_text = input("Inserisci la combinazione affine di x e y da mutare:\n\n\t")
    linear_comb_text = linear_comb_text.strip()
    
    affine_offset = 0
    
    vars = {}
    matches = re.findall(regex_1, linear_comb_text)
    for i in range(len(matches) - 1):
        m_sign, m_coef, m_var = matches[i]

        # Skip empty matches
        if m_sign == '' and m_coef == '' and m_var == '':
            continue

        sign = 1 if m_sign != '-' else -1
        coef = 1 if m_coef == ''  else int(m_coef)

        # Offset
        if m_var == '':
            affine_offset += sign * coef
            continue

        if not m_var in vars:
            vars[m_var] = 0
    
        vars[m_var] += sign * coef


    # For now allow only x and y
    terms = [
        (vars['x'], x),
        (vars['y'], y)
    ]

    gen = MBAGenerator(EXPRS)
    mba = gen.mutate_affine(terms, affine_offset)
    
    print("\nGenerated MBA expression:\n")
    mba.print()

    print("\nRanom sampling of results:\n")
    for i in range(10):
        vars = np.random.randint(0, 10001, size=2)
        res1 = str(evaluate_affine(vars, terms, affine_offset))
        res2 = str(mba.evaluate(vars))

        print(f"\tinput: {res1:>10}, mba: {res2:>10} --> ", end='')
        if (res1 == res2):
            print("Correct!")
        else:
            print("ERROR!")
            exit(1)