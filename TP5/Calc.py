from __future__ import annotations
import tkinter as tk
import math
import typing


class Calculation :
    """Classe qui permet d'opérer des calculs donnés par des chaines de caractères.
    On aurait également pu utiliser la fonction eval."""
    def __init__(self, text : str) -> None:
        text = text.replace("sin", "s").replace("cos", "c").replace("tan", "t").replace("sqrt", "r").replace("²", "^2")
        while "π" in text :
            pi_index = text.index("π")
            if pi_index > 0 :
                if (text[pi_index - 1] in "x0123456789") :
                  text = text.replace("π", f"*{math.pi}", 1)
                else :  
                    text = text.replace("π", str(math.pi), 1)

            else :
                text = text.replace("π", str(math.pi), 1)


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
            for _ in range(parenthesis_level_op) :
                self.text_left_member = self.text_left_member.lstrip('(')
                self.text_right_member = self.text_right_member.rstrip(')')

        #print(f"Output : op : {self.operation}, left member : {self.text_left_member}, right member : {self.text_right_member}")
        if self.operation != "" :
            if self.text_right_member != "" :
                self.right_member = Calculation(self.text_right_member)
            if self.text_left_member != "" :
                self.left_member = Calculation(self.text_left_member)


    def Calculate(self, xval : None | float = None) -> float:
        match self.operation :
            case "" :
                if self.text_left_member != "" :
                    if self.text_left_member.strip("()") != "x" :
                        return float(self.text_left_member.strip("()"))
                    elif xval != None :
                        return xval
                    
                else :
                    if self.text_right_member.strip("()") != "x" :
                        return float(self.text_right_member.strip("()"))
                    elif xval != None :
                        return xval
                
            case "+" :
                return self.right_member.Calculate(xval) + self.left_member.Calculate(xval)
            
            case "-" :
                if self.text_left_member != "" :
                    return self.left_member.Calculate(xval) - self.right_member.Calculate(xval)
                return -self.right_member.Calculate(xval)
                
            case "*" :
                if self.text_left_member == "" :
                    return self.right_member.Calculate(xval)
                return self.left_member.Calculate(xval) * self.right_member.Calculate(xval)
            
            case "/" :
                return self.left_member.Calculate(xval) / self.right_member.Calculate(xval) 

            case "c" :
                if self.text_left_member == "" :
                    return math.cos(self.right_member.Calculate(xval))
                return  self.left_member.Calculate(xval)*math.cos(self.right_member.Calculate(xval))
            
            case "s" :
                if self.text_left_member == "" :
                    return math.sin(self.right_member.Calculate(xval))
                return  self.left_member.Calculate(xval)*math.sin(self.right_member.Calculate(xval))
            
            case "t" :
                if self.text_left_member == "" :
                    return math.tan(self.right_member.Calculate(xval))
                return  self.left_member.Calculate(xval)*math.tan(self.right_member.Calculate(xval))
            
            case "r" :
                if self.text_left_member == "" :
                    return math.sqrt(self.right_member.Calculate(xval))
                return self.left_member.Calculate(xval)*math.sqrt(self.right_member.Calculate(xval))
            
            case "^" :
                return self.left_member.Calculate(xval) ** self.right_member.Calculate(xval)
            
        print("Err",self.operation, self.text_left_member, self.text_right_member, xval)
                

class Historal :
    def __init__(self) -> None:
        self._list_op = []

    def opEffectued(self, op : str) :
        self._list_op.append(op)

    def getOps(self, page : int, lenght : int) -> tuple[int]:
        if lenght < len(self._list_op) :
            if len(self._list_op) >= (lenght*(page+1)) :
                if page == 0 :
                    return (self._list_op[-(lenght)*(page+1):])
                return (self._list_op[-(lenght)*(page+1):-lenght*(page)])
            return (self._list_op[:-lenght*(page)])
        return (self._list_op)
    
    def getNbPages(self, lenght : int) -> int :
        return len(self._list_op)//lenght + (1 if len(self._list_op) % lenght != 0 else 0)
    
