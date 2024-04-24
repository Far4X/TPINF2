import inspect
import typing

def secureAskType(target_type : typing.Callable, text : str | None  = None, condition : typing.Callable = lambda x : True, msg_unvalid_entry : str = "Entrée non valide, réessayez : ", msg_unvalid_value : str = "Valeur non valide, réessayez : ") -> typing.Any :
    """Permet d'être sur de recevoir un attribut du type demandé
    Le paramètre text permet de sélectionner le text lors de la demande
    La condition permet d'instaurer un controle sur la valeur entrée, comme une valeur maximale
    msg_unvalid_entry est affiché si on ne peut pas convertir l'entrée en le type demandé
    msg_unvalid_value est affiché si la valeur ne satisfait pas la condition posée dans condition"""

    if not inspect.isclass(target_type) :
        raise TypeError("Target_type n'est pas un type de variable.")
    if not callable(condition) :
        raise TypeError("La condition entrée n'est pas valide.")
    if text == None :
        text = f"Entrez quelque chose de type {type}"
    input_v = input(text)
    cont = True
    while (cont) :
        try :
            input_v = target_type(input_v)
        except ValueError :
            input_v = input(msg_unvalid_entry)
        else :
            if (condition(input_v)) :
                cont = False
            else :
                input_v = input(msg_unvalid_value)

 
    return input_v
        

def secureDisplayAndPick(list_objects : list[object], message =  "Entrez un identifieur : ", starter : int  = 0) -> object : 
    """Cette fonction permet d'afficher une liste afin d'en sélectionner un élément
    La valeur retournée sera forcément dans la liste."""
    
    if not isinstance(list_objects, list) :
        raise TypeError("Le paramètre list_objects n'est pas une liste.")
    if len(list_objects) == 0 :
        raise ValueError("La liste est vide")
    if type(starter) != int :
        raise ValueError("L'identifiant de départ n'est pas un entier")
    
    i = starter
    for elem in list_objects :
        print(f"{i} : {elem}")
        i += 1
    
    in_list = lambda x : (x >= starter and x < len(list_objects) + starter)

    ident = secureAskType(int, message, in_list)
    return list_objects[ident - starter]