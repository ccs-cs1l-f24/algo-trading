from utils import truncate


def unitScore(stock_history):
    return 1

def negativeUnitScore(stock_history):
    return -1

def getDerivative(stock_history, caution_coeff=10):
    #gets the average derivative over the last caution_coeff days
    if len(stock_history) <= caution_coeff:
        return 0

    dx = []
    for i in range(caution_coeff - 1):
        dx.append(0 if stock_history[-2-i] == 0 else truncate((stock_history[-1-i] - stock_history[-2-i])/stock_history[-2-i]))

    avg = 0
    for x in dx:
        avg += x
    avg /= len(dx)
    # print("average thing", avg)
    if truncate(avg) < 0:
        return max(-1,truncate(avg)/1000)
    else:
        return truncate(avg)

def dayTrade(stock_history, caution_coeff=5):
    #checks if local minimum or local maximum
    if len(stock_history) <= caution_coeff:
        return 0

    dx = []
    for i in range(caution_coeff):
        dx.append(stock_history[-1-i])

    if stock_history[-1] == max(dx):
        return -1
    elif stock_history[-1] == min(dx):
        return 1
    else:
        return 0

def biggestLosers(stock_history, caution_coeff=10):
    #buys the largest losers and sells the largest gainers
    if len(stock_history) <= caution_coeff or stock_history[-2] == 0:
        return 0
    percent_growth = truncate((stock_history[-1] - stock_history[-2])/stock_history[-2])
    #adjusted scores: +10% should be sell 50%, -10% should be buy 50%... +20% should be sell all, -20% should be buy all
    percent_growth = min(100, max(-100, percent_growth * 5))
    return percent_growth/100
