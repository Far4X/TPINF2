import tkinter as tk
import math


class Calculation :
    def __init__(self, text : str, x_val : float | None = None) :
        text = text.replace("sin", "s").replace("cos", "c").replace("tan", "t").replace("sqrt", "r").replace("²", "^2").replace("pi", f"{math.pi}")
        if x_val != None :
            text = text.replace("x", x_val)

        self.text_left_member = ""
        self.text_right_member = ""
        self.operation = ""

        parenthesis_level = 0
        parenthesis_level_op = None
        is_op_passed = False

        for char in text :
            if char == "(" :
                parenthesis_level += 1
            elif char == ")" :
                parenthesis_level -= 1

            if char in "cstr+-/*^" :
                if parenthesis_level_op == None or parenthesis_level_op > parenthesis_level :
                    is_op_passed = True
                    self.text_left_member += self.text_right_member
                    self.operation = char
                    parenthesis_level_op = parenthesis_level
                    self.text_right_member = ""

                elif parenthesis_level_op == parenthesis_level :
                    if self.operation in "cstr/*^" and char in "+-" :
                        self.text_left_member += self.text_right_member
                        self.text_right_member = ""
                        self.operation = char

                    elif self.operation in "cstr^" and char in "*/" :
                        self.text_left_member += self.text_right_member
                        self.operation = char
                        self.text_right_member = ""
                
            if is_op_passed :
                self.text_right_member += char
            else :
                self.text_left_member += char


        self.text_right_member = self.text_right_member.lstrip(self.operation)

        if (parenthesis_level_op != None) :
            for i in range(parenthesis_level_op) :
                print("Here")
                self.text_left_member = self.text_left_member.lstrip('(')
                self.text_right_member = self.text_right_member.rstrip(')')

        print(f"Output : op : {self.operation}, left member : {self.text_left_member}, right member : {self.text_right_member}")
        if self.operation != "" :
            if self.text_right_member != "" :
                self.right_member = Calculation(self.text_right_member)
            if self.text_left_member != "" :
                self.left_member = Calculation(self.text_left_member)

    def Calculate(self) -> float:
        match self.operation :
            case "" :
                if self.text_left_member != "" :
                    return float(self.text_left_member)
                else :
                    return float(self.text_left_member)
                
            case "+" :
                return self.right_member.Calculate() + self.left_member.Calculate()
            
            case "-" :
                if self.text_left_member != "" :
                    return self.left_member.Calculate() - self.right_member.Calculate()
                return -self.right_member.Calculate()
                
            case "*" :
                if self.text_left_member == "" :
                    return self.right_member.Calculate()
                return self.left_member.Calculate() * self.right_member.Calculate()
            
            case "/" :
                return self.left_member.Calculate() / self.right_member.Calculate() 

            case "c" :
                if self.text_left_member == "" :
                    return math.cos(self.right_member.Calculate())
                return  self.left_member.Calculate()*math.cos(self.right_member.Calculate())
            
            case "s" :
                if self.text_left_member == "" :
                    return math.sin(self.right_member.Calculate())
                return  self.left_member.Calculate()*math.sin(self.right_member.Calculate())
            
            case "t" :
                if self.text_left_member == "" :
                    return math.tan(self.right_member.Calculate())
                return  self.left_member.Calculate()*math.tan(self.right_member.Calculate())
            
            case "r" :
                if self.text_left_member == "" :
                    return math.sqrt(self.right_member.Calculate())
                return self.left_member.Calculate()*math.sqrt(self.right_member.Calculate())
            
            case "^" :
                return self.left_member.Calculate() ** self.left_member.Calculate()
                
        

class Historal :
    def __init__(self) :
        self._list_op = []

    def opEffectued(self, op : str) :
        self._list_op.append(op)

    def getOps(self, page, lenght) :
        if lenght > len(self._list_op) :
            return (self._list_op[-1-lenght*(page+1):-1-lenght*page])
        return (self._list_op)

class CalculatriceButtonChar(tk.Button) :
    def __init__(self, parent, char, calc_host) :
        tk.Button.__init__(self, parent, command=self.clickedOn, text=char, background = ("#909090" if str(char) not in "0123456789" else "#aaa"), relief="flat")
        self.parent : tk.Frame = parent
        self.calc_host : Calculatrice = calc_host
        self.char = char

    def clickedOn(self) :
        self.calc_host.addChar(str(self.char))

    def setChar(self, char) :
        self.config(text = char)
        self.char = char


