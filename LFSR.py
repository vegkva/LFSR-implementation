
# Linear Feedback Shift Register
# Efficient design for Test Pattern Generators & Output Response Analyzers
# (also used in CRC, Cyclic Redundency Check, used for almost all data entities,
# files and transiver data-packets) 

# "this is a test" in binary
plaintext = [0,1,1,1,0,1,0,0,0,1,1,0,1,0,0,0,0,1,1,0,1,0,0,1,0,1,1,1,0,0,1,1,0,0,1,0,0,0,0,0,0,1,1,0,1,0,0,1,0,1,1,1,0,0,1,1,
             0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,1,0,0,1,0,0,0,0,0,0,1,1,1,0,1,0,0,0,1,1,0,0,1,0,1,0,1,1,1,0,0,1,1,0,1,1,1,0,1,0,0]

"""
With this initial state, the cycle will
repeat after 254 cycles.
This means one can create a key with length
254 without repeating states
"""
feedback = [0,1,1,0,1,0,0,1] # 8 bit?
initial_state = [1,0,0,1,0,1,0,0] # 8 bit?


"""
Simple implementation of the LFSR
Can only XOR 4 digits
"""
def lfsr(feedback, state, k):
    new_first_pos = 0
    xor_index = indices(feedback, 1)
    print(xor_index)
    next_state = initial_state.copy()
    output = []
    count = 0
    #print("initial: ", next_state)
    for i in range(k):
        if (len(xor_index) == 2):
            new_first_pos = ((next_state[xor_index[0]] + next_state[xor_index[1]]) % 2)
            #print("xor'd index", xor_index[0], "and", xor_index[1], "of", next_state, " and got:", new_first_pos)
        if (len(xor_index) == 3):
            new_first_pos = ((next_state[xor_index[0]] + next_state[xor_index[1]] + next_state[xor_index[2]]) % 2)
            #print("xor'd index", xor_index[0], "and", xor_index[1], "and", xor_index[2], "of", next_state, " and got:", new_first_pos)
        if (len(xor_index) == 4):
            new_first_pos = ((next_state[xor_index[0]] + next_state[xor_index[1]] + next_state[xor_index[2]] + next_state[xor_index[3]]) % 2)
            #print("xor'd index", xor_index[0], "and", xor_index[1], "and", xor_index[2], "and", xor_index[3], "of", next_state, " and got:", new_first_pos)
        output.append(next_state.pop())
        #print("popped ", output[-1], " to output")
        #print("state before new first pos: ", next_state)
        next_state.insert(0, new_first_pos)
        #print("next state completed with new first pos: ", next_state)

        # Check if initial state repeats
        if state == next_state:
            print("cycle repeated after ", count, "steps")
        count += 1

    return output


"""
Encrypts plaintext by xor'ing 
'plaintext' with 'key'. 'Space' is
the number of digits in the binary
"""
def encrypt(plaintext, key, space):
    encrypted_list = []
    encrypted = ""

    for i in range(len(key)):
        encrypted_list.append((plaintext[i] + key[i]) % 2)
        encrypted += str((plaintext[i] + key[i]) % 2)
        if len(encrypted_list) % space == 0:
            encrypted += " "

    return encrypted_list


"""
Decrypts ciphertext by xor'ing 
'ciphertext' with 'key'. 'Space' is
the number of digits in the binary
"""
# Does each digit represet one bit?
def decrypt(ciphertext, key, space):
    decrypted_list = []
    decrypted_list_final = []
    decrypted = ""

    for i in range(len(key)):
        decrypted_list.append((ciphertext[i] + key[i]) % 2)
        decrypted += str((ciphertext[i] + key[i]) % 2)
        if len(decrypted_list) % space == 0:
            decrypted_list_final.append(decrypted)
            decrypted = ""

    return decrypted_list_final


"""
Creates a list with indexes that
will be xor'ed
"""
# for each byte?
def indices(lst, item):
    return [i for i, x in enumerate(lst) if x == item]






key = lfsr(feedback, initial_state, 112) # 112 = 14*8

ciphertext = encrypt(plaintext, key, 8)
print("encrypted: ", ciphertext)
decryptText = decrypt(ciphertext, key, 8)

# "double character conversion"
# Binary byte value by use of Ascii characters '0' and '1' is considered a bitString
# bitString2Char takes a bitString and calculates its desimal value in order to
# return the bitStrings assosiated Ascii character
def bitString2Char(bitString):
    byteValue = 0
    for i in range(8):
        if bitString[i] == '1':
            byteValue += 2**(7-i) # The bitString is organized as a littl-endian byte
                                  # meaning that the first position in the bitString
                                  # is the most significant bit having the value of
                                  # 2 with the exponent of 7, which will give the 
                                  # value of 128 IF this bit is set to one ('1').
    
    return chr(byteValue)

print("decrypted: ", decrypt(ciphertext, key, 8))

# Print the ascii text on one line.
for i in decryptText:
    print(bitString2Char(i), end="")
