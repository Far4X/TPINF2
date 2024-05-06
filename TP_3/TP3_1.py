class Rectangle:
    def __init__(self, longueur, largeur):
        self.set_longueur(longueur)
        self.set_largeur(largeur)

    def get_longueur(self):
        return self.longueur

    def get_largeur(self):
        return self.largeur

    def switch(self):  # Cette méthode interchange la longueur et la largeur car la longueur est par convention
        # la mesure la plus grande
        if self.get_longueur() < self.get_largeur():
            temp = self.get_longueur()
            self.set_longueur(self.get_largeur())
            self.set_largeur(temp)

    def set_longueur(self, longueur):
        if not isinstance(longueur, float) and not isinstance(longueur, int):
            raise TypeError("La longueur doit être un nombre(int ou float).")
        self.longueur = float(longueur)

    def set_largeur(self, largeur):
        if not isinstance(largeur, float) and not isinstance(largeur, int):
            raise TypeError("La largeur doit être un nombre (int ou float).")
        self.largeur = float(largeur)

    def perimetre(self):
        return (self.get_longueur() + self.get_largeur())*2

    def aire(self):
        return self.get_longueur() * self.get_largeur()

    def est_carre(self):
        return self.get_longueur() == self.get_largeur()

    def le_plus_grand(self, other):
        if self.aire() > other.aire():
            return self
        else:
            return other

    def afficher(self):
        print(f"La longueur: [{self.get_longueur()}] - Largeur: [{self.get_largeur()}]", end=" - ")
        print(f"Périmètre: [{self.perimetre()}] - Aire: [{self.aire()}]", end=" - ")
        if self.est_carre():
            print(f"C'est un carré.")
        else:
            print(f"Ce n'est pas un carré")


def main():
    r1 = Rectangle(3, 3)  # Carré
    r2 = Rectangle(2, 3)  # Longueur < Largeur
    r1.switch(), r2.switch()
    r1.afficher(), r2.afficher()


if __name__ == "__main__":
    main()
