from abc import ABC

import llvmlite.ir as ir
import llvmlite.binding as llvm

from lexer import Lexer
from helper import Helper, SymbolTable

tokens = Lexer.tokens


class Node(ABC):
    builder = None
    module = None
    main_func = None
    symbol_table = SymbolTable()


class Program(Node):
    def __init__(self, name, body):
        super().__init__()
        self.name = name
        self.body = body

    def irgen(self):
        # initialize llvm binder
        llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()

        # Declare module
        Node.module = ir.Module()
        # Declare main function
        func_type = ir.FunctionType(ir.VoidType(), [])
        main_func = ir.Function(self.module, func_type, self.name)
        block = main_func.append_basic_block()
        # Declare builder
        Node.builder = ir.IRBuilder(block)

        Node.main_func = main_func

        self.body.irgen()
        Node.builder.ret_void()  # end of main block


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
                if self.exp:  # initialize variable
                    self.exp.irgen()
                    Node.builder.store(self.exp.ir_var, addr)  # store value
                # add to symbol table
                if isinstance(self.vartype, ArrayType):  # array
                    Node.symbol_table.add_symbol(id, self.type, addr, self.vartype.length, self.vartype.low_bound,
                                                 self.vartype.type)
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
                Node.builder.store(self.var.ir_var, addr)  # store value
                Node.symbol_table.add_symbol(id, self.var.type, addr)


class IdExp(Node):
    def __init__(self, id):
        super().__init__()
        self.id = id  # a string

    def irgen(self):
        self.type = Node.symbol_table.get_symbol_type(self.id)
        addr = Node.symbol_table.get_symbol(self.id)['addr']
        self.ir_var = Node.builder.load(addr)


class LiteralVar(Node):
    def __init__(self, var, type):
        super().__init__()
        self.var = var
        self.type = type  # a string in ['int', 'real', 'bool', 'char', 'string']

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

    def irgen(self):
        for id in self.id_list:
            # add to symbol table
            Node.symbol_table.add_symbol(id, 'label', None)


class ConstList(Node):
    def __init__(self, const_list):
        super().__init__()
        self.const_list = const_list

    def irgen(self):
        for const_exp in self.const_list:
            const_exp.irgen()


class LocalHeader(Node):
    def __init__(self, header, body):
        super().__init__()
        self.header = header
        self.body = body

    def irgen(self):
        ''' register function/procedure to symbol table
            open symbol tbale scope
            impelement statements
            close scope
        '''
        header_type = 'procedure' if isinstance(self.header, ProcHeader) else 'function'
        ret_type = None if isinstance(self.header, ProcHeader) else self.header.ret_type
        ret_ir_type = ir.VoidType() if isinstance(self.header, ProcHeader) else Helper.get_ir_type(self.header.ret_type)

        # get type and ir_type of formal parameters
        formal_ir_types, formal_types = self.header.get_formal_type()
        # declare function
        header_ir_type = ir.FunctionType(ret_ir_type, formal_ir_types)
        ir_func = ir.Function(Node.module, header_ir_type, self.header.id)
        # add function to symbol table
        Node.symbol_table.add_symbol(self.header.id, header_type, ir_func, ret_type=ret_type, formal_list=formal_types)

        Node.symbol_table.open_scope()
        # the return value has the same id as the function
        if header_type == 'function':
            ret_formal = Formal([self.header.id], ret_type)
            ret_formal.get_formal_type()
            ret_formal.irgen()
            ret_addr = Node.symbol_table.get_symbol_addr(self.header.id)
        self.header.irgen()  # add formal parameters to symbol table

        # create a new block
        header_block = ir_func.append_basic_block(self.header.id + '_entry')
        # Node.builder = ir.IRBuilder(header_block)
        with Node.builder.goto_block(header_block):
            self.body.irgen()  # implement statements

            if header_type == 'function':
                ret_var = Node.builder.load(ret_addr)
                Node.builder.ret(ret_var)
            else:
                Node.builder.ret_void()

        Node.symbol_table.close_scope()


