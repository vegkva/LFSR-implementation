
key = ("1"*80)+"0"*4
IV = ("0"*80)+"0"*13
lfsr_11 = ("0"*108)+"1"*3



def split(string):
    return [int(i) for i in string]

def toString(list):
    result = ""
    for bit in list:
        result += str(bit)
    return result

def trivium(one, two, three):

    output = []
    next1 = split(one)
    next2 = split(two)
    next3 = split(three)

    # 1152 warm-up steps
    for i in range(1152):
        # compute output
        reg1 = lfsr(next1, 65, 90, 91)
        reg2 = lfsr(next2, 68, 81, 82)
        reg3 = lfsr(next3, 65, 108, 109)
        output.append(reg1 ^ reg2 ^ reg3)

        # feedback
        next1.pop()
        next1.insert(0, next1[68] ^ reg3)
        next2.pop()
        next2.insert(0, next2[77] ^ reg1)
        next3.pop()
        next3.insert(0, next3[86] ^ reg2)
    output = []
    for i in range(50):
        # compute output
        reg1 = lfsr(next1, 65, 90, 91)
        reg2 = lfsr(next2, 68, 81, 82)
        reg3 = lfsr(next3, 65, 108, 109)
        output.append(reg1 ^ reg2 ^ reg3)

        # feedback
        next1.pop()
        next1.insert(0, next1[68] ^ reg3)
        next2.pop()
        next2.insert(0, next2[77] ^ reg1)
        next3.pop()
        next3.insert(0, next3[86] ^ reg2)

    return output

def lfsr(inputStream, a, b, c):
    bits = split(inputStream)

    bit_a = bits[a]
    bit_b_c = bits[b] & bits[c]
    output = bit_a ^ bit_b_c ^ bits[-1]
    return output


print(toString(trivium(IV, key, lfsr_11)))
