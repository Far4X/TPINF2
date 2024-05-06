from __future__ import annotations
import inputControl
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
    Classe repésentant un Pokémon.
    Attributs :
    name (str) : Nom du Pokémon
    pv (int) : Points de vie du Pokémon
    atk (int) : Points de dégâts du Pokémon
    """

    def __init__(self, nom: str, pv: int, atk: int):
        self.nom = nom
        self.pv = pv
        self.atk = atk
        self.max_pv = pv

    def heal(self):
        "Permet de soigner le pokémon (remet ses pv au max)"
        self.pv = self.max_pv

    @property
    def nom(self):
        """Property définissant le nom du pokémon"""
        return self._nom

    @nom.setter
    def nom(self, val: str):
        self._nom = str(val)

    @property
    def pv(self):
        """Property définissant les points de vie restants du pokémon"""
        return self._pv

    @pv.setter
    def pv(self, can_val: int):
        if isinstance(can_val, int):
            if can_val >= 0:
                self._pv = can_val
            else:
                raise ValueError("Le nombre de points de vie ne peut être négatif")
        else:
            raise TypeError("Le nombre de points de vie doit être un entier")

    @property
    def max_pv(self):
        """Property définissant les pv maximum du Pokémon. Utile pour l'affichage et le soin de ces derniers"""
        return self._mpv

    @max_pv.setter
    def max_pv(self, can_val: int):
        if isinstance(can_val, int):
            if can_val > 0:
                self._mpv = can_val
            else:
                raise ValueError("Le nombre de points de vie ne peut être négatif")
        else:
            raise TypeError("Le nombre de points de vie doit être un entier")

    @property
    def atk(self):
        """Property définissant l'attaque du pokémon"""
        return self._atk

    @atk.setter
    def atk(self, can_val: int):
        if isinstance(can_val, int):
            if can_val >= 0:
                self._atk = can_val
            else:
                raise ValueError("Le nombre de points d'attaque ne peut être négatif")
        else:
            raise TypeError("Le nombre de points de vie doit être un entier")

    def estKo(self):
        return self.pv <= 0

    def takeDamage(self, amount: int):
        """Méthode qui permet de prendre des dégats. Controle de valeur et affichage des pv restants"""
        if type(amount) == int:
            if (self.pv < amount):
                self.pv = 0
            else:
                self.pv -= amount
            print(f"{self.print_nom()} a pris\033[31m {amount}\033[0m dágâts! {self}")

        else:
            raise TypeError("Le nombre de dégats pris n'est pas un entier")

    def attaquer(self, other: Pokemon):
        "Permet d'attaquer un pokémon. Prend en compte les différences de type"
        if isinstance(other, Pokemon):
            print(f"{self.print_nom()} attaque {other.print_nom()} !")
            coeff = self.calcMultiplicator(other)
            other.takeDamage(random.randint(0, int(self.atk * coeff)))
            match coeff:
                case 0.5:
                    print("Ce n'est pas très efficace...")
                case 2:
                    print("C'est super efficace !")
        else:
            raise TypeError

    def calcMultiplicator(self, other):
        return 1

    def combattre(self, autre: Pokemon):
        """Permet d'organiser le combat entre pokémons"""
        if isinstance(autre, Pokemon):
            i = 0
            while (not self.estKo() and not autre.estKo()):
                i += 1
                print("======================================")
                print(f"Tour {i}")
                print("======================================")
                self.attaquer(autre)
                if autre.estKo():
                    break
                autre.attaquer(self)
            if (autre.estKo()):
                print(f"{autre.print_nom()} est K.O. !")
                return (self, i)
            print(f"{self.print_nom()} est K.O. !")
            return (autre, i)

        else:
            raise TypeError("L'autre objet n'est pas un pokémon")

    def print_nom(self):
        return f"{self.nom}"

    def __str__(self):
        return f"[{self.pv}/{self.max_pv} PV(s); {self.atk} ATK]"


class PokemonNormal(Pokemon):
    """Classe définissant les Pokémons de type normal"""

    def __init__(self, nom: str, pv: int, atk: int):
        super().__init__(nom, pv, atk)


class PokemonFeu(Pokemon):
    """Classe définissant les Pokémons de type feu"""

    def __init__(self, nom: str, pv: int, atk: int):
        super().__init__(nom, pv, atk)

    def print_nom(self):  # print_nom() surchargée afin d'imprimer le nom en couleur orange
        return f"\033[38;2;255;165;0m{self.nom}\033[0m"

    def calcMultiplicator(self, other: Pokemon):
        if isinstance(other, PokemonFeu):
            return 0.5
        elif isinstance(other, PokemonEau):
            return 0.5
        elif isinstance(other, PokemonPlante):
            return 2
        return 1


class PokemonEau(Pokemon):
    """Classe définissant les Pokémons de type eau"""

    def __init__(self, nom: str, pv: int, atk: int):
        super().__init__(nom, pv, atk)

    def print_nom(self):  # print_nom() surchargée afin d'imprimer le nom en couleur bleue
        return f"\033[34m{self.nom}\033[0m"

    def calcMultiplicator(self, other: Pokemon):
        if isinstance(other, PokemonPlante):
            return 0.5
        elif isinstance(other, PokemonEau):
            return 0.5
        elif isinstance(other, PokemonFeu):
            return 2
        return 1


