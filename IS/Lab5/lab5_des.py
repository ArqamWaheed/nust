# Lab 05 - Implementation of DES
# Arqam Waheed - 553514

# ======================= DES tables =======================

# Initial Permutation (8 x 8)
IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17,  9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

# Final Permutation (8 x 8) - inverse of IP
FP = [40, 8, 48, 16, 56, 24, 64, 32,
      39, 7, 47, 15, 55, 23, 63, 31,
      38, 6, 46, 14, 54, 22, 62, 30,
      37, 5, 45, 13, 53, 21, 61, 29,
      36, 4, 44, 12, 52, 20, 60, 28,
      35, 3, 43, 11, 51, 19, 59, 27,
      34, 2, 42, 10, 50, 18, 58, 26,
      33, 1, 41,  9, 49, 17, 57, 25]

# Expansion Permutation (8 x 6) : 32 bits -> 48 bits
E = [32,  1,  2,  3,  4,  5,
      4,  5,  6,  7,  8,  9,
      8,  9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32,  1]

# Round Permutation P (4 x 8)
P = [16,  7, 20, 21, 29, 12, 28, 17,
      1, 15, 23, 26,  5, 18, 31, 10,
      2,  8, 24, 14, 32, 27,  3,  9,
     19, 13, 30,  6, 22, 11,  4, 25]

