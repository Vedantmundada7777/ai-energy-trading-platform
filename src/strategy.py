def simple_strategy(price, soc):

    if price < 6:
        return 10   # charge

    elif price > 10:
        return -15  # discharge

    else:
        return 0