# Lab 03 - Rail Fence Cipher
# Task 1 (Part B): Decryption

from railfence_encrypt import rail_pattern, rail_fence_encrypt


def rail_fence_decrypt(ciphertext, key):
    pattern = rail_pattern(len(ciphertext), key)

    # how many letters sit on each rail
    counts = [pattern.count(r) for r in range(key)]

    # cut the ciphertext into its rails
    rails = []
    start = 0
    for c in counts:
        rails.append(list(ciphertext[start:start + c]))
        start += c

    # walk the zigzag again and take letters from each rail in order
    plain = ""
    for row in pattern:
        plain += rails[row].pop(0)
    return plain


def show_dashes(ciphertext, key):
    # the empty grid with dashes where letters will go
    grid = [["."] * len(ciphertext) for _ in range(key)]
    for col, row in enumerate(rail_pattern(len(ciphertext), key)):
        grid[row][col] = "-"
    for i, line in enumerate(grid):
        print(f"  Rail {i + 1}:  " + " ".join(line))


if __name__ == "__main__":
    tests = [("TEKOOHRACIRMNREATANFTETYTGHH", 4),
             ("DNETLEEDHESWLXFTAAX", 3)]

    for cipher, key in tests:
        print("Cipher text :", cipher)
        print("Key         :", key)
        print("Grid before filling:")
        show_dashes(cipher, key)
        plain = rail_fence_decrypt(cipher, key)
        print("Plain text  :", plain)
        print("-" * 50)

    # quick check: encrypt then decrypt should give the message back
    msg = "information security"
    enc = rail_fence_encrypt(msg, 5)
    print("Round trip test with key 5")
    print("  Encrypted :", enc)
    print("  Decrypted :", rail_fence_decrypt(enc, 5))