class PokemonPlante(Pokemon):
    """Classe définissant les Pokémons de type plante"""

    def __init__(self, nom: str, pv: int, atk: int):
        super().__init__(nom, pv, atk)

    def print_nom(self):  # print_nom() surchargée afin d'imprimer le nom en couleur verte
        return f"\033[32m{self.nom}\033[0m"

    def calcMultiplicator(self, other: Pokemon):
        if isinstance(other, PokemonPlante):
            return 0.5
        elif isinstance(other, PokemonFeu):
            return 0.5
        elif isinstance(other, PokemonEau):
            return 2
        return 1


def createPokemon():
    """Permet d'instancier un nouveau Pokémon en entrant ses caractéristiques"""

    # type_p = input("Quel type de pokémon voulez-vous ? ").lower().strip(" \n")
    # while type_p not in ["plante", "normal", "feu", "eau"] :
    #    type_p = input("Type entré non reconnu. Veuillez réessayer : ").lower().strip(" \n")

    type_p = inputControl.secureAskType(str, "Quel type de pokémon voulez-vous ? ",
                                   lambda x: x.lower().strip() in ["plante", "normal", "feu", "eau"])
    hp = inputControl.secureAskType(int, "Entrez les points de vie, de type entier : ")
    atk = inputControl.secureAskType(int, "Entrez les points d'attaque, de type entier : ")
    nom = input("Entrez le nom du Pokémon : ")
    attr = (nom.capitalize(), hp, atk)

    match type_p:
        case "plante":
            return PokemonPlante(*attr)
        case "feu":
            return PokemonFeu(*attr)
        case "normal":
            return PokemonNormal(*attr)
        case "eau":
            return PokemonEau(*attr)


def printListPok(list_p: list | Pokemon):
    """Affiche la liste des pokémons en mettant leur identifiant devant"""
    i = 0
    for pokemon in list_p:
        print(f"{i} : {pokemon.print_nom()} {pokemon}")
        i += 1


def pickPokemon(list_pokemons: list | Pokemon) -> Pokemon:
    printListPok(list_pokemons)
    in_list = lambda x: (x >= 0 and x < len(list_pokemons))
    ident = inputControl.secureAskType(int, "Entrez un identifieur de Pokémon : ", in_list)
    return list_pokemons[ident]


def combat(list_pokemons: list | Pokemon) -> None:
    """Permet d'organiser un combat entre Pokémons en utilisant leur méthode."""
    pokemon1 = pickPokemon(list_pokemons)
    pokemon2 = pickPokemon(list_pokemons)
    if (pokemon1 != pokemon2):
        result = pokemon1.combattre(pokemon2)
        print("======================================")
        print(f"{result[0].print_nom()} gagne en {result[1]} tour(s)")


def soigner(list_pokemons):
    pickPokemon(list_pokemons).heal()


def importer(pokedex_dict: dict) -> list:
    pokemon_plante = [PokemonPlante(nom.capitalize(), stats[1], stats[2]) for nom, stats in pokedex_dict.items()
                      if stats[0] == "Plante"]
    pokemon_feu = [PokemonFeu(nom.capitalize(), stats[1], stats[2]) for nom, stats in pokedex_dict.items()
                   if stats[0] == "Feu"]
    pokemon_eau = [PokemonEau(nom.capitalize(), stats[1], stats[2]) for nom, stats in pokedex_dict.items()
                   if stats[0] == "Eau"]
    pokemon_normal = [PokemonNormal(nom.capitalize(), stats[1], stats[2]) for nom, stats in pokedex_dict.items()
                      if stats[0] == "Normal"]
    list_pokemons = pokemon_plante + pokemon_feu + pokemon_eau + pokemon_normal
    return list_pokemons


def main():
    """Boucle principale du jeu. Permet d'utiliser les Pokémons"""
    continuer = True
    list_pokemons = []
    while continuer:
        print("Que voulez-vous faire : ")
        print("0 : Quitter")
        print("1 : Créer un Pokémon")
        print("2 : Organiser un combat")
        print("3 : Afficher la liste des Pokémons")
        print("4 : Soigner un Pokemon")
        print("5 : Importer le Pokédex")

        in_list = lambda x: (x >= -1 and x < 6)
        option = inputControl.secureAskType(int, "Quelle option choissez-vous ? ", in_list)
        match option:
            case 0:
                continuer = False
            case 1:
                list_pokemons.append(createPokemon())
            case 2:
                if len(list_pokemons) >= 2:
                    combat(list_pokemons)
                else:
                    print("Vous n'avez pas assez de Pokémons pour organiser un combat !")
            case 3:
                printListPok(list_pokemons)
            case 4:
                soigner(list_pokemons)
            case 5:
                list_pokemons = list_pokemons + importer(pokedex)
                print("Pokédex importé !")


if __name__ == "__main__":
    main()
