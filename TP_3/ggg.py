import tkinter as tk
from tkinter import ttk, scrolledtext

class PokemonBattleApp:
    def __init__(self, master):
        self.master = master
        master.title("Pokémon Battle Simulator")

        # Dropdown to select Pokémon
        self.pokemon_choice = tk.StringVar()
        self.pokemon_choice.set("Select a Pokémon")
        self.pokemon_menu = ttk.Combobox(master, textvariable=self.pokemon_choice,
                                         values=list(pokemons.keys()))
        self.pokemon_menu.pack()

        # Button to confirm Pokémon selection
        self.select_button = tk.Button(master, text="Select Pokémon", command=self.select_pokemon)
        self.select_button.pack()

        # Stats and battle log
        self.stats_label = tk.Label(master, text="")
        self.stats_label.pack()

        self.battle_log = scrolledtext.ScrolledText(master, width=40, height=10)
        self.battle_log.pack()

        # Battle actions
        self.attack_button = tk.Button(master, text="Attack", command=self.attack)
        self.attack_button.pack()

        self.selected_pokemon = None
        self.opponent_pokemon = None

    def select_pokemon(self):
        pokemon_name = self.pokemon_choice.get()
        if pokemon_name in pokemons:
            type, pv, atk = pokemons[pokemon_name]
            self.selected_pokemon = Pokemon(pokemon_name, pv, atk)
            self.stats_label.config(text=f"{pokemon_name} - PV: {pv}, ATK: {atk}")
            # Select a random opponent for simplicity
            import random
            opponent_name, stats = random.choice(list(pokemons.items()))
            self.opponent_pokemon = Pokemon(opponent_name, *stats[1:])
            self.update_battle_log(f"Your opponent is {opponent_name}")

    def attack(self):
        if self.selected_pokemon and self.opponent_pokemon:
            self.selected_pokemon.attaquer(self.opponent_pokemon)
            self.update_battle_log(f"Attacked {self.opponent_pokemon.nom}!")
            if self.opponent_pokemon.est_ko():
                self.update_battle_log(f"{self.opponent_pokemon.nom} is K.O.!")
            # Update stats display
            self.stats_label.config(text=f"{self.selected_pokemon.nom} - PV: {self.selected_pokemon.pv}, ATK: {self.selected_pokemon.atk}")

    def update_battle_log(self, message):
        self.battle_log.insert(tk.END, message + "\n")
        self.battle_log.see(tk.END)

# Main setup
root = tk.Tk()
app = PokemonBattleApp(root)
root.mainloop()
