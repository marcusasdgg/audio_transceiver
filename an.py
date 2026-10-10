import matplotlib.pyplot as plt
import statistics
bigarr = []
with open("log.txt", "r") as file:
    n = len(file.readlines())
    file.seek(0)
    for line in file:
        if line.startswith("LOG"):
            continue
        bigarr += [int(x) for x in line.split(",")]




print(f"out of {n} data samples")
x = 0
while True:
    x = input("enter frequency: ")
    if (x == "c"):
        break
    x = int(x)
    print(f"{100 * bigarr.count(x) / n}% of samples had {x}hz")
print(statistics.mode(bigarr))
# do basic statistical analysis on it
plt.hist(bigarr, 40)
plt.show()

