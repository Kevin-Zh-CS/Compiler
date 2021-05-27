from abc import ABC, abstractmethod
import enum

from llvmlite.ir.types import ArrayType

from lexer import Lexer
import llvmlite.ir as ir
import llvmlite.binding as llvm

tokens = Lexer.tokens

# @enum.unique
# class Type(enum):

class Helper():
    base_type = {'integer': ir.IntType(32),
               'real': ir.FloatType(),
               'char': ir.IntType(8),
               'bool': ir.IntType(1)
               }

    @staticmethod
    def get_ir_type(type, length=0, str=None):
        if str != None:
            length = len(str)
        if length == 0:
            if isinstance(type, ir.Type):
                return type
            if type in Helper.base_type:
                return Helper.base_type[type]
        else:
            if type == 'string':
                return ir.ArrayType(ir.IntType(8), length)
            else:   # for arrays, 'type' is the type of elements
                if isinstance(type, ir.Type):
                    return ir.ArrayType(type, length)
                if type in Helper.base_type:
                    return ir.ArrayType(Helper.base_type[type], length)
                
        raise Exception("Invalid data type")
    
    @staticmethod
    def get_ir_var(ir_type, var):
        if type == 'string':
            value = bytearray(var.encode("utf-8"))
        elif type == 'bool':
                if var == 'true':
                    value = 1
                elif var == 'flase':
                    value = 0
                else:
                    value = var
            # value = int(eval(var.capitalize())) if type == 'bool' else var
        else:
            value = var
        ir_var = ir.Constant(ir_type, value)
        return ir_var
    

class SymbolTable(object):


    def __init__(self):
        self.global_table = {}
        # self.func_table = {}
        # self.scope_table = []   # each item stores symbols' id for a single scope
        # self.var_table = {}
        # self.fn_table = {}
        # self.scope_var = {}
        # self.scope_fn = {}
        # self.type_table = {}
        # self.scope_type = {}
        self.scope_table = [[]]   # each item stores symbols' id for a single scope
    
    def open_scope(self):
        self.scope_table.append([])
    
    def close_scope(self):
        for id in self.scope_table[-1]:
            self.global_table[id].pop() # delete from global table
            if self.global_table[id] == []:
                self.global_table.pop(id)
        self.scope_table.pop()  # delete this scope
    
    def add_symbol(self, id, type, addr, ele_type=None, ret_type=None, formal_list=[]):    # TODO func and proc entry(type)
        if id in self.scope_table[-1]:
            raise Exception("Redefine symbol %s!" % id)

        self.scope_table[-1].append(id)
        self.global_table.setdefault(id, [])    # add an empty list if the symbol is not in the table

        entry = {}
        entry['type'] = type
        entry['addr'] = addr
        if type not in Helper.base_type and type != 'string':
            # array, function or procedure
            if type == 'array':
                entry['ele_type'] = ele_type
            elif type == 'function':
                entry['ret_type'] = ret_type
                entry['formal_list'] = formal_list
            elif type == 'procedure':
                entry['formal_list'] = formal_list
            else:
                raise Exception("Invalid data type")

        self.global_table[id].append(entry)

    # def add_var(self, var_name, addr, scope_id, var_type=None):
    #     self.var_table.setdefault(var_name, []).append((addr, var_type))
    #     self.scope_var.setdefault(scope_id, []).append(var_name)

    # def add_fn(self, fn_name, fn_block, scope_id):
    #     self.fn_table.setdefault(fn_name, []).append(fn_block)
    #     self.scope_fn.setdefault(scope_id, []).append(fn_name)

    # def add_type(self, name, type_def, scope_id):
    #     self.type_table.setdefault(name, []).append(type_def)
    #     self.scope_type.setdefault(scope_id, []).append(name)

    # def fetch_var_addr(self, var_name):
    #     o = self.var_table.get(var_name, None)
    #     if o:
    #         return o[-1][0]
    #     else:
    #         raise CodegenError('Can not find symble {0}'.format(var_name))

    # def fetch_var_addr_type(self, var_name):
    #     o = self.var_table.get(var_name, None)
    #     if o:
    #         return o[-1]
    #     else:
    #         raise CodegenError('Can not find symble {0}'.format(var_name))

    # def fetch_fn_block(self, fn_name):
    #     o = self.fn_table.get(fn_name, None)
    #     if o:
    #         return o[-1]
    #     else:
    #         raise CodegenError('Can not find function {0}'.format(fn_name))

    # def fetch_type(self, type_name):
    #     o = self.type_table.get(type_name, None)
    #     if o:
    #         return o[-1]
    #     else:
    #         raise CodegenError('Can not find type {0}'.format(type_name))

    # def remove_var(self, var_name):
    #     o = self.var_table.get(var_name, None)
    #     if o:
    #         del o[-1]
    #     else:
    #         raise CodegenError('Remove var {0} that not exsists!'.format(var_name))

    # def remove_scope(self, scope_id):
    #     for name in self.scope_var.get(scope_id, []):
    #         o = self.var_table.get(name, None)
    #         if o:
    #             del o[-1]
    #         else:
    #             raise CodeGenerator('Remove var {0} that not exsists!'.format(name))
    #     del self.scope_var[scope_id]
    #     scope_id += 1
    #     for name in self.scope_fn.get(scope_id, []):
    #         o = self.fn_table.get(name, None)
    #         if o:
    #             del o[-1]
    #         else:
    #             raise CodeGenerator('Remove var {0} that not exsists!'.format(name))
    #     if scope_id in self.scope_fn.keys():
    #         del self.scope_fn[scope_id]


