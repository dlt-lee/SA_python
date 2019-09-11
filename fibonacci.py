def fibonacci(n):
    a = 0
    b = 1
    result = []
    while True:
        future = a + b
        if b == n:
            break
        a = b
        b = future
        print(future)
        result.append(future)
    return result
