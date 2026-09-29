def build_matrix(key):
    letters = ""
    for ch in key.upper().replace("J", "I") + "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if ch.isalpha() and ch not in letters:
            letters += ch
    return [list(letters[i:i + 5]) for i in range(0, 25, 5)]


def find(matrix, ch):
    for r in range(5):
        for c in range(5):
            if matrix[r][c] == ch:
                return r, c


def strip_message(text):
    return "".join(ch for ch in text.upper() if ch.isalpha()).replace("J", "I")


def make_pairs(text):
    pairs = []
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i + 1] if i + 1 < len(text) else "Q"
        if a == b:
            b = "X" if a == "Q" else "Q"
            i += 1
        else:
            i += 2
        pairs.append(a + b)
    return pairs


def encrypt_pair(matrix, pair):
    r1, c1 = find(matrix, pair[0])
    r2, c2 = find(matrix, pair[1])
    if r1 == r2:
        return matrix[r1][(c1 + 1) % 5] + matrix[r2][(c2 + 1) % 5]
    if c1 == c2:
        return matrix[(r1 + 1) % 5][c1] + matrix[(r2 + 1) % 5][c2]
    return matrix[r1][c2] + matrix[r2][c1]


def print_matrix(matrix):
    for row in matrix:
        print("  " + " ".join("I/J" if ch == "I" else ch + "  " for ch in row))


if __name__ == "__main__":
    key = input("Enter key: ")
    message = input("Enter message: ")

    matrix = build_matrix(key)
    stripped = strip_message(message)
    pairs = make_pairs(stripped)
    cipher = [encrypt_pair(matrix, p) for p in pairs]

    print("\nKey:", key.upper())
    print("Matrix:")
    print_matrix(matrix)
    print("\nPlain text:", message)
    print("Stripped message:", stripped)
    print("Pairs:", " ".join(pairs))
    print("Encrypted:", " ".join(cipher))