class CalulatriceButton(tk.Button) :
    def __init__(self, parent : tk.Frame | tk.Tk, **kwargs) :
        super().__init__(parent, kwargs)
        if ("background" in kwargs or "bg" in kwargs) :
            
            init_color_str = (kwargs["background"] if "background" in kwargs else kwargs["bg"] )
            base_color = (init_color_str[1:3], init_color_str[3:5], init_color_str[5:7])
            changed_color = (int(int(color, 16)*0.9) for color in base_color)
            changed_color_str = "#"
            for color in changed_color :
                changed_color_str += str(hex(color)).lstrip("0x") 

            self.bind("<Enter>", func=lambda e: self.config(background=changed_color_str))
            self.bind("<Leave>", func=lambda e: self.config(background=init_color_str))
        else :
            print(kwargs)


class CalculatriceButtonChar(CalulatriceButton) :
    def __init__(self, parent : tk.Frame | tk.Tk, char : str, calc_host : Calculatrice) -> None :
        CalulatriceButton.__init__(self, parent, command=self.clickedOn, text=char, background = ("#909090" if str(char) not in "0123456789" else "#a0a0a0"), relief="flat")
        self.parent : tk.Frame = parent
        self.calc_host : Calculatrice = calc_host
        self.char = char

    def clickedOn(self) :
        self.calc_host.addChar(str(self.char))

    def setChar(self, char) :
        self.config(text = char)
        self.char = char

class HistoralWindow(tk.Toplevel) :
    def __init__(self, master : Calculatrice, historal : Historal) -> None :
        super().__init__(master, bg="#202030")
        self._historal = historal
        self.first_label = tk.Label(self, text=f"Historique - Page 1/{self._historal.getNbPages(10)}", relief="flat", bg="#5585f0")
        self.first_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.num_page = 0
        self._list_labels : tk.Label = []

        for i in range(10) :
            self._list_labels.append(tk.Label(self, relief="flat", bg="#202030", fg ="#202030", text="A"))
            self.rowconfigure(10-i, weight=1)

        self.geometry("300x450+200+200")

        self.button_next = CalulatriceButton(self, text="->", command=self.nextPage, bg="#5585f0", relief="flat")
        self.button_prev = CalulatriceButton(self, text="<-", command=self.prevPage, bg="#5585f0", relief="flat")
        self.button_prev.grid(column=0, row=11, sticky="nsew", padx=5, pady=5)
        self.button_next.grid(column=1, row=11, sticky="nsew", padx=5, pady=5)
        self.rowconfigure(11, weight=1)

        self.updatePage()

    def updatePage(self) -> None:
        """Permet de mettre à jour le contenu de la page.
        On garde les anciens labels affichés pour ne pas avoir de problème de redimensionnement de fenêtre ou d'autres éléments."""
        list_op = self._historal.getOps(self.num_page, 10)

        if self.num_page == 0 :
            self.button_prev.config(bg = "#2555a0")
        elif self.num_page == 1 :
            self.button_prev.config(bg = "#5585f0")

        if self.num_page == self._historal.getNbPages(10)-1 :
            self.button_next.config(bg = "#2555a0")
        elif self.num_page == self._historal.getNbPages(10)-2 :
            self.button_next.config(bg = "#5585f0")

        for i in range(10) :
            if i < len(list_op) :
                self._list_labels[i].config(text = list_op[i], fg = "#ffffff")
                self._list_labels[i].grid(column = 0, row = 10-i+(len(list_op)-10), columnspan = 2, padx=5, pady=4, sticky="nsew")

            else :
                self._list_labels[i].config(fg = "#202030")
                self._list_labels[i].grid(column = 0, row = 10-i+(+len(list_op)), columnspan = 2, padx=5, pady=4, sticky="nsew")


        self.first_label.config(text=f"Page {self.num_page+1}/{self._historal.getNbPages(10)}")

    def nextPage(self) :
        if self.num_page < self._historal.getNbPages(10)-1 :
            self.num_page += 1
        self.updatePage()

    def prevPage(self) :
        if self.num_page > 0 :
            self.num_page -= 1
        self.updatePage()

