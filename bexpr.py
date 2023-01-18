
import utils

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
        for bits in utils.get_bits_seq(pow(2, bexpr.size)):
            if not self.evaluate(bits) == 0:
                return False
        return True