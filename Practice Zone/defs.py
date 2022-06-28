import this

print(list(map(lambda x: x[0], ['red', 'green', 'blue'])))

print(list(map(lambda x, y: str(x) + ' ' + y + 's', [0, 2, 2], ['apple', 'orange', 'banana'])))

print(list(map(lambda x, y: f"{x} {y}s", [0, 1, 2], ['rice', 'beans', 'custard'])))

print(" marries ".join(['Alice', 'Bob']))

print(list(filter(lambda x: True if x > 17 else False, [1, 15, 17, 18])))

print("\n   \t  42    \t".strip())

print(sorted([6, 35, 1, 6, 9, 36]))

print(sorted([8, 4, 42, 3, 5], key=lambda x: 0 if x == 42 else x))

print(sorted([8, 4, 42, 3, 5], key=lambda x: 0 if x == 41 else x))

print(list(zip(['Alice', 'Anna'], ['Bob', 'John', 'Frank'])))

print(list(zip(['Alice', 'Anna'], ['Bob', 'Pawn'])))

print(list(zip(*[('Alice', 'Bob'), ('Anna', 'Pawn')])))

print(list(enumerate(['Alice', 'Bob', 'Anna'])))


def f(x, y, z):
    return x + y * z


print(f(*[1, 3, 4]))
print(f(*(1, 3, 4)))
print(f(**{'z': 4, 'y': 3, 'x': 1}))
a, *b = ['orange', 2, 3, 4, 5]
print(a, *b)

x = {'Alice': 18}
y = {'Bob': 27, 'Ann': 22}
z = {**x, **y}
print(z)