def fibonacci(n):
    a = 0
    b = 1
    result = []
    while True:
        a, b = b, a+b
        if b >= n:
            break
        result.append(b)
    return result

print(fibonacci(1000))