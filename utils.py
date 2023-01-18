
# Ritorna un array con i bit del valore in input
def get_bits(value, bitsize = 2):
    result = []
    for i in range(bitsize):
        result.append((value >> i) & 0b1)
    return list(reversed(result))

# Ritorna una sequenza di 'count' array di bit in ordine incrementale
def get_bits_seq(count):
    return [ get_bits(i) for i in range(count) ]