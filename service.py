
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
    BExpr("-1",      lambda vars: -1), # Ogni bit a 1
    BExpr("1",       lambda vars: 1)   # Ultimo bit a 1
]

x = BExpr("x", lambda vars: vars[0])
y = BExpr("y", lambda vars: vars[1])

if __name__ == "__main__":
    terms = []
    
    linear_comb_text = input("Inserisci la combinazione lineare di x e y da mutare:\n\t")
    linear_comb_text = linear_comb_text.strip()
    
    matches = re.findall("([+-]*[0-9]*)(?:\*)*([a-z]+)", linear_comb_text)
    for coef, var in matches:
        
        if coef == '+' or coef == '': 
            coef = '+1'
        elif coef == '-': 
            coef = '-1'

        var = x if var == 'x' else y
        terms.append((int(coef), var))


    gen = MBAGenerator(EXPRS)
    mba = gen.mutate_affine(terms, 0)
    
    print("\nGenerated MBA expression:\n")
    mba.print()

    print("\nRanom sampling of results:\n")
    for i in range(10):
        vars = np.random.randint(0, 10001, size=2)
        res1 = str(evaluate_affine(vars, terms, 0))
        res2 = str(mba.evaluate(vars))

        print(f"\tinput: {res1:>10}, mba: {res2:>10} --> ", end='')
        if (res1 == res2):
            print("Correct!")
        else:
            print("ERROR!")
            exit(1)