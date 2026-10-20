# Lab 03 - Rail Fence Cipher
# Task 2: Brute force (key is not known)

from railfence_decrypt import rail_fence_decrypt


def rail_fence_brute_force(ciphertext):
    results = {}
    for key in range(2, len(ciphertext) + 1):
        results[key] = rail_fence_decrypt(ciphertext, key)
        print(f"  Key {key:2}: {results[key]}")
    return results


if __name__ == "__main__":
    tests = [("HOLELWRDLOX", None),
             ("AAXTKTNXTCDWXAAX", "ATTACKATDAWN"),
             ("CYTGAHRPORPY", "CRYPTOGRAPHY")]

    for cipher, known in tests:
        print("Ciphertext:", cipher)
        results = rail_fence_brute_force(cipher)
        if known:
            for key, text in results.items():
                if text.rstrip("X") == known:
                    print(f"  --> match found at key {key}: {text}")
                    break
        print()
