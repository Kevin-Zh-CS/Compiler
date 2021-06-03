from abc import ABC

import llvmlite.ir as ir
import llvmlite.binding as llvm

from lexer import Lexer
from helper import Helper, SymbolTable

tokens = Lexer.tokens

def get_format(Node):
    if hasattr(Node,"addr"):
        return Node.addr
    if hasattr(Node,"type") and Node.type == "string":
        return Node.symbol_table.get_symbol_addr(Node.id)
    return Node.ir_var

def IO_func(funcname, args):
    voidptr_ty = ir.IntType(8).as_pointer()
    io_funcname = "scanf" if funcname[:4] == "read" else "printf"
    io_function = Node.symbol_table.get_symbol(io_funcname)['addr']

    left_str = "".join([Helper.write_op[arg.type] for arg in args])
    if funcname[-2:] == "ln":
        left_str += "\n"
    left_str += "\0"
    c_fmt = ir.Constant(ir.ArrayType(ir.IntType(8), len(left_str)),
                        bytearray(left_str.encode("utf8")))
    c_str = Node.builder.alloca(c_fmt.type)
    Node.builder.store(c_fmt, c_str)
    fmt_arg = Node.builder.bitcast(c_str, voidptr_ty)
    for arg in args:
        print(arg.ir_var)
    if io_funcname=="scanf":
        args = [fmt_arg, *[Node.symbol_table.get_symbol_addr(arg.id) for arg in args]]
    else:
        args = [fmt_arg, *[get_format(arg) for arg in args]]
    Node.builder.call(io_function,args)

def register_IO():
    voidptr_ty = ir.IntType(8).as_pointer()
    printf_ty = ir.FunctionType(ir.IntType(32), [voidptr_ty], var_arg=True)
    scanf_ty = ir.FunctionType(ir.IntType(32), [voidptr_ty], var_arg=True)
    printf_function = ir.Function(Node.module, printf_ty, name="printf")
    scanf_function = ir.Function(Node.module, scanf_ty, name="scanf")
    Node.symbol_table.add_symbol("printf", "function", printf_function, ret_type=ir.IntType(32), formal_list=[voidptr_ty])
    Node.symbol_table.add_symbol("scanf", "function", scanf_function, ret_type=ir.IntType(32), formal_list=[voidptr_ty])

class Node(ABC):
    builder = None
    module = None
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

        # declare module
        Node.module = ir.Module(__file__)
        # declare main function
        func_type = ir.FunctionType(ir.VoidType(), [])
        main_func = ir.Function(self.module, func_type, self.name)
        block = main_func.append_basic_block()
        # declare builder
        Node.builder = ir.IRBuilder(block)
        # open scope for the whole program
        Node.symbol_table.open_scope()

        register_IO()

        self.body.irgen()
        Node.builder.ret_void()  # end of main block
        Node.symbol_table.close_scope()

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

        for id in self.id_list:
            addr = ir.GlobalVariable(Node.module, ir_type, name=id + Node.symbol_table.get_symbol_level(id))
            addr.linkage = 'internal'
            if self.exp:  # initialize variable
                self.exp.irgen()
                addr.initializer = self.exp.ir_var

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
        for id in self.id_list:
            if self.var.type !="string":
                addr = ir.GlobalVariable(Node.module, self.var.ir_type, name=id+Node.symbol_table.get_symbol_level(id))
                addr.linkage = 'internal'
                Node.builder.store(self.var.ir_var, addr)  # initialize value
                addr.global_constant = True # declare as a constant
                Node.symbol_table.add_symbol(id, self.var.type, addr)
            else:
                Node.symbol_table.add_symbol(id, self.var.type, self.var.addr)

class IdExp(Node):
    def __init__(self, id):
        super().__init__()
        self.id = id  # a string

    def irgen(self):
        self.type = Node.symbol_table.get_symbol_type(self.id)
        addr = Node.symbol_table.get_symbol(self.id)['addr']
        if isinstance(addr, ir.Argument):   # function argument
            self.ir_var = addr
        else:
            self.ir_var = Node.builder.load(addr)

