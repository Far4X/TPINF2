import random
pokedex = {
    "Bulbasaur": ("Plante", 45, 49),
    "Ivysaur": ("Plante", 60, 62),
    "Venusaur": ("Plante", 80, 82),
    "Charmander": ("Feu", 39, 52),
    "Charmeleon": ("Feu", 58, 64),
    "Charizard": ("Feu", 78, 84),
    "Squirtle": ("Eau", 44, 48),
    "Wartortle": ("Eau", 59, 63),
    "Blastoise": ("Eau", 79, 83),
    "Pidgey": ("Normal", 40, 45),
    "Pidgeotto": ("Normal", 63, 60),
    "Pidgeot": ("Normal", 83, 80),
    "Rattata": ("Normal", 30, 56),
    "Raticate": ("Normal", 55, 81),
    "Spearow": ("Normal", 40, 60),
    "Fearow": ("Normal", 65, 90)
}


class Pokemon:
    """
    Classe repésentant un Pokémon non typé.
    Attributs :
    name (str) : Nom du Pokémon
    pv (int) : Points de vie du Pokémon
    atk (int) : Points de dégâts du Pokémon
    """
    def __init__(self, nom, pv, atk):
        self.nom = nom
        self.pv = pv
        self.pv_max = pv
        self.atk = atk

    @property
    def nom(self):
        return self._nom

    @nom.setter
    def nom(self, nom):
        if not isinstance(nom, str):
            raise TypeError("Le nom du Pokémon doit être de type str.")
        self._nom = nom

    @property
    def pv(self):
        return self._pv

    @pv.setter
    def pv(self, pv):
        if not isinstance(pv, int):
            raise TypeError("Les points de vie du Pokemon doivent être de type int.")
        if pv < 0:
            self._pv = 0
        else:
            self._pv = pv

    @property
    def atk(self):
        return self._atk

    @atk.setter
    def atk(self, atk):
        if not isinstance(atk, int):
            raise TypeError("Les Les points de dégâts du Pokémon doivent être de type int.")
        if atk < 0:
            raise ValueError("Les points de dégâts du Pokémon doivent être positifs.")
        self._atk = atk

    def est_ko(self):
        return self.pv <= 0

    @staticmethod  # Utilisé pour éviter la confusion de ce décorateur avec un méthode de classe
    def bonus(func):
        """
        Le principe de ce décorateur est d'établir la hiérarchie des avantages de type de manière cyclique,
        en utilisant la logique mathématique du modulo.
        J'ai opté pour l'utilisation d'un décorateur au lieu de la méthode calc_multiplicateur(self, autre)
        pour plus de généralisation.
        :param func: function
        :return: func décorée par le multiplicateur d'avantage et les messages d'efficacité
        """
        def wrapper(self, other):
            if not isinstance(self, PokemonNormal) and not isinstance(other, PokemonNormal):  # self & other non normaux
                if isinstance(self, type(other)) or other.hierarchie != (self.hierarchie + 1) % 3:
                    multiplicateur = 0.5  # Multiplicateur en cas de désavantage de type
                    efficacite = "Ce n'est pas très efficace..."
                else:
                    multiplicateur = 2  # Multiplicateur en cas d'avantage de type
                    efficacite = "C'est super efficace !"
            else:
                multiplicateur = 1  # Multiplicateur associé au type normal
                efficacite = None
            return func(self, other, multiplicateur, efficacite)
        return wrapper

    @bonus
    def attaquer(self, autre, multiplicateur, efficacite):
        print(f"{self.print_nom()} attaque {autre.print_nom()}.")
        degats = round((random.randint(0, self.atk)) * multiplicateur)
        print(f"\033[31m -{degats} \033[0m")
        if degats > autre.pv:
            print(f"Le pokemon {autre.print_nom()} a perdu {autre.pv} PV(s) !", end=" ")
            autre.pv = 0
            print(f"{autre}")
        else:
            autre.pv -= degats
            print(f"Le pokemon {autre.print_nom()} a perdu {degats} PV(s) ! {autre}")
        if efficacite is not None:
            print(efficacite)

    def combattre(self, autre):
        state = True
        tours = 0
        while state:
            print(f"======================================\nTour {tours + 1} :\n======================================")
            self.attaquer(autre)
            tours += 1
            if autre.est_ko():
                print(f"Le Pokémon {autre.print_nom()} est K.O. !")
                return self, tours
            else:
                autre.attaquer(self)
                if self.est_ko():
                    print(f"Le Pokémon {self.print_nom()} est K.O. !")
                    return autre, tours

    def reset_pv(self):
        """
        Méthode pour s'assurer que les PVs des Pokémons sont réinitialisés à chaque exécution.
        """
        self.pv = self.pv_max

    def print_nom(self):
        return f"{self.nom}"

    def __str__(self):
        """
        Méthode qui affiche les détails (PVs et ATK) du Pokémon.
        :return: fstring contenant PVs et ATK
        """
        return f"[PV(s):{self.pv}; ATK:{self.atk}]"


