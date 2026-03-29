

import random
from task1_lat_spn import SPN_SBOX, build_lat, dot


def encrypt(x: int, k: int) -> int:
    """Single-round cipher: y = S(x XOR k)."""
    return SPN_SBOX[(x ^ k) & 0xF]


if __name__ == "__main__":
    TRUE_KEY = 0x6
    N_PAIRS  = 10_000

    random.seed(42)
    pairs = [(x, encrypt(x, TRUE_KEY)) for x in
             (random.randint(0, 15) for _ in range(N_PAIRS))]

    print(f"Cipher:        y = S(x XOR k)  with S = SPN_SBOX")
    print(f"True key:      k = 0x{TRUE_KEY:X}  (binary {TRUE_KEY:04b})")
    print(f"# PT/CT pairs: {N_PAIRS}")

    lat = build_lat(SPN_SBOX, n_in=4, n_out=4)

    # Best single-bit-mask approximations
    # a=1 → b=7,  bias=+6   (recover bit 0)
    # a=2 → b=e,  bias=-6   (recover bit 1)
    # a=4 → b=5,  bias=-4   (recover bit 2)
    # a=8 → b=f,  bias=-6   (recover bit 3)
    bit_approx = [
        (0x1, 0x7),
        (0x2, 0xE),
        (0x4, 0x5),
        (0x8, 0xF),
    ]

    print("\nBit-by-bit key recovery using one strong approximation per key bit:")
    print(f"  {'bit':>4}  {'a':>4}  {'b':>4}  {'lat[a,b]':>9}  "
          f"{'count_0':>8}  {'bias':>8}  {'recovered':>10}  {'truth':>6}")
    print("  " + "-" * 62)

    recovered_key = 0
    for bit_idx, (a, b) in enumerate(bit_approx):
        lat_val = lat[a][b]
        count_0 = sum(1 for (x, y) in pairs if dot(a, x) ^ dot(b, y) == 0)
        d       = count_0 - N_PAIRS // 2
        rec_bit = 0 if (d * lat_val > 0) else 1
        true_bit = (TRUE_KEY >> bit_idx) & 1
        match = "✓" if rec_bit == true_bit else "✗"
        print(f"  {bit_idx:>4}  {a:>4x}  {b:>4x}  {lat_val:>9}  "
              f"{count_0:>8}  {d:>8}  {rec_bit:>10}  {true_bit:>4}  {match}")
        recovered_key |= (rec_bit << bit_idx)

    print(f"\nRecovered key: 0x{recovered_key:X}  "
          f"({'CORRECT' if recovered_key == TRUE_KEY else 'WRONG'})")

    # Signal growth for bit 0
    a, b = bit_approx[0]
    lat_val = lat[a][b]
    print(f"\nSignal growth for bit 0 (a=0x{a:X}, b=0x{b:X}, lat={lat_val}):")
    print(f"  {'N':>8}  {'count_0':>10}  {'bias(count_0)':>14}  {'recovered bit0':>16}")
    print("  " + "-" * 54)
    for n in [50, 100, 200, 500, 1000, 5000, N_PAIRS]:
        c0 = sum(1 for (x, y) in pairs[:n] if dot(a, x) ^ dot(b, y) == 0)
        d  = c0 - n // 2
        rb = 0 if (d * lat_val > 0) else 1
        print(f"  {n:>8}  {c0:>10}  {d:>14}  {rb:>16}")