class LiteralVar(Node):
    def __init__(self, var, type):
        super().__init__()
        self.var = var
        if type == "string":
            self.var+='\0'
        self.type = type  # a string in ['int', 'real', 'bool', 'char', 'string']

    def irgen(self):
        ''' set self.ir_var '''
        if self.type == 'string':
            self.ir_type = Helper.get_ir_type(self.type, str=self.var)
            self.ir_var = Helper.get_ir_var(self.ir_type, self.var, is_str=1)
            self.addr = Node.builder.alloca(self.ir_type)
            Node.builder.store(self.ir_var, self.addr)
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

        # create a new block
        header_block = ir_func.append_basic_block(self.header.id + '_entry')
        # Node.builder = ir.IRBuilder(header_block)
        with Node.builder.goto_block(header_block):
            # the return value has the same id as the function
            if header_type == 'function':
                ret_formal = Formal([self.header.id], ret_type)
                ret_formal.get_formal_type()
                with Node.builder.goto_entry_block():
                    addr = ir.GlobalVariable(Node.module, ret_formal.ir_type, name=self.header.id+Node.symbol_table.get_symbol_level(self.header.id))
                    addr.linkage = 'internal'
                    if isinstance(ret_formal.ir_type, ArrayType): # array
                        Node.symbol_table.add_symbol(self.header.id, ret_formal.type, addr, ret_formal.vartype.length, ret_formal.vartype.low_bound, ret_formal.vartype.type)
                    else:
                        Node.symbol_table.add_symbol(self.header.id, ret_formal.type, addr)
                ret_addr = Node.symbol_table.get_symbol_addr(self.header.id)
            self.header.irgen(ir_func) # add formal parameters to symbol table
            
            self.body.irgen()   # implement statements

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
    
    def irgen(self, func):
        for i, formal in enumerate(self.formal_list):
            formal.irgen(func.args[i])
   
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
    
    def irgen(self, func):
        for i, formal in enumerate(self.formal_list):
            formal.irgen(func.args[i])

class Formal(Node):
    def __init__(self, id, para_type):
        super().__init__()
        self.id = id
        self.vartype = para_type   # type or ArrayType
    
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

        return [self.ir_type], [self.type]
    
    def irgen(self, ir_var):
        ''' add ids to symbol table '''
        with Node.builder.goto_entry_block():
            addr = ir.GlobalVariable(Node.module, self.ir_type, name=self.id+Node.symbol_table.get_symbol_level(self.id))
            addr.linkage = 'internal'
            Node.builder.store(ir_var, addr)    # store input parameter to local variable
            if isinstance(self.vartype, ArrayType): # array
                Node.symbol_table.add_symbol(self.id, self.type, addr, self.vartype.length, self.vartype.low_bound, self.vartype.type)
            else:
                Node.symbol_table.add_symbol(self.id, self.type, addr)

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
        if isinstance(self.lvalue.addr, ir.Argument):   # it's a value instead of ptr
            self.lvalue.addr = self.exp.ir_var
        else:
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
        if self.exp:  # array
            assert self.type == 'array'
            self.type = symbol_entry['ele_type']
            low_bound = symbol_entry['low_bound']
            exp_ind = BinExp('-', self.exp, LiteralVar(low_bound, 'int'))
            exp_ind.irgen()
            # gep: get element ptr
            self.addr = Node.builder.gep(self.addr, [ir.Constant(ir.IntType(32),0), exp_ind.ir_var])

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
            if len(self.exp_list) != 1:
                raise Exception("the type conversion function only supports a single parameter.")
            if self.id == 'int' and self.exp_list[0].type == 'real':    # real -> int
                self.type = 'int'
                self.ir_var = Node.builder.fptosi(self.exp_list[0].ir_var, Helper.base_type['int'])
            elif self.id == 'real' and self.exp_list[0].type == 'int':  # int -> real
                self.type = 'real'
                self.ir_var = Node.builder.sitofp(self.exp_list[0].ir_var, Helper.base_type['real'])
            elif self.id == 'int' and self.exp_list[0].type == 'char':  # char -> int
                self.type = 'int'
                self.ir_var = Node.builder.sext(self.exp_list[0].ir_var, Helper.base_type['int'])
            elif self.id == 'char' and self.exp_list[0].type == 'int':  # int -> char
                self.type = 'char'
                self.ir_var = Node.builder.trunc(self.exp_list[0].ir_var, Helper.base_type['char'])
            else:
                raise Exception("unsupported type conversion from %s to %s." % (self.exp_list[0].type, self.id))
        elif self.id in Helper.IO_type:
            IO_func(self.id,self.exp_list)
        else:
            func = Node.symbol_table.get_symbol(self.id, is_func=1)
            assert func['type'] == 'function' or func['type'] == 'procedure'
            formal_list = func['formal_list']
            if func['type'] == 'function':
                self.type = func['ret_type']
            # check arguments number
            if len(formal_list) != len(self.exp_list):
                raise Exception("%s() takes %d positional arguments but %d were given." % (self.id, len(formal_list),
                                len(self.exp_list)))
            # check arguments type
            for i in range(len(self.exp_list)):
                if self.exp_list[i].type != formal_list[i]:
                    raise Exception("%s() gets wrong parameter type." % self.id)
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
    
    def irgen(self):
        for_block = Node.builder.append_basic_block()
        buff_block = Node.builder.append_basic_block()  # eliminate excess increment/decrement
        next_block = Node.builder.append_basic_block()

        assign_stmt = Assign(lvalue=LValue(self.id, None), exp=self.exp1)
        assign_stmt.irgen()
        self.exp2.irgen()
        right_ir_var = self.exp2.ir_var

        if self.direct == 0:    # increase
            relat_op = '<='
            inc_dec_var = ir.Constant(ir.IntType(32), 1)
        else:   # decrease
            relat_op = '>='
            inc_dec_var = ir.Constant(ir.IntType(32), -1)

        left_ir_var = self.exp1.ir_var
        cond = Node.builder.icmp_signed(relat_op, left_ir_var, right_ir_var)
        Node.builder.cbranch(cond, for_block, next_block)
        Node.builder.position_at_start(for_block)
        self.stmt.irgen()
        # increase or decrease iteration variable
        left_ir_var = Node.builder.load(Node.symbol_table.get_symbol_addr(self.id)) # current value of iteration variable
        Node.builder.store(Node.builder.add(left_ir_var, inc_dec_var), Node.symbol_table.get_symbol_addr(self.id))  # inc of dec
        left_ir_var = Node.builder.load(Node.symbol_table.get_symbol_addr(self.id)) # value after inc/dec
        cond = Node.builder.icmp_signed(relat_op, left_ir_var, right_ir_var)
        Node.builder.cbranch(cond, for_block, buff_block)
        # buff block is used to eliminate excess inc/dec
        # e.g., for a:= 0 to 5 do... after loops, the value of a should be 5 instead of 6
        Node.builder.position_at_start(buff_block)
        Node.builder.store(Node.builder.sub(left_ir_var, inc_dec_var), Node.symbol_table.get_symbol_addr(self.id))  # inc of dec
        Node.builder.branch(next_block)
        Node.builder.position_at_start(next_block)

