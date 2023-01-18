
import sympy as sp
import numpy as np

import random as rnd
from pprint import pprint

# Genera bits da un intero
def get_bits(value, bitsize = 2):
    result = []
    for i in range(bitsize):
        result.append((value >> i) & 0b1)
    return list(reversed(result))

# Genera matrice A da una serie di espressioni booleane e un numero di variabili
def gen_A(bexprs, vars_num = 2):
    A = []
    for bexp in bexprs:
        R = []
        for bits in [ get_bits(i) for i in range(0, pow(2, vars_num))]:
            R.append(bexp[0](bits))
        A.append(R)
    return sp.Matrix(A).transpose()


def calculate(MBA, bits):
    res = 0
    for (coeff, bexp) in MBA:
        res += coeff * bexp[0](bits)
    return res

def mba_print(MBA):
    for (coeff, bexp) in MBA:
        sign = '-' if coeff < 0 else '+'
        print(f"{sign} {abs(coeff)} * ({bexp[1]}) ", end='')

# Controlla che la MBA sia un'identità
def assert_identity(MBA):
    for bits in [ get_bits(i) for i in range(pow(2, VARS_NUM))]:
        assert(calculate(MBA, bits) == 0)

# Estrae termini dalla MBA
def extract(MBA, terms):
    sol = []
    eeq = []
    for (coeff, bexp) in MBA:
        found = False
        for term in terms:
            if bexp[1] == term[1] and coeff == term[0]:
                found = True
                break

        if found:
            sol.append((-coeff, bexp))
        else:
            eeq.append((coeff, bexp))

    return sol, eeq


# Numero di variabili
VARS_NUM = 2
# Numero di espressioni booleane
BEXP_NUM = 4

BEXPS = [
    (lambda vars: vars[0], "x"), # Identità di x
    (lambda vars: vars[1], "y"), # Identità di y
    (lambda vars: vars[0] & vars[1],   "x & y"),
    (lambda vars: vars[0] | ~vars[1],  "x | ~y"),
    (lambda vars: vars[0] ^ vars[1],   "x ^ y"),
    (lambda vars: ~vars[0] & ~vars[1], "~x & ~y"),
    (lambda vars: ~vars[0], "~x"),
    (lambda vars: ~vars[1], "~y"),
    (lambda vars: ~vars[0] ^ ~vars[1], "~x ^ ~y"),
    (lambda vars: 1, "1")
]

A = gen_A(BEXPS)
pprint(A)

# ============================================================
# IDENTITA'

print("Identità trovate:")
for generator in A.nullspace():
    
    MBA = []
    for i, bexp in enumerate(BEXPS):
        coeff = generator[(i, 0)]
        if coeff != 0:
            MBA.append((coeff, bexp))

    assert_identity(MBA)

    print("\t0 == ", end='')
    mba_print(MBA)
    print("")

    vars, terms = extract(MBA, [(-1, "x"), (-1, "y")])
    if len(vars) == 2:
        print("\tRegola di riscrittura per x + y: ", end='')
        mba_print(terms)
        print("")


exit(0)

# ============================================================
# ESPRESSIONI LOGICHE GENERICHE

# Funzione logica da rappresentare come MBA lineare
f = (lambda vars: ~(vars[0] & ~vars[1]) | (~vars[0] ^ vars[1]), "~(x & ~y) | (~x ^ y)")

# Ottiene rappresentazione binaria della funzione f
# F = [
#   f(00)
#   f(01)
#   f(10)
#   f(11)
# ]
F = sp.zeros(pow(2, VARS_NUM), 1)
for input in range(pow(2, VARS_NUM)):
    F[input] = (f[0])(get_bits(input))
#pprint(F)

#x = A.LDLsolve(F)
#pprint(x)
#exit(0)

# Pseudo inversa
K = A.pinv()

# Controlla che esistano soluzioni
assert(A * K * F == F)

w = sp.Matrix(8, 1, [0, 1, 0, 1, 0, 1, 0, 1])
x = K * F + (sp.eye(8, 8) - K * A) * w
# pprint(x)

# Ottiene una forma migliore della MBA
g = sp.gcd([ e for e in x[:, 0]])
x = x * (1 / g)
# pprint(x)

MBA = []
for i, bexp in enumerate(BEXPS):
    coeff = x[(i, 0)]
    if coeff != 0:
        MBA.append((coeff, bexp))

# Visualizza MBA

print("Conversione di funzioni logiche:")
print(f"\t[ {f[1]} ] <=> [ ", end='')
for (coeff, bexp) in MBA:
    sign = '-' if coeff < 0 else '+'
    print(f"{sign} {abs(coeff)} * ({bexp[1]}) ", end='')
print("]")


# Controlla che il risultato sia uguale per f è la mba lineare
for bits in [ get_bits(i) for i in range(pow(2, VARS_NUM))]:
    res1 = f[0](bits)
    res2 = calculate(MBA, bits)
    if res1 != res2:
        print(f"Failed check at {bits}, f = {res1}, mba = {res2}")
        exit(-1)

# Controlla per valori superiori a 2
for i in range(100):
    values = np.random.randint(1, 100, 2)
    # print(f"check {values}")
    assert(f[0](values) == calculate(MBA, values))

# ============================================================
# ESPRESSIONI AFFINI GENERICHE