class PokemonNormal(Pokemon):
    """
    Classe repésentant un Pokémon de type normal et héritant de la classe Pokemon.
    Les Pokémons normaux infligent et reçoivent des dégâts normaux de tous les types.
    """
    def __init__(self, nom, pv, atk):
        Pokemon.__init__(self, nom, pv, atk)


class PokemonFeu(Pokemon):
    """
    Classe repésentant un Pokémon de type feu et héritant de la classe Pokemon.
    Les Pokémons feu font deux fois plus de dégâts aux Pokémons plante mais font deux fois
    moins de dégâts aux Pokémons eau ou feu.
    L'attribut hierarchie sert à établir l'aventage du type de manière cyclique à l'aide de
    l'opération modulo utilisée dans le décorateur bonus.
    """
    def __init__(self, nom, pv, atk):
        Pokemon.__init__(self, nom, pv, atk)
        self.hierarchie = 0

    def print_nom(self):
        return f"\033[38;2;255;165;0m{self.nom}\033[0m"


class PokemonPlante(Pokemon):
    """
    Classe repésentant un Pokémon de type plante et héritant de la classe Pokemon.
    Les Pokémons plante font deux fois plus de dégâts aux Pokémons eau mais font deux fois
    moins de dégâts aux Pokémons plante ou feu.
    L'attribut hierarchie sert à établir l'aventage du type de manière cyclique à l'aide de
    l'opération modulo utilisée dans le décorateur bonus.
    """
    def __init__(self, nom, pv, atk):
        Pokemon.__init__(self, nom, pv, atk)
        self.hierarchie = 1

    def print_nom(self):
        return f"\033[32m{self.nom}\033[0m"


class PokemonEau(Pokemon):
    """
    Classe repésentant un Pokémon de type normal et héritant de la classe Pokemon.
    Les Pokémons eau font deux fois plus de dégâts aux Pokémons feu mais font deux fois
    moins de dégâts aux Pokémons eau ou plante.
    L'attribut hierarchie sert à établir l'aventage du type de manière cyclique à l'aide de
    l'opération modulo utilisée dans le décorateur bonus.
    """
    def __init__(self, nom, pv, atk):
        Pokemon.__init__(self, nom, pv, atk)
        self.hierarchie = 2

    def print_nom(self):
        return f"\033[34m{self.nom}\033[0m"


def main():
    try:
        pokemon_plante = [PokemonPlante(nom, stats[1], stats[2]) for nom, stats in pokedex.items()
                          if stats[0] == "Plante"]
        pokemon_feu = [PokemonFeu(nom, stats[1], stats[2]) for nom, stats in pokedex.items() if stats[0] == "Feu"]
        pokemon_eau = [PokemonEau(nom, stats[1], stats[2]) for nom, stats in pokedex.items() if stats[0] == "Eau"]
        pokemon_normal = [PokemonNormal(nom, stats[1], stats[2]) for nom, stats in pokedex.items()
                          if stats[0] == "Normal"]
        list_pokemons = pokemon_plante + pokemon_feu + pokemon_eau + pokemon_normal
        for pokemon in list_pokemons:
            pokemon.reset_pv()  # Réinitialisation des PVs de tous les Pokémons du dictionnaire
            print(pokemon.print_nom(), end=" ")  # Affichage des noms de tous les Pokémons
            print(pokemon)  # Affichage des détails de tous les Pokémons
        pokemon = input("Choisissez votre Pokémon! -> ").capitalize()  # Robustesse recherche
        pokemon_adv = input("Choisissez le Pokémon adversaire ! -> ").capitalize()  # Robustesse recherche

        def trouver_pokemon(poke):
            for i, p in enumerate(list_pokemons):
                if p.nom == poke:
                    indice = i
                    return True, indice
            return False, None

        state, index = trouver_pokemon(pokemon)
        state_adv, index_adv = trouver_pokemon(pokemon_adv)
        if not state or not state_adv:
            print("Pokémon(s) introuvable(s)")
        else:
            gagnant, nb_tours = list_pokemons[index].combattre(list_pokemons[index_adv])
            print(f"======================================\nLe gagnant est le Pokémon {gagnant.print_nom()} "
                  f"{gagnant} au bout de {nb_tours} tour(s)")
    except TypeError as te:
        print(te)
    except ValueError as ve:
        print(ve)


if __name__ == "__main__":
    main()
