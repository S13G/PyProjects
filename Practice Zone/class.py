# class Dog:
#     species = ["canis lupus"]
#
#     def __init__(self, n, c):
#         self.name = n
#         self.state = "sleeping"
#         self.color = c
#
#     def command(self, x):
#         if x == self.name:
#             self.bark(2)
#         elif x == "sit":
#             self.state = "sit"
#         else:
#             self.state = "wag tail"
#
#     def bark(self, freq):
#         for i in range(freq):
#             bark = self.name + ": Woof!"
#             print(bark)
#
#
# daniel = Dog("daniel", "black")
# alice = Dog("alice", "white")
#
# print(daniel.color)
# print(alice.color)
# print(alice.species)
# print(daniel.state)
# print(alice.bark(5))
# print("daniel: " + daniel.state)
# print("alice: " + alice.state)
#
# print("daniel: " + daniel.state)
# print(daniel.name)
#
# daniel.species += ["wulf"]
# print(len(daniel.species) == len(alice.species))


class Employee:
    pass


employee = Employee()
employee.salary = 122000
employee.first_name = "alice"
employee.last_name = "wonderland"

print(f"{employee.first_name} {employee.last_name}  {employee.salary}")
