'''
radixSort(listIn):
    E: Lista de enteros
    S: Retorna las lista ordenada de forma ascendente
    R: -
'''


def radixSort(listIn):
    n = 0
    biggest = 0
    for elem in listIn:
        if elem > biggest:
            biggest = elem
        n += 1
    biggest = len(str(biggest))
    print(biggest)
    print(listIn)

    for x in range(biggest):
        print("###########################")
        listOut = []
        for i in range(len(listIn)):
            listOut += [0]
        digit = 10 ** x
        integers = []
        for i in range(10):
            integers += [0]
        for elem in listIn:
            dig = (elem // digit) % 10
            # print(dig)
            integers[dig] += 1
        for i in range(len(integers)):
            if i != 0:
                integers[i] += integers[i - 1]
        # print(integers)
        print(listIn)
        for i in range(len(listIn)):
            n = len(listIn) - (i + 1)
            dig = (listIn[n] // digit) % 10
            integers[dig] -= 1
            num = listIn[n]
            listOut[integers[dig]] = num
        print(listOut)
        listIn = listOut
    return listOut


'''
insertionSort(listOrd):
    E: Lista de elementos comparables
    S: Lista ordenada de forma descendente
    R: -
'''


def insertion_Sort(listOrd):
    print("desc org")
    position = 1
    while position < len(listOrd):
        ordered = False
        i = position
        while not ordered:
            if listOrd[i] > listOrd[i - 1] and i != 0:
                tmp = listOrd[i]
                listOrd[i] = listOrd[i - 1]
                listOrd[i - 1] = tmp
                i -= 1
            else:
                ordered = True
        position += 1
    print(listOrd)
    return listOrd


'''
shellSort(listOrd):
    E: Lista de elementos comparables
    S: Lista ordenada de forma ascendente
    R: -
'''
def shell_Sort(listOrd):
    print("asc org")
    ordered = False
    gap = len(listOrd)
    while not ordered:
        gap = gap // 2
        i = 0
        f = gap
        print(gap)
        if gap != 1:
            while f != len(listOrd):
                if listOrd[i] > listOrd[f]:
                    tmp = listOrd[i]
                    listOrd[i] = listOrd[f]
                    listOrd[f] = tmp
                i += 1
                f += 1

            print(gap, listOrd)
        else:
            i = 1
            position = 1
            while position < len(listOrd):
                orderedf = False
                i = position
                while not orderedf:
                    if listOrd[i] < listOrd[i - 1] and i != 0:
                        tmp = listOrd[i]
                        listOrd[i] = listOrd[i - 1]
                        listOrd[i - 1] = tmp
                        i -= 1
                    else:
                        orderedf = True
                position += 1
            ordered = True
    print(listOrd)
    return listOrd




print(shell_Sort(["c", "b", "a"]))
print(insertion_Sort(["c", "b", "a"]))
