"""Ce module permet sécuriser le type des inputs."""


def getint() -> int:
    ans = None
    while type(ans) != int :
        ans = input("Entrez un entier : ")
        try :
            ans = int(ans)
        except ValueError :
            print("None valide")

    return ans


def getString() -> str :
    return input("Entrez une chaine de caractères : ")

def getSet() -> set :
    m_set = set()
    ans = "a"
    while True :
        while ans[0] != "y" and ans[0] != "n" :
            ans = input("Voulez vous insérer un autre élément ? (y/n) : ")
        if ans[0] == 'n' :
            break

        ans = input("Nouvel élément : ")
        m_set.add(ans)
    return set