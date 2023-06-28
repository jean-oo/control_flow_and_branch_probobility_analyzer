from sys import argv
def sumIfBothPositiveAndMore(x,y):
    resultString = ""
    for i in range(-5, x):
        for j in range(-5, y):
            if i > 0 or j > 0:
                resultString += str(i + j)
                if i == 6:
                    resultString += "Cool!"
                elif i == 7:
                    resultString +="Fabulous"
                elif i == 42:
                    resultString +="Awesome"
                else:
                    resultString +="Not cool"
            elif i < 0 or j < 0:
                resultString +=str(j)
            else:
                resultString +=str(0)
    return resultString


sumIfBothPositiveAndMore(int(argv[1]), int(argv[2]))