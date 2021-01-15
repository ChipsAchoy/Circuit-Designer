
def searchNameRes(dictionary, list): #Busca el nombre de las resistencias tomando un diccionario con estas y una lista ordenada de las resistencias
    result = {}
    for i in list:
        for j in dictionary:
            if i == dictionary.get(j):
                temp = {j:i}
                result.update(temp)
    return result