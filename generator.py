
import sympy as sp
import numpy as np

from pprint import pprint

from bexpr import BExpr, MBAExpr
import utils

class MBAGenerator:
    def __init__(self, exprs) -> None:
        self.exprs = exprs

    # Genera matrice A di analisi
    def matrix(self):
        result = []
        for bexp in self.exprs:
            R = []
            for bits in utils.get_bits_seq(pow(2, bexp.size)):
                R.append(bexp.func(bits))
            result.append(R)

        return sp.Matrix(result) \
            .transpose()

    # Genera array di mba che rappresentano un'identità
    def identities(self, max_coeff = 10, count = 4, check_identity = False):
        res = []

        A = self.matrix()
        kernel_basis = A.nullspace()
        for _ in range(count):
            mba = MBAExpr()
            
            # Crea combinazione lineare delle colonne del kernel
            # per generare diverse versioni valide della MBA
            coefs = np.random.randint(max_coeff, size=len(kernel_basis))
            gmask = np.random.randint(2, size=len(kernel_basis))
            combination = kernel_basis[0]
            for i, (coeff, generator) in enumerate(zip(coefs, kernel_basis)):
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
