from __future__ import annotations

class Rectangle:
    """Classe définissant un rectangle. 
    Deux attributs : longueur et largeur tels que longueur >= largeur théoriquement"""
    def __init__(self, longueur : float | int, largeur : float | int):
        self.set_longueur(longueur, True)
        self.set_largeur(largeur)

    def get_longueur(self) -> float :
        """Donne la longueur du rectangle"""
        return self.longueur

    def get_largeur(self) -> float:
        """Donne la largeur du rectangle"""
        return self.largeur

    def switch(self) -> None: 
        """Méthode qui vérifie si la largeur est plus grande que la longueur.
        Les échange si c'est le cas"""
        if self.get_longueur() < self.get_largeur():
            temp = self.get_longueur()
            self.set_longueur(self.get_largeur())
            self.set_largeur(temp)

    def set_longueur(self, longueur : float | int, skip_check : bool = False) -> None :
        """Permet de régler la longueur du rectangle. 
        Echange longueur et largeur si longueur < largeur"""
        if not isinstance(longueur, float) and not isinstance(longueur, int):
            raise TypeError("La longueur doit être un nombre(int ou float).")
        self.longueur = float(longueur)
        if not skip_check :
            self.switch()

    def set_largeur(self, largeur : float | int, skip_check : bool = False) -> None :
        """Permet de régler la longueur du rectangle. 
        Echange longueur et largeur si longueur < largeur"""
        if not isinstance(largeur, float) and not isinstance(largeur, int):
            raise TypeError("La largeur doit être un nombre (int ou float).")
        self.largeur = float(largeur)
        if not skip_check :
            self.switch()

    def perimetre(self) -> float :
        """Donne le périmètre du rectanfle"""
        return (self.get_longueur() + self.get_largeur())*2

    def aire(self) -> float :
        """Retourne l'aire du rectangle"""
        return self.get_longueur() * self.get_largeur()

    def est_carre(self) -> float :
        """Permet de savoir si un rectangle est un carré ou non"""
        return self.get_longueur() == self.get_largeur()

    def le_plus_grand(self, other : Rectangle) -> Rectangle :
        """Permet de comparer entre eux deux rectangles"""
        if not isinstance(other, Rectangle) :
            raise TypeError("Comparaison entre un rectangle et autre chose impossible") #-> Si on avait d'autres formes, on pourrait définir une classe abstraite shape, mère de toutes les autres formes, avec une méthode aire surchargée
        if self.aire() > other.aire():
            return self
        else:
            return other

    def afficher(self) -> None :
        """Permet l'affichage du rectangle selon le cahier des charges"""
        print(f"La longueur: [{self.get_longueur()}] - Largeur: [{self.get_largeur()}]", end=" - ")
        print(f"Périmètre: [{self.perimetre()}] - Aire: [{self.aire()}]", end=" - ")
        if self.est_carre():
            print("C'est un carré.")
        else:
            print("Ce n'est pas un carré")


def main():
    r1 = Rectangle(3, 3)  # Carré
    r2 = Rectangle(2, 3)  # Longueur < Largeur
    r1.afficher()
    r2.afficher()
    print("---Comaparaison de r1 et r2---")
    print("Le rectangle de paramètres", end="")
    r1.le_plus_grand(r2).afficher()
    print("est plus grand")


if __name__ == "__main__":
    main()
