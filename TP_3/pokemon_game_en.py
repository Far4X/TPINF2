import random
pokedex = {
    "Bulbasaur": ("Grass", 45, 49),
    "Ivysaur": ("Grass", 60, 62),
    "Venusaur": ("Grass", 80, 82),
    "Charmander": ("Fire", 39, 52),
    "Charmeleon": ("Fire", 58, 64),
    "Charizard": ("Fire", 78, 84),
    "Squirtle": ("Water", 44, 48),
    "Wartortle": ("Water", 59, 63),
    "Blastoise": ("Water", 79, 83),
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
    Class representing an untyped Pokémon.
    Attributes:
    name (str): Name of the Pokémon
    hp (int): Health points of the Pokémon
    atk (int): Attack points of the Pokémon
    """
    def __init__(self, name, hp, atk):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.atk = atk

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise TypeError("The Pokémon's name must be a string.")
        self._name = name

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, hp):
        if not isinstance(hp, int):
            raise TypeError("The Pokémon's health points must be an integer.")
        if hp < 0:
            self._hp = 0
        else:
            self._hp = hp

    @property
    def atk(self):
        return self._atk

    @atk.setter
    def atk(self, atk):
        if not isinstance(atk, int):
            raise TypeError("The Pokémon's attack points must be an integer.")
        if atk < 0:
            raise ValueError("The Pokémon's attack points must be positive.")
        self._atk = atk

    def is_knocked_out(self):
        return self.hp <= 0

    @staticmethod  # Used to avoid confusion with a class method
    def type_advantage(func):
        """
        The idea of this decorator is to establish a cyclic hierarchy of type advantages,
        using the mathematical logic of modulo.
        I opted to use a decorator instead of the method calc_multiplier(self, other)
        for more generalization.
        :param func: function
        :return: function decorated with the type advantage multiplier and effectiveness messages
        """
        def wrapper(self, other):
            if not isinstance(self, PokemonNormal) and not isinstance(other, PokemonNormal):  # self & other non-normal
                if isinstance(self, type(other)) or other.hierarchy != (self.hierarchy + 1) % 3:
                    multiplier = 0.5  # Multiplier in case of type disadvantage.
                    effectiveness = "It's not very effective..."
                else:
                    multiplier = 2  # Multiplier in case of type advantage
                    effectiveness = "It's super effective!"
            else:
                multiplier = 1  # Multiplier associated with the normal type
                effectiveness = None
            return func(self, other, multiplier, effectiveness)
        return wrapper

    @type_advantage
    def attack(self, other, multiplier, effectiveness):
        print(f"{self.print_name()} attacks {other.print_name()}.")
        damage = round((random.randint(0, self.atk)) * multiplier)
        print(f"\033[31m -{damage} \033[0m")
        if damage > other.hp:
            print(f"The Pokémon {other.print_name()} has lost {other.hp} HP(s)!", end=" ")
            other.hp = 0
            print(f"{other}")
        else:
            other.hp -= damage
            print(f"The Pokémon {other.print_name()} has lost {damage} HP(s)! {other}")
        if effectiveness is not None:
            print(effectiveness)

    def battle(self, other):
        state = True
        rounds = 0
        while state:
            print(f"=====================================\nRound {rounds + 1}:\n=====================================")
            self.attack(other)
            rounds += 1
            if other.is_knocked_out():
                print(f"The Pokémon {other.print_name()} is K.O.!")
                return self, rounds
            else:
                other.attack(self)
                if self.is_knocked_out():
                    print(f"The Pokémon {self.print_name()} is K.O.!")
                    return other, rounds

    def reset_hp(self):
        """
        Method to ensure that Pokémon HPs are reset for each execution.
        """
        self.hp = self.max_hp

    def print_name(self):
        return f"{self.name}"

    def __str__(self):
        """
        Method that displays the details (HPs and ATK) of the Pokémon.
        :return: string containing HPs and ATK
        """
        return f"[HP(s):{self.hp}; ATK:{self.atk}]"


class PokemonNormal(Pokemon):
    """
    Class representing a Grass type Pokémon, inheriting from the Pokémon class.
    Grass type Pokémon deal double damage to Water type but deal half damage to
    Grass or Fire type Pokémon.
    Normal type Pokémon deal and receive normal damage from all types.
    """
    def __init__(self, nom, pv, atk):
        Pokemon.__init__(self, nom, pv, atk)


class PokemonGrass(Pokemon):
    """
    Class representing a Grass type Pokémon, inheriting from the Pokémon class.
    Grass type Pokémon deal double damage to Water type but deal half damage to
    Grass or Fire type Pokémon.
    The hierarchy attribute is used to establish a cyclic type advantage using
    the modulo operation in the type_advantage decorator.
    """
    def __init__(self, name, hp, atk):
        Pokemon.__init__(self, name, hp, atk)
        self.hierarchy = 1

    def print_name(self):
        return f"\033[32m{self.name}\033[0m"


class PokemonFire(Pokemon):
    """
    Class representing a Fire type Pokémon, inheriting from the Pokémon class.
    Fire type Pokémon deal double damage to Grass type but deal half damage to
    Water or Fire type Pokémon.
    The hierarchy attribute is used to establish a cyclic type advantage using
    the modulo operation in the type_advantage decorator.
    """
    def __init__(self, name, hp, atk):
        Pokemon.__init__(self, name, hp, atk)
        self.hierarchy = 0

    def print_name(self):
        return f"\033[38;2;255;165;0m{self.name}\033[0m"


class PokemonWater(Pokemon):
    """
    Class representing a Water type Pokémon, inheriting from the Pokémon class.
    Water type Pokémon deal double damage to Fire type but deal half damage to
    Water or Grass type Pokémon.
    The hierarchy attribute is used to establish a cyclic type advantage using
    the modulo operation in the type_advantage decorator.
    """
    def __init__(self, name, hp, atk):
        Pokemon.__init__(self, name, hp, atk)
        self.hierarchy = 2

    def print_name(self):
        return f"\033[34m{self.name}\033[0m"


def main():
    try:
        grass_pokemon = [PokemonGrass(name, stats[1], stats[2]) for name, stats in pokedex.items()
                         if stats[0] == "Grass"]
        fire_pokemon = [PokemonFire(name, stats[1], stats[2]) for name, stats in pokedex.items() if stats[0] == "Fire"]
        water_pokemon = [PokemonWater(name, stats[1], stats[2]) for name, stats in pokedex.items()
                         if stats[0] == "Water"]
        normal_pokemon = [PokemonNormal(name, stats[1], stats[2]) for name, stats in pokedex.items()
                          if stats[0] == "Normal"]
        list_pokemon = grass_pokemon + fire_pokemon + water_pokemon + normal_pokemon
        for pokemon in list_pokemon:
            pokemon.reset_hp()  # Resetting HPs of all Pokémon in the dictionary
            print(pokemon.print_name(), end=" ")  # Displaying the names of all Pokémon
            print(pokemon)  # Displaying the details of all Pokémon
        pokemon = input("Choose your Pokémon! -> ").capitalize()  # Robustness in search
        opponent_pokemon = input("Choose the opponent Pokémon! -> ").capitalize()  # Robustness in search

        def find_pokemon(poke):
            for i, p in enumerate(list_pokemon):
                if p.name == poke:
                    index_found = i
                    return True, index_found
            return False, None

        state, index = find_pokemon(pokemon)
        state_opp, index_opp = find_pokemon(opponent_pokemon)
        if not state or not state_opp:
            print("Pokémon(s) not found")
        else:
            winner, num_rounds = list_pokemon[index].battle(list_pokemon[index_opp])
            print(f"=====================================\nThe winner is Pokémon {winner.print_name()} "
                  f"{winner} after {num_rounds} round(s)")
    except TypeError as te:
        print(te)
    except ValueError as ve:
        print(ve)


if __name__ == "__main__":
    main()
