from abc import ABC, abstractmethod
from lexer import Lexer
import llvmlite.ir as ir
import llvmlite.binding as llvm

tokens = Lexer.tokens

class SymbleTable(object):
    def __init__(self):
        self.var_table = {}
        self.fn_table = {}
        self.scope_var = {}
        self.scope_fn = {}
        self.type_table = {}
        self.scope_type = {}

    def add_var(self, var_name, addr, scope_id, var_type=None):
        self.var_table.setdefault(var_name, []).append((addr, var_type))
        self.scope_var.setdefault(scope_id, []).append(var_name)

    def add_fn(self, fn_name, fn_block, scope_id):
        self.fn_table.setdefault(fn_name, []).append(fn_block)
        self.scope_fn.setdefault(scope_id, []).append(fn_name)

    def add_type(self, name, type_def, scope_id):
        self.type_table.setdefault(name, []).append(type_def)
        self.scope_type.setdefault(scope_id, []).append(name)

    def fetch_var_addr(self, var_name):
        o = self.var_table.get(var_name, None)
        if o:
            return o[-1][0]
        else:
            raise CodegenError('Can not find symble {0}'.format(var_name))

    def fetch_var_addr_type(self, var_name):
        o = self.var_table.get(var_name, None)
        if o:
            return o[-1]
        else:
            raise CodegenError('Can not find symble {0}'.format(var_name))

    def fetch_fn_block(self, fn_name):
        o = self.fn_table.get(fn_name, None)
        if o:
            return o[-1]
        else:
            raise CodegenError('Can not find function {0}'.format(fn_name))

    def fetch_type(self, type_name):
        o = self.type_table.get(type_name, None)
        if o:
            return o[-1]
        else:
            raise CodegenError('Can not find type {0}'.format(type_name))

    def remove_var(self, var_name):
        o = self.var_table.get(var_name, None)
        if o:
            del o[-1]
        else:
            raise CodegenError('Remove var {0} that not exsists!'.format(var_name))

    def remove_scope(self, scope_id):
        for name in self.scope_var.get(scope_id, []):
            o = self.var_table.get(name, None)
            if o:
                del o[-1]
            else:
                raise CodeGenerator('Remove var {0} that not exsists!'.format(name))
        del self.scope_var[scope_id]
        scope_id += 1
        for name in self.scope_fn.get(scope_id, []):
            o = self.fn_table.get(name, None)
            if o:
                del o[-1]
            else:
                raise CodeGenerator('Remove var {0} that not exsists!'.format(name))
        if scope_id in self.scope_fn.keys():
            del self.scope_fn[scope_id]


class Node(ABC):
    
    builder  = None
    module = ir.Module
    symbol_table = SymbleTable()

    @staticmethod
    def init_nodes(workbase):
        builder, module, symbol_table = workbase

    
    
    # @abstractmethod
    def irgen(self):
        ''' code generation '''
        msg = f'irgen method not implemented for {self.__class__.__name__}'
        raise NotImplementedError(msg)

class Program(Node):
    def __init__(self, name, body):
        super().__init__()
        self.name = name
        self.body = body

    def irgen(self):
        ir.FunctionType(ir.VoidType(), ())
        



class Body(Node):
    def __init__(self, block, local_list):
        super().__init__()
        self.block = block
        self.local_list = local_list

    def irgen(self):
        for local in self.local_list:
            local.irgen()
        self.block.irgen()


class VarList(Node):
    def __init__(self, var_list):
        super().__init__()
        self.var_list = var_list
    def irgen(self):
        for var in self.vars:
            var.irgen()

class Var(Node):
    def __init__(self, id_list, vartype, var):
        super().__init__()
        self.id_list = id_list
        self.vartype = vartype
        self.var = var

class ConstExp(Node):
    def __init__(self, id_list, var):
        super().__init__()
        self.id_list = id_list
        self.var = var

class LiteralVar(Node):
    def __init__(self, var, type):
        super().__init__()
        self.var = var
        self.type = type    # a string in ['int', 'real', 'bool', 'char', 'string']
    
class LabelList(Node):
    def __init__(self, label_list) -> None:
        super().__init__()
        self.id_list = label_list

class ConstList(Node):
    def __init__(self, const_list) -> None:
        super().__init__()
        self.const_list = const_list

class LocalHeader(Node):
    def __init__(self,header,body):
        super().__init__()
        self.header = header
        self.body = body

class ProcHeader(Node):
    def __init__(self, id, formal_list):
        super().__init__()
        self.id = id
        self.formal_list = formal_list
        
class FuncHeader(Node):
    def __init__(self, id, formal_list, ret_type):
        super().__init__()
        self.id = id
        self.formal_list = formal_list
        self.ret_type = ret_type

class Formal(Node):
    def __init__(self, id_list, para_type) -> None:
        super().__init__()
        self.id_list = id_list
        self.var_type = para_type
        
class Type(Node):
    def __init__(self, type) -> None:
        super().__init__()
        self.type = type

class ArrayType(Node):
    def __init__(self,length,type) -> None:
        super().__init__()
        self.length = length
        self.type = type    
    def irgen(self):
        array_range = self.length
        left_bound = None   # TODO
    
class Compound(Node):
    def __init__(self,stmt_list) -> None:
        super().__init__()
        self.stmt_list = stmt_list

class LabelStmt(Node):
    def __init__(self,id,non_label_stmt) -> None:
        super().__init__()
        self.id = id
        self.label_stmt = non_label_stmt

class Assign(Node):
    def __init__(self, lvalue, exp) -> None:
        super().__init__()
        self.lvalue = lvalue
        self.exp = exp

class LValue(Node):
    def __init__(self, id, exp) -> None:
        super().__init__()
        self.id = id
        self.exp = exp


class Call(Node):
    def __init__(self,id,exp) -> None:
        super().__init__()
        self.id = id
        self.exp = exp

class For(Node):
    def __init__(self,id,exp1,direct,exp2,stmt) -> None:
        super().__init__()
        self.id = id
        self.exp1 = exp1
        self.direct = direct
        self.exp2 = exp2
        self.stmt = stmt

class Case(Node):
    def __init__(self, exp, case_exp_list) -> None:
        super().__init__()
        self.exp  = exp
        self.case_exp_list = case_exp_list

class While(Node):
    def __init__(self, exp, stmt) -> None:
        super().__init__()
        self.exp = exp
        self.stmt = stmt

class Repeat(Node):
    def __init__(self, stmt_list, exp) -> None:
        super().__init__()
        self.stmt_list = stmt_list
        self.exp = exp

class If(Node):
    def __init__(self, exp, stmt, else_stmt) -> None:
        super().__init__()
        self.exp = exp
        self.stmt = stmt
        self.else_stmt = else_stmt

class CaseExp(Node):
    def __init__(self, name, stmt) -> None:
        super().__init__()
        self.name = name
        self.stmt = stmt

class Goto(Node):
    def __init__(self, id) -> None:
        super().__init__()
        self.id = id

class BinExp(Node):
    def __init__(self, operant, exp1, exp2) -> None:
        super().__init__()
        self.operant = operant
        self.exp1 = exp1
        self.exp2 = exp2

class UniExp(Node):
    def __init__(self, operant, exp) -> None:
        super().__init__()
        self.operant = operant
        self.exp = exp

class Array(Node):
    def __init__(self, id, index) -> None:
        super().__init__()
        self.id = id
        self.index = index

