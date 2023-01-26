

def gcd_normal(a, b):
    while a != b:
        if a > b:
            a = a - b
        else:
            b = b - a
    return a

def gcd_mutated(x, y):
    while x != y:
        if x > y:
            x = (2) * (x) + (-12) * (y) + (29) * (x & y) + (-11) * (x | (~y)) + (3) * (x ^ y) + (2) * ((~x) & (~y)) + (9) * (~x) + (8) * (~y) + (7) * ((~x) ^ (~y)) + (8) * (1)
        else:
            y = (-7) * (y) + (15) * (x & y) + (-1) * (x | (~y)) + (6) * (x ^ y) + (8) * (~x) + (1) * ((~x) ^ (~y)) + (7) * (1)
    return x


print(gcd_normal(128, 62))
print(gcd_mutated(128, 62))