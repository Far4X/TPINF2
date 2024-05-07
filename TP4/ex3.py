import ex2
import os
import pickle
import control
import functiontools

class GroupeBin(ex2.Groupe) :
    @classmethod
    def charger(cls, file) :
        if not os.path.isfile(file) :
            raise ValueError("Impossible de trouver le fichier.")
        
        new_gr = ex2.Groupe(file)
        with open(file, "rb") as f:
            list_et = pickle.load(f)

        for etu in list_et :
            new_gr.addEtu(etu)

        return new_gr
    
    @property
    def file(self) -> str:
        return self._file + (".bin" if (self._file[-4:] != ".bin") else "")
    
    @file.setter
    def file(self, val : str | object) -> str :
        self._file = str(val)

    def sauvegarder(self) -> None :
        with open(self.file, "wb") as f:
            pickle.dump(self.list_etu, f)


def main() -> None :
    list_groupes = []
    creerGroupep = functiontools.PrintableFunction(creerGroupe, "Créer un groupe", list_groupes)
    printGroups = functiontools.PrintableFunction(printListGroupes, "Afficher la liste des groupes", list_groupes)
    saveAGroupPrintable = functiontools.PrintableFunction(saveAGroup, "Sauvegarder un groupe", list_groupes)
    loadAGroup = functiontools.PrintableFunction(loadFile, "Charger un groupe dans un fichier", list_groupes)
    quit_b = functiontools.PrintableFunction(quit, "Quitter")


    list_act = [quit_b, creerGroupep, printGroups, saveAGroupPrintable, loadAGroup]

    while 1 :
        ans = control.secureDisplayAndPick(list_act)
        ans()


def creerGroupe(list_groups : list[GroupeBin]) :
    list_et = GroupeBin(control.secureAskType(str, "Nom du fichier : "))
    
    while control.secureAskType(int, "Voulez vous ajouter un nouvel étudiant ? : (0/1) : ", lambda x : (x == 0 or x == 1)) :
        creerEtu(list_et)

    list_groups.append(list_et)

def printListGroupes(list_groups : list[GroupeBin]) :
    for group in list_groups :
        print(group)

def creerEtu(group : GroupeBin) -> None :
    nom = control.secureAskType(str, "Entrez le nom de l'étudiant : ")
    naiss = control.secureAskType(int, "Entrez l'année de naissance de l'étudiant : ", lambda x : 1900 < x < 2025, "Vous n'avez pas entré un entier", "L'année n'est pas valide. Réessayez : ")
    gpa = control.secureAskType(float, "Entrez la gpa de l'étudiant : ", lambda x : 0 <= x <= 5,  "Vous n'avez pas entré un flottant", "La gpa n'a pas une valeur valide. Réessayez : ")
    connais_python = control.secureAskType(int, "L'étudiant connait-il python ? (0/1) : ", lambda x : (x == 0 or x == 1))
    group.addEtu(ex2.Etudiant(nom, naiss, gpa, bool(connais_python)))


def loadFile(list_gr : list[GroupeBin]) :
    path = control.secureAskType(str, "Entrez le nom du fichier : ")
    try : 
        list_gr.append(GroupeBin.charger(path))
        print("Groupe chargé")
    except ValueError as e:
        print(f"Erreur : {e}")

def saveAGroup(list_gr : list[GroupeBin]) :
    gr = control.secureDisplayAndPick(list_gr, "Sélectionnez le groupe à enregistrer : ", 1)
    gr.sauvegarder()
    print("Groupe sauvegardé")


if __name__ == "__main__" :
    main()


"""Ici, le mode texte nous permet de pouvoir visualiser les données sans utiliser directement le programme.
On peut donc également plus facilement les exploiter avec un autre programme.
Le mode binaire permet, au contraire, de passer obligatoirement le programme. Cela peut être utile lorsque l'on veut
obfusquer l'accès aux données.

Le mode binaire permet plus facilement de stocker des données complexes, comme par exemple un arbre binaire de recherche
qu'il est plus dur, de part leur nature, d'enregistrer sous forme textuelle.
Le mode binaire peut, dans le cas d'une mauvaise optimisation lors de l'utilisation des fichiers texte, se révéler plus
économe en stockage. De plus, la lecture en binaire peut parfois être plus rapide que celle en clair."""