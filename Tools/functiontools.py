class PrintableFunction :
    def __init__(self, func, name, params = None) :
        self.func = func
        self.name = name
        self.params = params

    @property
    def name(self) :
        return self._name

    @name.setter
    def name(self, val) :
        self._name = str(val)

    @property
    def func(self) :
        return self._func

    @func.setter
    def func(self, val) :
        if not callable(val) :
            raise TypeError("Le type n'est pas une fonction.")
        self._func = val

    @property
    def params(self) :
        return self._params

    @params.setter
    def params(self, val) :
        self._params = val    

    def __str__(self) :
        return self.name
    
    def __call__(self, *args, **kwargs) :
        if self.params != None :
            self.func.__call__(self.params, *args, **kwargs)
        else :
            self.func.__call__(*args, **kwargs)