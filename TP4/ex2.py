from __future__ import annotations
import csv
import os
import pickle
import control

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
    def nom(self) :
        return self._name
    
    @nom.setter
    def nom(self, val) :
        self._name = str(val)

    @property
    def annee_de_naissance(self) :
        return self._bday
    
    @annee_de_naissance.setter
    def annee_de_naissance(self, val) :
        if type(val) == int :
            if val > 1900 and val < 2025 :
                self._bday = val
            else :
                raise ValueError("Année de naissance non valide")
        else :
            raise TypeError("Type de l'année non valide. Entier.")
        
    @property
    def gpa(self) :
        return self._gpa
    
    @gpa.setter
    def gpa(self, val) :
        if type(val) == float or type(val) == int :
            if val >= 0 and val <= 5 :
                self._gpa = val
            else :
                raise ValueError("GPA non valide.")
        else :
            raise TypeError("Type du GPA non valide. Entier.")
        
    @property
    def connais_python(self) :
        return self._knpy
    
    @connais_python.setter
    def connais_python(self, val) :
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
        return f"Nom : {self.nom}, né(e) en {self.annee_de_naissance}, avec une GPA de {self.gpa}. {"Connait le python" if self.connais_python else "Ne connait pas le python"}"
    

class Groupe :
    @classmethod
    def charger(cls, file) :
        if not os.path.isfile(file) :
            raise ValueError("Impossible de trouver le fichier.")
        
        new_gr = Groupe(file)
        with open(file, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader :
                new_gr.addEtu(Etudiant.from_dict(row))

        return new_gr
    

    def __init__(self, file = "Etu") :
        self._etu = []
        self.file = file

    @property
    def etu(self) -> list[Etudiant]:
        return self._etu
    
    def addEtu(self, etu) :
        if isinstance(etu, Etudiant) :
            self._etu.append(etu)
        else :
            raise TypeError("Impossible d'ajouter autre chose qu'un étudiant")
        

    @property
    def file(self) :
        return self._file + (".csv" if (self._file[-4:] != ".csv") else "")
    
    @file.setter
    def file(self, val) :
        self._file = str(val)

    def sauvegarder(self) :
        with open(self.file, "w", newline = "") as f :
            header = ["Nom", "Date_de_naissance", "Gpa", "Connais_python"]
            writer = csv.DictWriter(f, fieldnames=header)

            writer.writeheader()
            for student in self.etu :
                writer.writerow(student.to_dict())
            

def main() :

    list_et = Groupe()
    
    while control.secureAskType(int, "Continuer ? : (0/1) : ", lambda x : (x == 0 or x == 1)) :
        creerEtu(list_et)


    print(list_et.file)
    list_et.sauvegarder()
    
    print("L1")
    for etu in list_et.etu :
        print(etu)

    list_etu_2 = Groupe.charger("Etu.csv")

    print("L2: ")
    for etu in list_etu_2.etu :
        print(etu)

def creerEtu(group : Groupe) :
    nom = control.secureAskType(str, "Entrez le nom de l'étudiant : ")
    naiss = control.secureAskType(int, "Entrez l'année de naissance de l'étudiant : ", lambda x : 1900 < x < 2025, "Vous n'avez pas entré un entier", "L'année n'est pas valide. Réessayez : ")
    gpa = control.secureAskType(float, "Entrez la gpa de l'étudiant : ", lambda x : 0 <= x <= 5,  "Vous n'avez pas entré un flottant", "La gpa n'a pas une valeur valide. Réessayez : ")
    connais_python = control.secureAskType(int, "L'étudiant connait-il python ? (0/1) : ", lambda x : (x == 0 or x == 1))
    group.addEtu(Etudiant(nom, naiss, gpa, bool(connais_python)))

if __name__ == "__main__" :

    main()


