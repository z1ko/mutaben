
import sympy as sp
import numpy as np
from pprint import pprint

def get_bits(value, bitsize = 2):
    result = []
    for i in range(bitsize):
        result.append((value >> i) & 0b1)
    return list(reversed(result))


# Rappresenta una generica espressione booleana
class BExpr:
    def __init__(self, text, func, size = 2) -> None:
        self.text = text
        self.func = func
        self.size = size

# Rappresenta una espressione in mixed-boolean-arithmetic   
class MBA:
    def __init__(self) -> None:
        self.elements = []

    def add_term(self, coef: int, expr: BExpr):
        self.elements.append((coef, expr))

    # Visualizza la MBA in un formato leggibile
    def print(self):
        for (coef, expr) in self.elements:
            sign = '-' if coef < 0 else '+'
            print(f"{sign} {abs(coef)} * ({expr.text}) ", end='')
        print("")

    # Valuta la MBA date le variabili
    def evaluate(self, vars):
        res = 0
        for coef, expr in self.elements:
            assert(expr.size == len(vars))
            res += coef * expr.func(vars)
        return res

    # Controlla che la MBA sia un'identità uguale a 0
    def is_zero_identity(self):
        _, bexpr = self.elements[0]
        for bits in [ get_bits(i) for i in range(pow(2, bexpr.size))]:
            if not self.evaluate(bits) == 0:
                return False
        return True


class Generator:
    def __init__(self, exprs) -> None:
        self.exprs = exprs

    # Genera matrice A di analisi
    def matrix(self):
        result = []
        for bexp in self.exprs:
            R = []
            for bits in [ get_bits(i) for i in range(0, pow(2, bexp.size))]:
                R.append(bexp.func(bits))
            result.append(R)

        return sp.Matrix(result) \
            .transpose()

    # Genera array di mba che rappresentano un'identità
    def identities(self, max_coeff = 10, count = 4, check_identity = False):
        res = []

        A = self.matrix()
        nullspace_basis = A.nullspace()
        print(f"Colonne del kernel: {len(nullspace_basis)}")

        for _ in range(count):
            mba = MBA()
            
            # Crea combinazione lineare delle colonne del kernel
            # per generare diverse versioni valide della MBA
            coefs = np.random.randint(max_coeff, size=len(nullspace_basis))
            gmask = np.random.randint(2, size=len(nullspace_basis))
            combination = nullspace_basis[0]
            for i, (coeff, generator) in enumerate(zip(coefs, nullspace_basis)):
                if i != 0 and gmask[i] != 0:
                    combination += coeff * generator
            
            # Utilizza la combinazione per selezionare solo le espressioni
            # con un coefficente diverso da zero
            for i, bexp in enumerate(self.exprs):
                coeff = combination[i]
                if coeff != 0:
                    mba.add_term(coeff, bexp)

            # Test sulle possibili combinazioni booleane di input
            # se queste sono corrette allora anche le combinazioni
            # a più bit lo sono
            if check_identity:
                assert(mba.is_zero_identity())
            
            res.append(mba)
        return res

    # Genera delle MBA che si comportano allo stesso modo rispetto 
    # ad una generica funzione booleana
    def mutate(self, expr: BExpr):
        pass