class ParamWindow(tk.Toplevel) :
    def __init__(self, master : GraphWindow) :
        if (type(master) != GraphWindow) :
            raise TypeError
        
        super().__init__(master, bg="#202030")
       
        self._params = (tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar())

        self._button_push = CalulatriceButton(self, text = "Valider", fg = "#ffffff", border=0, bg="#5585f0", command=self.checkAndPush)

        self._label_params = tk.Label(self, text="Nom des paramètres", fg = "#ffffff", border=0, bg="#202030")
        self._label_val_x = tk.Label(self, text="Valeur en x", fg = "#ffffff", border=0, bg="#202030")
        self._label_val_y = tk.Label(self, text="Valeur en y", fg = "#ffffff", border=0, bg="#202030")

        self._label_topleft = tk.Label(self, text="Point en haut à gauche : ", fg = "#ffffff", border=0, bg="#202030")
        self._label_size_graph = tk.Label(self, text="Taille du graphique : ", fg = "#ffffff", border=0, bg="#202030")
        self._label_step_mv = tk.Label(self, text="Pas du mouvement : ", fg = "#ffffff", border=0, bg="#202030")
        self._label_graduation = tk.Label(self, text="Pas de la graduation : ", fg = "#ffffff", border=0, bg="#202030")
        self._label_step_x = tk.Label(self, text="Pas du tracé du graphe : ", fg = "#ffffff", border=0, bg="#202030")

        self._entry_topleft_x = tk.Entry(self, fg = "#ffffff", border=0, bg="#4065d0", textvariable=self._params[0])
        self._entry_topleft_y = tk.Entry(self, fg = "#ffffff", border=0, bg="#4065d0", textvariable=self._params[1])
        self._entry_size_graph_x = tk.Entry(self, fg = "#ffffff", border=0, bg="#4065d0", textvariable=self._params[2])
        self._entry_size_graph_y = tk.Entry(self, fg = "#ffffff", border=0, bg="#4065d0", textvariable=self._params[3])
        self._entry_step_mv_x = tk.Entry(self, fg = "#ffffff", border=0, bg="#4065d0", textvariable=self._params[4])
        self._entry_step_mv_y = tk.Entry(self, fg = "#ffffff", border=0, bg="#4065d0", textvariable=self._params[5])
        self._entry_graduation_x = tk.Entry(self, fg = "#ffffff", border=0, bg="#4065d0", textvariable=self._params[6])
        self._entry_graduation_y = tk.Entry(self, fg = "#ffffff", border=0, bg="#4065d0", textvariable=self._params[7])
        self._entry_step_x = tk.Entry(self, fg = "#ffffff", border=0, bg="#4065d0", textvariable=self._params[8])


        self._params[0].set(str(master.top_left[0]))
        self._params[1].set(str(master.top_left[1]))
        self._params[2].set(str(master.size_graph[0]))
        self._params[3].set(str(master.size_graph[1]))
        self._params[4].set(str(master.step_mv[0]))
        self._params[5].set(str(master.step_mv[1]))
        self._params[6].set(str(master.graduations[0]))
        self._params[7].set(str(master.graduations[1]))
        self._params[8].set(str(master.stepx))
        

        self._label_params.grid(row = 0, column=0, sticky="nsew", padx= 20, pady= 5)
        self._label_val_x.grid(row=0, column=1, sticky="nsew", padx= 20, pady= 5)
        self._label_val_y.grid(row=0, column=2, sticky="nsew", padx= 20, pady= 5)
        self._label_topleft.grid(row=1, column=0, sticky="e", padx= 5, pady= 5)
        self._label_size_graph.grid(row=2, column=0, sticky="e", padx= 5, pady= 5)
        self._label_step_mv.grid(row=3, column=0, sticky="e", padx= 5, pady= 5)
        self._label_graduation.grid(row=4, column=0, sticky="e", padx= 5, pady= 5)
        self._label_step_x.grid(row=5, column=0, sticky="e", padx= 5, pady= 5)

        self._entry_topleft_x.grid(column=1, row = 1, sticky="nsew", padx=2, pady=2)
        self._entry_topleft_y.grid(column=2, row = 1, sticky="nsew", padx=2, pady=2)
        self._entry_size_graph_x.grid(column=1, row = 2, sticky="nsew", padx=2, pady=2)
        self._entry_size_graph_y.grid(column=2, row = 2, sticky="nsew", padx=2, pady=2)
        self._entry_step_mv_x.grid(column=1, row = 3, sticky="nsew", padx=2, pady=2)
        self._entry_step_mv_y.grid(column=2, row = 3, sticky="nsew", padx=2, pady=2)
        self._entry_graduation_x.grid(column=1, row = 4, sticky="nsew", padx=2, pady=2)
        self._entry_graduation_y.grid(column=2, row = 4, sticky="nsew", padx=2, pady=2)
        self._entry_step_x.grid(column=1, row = 5, sticky="nsew", padx=2, pady=2)

        self._button_push.grid(column=2, row = 5, sticky="nsew", padx=2, pady=2)


    def checkAndPush(self) :
        result = []
        for elem in self._params :
            try :
                result.append(float(elem.get()))
            except ValueError :
                label_output = tk.Label(self, text = "Erreur sur une des variables. Merci de vérifier.", fg = "#ffffff", border=0, bg="#202030")
                label_output.grid(column=0, columnspan= 3, row = 6, sticky="nsew", padx=2, pady=2)
                return

        self.master.setParams(result)
        label_output = tk.Label(self, text = "Les valeurs ont été appliquées.", fg = "#ffffff", border=0, bg="#202030")
        label_output.grid(column=0, columnspan= 3, row = 6, sticky="nsew", padx=2, pady=2)

        
