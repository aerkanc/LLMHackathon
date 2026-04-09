import math

# n^2 has form 1_2_3_4_5_6_7_8_9_0 (19 digits)
# n divisible by 10 => n^2 divisible by 100 => last two digits 00
# So pattern is actually 1_2_3_4_5_6_7_8_900
# Let n = 10*m, then 100*m^2 matches pattern => m^2 matches 1_2_3_4_5_6_7_8_9 (17 digits)

lo = math.isqrt(1020304050607080900)
hi = math.isqrt(1929394959697989990) + 1

m_lo = lo // 10
m_hi = hi // 10 + 1

# m^2 mod 10 must be 9 => m mod 10 in {3, 7}
# m^2 mod 1000 must be 8X9 for some digit X (positions from right: digit3=9, digit5=8)
# Pre-filter valid m mod 1000

valid_residues = []
for r in range(1000):
    if r % 10 not in (3, 7):
        continue
    sq_mod = (r * r) % 1000
    # Need last digit 9 and hundreds digit 8
    if sq_mod % 10 == 9 and sq_mod // 100 == 8:
        valid_residues.append(r)

# Search with stride 1000 for each valid residue
for r in valid_residues:
    start = m_lo + ((r - m_lo % 1000) % 1000)
    if start < m_lo:
        start += 1000
    m = start
    while m <= m_hi:
        sq = m * m
        s = str(sq)
        if (len(s) == 17 and
            s[0] == '1' and s[2] == '2' and s[4] == '3' and
            s[6] == '4' and s[8] == '5' and s[10] == '6' and
            s[12] == '7' and s[14] == '8' and s[16] == '9'):
            print(10 * m)
            exit()
        m += 1000