class ProcHeader(Node):
    def __init__(self, id, formal_list):
        super().__init__()
        self.id = id
        self.formal_list = formal_list

    def get_formal_type(self):
        ''' return formal_ir_type_list
        '''
        formal_ir_type_list = []
        formal_type_list = []
        for formal in self.formal_list:
            formal_ir_type, formal_type = formal.get_formal_type()
            formal_ir_type_list += formal_ir_type
            formal_type_list += formal_type
        return formal_ir_type_list, formal_type_list

    def irgen(self):
        for formal in self.formal_list:
            formal.irgen()


class FuncHeader(Node):
    def __init__(self, id, formal_list, ret_type):
        super().__init__()
        self.id = id
        self.formal_list = formal_list  # a list of formal
        self.ret_type = ret_type

    def get_formal_type(self):
        ''' return formal_ir_type_list and formal_type_list
        '''
        formal_ir_type_list = []
        formal_type_list = []
        for formal in self.formal_list:
            formal_ir_type, formal_type = formal.get_formal_type()
            formal_ir_type_list += formal_ir_type
            formal_type_list += formal_type
        return formal_ir_type_list, formal_type_list

    def irgen(self):
        for formal in self.formal_list:
            formal.irgen()


class Formal(Node):
    def __init__(self, id_list, para_type):
        super().__init__()
        self.id_list = id_list  # a list of strings
        self.vartype = para_type  # type or ArrayType

    def get_formal_type(self):
        ''' return formal_ir_type_list and formal_type_list
        '''
        if isinstance(self.vartype, ArrayType):
            self.ir_type = Helper.get_ir_type(self.vartype.type, length=self.vartype.length)
            self.type = 'array'
        elif self.vartype == 'string':
            self.ir_type = Helper.get_ir_type(self.vartype, str="formal")
            self.type = self.vartype
        else:
            self.ir_type = Helper.get_ir_type(self.vartype)
            self.type = self.vartype

        return [self.ir_type] * len(self.id_list), [self.type] * len(self.id_list)

    def irgen(self):
        ''' add ids to symbol table '''
        with Node.builder.goto_entry_block():
            for id in self.id_list:
                addr = Node.builder.alloca(self.ir_type, name=id)
                if isinstance(self.vartype, ArrayType):  # array
                    Node.symbol_table.add_symbol(id, self.type, addr, self.vartype.length, self.vartype.low_bound,
                                                 self.vartype.type)
                else:
                    Node.symbol_table.add_symbol(id, self.type, addr)


class ArrayType(Node):
    def __init__(self, length, low_bound, type):
        super().__init__()
        self.length = length
        self.low_bound = low_bound
        self.type = type


class Compound(Node):
    def __init__(self, stmt_list):
        super().__init__()
        self.stmt_list = stmt_list

    def irgen(self):
        for stmt in self.stmt_list:
            stmt.irgen()


class LabelStmt(Node):
    def __init__(self, id, non_label_stmt):
        super().__init__()
        self.id = id
        self.non_label_stmt = non_label_stmt

    def irgen(self):
        # declare labeled statement as a basic block
        self.ir_var = Node.builder.append_basic_block(self.id)
        Node.builder.branch(self.ir_var)
        # add label to symbol table
        Node.symbol_table.add_symbol(self.id, 'label', self.ir_var)
        Node.builder.position_at_start(self.ir_var)
        next_block = Node.builder.append_basic_block()

        self.non_label_stmt.irgen()

        # branch to next block
        Node.builder.branch(next_block)
        Node.builder.position_at_start(next_block)


class Assign(Node):
    def __init__(self, lvalue, exp):
        super().__init__()
        self.lvalue = lvalue  # lvalue can be either ID or array
        self.exp = exp  # exp is None if lvalue is ID

    def irgen(self):
        self.lvalue.irgen()
        self.exp.irgen()
        # check type
        if self.lvalue.type != self.exp.type:
            raise Exception("unsupported operand type(s) for :=: '%s' and '%s'." % (self.lvalue.type, self.exp.type))
        with Node.builder.goto_entry_block():
            Node.builder.store(self.exp.ir_var, self.lvalue.addr)  # assign value


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
        if self.exp:  # array
            assert self.type == 'array'
            self.type = symbol_entry['ele_type']
            # add1 = Node.builder.gep(addr, [ir.Constant(ir.IntType(32),0)])
            self.exp.irgen()
            # gep: get element ptr
            self.addr = Node.builder.gep(self.addr, [ir.Constant(ir.IntType(32), 0), self.exp.ir_var])


