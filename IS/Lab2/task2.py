from task1 import build_matrix, find, print_matrix


def decrypt_pair(matrix, pair):
    r1, c1 = find(matrix, pair[0])
    r2, c2 = find(matrix, pair[1])
    if r1 == r2:
        return matrix[r1][(c1 - 1) % 5] + matrix[r2][(c2 - 1) % 5]
    if c1 == c2:
        return matrix[(r1 - 1) % 5][c1] + matrix[(r2 - 1) % 5][c2]
    return matrix[r1][c2] + matrix[r2][c1]


def remove_fillers(text):
    if text.endswith("Q"):
        text = text[:-1]
    result = ""
    for i, ch in enumerate(text):
        if ch == "Q" and 0 < i < len(text) - 1 and text[i - 1] == text[i + 1]:
            continue
        result += ch
    return result


if __name__ == "__main__":
    key = input("Enter key: ")
    cipher = input("Enter cipher text: ")

    matrix = build_matrix(key)
    letters = "".join(ch for ch in cipher.upper() if ch.isalpha()).replace("J", "I")
    pairs = [letters[i:i + 2] for i in range(0, len(letters), 2)]
    plain = "".join(decrypt_pair(matrix, p) for p in pairs)

    print("\nKey:", key.upper())
    print("Matrix:")
    print_matrix(matrix)
    print("\nCipher pairs:", " ".join(pairs))
    print("Decrypted pairs:", " ".join(plain[i:i + 2] for i in range(0, len(plain), 2)))
    print("Plain text:", remove_fillers(plain))
