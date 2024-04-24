import time
from timeit import timeit

"""Ce fichier regroupe les fonctions nécessaires pour les parties 2 et 3 du TP, les fonctions utilisées étant les mêmes.
"""

def cache(func) :
    dict_val = {}
    def wrapper(*arg) :
        if arg in dict_val.keys() :
            return dict_val[arg]
        else :
            result = func(*arg)
            dict_val[arg] = result
            return result
        
    return wrapper


@cache
def test_func(x : int) -> int :
    time.sleep(1)
    return x

@cache
def test_func2p(x : int, y : int) -> int :
    time.sleep(1)
    return x + y

def fibonacci_recursif(n : int) -> int :
    if n <= 1 :
        return n
    else :
        return fibonacci_recursif(n-1) + fibonacci_recursif(n-2)

@cache
def fibonacci_recursif_cached(n : int) -> int :
    if n <= 1 :
        return n
    else :
        return fibonacci_recursif_cached(n-1) + fibonacci_recursif_cached(n-2)
    
def fibonacci_iter(n : int) -> int :
    a = 0
    b = 1
    for i in range(n) :
        t = b
        b = a + b
        a = t
    return a
    
def test_cache() -> None :
    print("Appel de la fonction de test avec n = 5")
    print(test_func(5))
    print("Appel de la fonction de test avec n = 6")
    print(test_func(6))
    print("Appel de la fonction de test avec n = 5")
    print(test_func(5))
    print("Appel de la fonction de test avec n = 6")
    print(test_func(6))

    print("Appel de la fonction de test avec n = 5, m = 6")
    print(test_func2p(5, 6))
    print("Appel de la fonction de test avec n = 6, m = 7")
    print(test_func2p(6, 7))
    print("Appel de la fonction de test avec n = 5, m = 6")
    print(test_func2p(5, 6))
    print("Appel de la fonction de test avec n = 6, m = 7")
    print(test_func2p(6, 7))


if __name__ == "__main__" :
    print("\n---Test des fonction avec cache---")

    test_cache()

    print("\n---Tests de fibonnacci en mode récursif et itératif : ---")
    for i in range(11) :
        print(fibonacci_recursif(i), end = "; ")
        print(fibonacci_iter(i))

    print("\n---Tests de rapidité---")

    print("Test de Fibonnacci récusrif pour n = 35")
    print(timeit('fibonacci_recursif(35)', globals=globals(), number=1), "s")
    print("Test de Fibonnacci récusrif pour n = 36")
    print(timeit('fibonacci_recursif(36)', globals=globals(), number=1), "s")
    print("Test de Fibonnacci itératif pour n = 35")
    print(timeit('fibonacci_iter(35)', globals=globals(), number=1), "s")
    print("Test de Fibonnacci itératif pour n = 36")
    print(timeit('fibonacci_iter(36)', globals=globals(), number=1), "s")
    print("Test de Fibonnacci récusrif avec cache pour n = 35")
    print(timeit('fibonacci_recursif_cached(35)', globals=globals(), number=1), "s")
    print("Test de Fibonnacci récusrif avec cache pour n = 35")
    print(timeit('fibonacci_recursif_cached(35)', globals=globals(), number=1), "s")
    print("Test de Fibonnacci récusrif avec cache pour n = 36")
    print(timeit('fibonacci_recursif_cached(36)', globals=globals(), number=1), "s")


    #On observe que le cache fait gagner beaucoup de temps au modde récursif, au point de rattraper
    #l'efficience du mode itératif au bout du deuxième appel