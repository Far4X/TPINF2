import typing

class PrintableFunction :
    def __init__(self, func : typing.Callable, name : str, params = None) :
        self.func = func
        self.name = name
        self.params = params

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, val : str) -> None :
        self._name = str(val)

    @property
    def func(self) -> typing.Callable:
        return self._func

    @func.setter
    def func(self, val : typing.Callable) :
        if not callable(val) :
            raise TypeError("Le type n'est pas une fonction.")
        self._func = val

    @property
    def params(self) :
        return self._params

    @params.setter
    def params(self, val : dict | object) :
        self._params = val   

    def __str__(self) :
        return self.name
    
    def __call__(self, *args, **kwargs) -> typing.Any :
        if self.params != None :
            return self.func.__call__(self.params, *args, **kwargs)
        else :
            return self.func.__call__(*args, **kwargs)