"""
Task 1 – Linear Approximation Table (LAT) for the SPN 4-bit S-box
"""

# S-box: S = [E, 4, D, 1, 2, F, B, 8, 3, A, 6, C, 5, 9, 0, 7]
SPN_SBOX = [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8,
            0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7]


def dot(a: int, b: int) -> int:
    """Bitwise dot product (parity of a AND b) mod 2."""
    return bin(a & b).count("1") % 2


def build_lat(sbox: list, n_in: int, n_out: int) -> list:
    """
    Build the Linear Approximation Table for sbox.
    lat[a][b] = #{x : a·x = b·S(x)} − 2^(n_in−1)
    """
    size_in = 1 << n_in
    size_out = 1 << n_out
    half = size_in >> 1

    lat = [[0] * size_out for _ in range(size_in)]
    for a in range(size_in):
        for b in range(size_out):
            count = sum(1 for x in range(size_in) if dot(a, x) == dot(b, sbox[x]))
            lat[a][b] = count - half
    return lat


def print_lat(lat: list) -> None:
    """Pretty-print the LAT."""
    n_in  = len(lat)
    n_out = len(lat[0])
    col_w = 5

    print(f"\n{'=' * 60}")
    print("  SPN 4-bit S-box LAT  (entries = #matches − 8)")
    print(f"{'=' * 60}")

    header = " " * col_w + "".join(f"{b:>{col_w}x}" for b in range(n_out))
    print(header)
    print(" " * col_w + "-" * (col_w * n_out))

    for a in range(n_in):
        row = f"{a:>{col_w - 1}x} |" + "".join(f"{lat[a][b]:>{col_w}}" for b in range(n_out))
        print(row)


def print_strongest(lat: list) -> None:
    """Print all non-trivial approximations with |bias| >= 4."""
    print("\nStrongest non-trivial linear approximations (|bias| >= 4):")
    print(f"  {'a':>4}  {'b':>4}  {'bias':>6}  {'prob':>8}")
    print("  " + "-" * 28)

    entries = [(abs(lat[a][b]), a, b, lat[a][b])
               for a in range(1, 16) for b in range(1, 16)]
    entries.sort(reverse=True)

    for abs_bias, a, b, bias in entries:
        if abs_bias >= 4:
            prob = 0.5 + bias / 16.0
            print(f"  {a:>4x}  {b:>4x}  {bias:>6}  {prob:>8.4f}")


if __name__ == "__main__":
    lat = build_lat(SPN_SBOX, n_in=4, n_out=4)
    print_lat(lat)
    print_strongest(lat)
