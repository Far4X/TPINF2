import pickle
import random
# 1. Définir une classe Pokemon qui contient les attributs suivants :
# • Un attribut nom qui représente le nom du Pokémon avec une chaîne ;
# • Un attribut pv qui représente les points de vie du Pokémon avec un entier positif ;
# • Un attribut atk qui représente les points de dégâts du Pokémon avec un entier positif.

# 2. Implémenter tous les getters ainsi que les setters pertinents puis un constructeur.
with open("pokemon_data.pkl", 'rb') as file:
    pokedex = pickle.load(file)
# pokedex = {
#     "Bulbasaur": ("Plante", 45, 49),
#     "Ivysaur": ("Plante", 60, 62),
#     "Venusaur": ("Plante", 80, 82),
#     "Charmander": ("Feu", 39, 52),
#     "Charmeleon": ("Feu", 58, 64),
#     "Charizard": ("Feu", 78, 84),
#     "Squirtle": ("Eau", 44, 48),
#     "Wartortle": ("Eau", 59, 63),
#     "Blastoise": ("Eau", 79, 83),
#     "Pidgey": ("Normal", 40, 45),
#     "Pidgeotto": ("Normal", 63, 60),
#     "Pidgeot": ("Normal", 83, 80),
#     "Rattata": ("Normal", 30, 56),
#     "Raticate": ("Normal", 55, 81),
#     "Spearow": ("Normal", 40, 60),
#     "Fearow": ("Normal", 65, 90)
# }
# Le même dictionnaire stocké dans le fichier


class Pokemon:
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

# 3. Implémenter une propriété est_ko(self) qui retourne un booléen indiquant s’il ne reste
# plus de PV au Pokémon.

    def est_ko(self):
        return self.pv <= 0

# 4. Implémenter les méthodes suivantes :
# • attaquer(self, autre) : permet au Pokémon self d’attaquer autre en lui reti‑
# rant un certain nombre de points de vie. Ce nombre est tiré aléatoirement entre 0 et atk.
# • combattre(self, autre) : permet aux deux Pokémon de s’attaquer à tour de rôle.
# La méthode retourne le gagnant et le nombre de tours d’attaque.
# • __str__(self) : retourne les informations du Pokémon sous forme de chaîne.

    @staticmethod
    def bonus(func):
        def wrapper(self, other):
            if not isinstance(self, PokemonNormal) and not isinstance(other, PokemonNormal):
                if isinstance(self, type(other)):
                    multiplicateur = 0.5
                    efficacite = "Ce n'est pas très efficace..."
                elif other.hierarchie == (self.hierarchie + 1) % 3:
                    multiplicateur = 2
                    efficacite = "C'est super efficace !"
                else:
                    multiplicateur = 0.5
                    efficacite = "Ce n'est pas très efficace..."
            else:
                multiplicateur = 1
                efficacite = None
            return func(self, other, multiplicateur, efficacite)
        return wrapper

    @bonus
    def attaquer(self, autre, multiplicateur, efficacite):
        print(f"{self.print_nom()} attaque {autre.print_nom()}.")
        degats = round((random.randint(0, self.atk)) * multiplicateur)
        autre.pv -= degats
        print(f"Le pokemon {autre.print_nom()} a perdu {degats} PV(s) ! {autre}")
        if efficacite is not None:
            print(efficacite)

    def combattre(self, autre):
        state = True
        tours = 0
        while state:
            print(f"======================================\nTour {tours+1} :\n======================================")
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
        self.pv = self.pv_max

    def print_nom(self):
        return f"{self.nom}"

    def __str__(self):
        return f"[PV(s):{self.pv}; ATK:{self.atk}]"

# 5. Définir les classes PokemonNormal, PokemonFeu, PokemonEau et PokemonPlante qui
# héritent de la classe Pokemon. Ces classes filles implémentent que certains types font plus ou
# moins de dégâts à d’autres types :

# • Les Pokémons feu font deux fois plus de dégâts aux Pokémons plante mais font deux fois
# moins de dégâts aux Pokémons eau ou feu.
# • Les Pokémons eau font deux fois plus de dégâts aux Pokémons feu mais font deux fois
# moins de dégâts aux Pokémons eau ou plante.
# • Les Pokémons plante font deux fois plus de dégâts aux Pokémons eau mais font deux fois
# moins de dégâts aux Pokémons plante ou feu.
# • Les Pokémons normaux infligent et reçoivent des dégâts normaux de tous les types.
# On pourra s’aider d’une fonction calc_multiplicateur(self, autre) surchargée
# dans les classes filles afin de retourner 0.5, 1 ou 2 en fonction du type de autre.


class PokemonNormal(Pokemon):
    def __init__(self, nom, pv, atk):
        Pokemon.__init__(self, nom, pv, atk)


class PokemonFeu(Pokemon):
    def __init__(self, nom, pv, atk):
        Pokemon.__init__(self, nom, pv, atk)
        self.hierarchie = 0

    def print_nom(self):
        return f"\033[38;2;255;165;0m{self.nom}\033[0m"


class PokemonPlante(Pokemon):
    def __init__(self, nom, pv, atk):
        Pokemon.__init__(self, nom, pv, atk)
        self.hierarchie = 1

    def print_nom(self):
        return f"\033[32m{self.nom}\033[0m"


class PokemonEau(Pokemon):
    def __init__(self, nom, pv, atk):
        Pokemon.__init__(self, nom, pv, atk)
        self.hierarchie = 2

    def print_nom(self):
        return f"\033[34m{self.nom}\033[0m"

# 6. Dans une fonction main(), créer des Pokemon de diférents types et amusez‑vous à faire des
# combats de Pokémon.


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
        pokemon = input("Choisissez votre Pokémon! -> ").capitalize()
        pokemon_adv = input("Choisissez le Pokémon adversaire ! -> ").capitalize()

        def trouver_pokemon(poke):
            for i, p in enumerate(list_pokemons):
                if p.nom == poke:
                    indice = i
                    return True, indice
            return False, None

        state, index = trouver_pokemon(pokemon)
        state_adv, index_adv = trouver_pokemon(pokemon_adv)
        if not state or not state_adv:
            print("Pokémon(s) introuvable")
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
