
import numpy as np
import utils

# Funzione comoda per valutare combinazioni affini
def evaluate_affine(vars, terms, offset):
    result = sum(map(lambda term: term[0] * term[1].func(vars), terms)) + offset
    return result


# Rappresenta una generica espressione booleana
class BExpr:
    def __init__(self, text, func, size = 2) -> None:
        self.text = text
        self.func = func
        self.size = size


# Rappresenta una espressione in mixed-boolean-arithmetic   
class MBAExpr:
    def __init__(self) -> None:
        self.elements = []

    def add_term(self, coef: int, expr: BExpr):
        self.elements.append((coef, expr))

    # Visualizza la MBA in un formato leggibile
    def print(self):
        print("{ ", end='')
        for (coef, expr) in self.elements:
            #sign = '-' if coef < 0 else '+'
            #print(f"{sign} {abs(coef)} * ({expr.text}) ", end='')
            print(f"({coef}, {expr.text}), ", end='')
        print("}")

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
        for bits in utils.get_bits_seq(pow(2, bexpr.size)):
            if not self.evaluate(bits) == 0:
                return False

        for _ in range(100):
            vars = np.random.randint(10000, size=2)
            if self.evaluate(vars) != 0:
                return False

        return True

    # Controlla che la MBA si comporti come expr
    def is_mutation(self, expr: BExpr):
        _, bexpr = self.elements[0]
        for bits in utils.get_bits_seq(pow(2, bexpr.size)):

            eval1 = self.evaluate(bits)
            eval2 = expr.func(bits)

            #print(f"Evaluate: {eval1} vs {eval2}")
            if eval1 != eval2:
                return False

        # Controllo stocastico
        for _ in range(100):
            vars = np.random.randint(10000, size=2)
            if self.evaluate(vars) != expr.func(vars):
                return False

        return True

    # Controlla che la MBA si comporto come una combinazione affine
    def is_mutation_affine(self, terms, offset):

        _, bexpr = self.elements[0]
        for bits in utils.get_bits_seq(pow(2, bexpr.size)):

            eval1 = self.evaluate(bits)
            eval2 = evaluate_affine(bits, terms, offset)

            #print(f"Evaluate for (x: {bits[0]}, y: {bits[1]}) -> {eval1} vs {eval2}")
            if eval1 != eval2:
                return False

        # Controllo stocastico
        for _ in range(100):
            vars = np.random.randint(10000, size=2)

            eval1 = self.evaluate(vars)
            eval2 = evaluate_affine(vars, terms, offset)

            #print(f"Evaluate for (x: {vars[0]}, y: {vars[1]}) -> {eval1} vs {eval2}")
            if eval1 != eval2:
                return False
        
        return True
    
    # Ritorna una versione in stringa della mba
    def as_string(self):
        result = ""
        for i, (coef, expr) in enumerate(self.elements):
            if i != 0:
                result += " + "
            result += f"({coef}) * ({expr.text})"
        return result
