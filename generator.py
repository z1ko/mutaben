
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
        A = self.matrix()

        # Genera vettore binario di risposta all'input
        b = sp.zeros(pow(2,expr.size), 1)
        for i, bits in enumerate(utils.get_bits_seq(pow(2, expr.size))):
            b[i] = expr.func(bits)

        # Genera simboli per ogni espressioni booleana utilizzabile
        symbols = []
        for i in range(len(self.exprs)):
            symbols.append(sp.symbols("e%d" % i))

        # Risolve sistema indeterminato, ottenendo uno spazio delle soluzioni
        solution = sp.linsolve((A, b), symbols).args[0]
        
        # Ottiene soluzione randomica
        coef = np.random.randint(10, size=len(self.exprs))
        subs = [ ("e%d" % i, coef[i]) for i in range(len(self.exprs))]
        solution = solution.subs(subs)
        #print(solution)

        # Genera MBA
        mba = MBAExpr()
        for i, bexp in enumerate(self.exprs):
            coeff = solution[i]
            if coeff != 0:
                mba.add_term(coeff, bexp)

        assert(mba.is_mutation(expr))
        return mba

    # Genera una MBA che simula una combinazione affine
    def mutate_affine(self, terms, offset):
        A = self.matrix()

        # Genera vettore binario di risposta all'input
        b = sp.zeros(pow(2, terms[0][1].size), 1)
        for i, bits in enumerate(utils.get_bits_seq(pow(2, terms[0][1].size))):
            b[i] = -offset
            for term in terms:
                b[i] += term[0] * term[1].func(bits)

        # Genera simboli per ogni espressioni booleana utilizzabile
        symbols = []
        for i in range(len(self.exprs)):
            symbols.append(sp.symbols("e%d" % i))

        # Risolve sistema indeterminato, ottenendo uno spazio delle soluzioni
        solution = sp.linsolve((A, b), symbols).args[0]

        coef = np.random.randint(10, size=len(self.exprs))
        subs = [ ("e%d" % i, coef[i]) for i in range(len(self.exprs))]
        solution = solution.subs(subs)

        mba = MBAExpr()
        for i, bexp in enumerate(self.exprs):
            coeff = solution[i]
            if coeff != 0:
                mba.add_term(coeff, bexp)

        assert(mba.is_mutation_affine(terms, offset))
        return mba