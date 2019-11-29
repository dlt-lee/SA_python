def hanoi(high, left="left", right="right", middle="middle"):
    if high:
        hanoi(high-1, left, middle, right)
        print(left, "=>", right)
        hanoi(high-1, middle, right, left)

hanoi(2)