def binaty_search(list,target):
    low = 0
    high = len(list)
    while low <= high:
        mid = int((low+high)/2)
        if target is list[mid]:
            return mid
        elif target > list[mid]:
            low = mid+1
        elif target < list[mid]:
            high = mid-1
        else:
            return None
L=[2,5,8,13,49,80]
print(binaty_search(L, 50))