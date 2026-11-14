x = 0
for i in range(8_000_000):
    x = (x * 1664525 + i + 1013904223) & 0xFFFFFFFF
print(x)
