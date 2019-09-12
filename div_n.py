def div_n(n):
    n = float(n)
    i = 0
    while True:
        n = n // 2
        i += 1
        if n * n < 4:
            break
    return i


print("能被2除：", div_n(input("请输入：")), "次\n")