class GraphWindow(tk.Toplevel) :
    def __init__(self, master : Calculatrice, function : typing.Callable) -> None :
        if (type(master) != Calculatrice) :
            raise TypeError
        
        super().__init__(master, bg="#202030")

        self.function = function
        self.canevas = tk.Canvas(self, bg = "#dddddd", highlightthickness=0, height=200, width=300)
        self.canevas.grid(row = 0, column = 0, columnspan= 4, padx=2, pady=2)

        self.top_left = [-5, 5]
        self.size_graph = [10, -20/3]

        self.step_mv = [0.5, 0.5]
        self.graduations = [1, 1]
        self.stepx = 0.01

        self.button_options = CalulatriceButton(self, text="Options", command=self.openOptionWindow, bg = "#4065d0", relief="flat")
        self.button_go_right = CalulatriceButton(self, text=">", command=self.goRight, bg = "#5585f0", relief="flat")
        self.button_go_left = CalulatriceButton(self, text="<", command=self.goLeft, bg = "#5585f0", relief="flat")
        self.button_go_up = CalulatriceButton(self, text="     ^     ", command=self.goUp, bg = "#5585f0", relief="flat")
        self.button_go_down = CalulatriceButton(self, text="     v     ", command=self.goDown, bg = "#5585f0", relief="flat")
        self.button_zoom_in = CalulatriceButton(self, text="Zoom +", command=self.zoomIn, bg = "#4065d0", relief="flat")
        self.button_zoom_out = CalulatriceButton(self, text="Zoom -", command=self.zoomOut, bg = "#4065d0", relief="flat")


        self.button_options.grid(row = 1, column=0, rowspan=2, padx=5, pady=5, sticky="nsew")
        self.button_go_down.grid(row = 2, column=2, padx=5, pady=5, sticky="nsew")
        self.button_go_up.grid(row = 1, column=2, padx=5, pady=5, sticky="nsew")
        self.button_go_left.grid(row = 2, column=1, padx=5, pady=5, sticky="nsew")
        self.button_zoom_in.grid(row = 1, column=1, padx=5, pady=5, sticky="nsew")
        self.button_go_right.grid(row = 2, column=3, padx=5, pady=5, sticky="nsew")
        self.button_zoom_out.grid(row = 1, column=3, padx=5, pady=5, sticky="nsew")

        for i in range(4) :
            self.columnconfigure(i, weight=1)
            if i < 3 :
                self.rowconfigure(i, weight=1)

        self.drawGraph()

    @property
    def function(self) -> typing.Callable :
        return self._func
    
    @function.setter
    def function(self, func : typing.Callable) :
        if not callable(func) :
            raise TypeError("La fonction n'est pas callable")
        else :
            self._func = func

    def setParams(self, list_par) :
        if type(list_par) != list :
            return TypeError
        if len(list_par) != 9 :
            return ValueError
        
        for elem in list_par :
            if (type(elem) != float) :
                raise TypeError
            print(elem)
            
        self.top_left = [list_par[0], list_par[1]]
        self.size_graph = [list_par[2], list_par[3]]

        self.step_mv = [list_par[4], list_par[5]]
        self.graduations = [list_par[6], list_par[7]]
        self.stepx = list_par[8]

        self.drawGraph()
        

    def openOptionWindow(self) -> None:
        ParamWindow(self)

    def goRight(self) -> None :
        self.top_left[0] += self.step_mv[0]
        self.drawGraph()

    def goLeft(self) -> None :
        self.top_left[0] -= self.step_mv[0]
        self.drawGraph()

    def goUp(self) -> None:
        self.top_left[1] += self.step_mv[1]
        self.drawGraph()

    def goDown(self) -> None :
        self.top_left[1] -= self.step_mv[1]
        self.drawGraph()

    def zoomIn(self) -> None :
        self.top_left[0] = - 1/math.sqrt(2) * self.size_graph[0] / 2 + self.size_graph[0] / 2 + self.top_left[0]
        self.top_left[1] = - 1/math.sqrt(2) * self.size_graph[1] / 2 + self.size_graph[1] / 2 + self.top_left[1]

        self.size_graph[0] *= 1/math.sqrt(2)
        self.size_graph[1] *= 1/math.sqrt(2)

        self.drawGraph()


    def zoomOut(self) -> None :
        self.top_left[0] = - math.sqrt(2) * self.size_graph[0] / 2 + self.size_graph[0] / 2 + self.top_left[0]
        self.top_left[1] = - math.sqrt(2) * self.size_graph[1] / 2 + self.size_graph[1] / 2 + self.top_left[1]

        self.size_graph[0] *= math.sqrt(2)
        self.size_graph[1] *= math.sqrt(2)

        self.drawGraph()

    def translateCoords(self, coords : tuple[int]) -> tuple[int] :
        return (((coords[0] - self.top_left[0]) / self.size_graph[0]) * 300, ((coords[1] - self.top_left[1]) / self.size_graph[1]) * 200)


    def drawGraduations(self) -> None :
        x = self.top_left[0] // self.graduations[0]

        while x < self.top_left[0] + self.size_graph[0] :
            g = self.translateCoords((x, 0))
            self.canevas.create_line(g[0], g[1]-3, g[0], g[1]+3)
            x += self.graduations[0]

        y = self.top_left[1] // self.graduations[1]

        while y > self.top_left[1] + self.size_graph[1] :
            g = self.translateCoords((0, y))
            self.canevas.create_line(g[0]-3, g[1], g[0]+3, g[1])
            y -= self.graduations[1]
        

    def drawGraph(self) -> None :
        self.canevas.delete("all")
        ox1 = self.translateCoords((0, self.top_left[1]))
        ox2 = self.translateCoords((0, self.top_left[1] + self.size_graph[1]))
        oy1 = self.translateCoords((self.top_left[0], 0))
        oy2 = self.translateCoords((self.top_left[0] + self.size_graph[0], 0))

        self.canevas.create_line(ox1[0], ox1[1], ox2[0], ox2[1])
        self.canevas.create_line(oy1[0], oy1[1], oy2[0], oy2[1])
        
        self.drawGraduations()

        prev = None
        current_x = float(self.top_left[0])
        while current_x < self.size_graph[0] + self.top_left[0] :
            try :
                val = self.function(current_x)
            except ZeroDivisionError :
                val = None

            if prev != None and val != None:
                p1 = self.translateCoords(((current_x - self.stepx), prev))
                p2 = self.translateCoords((current_x, val))
                self.canevas.create_line(p1[0], p1[1], p2[0], p2[1])
                #self.canevas.create_line((((current_x - self.stepx) - self.top_left[0]) / self.size_graph[0]) * 300, ((prev - self.top_left[1]) / self.size_graph[1]) * 200, (((current_x) - self.top_left[0]) / self.size_graph[0]) * 300, ((val - self.top_left[1]) / self.size_graph[1]) * 200)
            prev = val
            current_x += self.stepx



