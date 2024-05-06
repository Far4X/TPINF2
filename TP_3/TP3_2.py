from __future__ import annotations
import inputControl

class PoupeeRusse :
    def __init__(self, nom : str, taille : int) -> None:
        self.nom = nom
        self.taille = taille
        self.est_ouverte = False
        self.dans = None
        self.contient = None


    @property
    def nom(self) -> str:
        return self.__nom

    @nom.setter
    def nom(self, val : str) -> None:
        self.__nom = str(val)

    @property
    def taille(self) -> int:
        return self.__taille

    @taille.setter
    def taille(self, can_val : int) :
        if (isinstance(can_val, int)) :
            self.__taille = can_val
        else :
            raise TypeError("Taille non entière")

    @property
    def est_ouverte(self) -> bool:
        return self.__isopen

    @est_ouverte.setter
    def est_ouverte(self, can_val : bool) -> None :
        if isinstance(can_val, bool) :
            self.__isopen = can_val
        else :
            raise TypeError("Est_ouverte non booléen")

    @property
    def dans(self) :
        return self.__sup

    @dans.setter
    def dans(self, can_val : PoupeeRusse) -> None :
        if isinstance(can_val, PoupeeRusse) or can_val == None:
            self.__sup = can_val
        else :
            raise TypeError("Pas une poupée russe")

    @property
    def contient(self) -> PoupeeRusse | None:
        return self.__cont

    @contient.setter
    def contient(self, can_val : PoupeeRusse) :
        if isinstance(can_val, PoupeeRusse) or can_val == None:
            self.__cont = can_val
        else :
            raise TypeError("Pas une poupée russe")

    def ouvrir(self) -> None:
        if self.dans == None and self.est_ouverte == False :
            print("Ouverture")
            self.est_ouverte = True

    def fermer(self) -> None:
        if self.dans == None and self.est_ouverte == True :
            print("Fermeture")
            self.est_ouverte = False

    def placer_dans(self, oth : PoupeeRusse) -> int :
        if not isinstance(oth, PoupeeRusse) :
            raise TypeError("Oth non valide")
        if (self.est_ouverte != False) :
            return 3
        if (self.dans != None) :
            return 2
        if (oth.taille < self.taille) :
            return 1
        if (oth.contient != None) :
            return 4
        if (oth.est_ouverte != True) :
            return 5

        oth.contient = self
        self.dans = oth
        return 0

    def sortir_de(self) -> int :
        if (self.dans == None) :
            return 1
        if not self.dans.est_ouverte :
            return 2
        self.dans.contient = None
        self.dans = None
        return 0

    def __str__(self) -> str:
        r = ""
        if self.dans != None :
            r += f"Poupée contenante : {self.dans.nom}. "
        if self.contient != None :
            r += f"Poupée contenue : {self.contient.nom}. "
        if self.est_ouverte :
            status = "est ouverte"
        else :
            status = "n'est pas ouverte"
        return f"Poupée russe de nom {self.nom}, de taille {self.taille}, {status}. " + r


def createPoupee() -> PoupeeRusse:
    """Permet d'instancier en toute sérenneté une poupée."""
    nom = inputControl.secureAskType(str, "Quel est le nom de la poupée : ", lambda x : len(x) > 0)
    taille = inputControl.secureAskType(int, "Quelle est sa taille (entier) : ", lambda x : x > 0)
    return PoupeeRusse(nom, taille)


def insererPoupee(list_poupees : list[PoupeeRusse]) -> None:
    """Permet d'appeler et d'interpréter le résultat de la méthode PoupeeRusse.placer_dans()"""
    p1 = inputControl.secureDisplayAndPick(list_poupees, "Entrez l'identificateur de la poupée à placer dans l'autre : ", 1)
    p2 = inputControl.secureDisplayAndPick(list_poupees, "Entrez l'identificateur de la poupée qui va recevoir : ", 1)
    result = p1.placer_dans(p2)
    match result :
        case 0 :
            print(f"La poupée {p1.nom} a bien été placée dans {p2.nom}.")
        case 1 :
            print(f"La poupée {p1.nom} est trop grande pour {p2.nom} !")
        case 2 :
            print(f"La poupée {p1.nom} est déjà dans {p1.dans.nom} !")
        case 3 :
            print(f"La poupée {p1.nom} est ouverte. Merci de la fermer avant l'opération.")
        case 4 :
            print(f"La poupée {p2.nom} contient déjà {p2.contient.nom}")
        case 5 :
            print(f"La poupée {p2.nom} est fermée.")

def sortirPoupee(poupee : PoupeeRusse) :
    """Permet d'appeler et d'interpréter le résultat de la méthode PoupeeRusse.sortir_de()"""
    result = poupee.sortir_de()
    match result :
        case 0 :
            print(f"Opération réussie : {poupee}")
        case 1 :
            print(f"La poupee {poupee.nom} n'est contenue dans aucune poupée !")
        case 2 :
            print(f"La poupee parente, {poupee.dans.nom}, n'est pas ouverte !")



def main() :
    """Permet de manipuler les poupées (Plus simple pour les tests)"""
    try:
        continuer = True
        list_poupees = []
        while continuer :
            print("Que voulez-vous faire : ")
            print("0 : Quitter")
            print("1 : Créer une poupée")
            print("2 : Ouvrir une poupée")
            print("3 : Fermer une poupée")
            print("4 : Mettre une poupée dans une autre")
            print("5 : Sortir une poupée de sa contenante")
            print("6 : Afficher la liste des poupées")

            in_list = lambda x : (x >= -1 and x < 7)
            option = inputControl.secureAskType(int, "Quelle option choissez-vous ? ", in_list)
            arg_display_and_pick = (list_poupees, "Entrez un identificateur de poupée : ", 1)
            match option :
                case 0 :
                    continuer = False
                case 1 :
                    list_poupees.append(createPoupee())
                case 2 :
                    if len(list_poupees) > 0 :
                        inputControl.secureDisplayAndPick(*arg_display_and_pick).ouvrir()
                    else:
                        print("Vous n'avez aucune poupée à ouvrir.")
                case 3 :
                    if len(list_poupees) > 0 :
                        inputControl.secureDisplayAndPick(*arg_display_and_pick).fermer()
                    else:
                        print("Vous n'avez aucune poupée à fermer.")
                case 4 :
                    if len(list_poupees) >= 2 :
                        insererPoupee(list_poupees)
                    else:
                        print("Vous n'avez pas assez de poupées.")
                case 5:
                    if len(list_poupees) >= 2 :
                        sortirPoupee(inputControl.secureDisplayAndPick(*arg_display_and_pick))
                    else:
                        print("Vous n'avez pas assez de poupées.")
                case 6 :
                    if len(list_poupees) == 0:
                        print("Rien à afficher.")
                    else:
                        for poupee in list_poupees :
                            print(poupee)
    except ValueError as ve:
        print(ve)
    except TypeError as te:
        print(te)

if __name__ == "__main__" :
    main()






