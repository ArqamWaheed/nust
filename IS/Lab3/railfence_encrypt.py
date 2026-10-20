# Lab 03 - Rail Fence Cipher
# Task 1 (Part A): Encryption


def strip_text(text):
    # keep only letters and make them capital
    return "".join(ch for ch in text.upper() if ch.isalpha())


def rail_pattern(length, key):
    # which rail each letter goes on (down, then back up)
    rows = []
    row, step = 0, 1
    for _ in range(length):
        rows.append(row)
        if key > 1:
            if row == 0:
                step = 1
            elif row == key - 1:
                step = -1
            row += step
    return rows


def pad_text(text, key):
    # add X (nulls) until the last letter is on the bottom rail
    if key < 2:
        return text
    cycle = 2 * (key - 1)
    while (len(text) - 1) % cycle != key - 1:
        text += "X"
    return text


def rail_fence_encrypt(text, key):
    text = pad_text(strip_text(text), key)
    rails = [""] * key
    for ch, row in zip(text, rail_pattern(len(text), key)):
        rails[row] += ch
    return "".join(rails)


def show_matrix(text, key):
    text = pad_text(strip_text(text), key)
    grid = [["."] * len(text) for _ in range(key)]
    for col, row in enumerate(rail_pattern(len(text), key)):
        grid[row][col] = text[col]
    for i, line in enumerate(grid):
        print(f"  Rail {i + 1}:  " + " ".join(line))
    return grid


if __name__ == "__main__":
    tests = [("defend the east wall", 3),
             ("they are attacking from the north", 4)]

    for plain, key in tests:
        print("Plain text    :", plain)
        print("Stripped text :", strip_text(plain))
        print("Key (rails)   :", key)
        print("Matrix:")
        grid = show_matrix(plain, key)
        print("Reading each rail:")
        for i, line in enumerate(grid):
            print(f"  Rail {i + 1} -> " + "".join(c for c in line if c != "."))
        print("Cipher text   :", rail_fence_encrypt(plain, key))
        print("-" * 50)
