from enum import Enum
from itertools import product
from llvmlite import ir
from collections import deque, defaultdict, OrderedDict
from error import *

class Builtin:
    def __init__(self) -> None:
        pass

class SysbolTable:
    def __init__(self, module) -> None:
        self.module = module
        self.scopes = []

    def __del__(self):
        if len(self.my_scopes)>1:
            raise PCLSymbolTableError("missing end")

    def begin(self,name = None):
        self.scopes.append(Scope(name))
    
    def end(self):
        self.scopes.pop(-1)
    
    def get(self,name,last = False):
        if last:
            result = self.scopes[-1].get(name)
            if result is not None:
                return result
        else:
            for scope in reversed(self.scopes):
                result = scope.get(name)
                if result is not None:
                    return result
        msg = f"Unknown name: {name}"
        raise PCLSymbolTableError(msg)
    
    def put(self,name,sta):
        if len(self.scopes)>0:
            self.scopes[-1].put(name,sta)
        else:
            msg = f"No existing scope"
            raise PCLSymbolTableError(msg)

class Scope:
    def __init__(self,name) -> None:
        self.name = name
        self.locals = {}
    
    def get(self,name):
        return self.locals.get(name,None)
    
    def put(self,name,sta):
        if name in self.locals.keys:
            msg = f"name {name}has been used"
            raise PCLSymbolTableError(msg)
        else:
            self.locals[name] = sta
