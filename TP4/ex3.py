import ex2
import os
import pickle
import control

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
            pickle.dump(self.etu, f)


def main() -> None:
    list_et = GroupeBin()
    
    while control.secureAskType(int, "Continuer ? : (0/1) : ", lambda x : (x == 0 or x == 1)) :
        creerEtu(list_et)


    print(list_et.file)
    list_et.sauvegarder()
    
    print("L1")
    for etu in list_et.etu :
        print(etu)

    list_etu_2 = GroupeBin.charger("Etu.bin")

    print("L2: ")
    for etu in list_etu_2.etu :
        print(etu)


def creerEtu(group : GroupeBin) -> None :
    nom = control.secureAskType(str, "Entrez le nom de l'étudiant : ")
    naiss = control.secureAskType(int, "Entrez l'année de naissance de l'étudiant : ", lambda x : 1900 < x < 2025, "Vous n'avez pas entré un entier", "L'année n'est pas valide. Réessayez : ")
    gpa = control.secureAskType(float, "Entrez la gpa de l'étudiant : ", lambda x : 0 <= x <= 5,  "Vous n'avez pas entré un flottant", "La gpa n'a pas une valeur valide. Réessayez : ")
    connais_python = control.secureAskType(int, "L'étudiant connait-il python ? (0/1) : ", lambda x : (x == 0 or x == 1))
    group.addEtu(ex2.Etudiant(nom, naiss, gpa, bool(connais_python)))

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