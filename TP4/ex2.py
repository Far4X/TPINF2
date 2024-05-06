from __future__ import annotations
import csv
import os
import pickle

class Etudiant :
    @classmethod
    def from_dict(cls, values) -> Etudiant:
        if type(values) != dict :
            raise TypeError("Vous n'avez pas entré un dictionnaire.")

        #Tres bon code, je t'offre 100000€
    
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
    def charger_csv(cls, file) :
        if not os.path.isfile(file) :
            raise ValueError("Impossible de trouver le fichier.")
        
        new_gr = Groupe(file)
        
        with open(file, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader :
                new_gr.addEtu(Etudiant.from_dict(row))

        return new_gr
    
    @classmethod
    def loadFromBin(cls, file) :
        if not os.path.isfile(file) :
            raise ValueError("Impossible de trouver le fichier.")
        
        new_gr = Groupe(file)
        with open(file, "rb") as f:
            list_et = pickle.load(f)

        for etu in list_et :
            new_gr.addEtu(etu)

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
    
    @property
    def file_bin(self) :
        return self._file + (".bin" if (self._file[-4:] != ".bin") else "")
    
    @file.setter
    def file(self, val) :
        self._file = str(val)

    def sauvegarder_csv(self) :
        with open(self.file, "w", newline = "") as f :
            header = ["Nom", "Date_de_naissance", "Gpa", "Connais_python"]
            writer = csv.DictWriter(f, fieldnames=header)

            writer.writeheader()
            for student in self.etu :
                writer.writerow(student.to_dict())

    def sauvegarderBin(self) :
        with open(self.file_bin, "wb") as f:
            pickle.dump(self.etu, f)

            

def main() :
    etu1 = Etudiant("RR", 2005, 5, True)
    etu2 = Etudiant("AP", 2005, 5, True)

    list_et = Groupe()
    list_et.addEtu(etu1)
    list_et.addEtu(etu2)

    print(list_et.file)
    list_et.sauvegarder_csv()
    list_et.sauvegarderBin()
    
    print("L1")
    for etu in list_et.etu :
        print(etu)

    list_etu_2 = Groupe.charger_csv("Etu.csv")
    list_etu_3 = Groupe.loadFromBin("Etu.bin")

    print("L2: ")
    for etu in list_etu_2.etu :
        print(etu)

    print("L3: ")
    for etu in list_etu_3.etu :
        print(etu)

if __name__ == "__main__" :
    main()