# S-boxes S1..S8, each 4 x 16
S = [
    [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
     [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
     [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
     [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
    [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
     [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
     [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
     [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
    [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
     [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
     [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
     [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
    [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
     [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
     [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
     [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
    [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
     [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
     [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
     [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
    [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
     [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
     [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
     [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
    [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
     [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
     [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
     [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
    [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
     [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
     [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
     [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]],
]

# Permuted Choice 1 (8 x 7) : 64-bit key -> 56 bits
PC1 = [57, 49, 41, 33, 25, 17,  9,
        1, 58, 50, 42, 34, 26, 18,
       10,  2, 59, 51, 43, 35, 27,
       19, 11,  3, 60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
       14,  6, 61, 53, 45, 37, 29,
       21, 13,  5, 28, 20, 12,  4]

# Permuted Choice 2 (8 x 6) : 56 bits -> 48-bit round key
PC2 = [14, 17, 11, 24,  1,  5,
        3, 28, 15,  6, 21, 10,
       23, 19, 12,  4, 26,  8,
       16,  7, 27, 20, 13,  2,
       41, 52, 31, 37, 47, 55,
       30, 40, 51, 45, 33, 48,
       44, 49, 39, 56, 34, 53,
       46, 42, 50, 36, 29, 32]

# Number of left rotations for rounds 1..16
SHIFTS = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]


# ======================= helpers =======================

def xor_bits(a, b):
    result = ""
    for i in range(len(a)):
        result += "0" if a[i] == b[i] else "1"
    return result


def hex_to_bits(hex_str):
    return "".join(format(int(h, 16), "04b") for h in hex_str)


def bits_to_hex(bits):
    return "".join(format(int(bits[i:i + 4], 2), "X") for i in range(0, len(bits), 4))


def bits_to_text(bits):
    # turn bits back into characters, dropping the 0-padding bytes
    text = ""
    for i in range(0, len(bits), 8):
        code = int(bits[i:i + 8], 2)
        if code != 0:
            text += chr(code)
    return text


def group(bits, size):
    return " ".join(bits[i:i + size] for i in range(0, len(bits), size))


# ================ Lab 4 methods (reused) ================

def desPlaintextBlock(plaintext):
    all_bits = ""
    for ch in plaintext:
        all_bits += format(ord(ch), "08b")
    while len(all_bits) % 64 != 0:
        all_bits += "0"
    blocks = []
    for i in range(0, len(all_bits), 64):
        blocks.append(all_bits[i:i + 64])
    return blocks


def desInitialPermutation(block64):
    permuted = ""
    for pos in IP:
        permuted += block64[pos - 1]
    return permuted


def desPermutedChoice1(key64):
    permuted = ""
    for pos in PC1:
        permuted += key64[pos - 1]
    return permuted


def desLeftShift(block28, round_no):
    shift = SHIFTS[round_no - 1]
    return block28[shift:] + block28[:shift]


def desPermutedChoice2(block56):
    permuted = ""
    for pos in PC2:
        permuted += block56[pos - 1]
    return permuted


def desRoundKeys(key64):
    # build all 16 round keys from the 64-bit key
    key56 = desPermutedChoice1(key64)
    C = key56[:28]
    D = key56[28:]
    keys = []
    for round_no in range(1, 17):
        C = desLeftShift(C, round_no)
        D = desLeftShift(D, round_no)
        keys.append(desPermutedChoice2(C + D))
    return keys


# ======================= Lab 5 Task 1 =======================

# ----------------------------- Task 1A -----------------------------
# Expand a 32-bit block to 48 bits using the 8 x 6 E table.
def desExpansionPermutation(block32):
    expanded = ""
    for pos in E:
        expanded += block32[pos - 1]
    return expanded


# ----------------------------- Task 1B -----------------------------
# Split 48 bits into 8 groups of 6. For each group:
# row = first and last bit, column = middle 4 bits -> 4-bit output.
def getSubBoxes(block48):
    output = ""
    for i in range(8):
        six = block48[i * 6:(i + 1) * 6]
        row = int(six[0] + six[5], 2)
        col = int(six[1:5], 2)
        value = S[i][row][col]
        output += format(value, "04b")
    return output


# ----------------------------- Task 1C -----------------------------
# Apply the 4 x 8 round permutation P to a 32-bit block.
def desRoundPermutation(block32):
    permuted = ""
    for pos in P:
        permuted += block32[pos - 1]
    return permuted


# ----------------------------- Task 1D -----------------------------
# Apply the 8 x 8 Final Permutation (inverse of IP) to a 64-bit block.
def desFinalPermutation(block64):
    permuted = ""
    for pos in FP:
        permuted += block64[pos - 1]
    return permuted


# Round function f(R, K) = P( S( E(R) xor K ) )
def desRoundFunction(R, K):
    expanded = desExpansionPermutation(R)
    mixed = xor_bits(expanded, K)
    substituted = getSubBoxes(mixed)
    return desRoundPermutation(substituted)


# ======================= Lab 5 Task 2 =======================

# One 64-bit block through IP, 16 Feistel rounds, swap and FP
def desBlock(block64, keys):
    ip = desInitialPermutation(block64)
    L = ip[:32]
    R = ip[32:]
    for i in range(16):
        new_R = xor_bits(L, desRoundFunction(R, keys[i]))
        L = R
        R = new_R
    return desFinalPermutation(R + L)


# ----------------------------- Task 2A -----------------------------
# Encrypt every 64-bit plaintext block with keys K1..K16.
def desEncryption(plaintext, key64):
    keys = desRoundKeys(key64)
    cipher = []
    for block in desPlaintextBlock(plaintext):
        cipher.append(desBlock(block, keys))
    return cipher


# ----------------------------- Task 2B -----------------------------
# Same algorithm, only the round keys are used in reverse (K16..K1).
def desDecryption(cipher, key64):
    keys = desRoundKeys(key64)
    reversed_keys = keys[::-1]
    bits = ""
    for block in cipher:
        bits += desBlock(block, reversed_keys)
    return bits_to_text(bits)


if __name__ == "__main__":
    plaintext = input("Enter plaintext: ")
    key_hex = input("Enter 64-bit key (16 hex digits, e.g. 133457799BBCDFF1): ")

    key64 = hex_to_bits(key_hex)
    keys = desRoundKeys(key64)
    block = desPlaintextBlock(plaintext)[0]
    ip = desInitialPermutation(block)
    R0 = ip[32:]

    print("\n========== Task 1A: desExpansionPermutation (R0 of Block 1) ==========")
    expanded = desExpansionPermutation(R0)
    print("R0     (32) :", group(R0, 4))
    print("E(R0)  (48) :", group(expanded, 6))

    print("\n========== Task 1B: getSubBoxes ==========")
    mixed = xor_bits(expanded, keys[0])
    s_out = getSubBoxes(mixed)
    print("K1     (48) :", group(keys[0], 6))
    print("E xor K1    :", group(mixed, 6))
    for i in range(8):
        six = mixed[i * 6:(i + 1) * 6]
        row, col = int(six[0] + six[5], 2), int(six[1:5], 2)
        print(f"  S{i + 1}({six}) row {row}, col {col:2} -> {S[i][row][col]:2} = {s_out[i * 4:i * 4 + 4]}")
    print("S-box  (32) :", group(s_out, 4))

    print("\n========== Task 1C: desRoundPermutation ==========")
    f = desRoundPermutation(s_out)
    print("Input  (32) :", group(s_out, 4))
    print("After P     :", group(f, 4))
    print("f(R0, K1)   =", bits_to_hex(f))

    print("\n========== Task 1D: desFinalPermutation ==========")
    fp = desFinalPermutation(ip)
    print("Input (IP of Block 1) :", group(ip, 8))
    print("After FP              :", group(fp, 8))
    print("FP(IP(block)) == block ?", "yes" if fp == block else "no")

    print("\n========== Task 2A: desEncryption ==========")
    cipher = desEncryption(plaintext, key64)
    blocks = desPlaintextBlock(plaintext)
    for i in range(len(cipher)):
        print(f"Block {i + 1} : {bits_to_hex(blocks[i])}  ->  {bits_to_hex(cipher[i])}")
    print("Ciphertext :", "".join(bits_to_hex(c) for c in cipher))

    print("\n========== Task 2B: desDecryption ==========")
    decrypted = desDecryption(cipher, key64)
    print("Decrypted  :", decrypted)
    print("Matches plaintext ?", "yes" if decrypted == plaintext else "no")
