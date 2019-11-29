def pop_order(list):
    for i in range(len(list)):
        for j in range(len(list)):
            if j + 1 == len(list):
                break
            if list[j] > list[j + 1]:
                list[j], list[j + 1] = list[j + 1], list[j]
    return list

L=[80,49,56,32,85,42,21,12]
print(pop_order(L))
