a = 0b11100000

print(bin(a))
print(a)

a <<= 1

print(bin(a))
print(a)

if  a >= 255:
    a -= 255

print(bin(a))
print(a)

