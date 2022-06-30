# def ask(prompt, retries=4, output='Error'):
#     for _ in range(retries):
#         response = input(prompt).lower()
#         if response in ['y', 'yes']:
#             return True
#         if response in ['n', 'no']:
#             return False
#     print(output)
#
#
# print(ask('Want to know the answer?', 5))
#
# letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
# letters[1:] = []
# print(letters)
#
# a, b = 0, 1
#
# while b < 5:
#     print(b)
#     a, b = b, a + b

# print(range(5, 10)[-1])
# print(range(0, 10, 3)[2])
# print(range(-10, -100, -30)[1])

# def matrix_find(matrix, value):
#     if not matrix or not matrix[0]:
#         return False
#     j = len(matrix) - 1
#     for row in matrix:
#         while row[j] > value:
#             j = j - 1
#             if j == -1:
#                 return False
#         if row[j] == value:
#             return True
#     return False
#
#
# matrix = [[3, 4, 4, 6],
#           [6, 8, 11, 12],
#           [6, 8, 11, 15],
#           [9, 11, 12, 17]]
#
# print(matrix_find(matrix=matrix, value=11))

def maximum_profit(prices):
    """Maximum profit of a single buying low and
    ,→ selling high"""
    profit = 0
    for i, buy_price in enumerate(prices):
        sell_price = max(prices[i:])
        profit = max(profit, sell_price - buy_price)
    return profit


# Ethereum daily prices in Dec 2017 ($)
eth_prices = [455, 460, 465, 451, 414, 415, 441]
print(maximum_profit(prices=eth_prices))