class Node(ABC):
    
    builder  = None
    module = None
    symbol_table = SymbolTable()

    # @staticmethod
    # def init_nodes(workbase):
    #     builder, module, symbol_table = workbase

    @staticmethod
    def get_exp_var(exp):
        pass
        return value

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
        self.irgen()

    def irgen(self):
        for var in self.var_list:
            var.irgen()

class Var(Node):
    def __init__(self, id_list, vartype, var):
        super().__init__()
        self.id_list = id_list
        self.vartype = vartype  # type or ArrayType
        self.var = var  # None if no initialization value
                        # otherwise Exp
    
    def irgen(self):
        ''' get addr
            initialize
            store symbol to symbol table
        '''
        if isinstance(self.vartype, ArrayType):
            ir_type = Helper.get_ir_type(self.vartype, length=self.vartype.length)
            self.type = 'array'
        elif self.vartype == 'string':
            ir_type = Helper.get_ir_type(self.vartype, str=self.var)
            self.type = self.vartype
        else:
            ir_type = Helper.get_ir_type(self.vartype)
            self.type = self.vartype

        with Node.builder.goto_entry_block():
            for id in self.id_list:
                addr = Node.builder.alloca(ir_type, name=id)
                if self.var:    # initialize variable
                    ir_var = Node.get_exp_var(self.var)
                    Node.builder.store(ir_var, addr)   # store value
                self.symbol_table.add_symbol(id, self.type, addr)

class ConstExp(Node):
    def __init__(self, id_list, var):
        super().__init__()
        self.id_list = id_list
        self.var = var  # LiteralVal

    def irgen(self):
        self.var.irgen()
        with Node.builder.goto_entry_block():
            for id in self.id_list:
                addr = Node.builder.alloca(self.var.ir_type, name=id)
                Node.builder.store(self.var.ir_var, addr)   # store value
                self.symbol_table.add_symbol(id, self.var.type, addr)
                # TODO add to symbol table, including id, type and ir_var


