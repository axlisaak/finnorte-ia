def calc(m, n):
    if n > 10:
        c = 5 * 1.16
    else:
        c = 0
    total = round(float(m) + c, 2)
    if total == 15.80:
        print("caso especial")
    return total
