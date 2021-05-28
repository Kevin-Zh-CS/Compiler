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
    base_type = {'int': ir.IntType(32),
                 'real': ir.FloatType(),
                 'char': ir.IntType(8),
                 'bool': ir.IntType(1)
                }

    artimetic_op = ['+', '-', '*', '/', '%']
    relation_op = ['=', '<>', '<', '>', '<=', '>=']
    logic_op = ['not', 'and']

    ir_relation_op = {'=': '==',
                      '<>': '!=',
                      '<': '<',
                      '>': '>',
                      '<=': '<=',
                      '>=': '>=' 
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
    def get_ir_var(ir_type, var, is_str=0):
        if is_str:
            value = bytearray(var.encode("utf-8"))
        elif ir_type == ir.IntType(1):  # bool
                if var == 'true':
                    value = 1
                elif var == 'false':
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
    
    def add_symbol(self, id, type, addr, length=0, low_bound=0, ele_type=None, ret_type=None, formal_list=[]):   
        # TODO func and proc entry(type)
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
                assert length != 0 and ele_type in Helper.base_type
                entry['ele_type'] = ele_type
                entry['length'] = length
                entry['low_bound'] = low_bound
            elif type == 'function':
                entry['ret_type'] = ret_type
                entry['formal_list'] = formal_list
            elif type == 'procedure':
                entry['formal_list'] = formal_list
            else:
                raise Exception("Invalid data type")

        self.global_table[id].append(entry)
    
    def get_symbol(self, id):
        id_list = self.global_table.get(id, None)
        if id_list:
            return id_list[-1]
        else:
            raise Exception("No symbol named \'%s\'!" % id)
    
    def get_symbol_type(self, id):
        return self.get_symbol(id)['type']
    
    def get_symbol_addr(self, id):
        return self.get_symbol(id)['addr']

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
    def __init__(self, id_list, vartype, exp):
        super().__init__()
        self.id_list = id_list
        self.vartype = vartype  # type or ArrayType
        self.exp = exp  # None if no initialization value
                        # otherwise Exp
    
    def irgen(self):
        ''' get addr
            initialize
            store symbol to symbol table
        '''
        if isinstance(self.vartype, ArrayType):
            ir_type = Helper.get_ir_type(self.vartype.type, length=self.vartype.length)
            self.type = 'array'
        elif self.vartype == 'string':
            ir_type = Helper.get_ir_type(self.vartype, str=self.exp.var)
            self.type = self.vartype
        else:
            ir_type = Helper.get_ir_type(self.vartype)
            self.type = self.vartype

        with Node.builder.goto_entry_block():
            for id in self.id_list:
                addr = Node.builder.alloca(ir_type, name=id)
                if self.exp:    # initialize variable
                    self.exp.irgen()
                    Node.builder.store(self.exp.ir_var, addr)   # store value
                # add to symbol table
                if isinstance(self.vartype, ArrayType): # array
                    Node.symbol_table.add_symbol(id, self.type, addr, self.vartype.length, self.vartype.low_bound, self.vartype.type)
                else:
                    Node.symbol_table.add_symbol(id, self.type, addr)

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
                Node.symbol_table.add_symbol(id, self.var.type, addr)

class IdExp(Node):
    def __init__(self, id):
        super().__init__()
        self.id = id    # a string
    
    def irgen(self):
        self.type = Node.symbol_table.get_symbol_type(self.id)
        addr = Node.symbol_table.get_symbol(self.id)['addr']
        self.ir_var = Node.builder.load(addr)

class LiteralVar(Node):
    def __init__(self, var, type):
        super().__init__()
        self.var = var
        self.type = type    # a string in ['int', 'real', 'bool', 'char', 'string']
    
    def irgen(self):
        ''' set self.ir_var '''
        if self.type == 'string':
            self.ir_type = Helper.get_ir_type(self.type, str=self.var)
            self.ir_var = Helper.get_ir_var(self.ir_type, self.var, is_str=1)
        else:
            self.ir_type = Helper.get_ir_type(self.type)
            self.ir_var = Helper.get_ir_var(self.ir_type, self.var)

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
    
    def irgen(self):
        for formal in self.formal_list:
            formal.irgen()

class Formal(Node):
    def __init__(self, id_list, para_type):
        super().__init__()
        self.id_list = id_list  # a list of strings
        self.vartype = para_type   # type or ArrayType
    
    def irgen(self):
        ''' add ids to symbol table '''
        for id in self.id_list:
            # get symbol type and ir_type
            if isinstance(self.vartype, ArrayType):
                ir_type = Helper.get_ir_type(self.vartype.type, length=self.vartype.length)
                self.type = 'array'
            elif self.vartype == 'string':
                ir_type = Helper.get_ir_type(self.vartype, str="formal")
                self.type = self.vartype
            else:
                ir_type = Helper.get_ir_type(self.vartype)
                self.type = self.vartype

            with Node.builder.goto_entry_block():
                for id in self.id_list:
                    addr = Node.builder.alloca(ir_type, name=id)
                    if isinstance(self.vartype, ArrayType): # array
                        Node.symbol_table.add_symbol(id, self.type, addr, self.vartype.length, self.vartype.low_bound, self.vartype.type)
                    else:
                        Node.symbol_table.add_symbol(id, self.type, addr)
            

class ArrayType(Node):
    def __init__(self,length,low_bound, type):
        super().__init__()
        self.length = length
        self.low_bound = low_bound
        self.type = type
    
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
    
    def irgen(self):
        self.lvalue.irgen()
        self.exp.irgen()
        # check type
        if self.lvalue.type != self.exp.type:
            raise Exception("unsupported operand type(s) for :=: '%s' and '%s'." % (self.lvalue.type, self.exp.type))
        with Node.builder.goto_entry_block():
            Node.builder.store(self.exp.ir_var, self.lvalue.addr)   # assign value

class LValue(Node):
    def __init__(self, id, exp):
        super().__init__()
        self.id = id
        self.exp = exp  # none if not array

    def irgen(self):
        ''' set the address of left value self.addr
            set self.type
        '''
        symbol_entry = Node.symbol_table.get_symbol(self.id)
        self.addr = symbol_entry['addr']
        self.type = symbol_entry['type']
        if self.exp:    # array
            assert self.type == 'array'
            self.type = symbol_entry['ele_type']
            # add1 = Node.builder.gep(addr, [ir.Constant(ir.IntType(32),0)])
            self.exp.irgen()
            # gep: get element ptr
            self.addr = Node.builder.gep(self.addr, [ir.Constant(ir.IntType(32),0), self.exp.ir_var])



class Call(Node):
    # include type conversion, e.g., Int(10.1)
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
    def __init__(self, operator, exp1, exp2):
        super().__init__()
        self.operator = operator
        self.exp1 = exp1
        self.exp2 = exp2

    def irgen(self):
        ''' operator belongs to ['+', '-', '*', '/', '%', 
            '=', '<>', '<', '>', '<=', '>=', 'and', 'or'
            generate self.type and self.ir_var
        '''
        self.exp1.irgen()
        self.exp2.irgen()
        # check type
        if self.exp1.type != self.exp2.type:
            raise Exception("unsupported operand type(s) for %s: '%s' and '%s'." % (self.operator, self.exp1.type, self.exp2.type))
        if self.operator in Helper.artimetic_op:
            # arithmetic operation
            self.type = self.exp1.type
            if self.type == 'int':
                if self.operator == '+':
                    self.ir_var = Node.builder.add(self.exp1.ir_var, self.exp2.ir_var)
                elif self.operator == '-':
                    self.ir_var = Node.builder.sub(self.exp1.ir_var, self.exp2.ir_var)
                elif self.operator == '*':
                    self.ir_var = Node.builder.mul(self.exp1.ir_var, self.exp2.ir_var)
                elif self.operator == '/':
                    self.ir_var = Node.builder.sdiv(self.exp1.ir_var, self.exp2.ir_var)
                elif self.operator == '%':
                    self.ir_var = Node.builder.srem(self.exp1.ir_var, self.exp2.ir_var)
            elif self.operator == 'real':
                if self.operator == '+':
                    self.ir_var = Node.builder.fadd(self.exp1.ir_var, self.exp2.ir_var)
                elif self.operator == '-':
                    self.ir_var = Node.builder.fsub(self.exp1.ir_var, self.exp2.ir_var)
                elif self.operator == '*':
                    self.ir_var = Node.builder.fmul(self.exp1.ir_var, self.exp2.ir_var)
                elif self.operator == '/':
                    self.ir_var = Node.builder.fdiv(self.exp1.ir_var, self.exp2.ir_var)
        elif self.operator in Helper.relation_op:
            # realationship operation
            self.type = 'bool'
            op = Helper.ir_relation_op[self.operator]
            operant_type = self.exp1.type
            if operant_type == 'int' or operant_type == 'bool':
                self.ir_var = Node.builder.icmp_signed(op, self.exp1.ir_var, self.exp2.ir_var)
            else:
                self.ir_var = Node.builder.fcmp_ordered(op, self.exp1.ir_var, self.exp2.ir_var)
        elif self.operator in Helper.logic_op:
            if self.operator == 'and':
                self.ir_var = Node.builder.and_(self.exp1.ir_var, self.exp2.ir_var)
            elif self.operator == 'or':
                self.ir_var = Node.builder.or_(self.exp1.ir_var, self.exp2.ir_var)      
        try:
            assert self.ir_var and self.type    # make sure the assignment is successful            
        except:
            raise Exception("unsupported operand type(s) for %s: '%s' and '%s'." % (self.operator, self.exp1.type, self.exp2.type))
        

class UniExp(Node):
    def __init__(self, operator, exp):
        super().__init__()
        self.operator = operator
        self.exp = exp
    
    def irgen(self):
        ''' set self.ir_var and self.type
            operator belongs to ['not', '+', '-']
        '''
        self.exp.irgen()
        if self.operator == 'not':
            self.type = 'bool'
            self.ir_var = Node.builder.not_(self.exp.ir_var)
        elif self.operator == '+':
            self.type = self.exp.type
            self.ir_var = self.exp.ir_var
        elif self.operator == '-':
            self.type = self.exp.type
            if self.type == 'int':
                self.ir_var = Node.builder.neg(self.exp.ir_var)
            elif self.type == 'real':
                self.ir_var = Node.builder.fsub(ir.Constant(ir.IntType(32), 0), self.exp.ir_var)
        
        try:
            assert self.ir_var and self.type    # make sure the assignment is successful            
        except:
            raise Exception("unsupported operand type(s) for %s: '%s'." % (self.operator, self.exp.type))
        

class Array(Node):
    def __init__(self, id, exp):
        super().__init__()
        self.id = id
        self.exp = exp
    
    def irgen(self):
        ''' set self.ir_var and self.type
        '''
        # ir_var = id[exp]
        symbol_entry = Node.symbol_table.get_symbol(self.id)
        self.addr = symbol_entry['addr']
        self.type = symbol_entry['type']

        assert self.type == 'array'
        self.type = symbol_entry['ele_type']
        self.exp.irgen()
        # gep: get element ptr
        addr = Node.builder.gep(self.addr, [ir.Constant(ir.IntType(32),0), self.exp.ir_var])
        self.ir_var = Node.builder.load(addr)

