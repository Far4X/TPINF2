import string
from getpass import getpass

"""On retrouve dans ce fichier les fonction, et leur tests, de la partie 1 du TP."""

dict_comment = {
    0 : "Très faible",
    20 : "Faible",
    40 : "Fort",
    80 : "Très fort"
}

def nb_min(password : str) -> int :
    #On met tous les caractères minuscules dans une liste, puis on regarde la taille de cette liste
    return len([char for char in password if char in string.ascii_lowercase])

def nb_maj(password : str) -> int :
    return len([char for char in password if char in string.ascii_uppercase])

def nb_non_alpha(password : str) -> int :
    return len([char for char in password if char not in string.ascii_letters])

def longueur_max_in_set(password : str, set : str) -> int:
    max = 0
    current_suite = ""
    for char in password :
        if char in set :
            current_suite += char
        else :
            if current_suite != "" :
                if (len(current_suite) > max) :
                    max = len(current_suite)
                current_suite = ""

    if (len(current_suite) > max) :
        max = len(current_suite)

    return max

def long_min(password : str) -> int :
    return longueur_max_in_set(password, string.ascii_lowercase)
    
def long_maj(password : str) -> int :
    return longueur_max_in_set(password, string.ascii_uppercase)

def score(password : str) -> int :
    score : int
    lg_password = len(password)
    #Bonus
    score = lg_password * 4
    score += (lg_password - long_maj(password)) * 2
    score += (lg_password - long_min(password)) * 3
    score += nb_non_alpha(password) * 5


    #Malus
    score -= long_maj(password) * 3
    score -= long_min(password) * 2

    return score



def comment_password(password : str) -> str :
    #Cette fonction analyse le mot de passe puis ajoute le commentaire associé dans le dictionnaire
    pwd_score = score(password)
    print(f"Le mot de passe a un score de {pwd_score}")
    current_max_score_commented = 0
    for comment_score in dict_comment.keys() :
        if pwd_score > comment_score and comment_score > current_max_score_commented:
            current_max_score_commented = comment_score

    return (dict_comment[current_max_score_commented])


if __name__ == "__main__" :
    print("Test de fiabilité de votre mot de passe.")
    password = getpass("Entrez le ci-contre : ")
    print(comment_password(password))