class Calculatrice(tk.Tk) :
    def __init__(self, size = (400, 500)) -> None :
        tk.Tk.__init__(self)
        self.title("Calculatrice")
        self.graph_mode = False
        self._trigger_reset = False
        self._txt = tk.StringVar()
        self._historal = Historal()
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

        list_btns_char =   [("cos", 2, 0), ("sin", 2, 1), ("tan", 2, 2), ('π', 2, 3), ('sqrt', 2, 4),
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

        self.do_opeation_button = CalulatriceButton(self.frame, command=self.doCalculation, text="=", background="#5585f0", relief="flat")
        self.do_opeation_button.grid(row = 6, column = 0, padx=5, pady=5, sticky="nsew")

        btm_color = "#4065d0"

        self.graphic_mode_button = CalulatriceButton(self.frame, command=self.goGraphicMode, text="Mode graphique", background=btm_color, relief="flat")
        self.graphic_mode_button.grid(row = 7, column = 1, padx=5, pady=5, sticky="nsew", columnspan=2)

        self.historique_mode_button = CalulatriceButton(self.frame, command=self.goHistoricMode, text="Historique", background=btm_color, relief="flat")
        self.historique_mode_button.grid(row = 7, column = 3, padx=5, pady=5, sticky="nsew", columnspan=2) 

        self.clear_button = CalulatriceButton(self.frame, command=self.clearArea, text="cls", background=btm_color, relief="flat")
        self.clear_button.grid(row = 7, column = 0, padx=5, pady=5, sticky="nsew", columnspan=1)       


    def addChar(self, char : str) -> None:
        if self._trigger_reset :
            self._txt.set("" if not self.graph_mode else "y = ") 
            self._trigger_reset = False

        self._txt.set(self._txt.get() + char)
            

    def clearArea(self) -> None:
        if not self.graph_mode :
            self._txt.set("")
        else :
            self._txt.set("y = ")
        
        self._trigger_reset = False


    def doCalculation(self) -> None:
        if not self.graph_mode :
            if "=" in self._txt.get() :
                return
            try :
                self._txt.set(self._txt.get() + f" = {Calculation(self._txt.get()).Calculate()}")
                self._historal.opEffectued(self._txt.get())
            except RecursionError:
                self._txt.set("Opération saisie non valide")
            except ValueError:
                self._txt.set("Opération saisie non valide")
            except AttributeError:
                self._txt.set("Opération saisie non valide")
            
        else :
            txt = self._txt.get().lstrip("y = ")
            try : 
                GraphWindow(self, Calculation(txt).Calculate)
            except RecursionError:
                self._txt.set("Opération saisie non valide")
            except ValueError:
                self._txt.set("Opération saisie non valide")
            except AttributeError:
                self._txt.set("Opération saisie non valide")

        self._trigger_reset = True
        
    def goGraphicMode(self) -> None:
        if not self.graph_mode :
            self.graph_mode = True
            self.button_multifunc.setChar("x")
        else :
            self.graph_mode = False
            self.button_multifunc.setChar("²")
        
        self.clearArea()


    def goHistoricMode(self) -> None:
        HistoralWindow(self, self._historal)
        
        

def main() :
    calc = Calculatrice()
    calc.mainloop()

if __name__ == "__main__" :
    main()
