last = 0
with open("number", "r") as file:
    lines = file.readlines()
    last = int(lines[-1])
    print(last)
    last += 1

with open("number", "a") as file:
    file.write("\n" + str(last))
