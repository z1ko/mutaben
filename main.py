
from generator import MBAGenerator
from bexpr import BExpr

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
    BExpr("1",       lambda vars: -1)
]

if __name__ == "__main__":
    gen = MBAGenerator(EXPRS)

    count = int(input("Quante identità MBA vuoi generare? "))
    maxcf = int(input("Quale valore massimo dei coef. vuoi usare? "))

    identities = gen.identities(count=count, max_coeff=maxcf, check_identity=True)
    for i, identity in enumerate(identities):
        print("%03s | " % i, end='')
        identity.print()