class Calculatrice(tk.Tk) :
    def __init__(self, size = (400, 500)) :
        tk.Tk.__init__(self)
        self.graph_mode = False
        self.trigger_reset = False
        self._txt = tk.StringVar()
        self.historal = Historal()
        #self.config()
        self.geometry(f"{size[0]}x{size[1]}+100+100")
        self.frame = tk.Frame(self, padx= 20, pady=20, bg = "#202030")
        self.separator = tk.Canvas(self.frame, height=20, bg = "#202030", relief="flat", highlightthickness=0)
        self.output = tk.Label(self.frame, bg = "#bbb", padx= 5, pady=20, anchor="center", textvariable=self._txt)


        self.frame.pack(fill="both", expand="true")
        self.output.grid(row = 0, column = 0, columnspan= 5, sticky="ew")
        self.frame.columnconfigure(0, weight=1)

        self.separator.grid(row = 1, column = 0, columnspan= 5, sticky="ew")
        self.separator.columnconfigure(0, weight=1)

        list_btns_char =   [("cos", 2, 0), ("sin", 2, 1), ("tan", 2, 2), ('pi', 2, 3), ('sqrt', 2, 4),
                            (1, 3, 0),     (2, 3, 1),     (3, 3, 2),     ('+', 3, 3),  ('^', 3, 4),
                            (4, 4, 0),     (5, 4, 1),     (6, 4, 2),     ('-', 4, 3),  ('(', 4, 4),
                            (7, 5, 0),     (8, 5, 1),     (9, 5, 2),     ('*', 5, 3),  (')', 5, 4),
                                           (0, 6, 1),     (".", 6, 2),   ('/', 6, 3),
                        ]
        
        for btn_data in list_btns_char :
            btn = CalculatriceButtonChar(self.frame, btn_data[0], self)
            btn.grid(row = btn_data[1], column=btn_data[2], sticky="ewns", padx=5, pady = 5)
            self.frame.columnconfigure(btn_data[2], weight=1)
            self.frame.rowconfigure(btn_data[1], weight=1)

        self.button_multifunc = CalculatriceButtonChar(self.frame, "²", self)
        self.button_multifunc.grid(row = 6, column=4, sticky="ewns", padx=5, pady = 5)

        self.do_opeation_button = tk.Button(self.frame, command=self.doCalculation, text="=", background="#5585f0", relief="flat")
        self.do_opeation_button.grid(row = 6, column = 0, padx=5, pady=5, sticky="nsew")

        btm_color = "#4065d0"

        self.graphic_mode_button = tk.Button(self.frame, command=self.goGraphicMode, text="Mode graphique", background=btm_color, relief="flat")
        self.graphic_mode_button.grid(row = 7, column = 1, padx=5, pady=5, sticky="nsew", columnspan=2)

        self.historique_mode_button = tk.Button(self.frame, command=self.goHistoricMode, text="Historique", background=btm_color, relief="flat")
        self.historique_mode_button.grid(row = 7, column = 3, padx=5, pady=5, sticky="nsew", columnspan=2) 

        self.clear_button = tk.Button(self.frame, command=self.clearArea, text="cls", background=btm_color, relief="flat")
        self.clear_button.grid(row = 7, column = 0, padx=5, pady=5, sticky="nsew", columnspan=1)       


    def addChar(self, char) :
        if not self.trigger_reset :
            self._txt.set(self._txt.get() + char)
        else :
            self._txt.set(char)
            self.trigger_reset = False

    def clearArea(self) :
        self._txt.set("")

    def doCalculation(self) :
        self.historal.opEffectued(self._txt.get())
        if not self.graph_mode :
            try :
                self._txt.set(self._txt.get() + f" = {Calculation(self._txt.get()).Calculate()}")
            except RecursionError:
                self._txt.set("Opération saisie non valide")
            self.trigger_reset = True
        
    def goGraphicMode(self) :
        if not self.graph_mode :
            self.graph_mode = True
            self.graphic_mode_button.configure(bg="#209010")
            self.button_multifunc.setChar("x")
        else :
            self.graph_mode = False
            self.graphic_mode_button.configure(bg="#4065d0")
            self.button_multifunc.setChar("²")


    def goHistoricMode(self) :
        pass



def main() :
    calc = Calculatrice()
    calc.mainloop()

if __name__ == "__main__" :
    main()
