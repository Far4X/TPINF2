from __future__ import annotations
import csv
import os
import control
import functiontools

class Etudiant :
    @classmethod
    def from_dict(cls, values) -> Etudiant:
        if type(values) != dict :
            raise TypeError("Vous n'avez pas entré un dictionnaire.")
    
        nom = dict.get(values, "Nom", None)
        annee = dict.get(values, "Date_de_naissance", None)
        gpa = dict.get(values, "Gpa", None)
        connais_python = dict.get(values, "Connais_python", None)

        if (nom == None) :
            raise ValueError("Pas de nom trouvé")
        
        if (annee == None) :
            raise ValueError("Pas d'année trouvée")
        try : 
            annee = int(annee)
        except ValueError :
            raise ValueError("Impossible de passer l'année en entier")
        
        if (gpa == None) :
            raise ValueError("Pas de GPA trouvée")
        try : 
            gpa = float(gpa)
        except ValueError :
            raise ValueError("Impossible de passer la gpa en floattant")
        
        if (connais_python == None) :
            raise ValueError("Pas d'information sur python trouvée")
        if connais_python in ["True", "False"] :
            connais_python = True if connais_python == "True" else False
        else :
            raise ValueError("Impossible de passer connais python en booléen")
                
        return Etudiant(nom, annee, gpa, connais_python)
    
        

    def __init__(self, nom, naissance, gpa, connais_python) :
        self.nom = nom
        self.annee_de_naissance = naissance
        self.gpa = gpa
        self.connais_python = connais_python

    @property
    def nom(self) -> str:
        return self._name
    
    @nom.setter
    def nom(self, val : str | object) -> None :
        self._name = str(val)

    @property
    def annee_de_naissance(self) -> int :
        return self._bday
    
    @annee_de_naissance.setter
    def annee_de_naissance(self, val : int) -> None:
        if type(val) == int :
            if val > 1900 and val < 2025 :
                self._bday = val
            else :
                raise ValueError("Année de naissance non valide")
        else :
            raise TypeError("Type de l'année non valide. Entier.")
        
    @property
    def gpa(self) -> float:
        return self._gpa
    
    @gpa.setter
    def gpa(self, val : float | int) -> None:
        if type(val) == float or type(val) == int :
            if val >= 0 and val <= 5 :
                self._gpa = val
            else :
                raise ValueError("GPA non valide.")
        else :
            raise TypeError("Type du GPA non valide. Entier.")
        
    @property
    def connais_python(self) -> bool:
        return self._knpy
    
    @connais_python.setter
    def connais_python(self, val : bool) :
        if isinstance(val, bool) :
            self._knpy = val
        else :
            raise TypeError("Connais python n'est pas de type bool.")
        
    def to_dict(self) -> dict:
        dct = {}
        dct["Nom"] = self.nom
        dct["Date_de_naissance"] = self.annee_de_naissance
        dct["Gpa"] = self.gpa
        dct["Connais_python"] = self.connais_python
        return dct
    
    def __str__(self) :
        return f"Nom : {self.nom}, né(e) en {self.annee_de_naissance}, avec une GPA de {self.gpa}. {"Connait le python." if self.connais_python else "Ne connait pas le python."}"
    

class Groupe :
    @classmethod
    def charger(cls, file : str) -> Groupe :
        if not os.path.isfile(file) :
            raise ValueError("Impossible de trouver le fichier.")
        
        new_gr = Groupe(file)
        with open(file, "r", newline="", encoding="UTF-8") as f:
            reader = csv.DictReader(f)
            for row in reader :
                new_gr.addEtu(Etudiant.from_dict(row))

        return new_gr
    

    def __init__(self, file : str = "Etu") -> None :
        self._etu = []
        self.file = file

    def __str__(self) :
        list_etu_str = ""
        for etu in self.list_etu :
            list_etu_str += str(etu) + "\n"
        
        return f"Groupe dont le fichier de sauvegarde est {self.file}. Liste des étudiants : \n{list_etu_str}"

    @property
    def list_etu(self) -> list[Etudiant]:
        return self._etu
    
    def addEtu(self, etu : Etudiant) -> None :
        if isinstance(etu, Etudiant) :
            self._etu.append(etu)
        else :
            raise TypeError("Impossible d'ajouter autre chose qu'un étudiant")
        

    @property
    def file(self) -> str:
        return self._file + (".csv" if (self._file[-4:] != ".csv") else "")
    
    @file.setter
    def file(self, val : str | object) :
        self._file = str(val)

    def sauvegarder(self) -> None :
        with open(self.file, "w", newline = "") as f :
            header = ["Nom", "Date_de_naissance", "Gpa", "Connais_python"]
            writer = csv.DictWriter(f, fieldnames=header)

            writer.writeheader()
            for student in self.list_etu :
                writer.writerow(student.to_dict())
            

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


def creerGroupe(list_groups : list[Groupe]) :
    list_et = Groupe(control.secureAskType(str, "Nom du fichier : "))
    
    while control.secureAskType(int, "Voulez vous ajouter un nouvel étudiant ? : (0/1) : ", lambda x : (x == 0 or x == 1)) :
        creerEtu(list_et)

    list_groups.append(list_et)

def printListGroupes(list_groups : list[Groupe]) :
    for group in list_groups :
        print(group)

def creerEtu(group : Groupe) -> None :
    nom = control.secureAskType(str, "Entrez le nom de l'étudiant : ")
    naiss = control.secureAskType(int, "Entrez l'année de naissance de l'étudiant : ", lambda x : 1900 < x < 2025, "Vous n'avez pas entré un entier", "L'année n'est pas valide. Réessayez : ")
    gpa = control.secureAskType(float, "Entrez la gpa de l'étudiant : ", lambda x : 0 <= x <= 5,  "Vous n'avez pas entré un flottant", "La gpa n'a pas une valeur valide. Réessayez : ")
    connais_python = control.secureAskType(int, "L'étudiant connait-il python ? (0/1) : ", lambda x : (x == 0 or x == 1))
    group.addEtu(Etudiant(nom, naiss, gpa, bool(connais_python)))


def loadFile(list_gr : list[Groupe]) :
    path = control.secureAskType(str, "Entrez le nom du fichier : ")
    try : 
        list_gr.append(Groupe.charger(path))
        print("Groupe chargé")
    except ValueError as e:
        print(f"Erreur : {e}")

def saveAGroup(list_gr : list[Groupe]) :
    gr = control.secureDisplayAndPick(list_gr, "Sélectionnez le groupe à enregistrer : ", 1)
    gr.sauvegarder()
    print("Groupe sauvegardé")


if __name__ == "__main__" :
    main()