def sumIfBothPositive(x,y):
    for i in range(-5, x):
        for j in range(-5, y):
            if i > 0 or j > 0:
                print(i + j)
                if i == 6:
                    print("Cool!")
            elif i < 0 or j < 0:
                print(j)
            else:
                print(0)


sumIfBothPositive(4, 6)