class While(Node):
    def __init__(self, exp, stmt):
        super().__init__()
        self.exp = exp
        self.stmt = stmt
    
    def irgen(self):
        while_block = Node.builder.append_basic_block()
        next_block = Node.builder.append_basic_block()
        self.exp.irgen()
        # jump to either part depending on the exp value
        Node.builder.cbranch(self.exp.ir_var, while_block, next_block)
        Node.builder.position_at_start(while_block)
        self.stmt.irgen()   # generate statements in while body
        self.exp.irgen()
        # jump back to while body if the condition is satisfied
        Node.builder.cbranch(self.exp.ir_var, while_block, next_block)
        Node.builder.position_at_start(next_block)

class Repeat(Node):
    def __init__(self, stmt, exp):
        super().__init__()
        self.stmt = stmt
        self.exp = exp
    
    def irgen(self):
        repeat_block = Node.builder.append_basic_block()
        next_block = Node.builder.append_basic_block()

        Node.builder.branch(repeat_block)
        Node.builder.position_at_start(repeat_block)
        self.stmt.irgen()   # generate statements in repeat body
        self.exp.irgen()
        # jump to either part depending on the exp value
        Node.builder.cbranch(self.exp.ir_var, next_block, repeat_block)

        Node.builder.position_at_start(next_block)

class If(Node):
    def __init__(self, exp, stmt, else_stmt):
        super().__init__()
        self.exp = exp
        self.stmt = stmt
        self.else_stmt = else_stmt
    
    def irgen(self):
        self.exp.irgen()

        if self.else_stmt:
            with Node.builder.if_else(self.exp.ir_var) as (then, otherwise):
                with then:
                    self.stmt.irgen()
                with otherwise:
                    self.else_stmt.irgen()
        else:
            with Node.builder.if_then(self.exp.ir_var):
                self.stmt.irgen()

class Case(Node):
    def __init__(self, exp, case_exp_list):
        super().__init__()
        self.exp  = exp
        self.case_exp_list = case_exp_list

    def irgen(self):
        self.exp.irgen()
        next_block = Node.builder.append_basic_block("endcase")
        switch_stmt = Node.builder.switch(self.exp.ir_var, next_block)

        case_var_list = []
        case_block_list = []
        for case_exp in self.case_exp_list:
            case_exp.exp.irgen()    # get the value of literal or id
            case_var_list.append(case_exp.exp.ir_var)
            block = Node.builder.append_basic_block("case")
            case_block_list.append(block)
            Node.builder.position_at_start(block)
            case_exp.irgen()    # generate statements for this case
            Node.builder.branch(next_block)
        
        for i in range(len(case_block_list)):
            switch_stmt.add_case(case_var_list[i], case_block_list[i])
        
        Node.builder.position_at_start(next_block)

class CaseExp(Node):
    def __init__(self, exp, stmt):
        super().__init__()
        self.exp = exp  # literal or id
        self.stmt = stmt
    
    def irgen(self):
        self.stmt.irgen() 

class Goto(Node):
    def __init__(self, id):
        super().__init__()
        self.id = id

    def irgen(self):
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

        # calculate the absolute subindex
        low_bound = symbol_entry['low_bound']
        exp_ind = BinExp('-', self.exp, LiteralVar(low_bound, 'int'))
        exp_ind.irgen()
        # gep: get element ptr
        addr = Node.builder.gep(self.addr, [ir.Constant(ir.IntType(32),0), exp_ind.ir_var])
        self.ir_var = Node.builder.load(addr)
