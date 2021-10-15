def First_task(list, k):
    result = 0
    for i in range(len(list)):
        for j in range(i, len(list)):
            summ = 0
            for m in range(i, j + 1):
                summ += list[m]
            if summ <= k:
                result += 1
    return result


def Second_task(list, k):
    result = 0
    for i in range(len(list)):
        summ = 0
        for j in range(i, len(list)):
            summ += list[j]
            if summ <= k:
                result += 1
            else:
                break
    return result


def Third_task(list, k):
    i = 0
    j = 0
    summ = list[i]
    result = 0
    while i < len(list) and j < len(list):
        if summ <= k:
            j += 1
            if j >= i:
                result += j - i

            if j < len(list):
                summ += list[j]

        else:
            summ -= list[i]
            i += 1

    return result


A = [4, 3, 2, 1]
k = 5
print(Third_task(A, k))
