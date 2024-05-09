import tkinter as tk

class CalculatriceButtonChar(tk.Button) :
    def __init__(self, parent, char, calc_host) :
        tk.Button.__init__(self, parent, command=self.clickedOn, text=char, background = ("#909090" if str(char) not in "0123456789" else "#aaa"), relief="flat")
        self.parent : tk.Frame = parent
        self.calc_host : Calculatrice = calc_host
        self.char = char

    def clickedOn(self) :
        self.calc_host.addChar(str(self.char))



class Calculatrice(tk.Tk) :
    def __init__(self, size = (400, 500)) :
        tk.Tk.__init__(self)
        self._txt = tk.StringVar()
        self.config()
        self.geometry(f"{size[0]}x{size[1]}+100+100")
        self.frame = tk.Frame(self, padx= 20, pady=20, bg = "#202030")
        self.separator = tk.Canvas(self.frame, height=20, bg = "#202030", relief="flat", highlightthickness=0)
        self.output = tk.Label(self.frame, bg = "#bbb", padx= 5, pady=20, anchor="center", textvariable=self._txt)


        self.frame.pack(fill="both", expand="true")
        self.output.grid(row = 0, column = 0, columnspan= 5, sticky="ew")
        self.frame.columnconfigure(0, weight=1)

        self.separator.grid(row = 1, column = 0, columnspan= 5, sticky="ew")
        self.separator.columnconfigure(0, weight=1)

        list_btns_char =   [("cos", 2, 0), ("sin", 2, 1), ("tan", 2, 2), ('pi', 2, 3), ('²', 2, 4),
                            (1, 3, 0),     (2, 3, 1),     (3, 3, 2),     ('+', 3, 3),  ('sqrt', 3, 4),
                            (4, 4, 0),     (5, 4, 1),     (6, 4, 2),     ('-', 4, 3),  ('^', 4, 4),
                            (7, 5, 0),     (8, 5, 1),     (9, 5, 2),     ('*', 5, 3),  ('(', 5, 4),
                                           (0, 6, 1),     (".", 6, 2),   ('/', 6, 3),  (')', 6, 4),
                        ]
        
        for btn_data in list_btns_char :
            btn = CalculatriceButtonChar(self.frame, btn_data[0], self)
            btn.grid(row = btn_data[1], column=btn_data[2], sticky="ewns", padx=5, pady = 5)
            self.frame.columnconfigure(btn_data[2], weight=1)
            self.frame.rowconfigure(btn_data[1], weight=1)

        self.do_opeation_button = tk.Button(self.frame, command=self.doCalculation, text="=", background="#5585f0", relief="flat")
        self.do_opeation_button.grid(row = 6, column = 0, padx=5, pady=5, sticky="nsew")

    def addChar(self, char) :
        self._txt.set(self._txt.get() + char)

    def doCalculation(self) :
        pass
        


def main() :
    calc = Calculatrice()
    calc.mainloop()

if __name__ == "__main__" :
    main()