class LiteralVar(Node):
    def __init__(self, var, type):
        super().__init__()
        self.var = var
        self.type = type    # a string in ['int', 'real', 'bool', 'char', 'string']
    
    def irgen(self):
        ''' generate self.ir_var '''
        if self.type == 'string':
            self.ir_type = Helper.get_ir_type(self.type, str=self.var)
        else:
            self.ir_type = Helper.get_ir_type(self.type)
        self.ir_var = Helper.get_ir_var(self.ir_type, self.var)
        # if self.type == 'string':
        #     length = len(self.var)
        #     value = bytearray(self.var.encode("utf-8"))
        # else:
        #     length = 0
        #     value = int(eval(self.var.capitalize())) if self.type == 'bool' else self.var
        # self.ir_type = Helper.get_ir_type(self.type, length)
        # self.ir_var = ir.Constant(self.ir_type, value)

class LabelList(Node):
    def __init__(self, label_list):
        super().__init__()
        self.id_list = label_list

class ConstList(Node):
    def __init__(self, const_list):
        super().__init__()
        self.const_list = const_list
        self.irgen()
    
    def irgen(self):
        for const_exp in self.const_list:
            const_exp.irgen()

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
        self.formal_list = formal_list  # a list of formal
        self.ret_type = ret_type

class Formal(Node):
    def __init__(self, id_list, para_type):
        super().__init__()
        self.id_list = id_list  # a list of strings
        self.var_type = para_type   # type or ArrayType

class ArrayType(Node):
    def __init__(self,length,low_bound, type):
        super().__init__()
        self.length = length
        self.low_bound = low_bound
        self.type = type    # Type?
    
class Compound(Node):
    def __init__(self,stmt_list):
        super().__init__()
        self.stmt_list = stmt_list

class LabelStmt(Node):
    def __init__(self,id,non_label_stmt):
        super().__init__()
        self.id = id
        self.label_stmt = non_label_stmt

class Assign(Node):
    def __init__(self, lvalue, exp):
        super().__init__()
        self.lvalue = lvalue    # lvalue can be either ID or array
        self.exp = exp  # exp is None if lvalue is ID

class LValue(Node):
    def __init__(self, id, exp):
        super().__init__()
        self.id = id
        self.exp = exp  # none if not array


class Call(Node):
    # include type conversion, e.g., Integer(10.1)
    def __init__(self,id,exp):
        super().__init__()
        self.id = id
        self.exp = exp

class For(Node):
    def __init__(self,id,exp1,direct,exp2,stmt):
        super().__init__()
        self.id = id
        self.exp1 = exp1
        self.direct = direct
        self.exp2 = exp2
        self.stmt = stmt

class Case(Node):
    def __init__(self, exp, case_exp_list):
        super().__init__()
        self.exp  = exp
        self.case_exp_list = case_exp_list

class While(Node):
    def __init__(self, exp, stmt):
        super().__init__()
        self.exp = exp
        self.stmt = stmt

class Repeat(Node):
    def __init__(self, stmt_list, exp):
        super().__init__()
        self.stmt_list = stmt_list
        self.exp = exp

class If(Node):
    def __init__(self, exp, stmt, else_stmt):
        super().__init__()
        self.exp = exp
        self.stmt = stmt
        self.else_stmt = else_stmt

class CaseExp(Node):
    def __init__(self, name, stmt):
        super().__init__()
        self.name = name
        self.stmt = stmt

class Goto(Node):
    def __init__(self, id):
        super().__init__()
        self.id = id

class BinExp(Node):
    def __init__(self, operant, exp1, exp2):
        super().__init__()
        self.operant = operant
        self.exp1 = exp1
        self.exp2 = exp2
        self.type = None    # type of result
        # self.irgen()

    def irgen(self):
        ''' operant belongs to ['+', '-', '*', '/', '%', 
            '=', '<>', '<', '>', '<=', '>=', 'and', 'or'
        '''
        # exp1 = self.exp1.irgen()
        # exp2 = self.exp2.irgen()
        a = 1
        

class UniExp(Node):
    def __init__(self, operant, exp):
        super().__init__()
        self.operant = operant
        self.exp = exp
        self.type = None

class Array(Node):
    def __init__(self, id, index):
        super().__init__()
        self.id = id
        self.index = index

