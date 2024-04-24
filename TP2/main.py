import ex1
import ex2et3
import inputControl
import os

"""Ce programme permet de lançer toutes les fonctions des différents fichiers individuellement
Cela permet de les tester. On peut choisir les paramètres, et on récupère le résultat.
Il suffit de regarder l'ordre des paramètres dans la défintion de la fonction pour savoir l'ordre
dans lequel il faut les saisir."""

dict_func = {
    "nb_min" : ex1.nb_min,
    "nb_maj" : ex1.nb_maj,
    "nb_non_alpha" : ex1.nb_non_alpha,
    "longueur_max_in_set" : ex1.longueur_max_in_set,
    "long_min" : ex1.long_min,
    "long_maj" : ex1.long_maj,
    "score" : ex1.score,
    "comment_password" : ex1.comment_password,
    "test_cache" : ex2et3.test_cache,
    "fibonacci_iter" : ex2et3.fibonacci_iter,
    "fibonacci_recursif_cached" : ex2et3.fibonacci_recursif_cached,
    "fibonacci_recursif" : ex2et3.fibonacci_recursif,
    "test_func" : ex2et3.test_func
}

dict_args = {
    "nb_min" : [str],
    "nb_maj" : [str],
    "nb_non_alpha" : [str],
    "longueur_max_in_set" : [str, str],
    "long_min" : [str],
    "long_maj" : [str],
    "score" : [str],
    "comment_password" : [str],
    "test_cache" : [],
    "fibonacci_iter" : [int],
    "fibonacci_recursif_cached" : [int],
    "fibonacci_recursif" : [int],
    "test_func" : [int],
}

if __name__ == "__main__" : 
    launched = True
    while launched :
        ans = "a"
        while ans[0] != "y" and ans[0] != "n" :
            ans = input("Voulez vous lancer une autre fonction ? (y/n) : ")
        if ans[0] == 'n' :
            break
        
        os.system("cls")
        print("Quelle fonction voulez-vous lancer ? ")
        for func in dict_func :
            print(func)

        ans = None
        while ans not in dict_func :
            ans = input("Entrez le nom d'une fonction : ")

        args = []

        for type_asked in dict_args[ans] :
            if type_asked == int :
                args.append(inputControl.getint())
            elif type_asked == str :
                args.append(inputControl.getString())
            elif type_asked == set :
                args.append(inputControl.getSet()) 

        print(f"Résultat de la fonction : {dict_func[ans](*args)}")
                

        


