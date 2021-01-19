def searchNameRes(dictionary,
                  list):  # Busca el nombre de las resistencias tomando un diccionario con estas y una lista ordenada de las resistencias
    result = {}
    for i in list:
        for j in dictionary:
            if i == dictionary.get(j):
                temp = {j: i}
                result.update(temp)
    return result


def calcularCuadricula(num):
    return calcularCuadricula_aux(num, num)


def calcularCuadricula_aux(temp1, temp2):
    if temp1 % 50 == 0:
        return temp1
    elif temp2 % 50 == 0:
        return temp2
    else:
        return calcularCuadricula_aux(temp1 - 1, temp2 + 1)