class Call(Node):
    # include type conversion, e.g., Int(10.1)
    def __init__(self, id, exp_list):
        super().__init__()
        self.id = id
        self.exp_list = exp_list

    def irgen(self):
        ''' set self.type and self.ir_var
            check function
        '''
        for exp in self.exp_list:
            exp.irgen()
        if self.id in Helper.base_type:
            # type conversion
            if self.id == 'int' and self.exp_list[0].type == 'real':
                self.type = 'int'
                self.ir_var = Node.builder.fptosi(self.exp_list[0].ir_var, Helper.base_type['int'])
            elif self.id == 'real' and self.exp_list[0].type == 'int':
                self.type = 'real'
                self.ir_var = Node.builder.sitofp(self.exp_list[0].ir_var, Helper.base_type['real'])
            else:
                raise Exception("unsupported type conversion from %s to %s." % (self.id, self.exp_list[0].type))
        else:
            func = Node.symbol_table.get_symbol(self.id)
            assert func['type'] == 'function'
            formal_list = func['formal_list']
            self.type = func['ret_type']
            # check arguments number
            if len(formal_list) != len(self.exp_list):
                raise Exception("%s() takes %d positional arguments but %d were given." % (self.id, len(formal_list)),
                                len(self.exp_list))
            # check arguments type
            for i in range(len(self.exp_list)):
                if self.exp_list[i].type != formal_list[i]:
                    raise Exception("%s() gets wrong parameter type." % self.type)
            # pass all check points
            self.ir_var = Node.builder.call(func['addr'], [exp.ir_var for exp in self.exp_list])


class For(Node):
    def __init__(self, id, exp1, direct, exp2, stmt):
        super().__init__()
        self.id = id
        self.exp1 = exp1
        self.direct = direct
        self.exp2 = exp2
        self.stmt = stmt


class Case(Node):
    def __init__(self, exp, case_exp_list):
        super().__init__()
        self.exp = exp
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

    def irgen(self):
        tmp_block = Node.builder.append_basic_block()
        Node.builder.branch(tmp_block)
        Node.builder.position_at_start(tmp_block)
        goto_block = Node.symbol_table.get_symbol_addr(self.id)
        Node.builder.branch(goto_block)
        next_block = Node.builder.append_basic_block()
        Node.builder.position_at_start(next_block)


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
            raise Exception(
                "unsupported operand type(s) for %s: '%s' and '%s'." % (self.operator, self.exp1.type, self.exp2.type))
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
            elif self.type == 'real':
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
            assert self.ir_var and self.type  # make sure the assignment is successful
        except:
            raise Exception(
                "unsupported operand type(s) for %s: '%s' and '%s'." % (self.operator, self.exp1.type, self.exp2.type))


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
            self.type = self.exp.type
            if self.type != 'int':
                raise Exception("'not' operator only support int type but %s was given." % self.type)
            self.ir_var = Node.builder.not_(self.exp.ir_var)
        elif self.operator == '+':
            self.type = self.exp.type
            self.ir_var = self.exp.ir_var
        elif self.operator == '-':
            self.type = self.exp.type
            if self.type == 'int':
                self.ir_var = Node.builder.neg(self.exp.ir_var)
            elif self.type == 'real':
                self.ir_var = Node.builder.fsub(ir.Constant(ir.FloatType(), 0), self.exp.ir_var)

        try:
            assert self.ir_var and self.type  # make sure the assignment is successful
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
        addr = Node.builder.gep(self.addr, [ir.Constant(ir.IntType(32), 0), self.exp.ir_var])
        self.ir_var = Node.builder.load(addr)