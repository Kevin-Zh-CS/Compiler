import llvmlite.ir as ir

class SymbolTable():

    def __init__(self):
        self.global_table = {}
        self.scope_table = []   # each item stores symbols' id for a single scope
        self.level_table = {}
    
    def open_scope(self):
        self.scope_table.append([])
    
    def close_scope(self):
        for id in self.scope_table[-1]:
            self.global_table[id].pop() # delete from global table
            if self.global_table[id] == []:
                self.global_table.pop(id)
        self.scope_table.pop()  # delete this scope
    
    def add_symbol(self, id, type, addr, length=0, low_bound=0, ele_type=None, ret_type=None, formal_list=[]):
        if type == 'label' and addr:    # use label to mark a position
            if self.global_table.get(id, None) == None:
                raise Exception("label '%s' not defined." % id)
            if not self.global_table[id][-1]['addr']:
                self.global_table[id][-1]['addr'] = addr
                return
            else:
                raise Exception("label %s reappeared." % id)
        if id in self.scope_table[-1]:
            raise Exception("redefine symbol %s." % id)

        self.scope_table[-1].append(id)
        self.global_table.setdefault(id, [])    # add an empty list if the symbol is not in the table

        entry = {}
        entry['type'] = type
        entry['addr'] = addr
        if type not in Helper.base_type and type != 'string' and type != 'label':
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
                raise Exception("invalid symbol type")

        self.global_table[id].append(entry)
    
    def get_symbol(self, id, is_func=0):
        id_list = self.global_table.get(id, None)
        if id_list:
            if is_func ==0:
                return id_list[-1]
            else:
                if id_list[-1]['type'] == 'function' or id_list[-1]['type'] == 'procedure':
                    return id_list[-1]
                elif id_list[-2]['type'] == 'function' or id_list[-2]['type'] == 'procedure':
                    return id_list[-2]
                else:
                    raise Exception("%s is not callable!" % id)
        else:
            raise Exception("no symbol named \'%s\'!" % id)
    
    def get_symbol_type(self, id):
        return self.get_symbol(id)['type']
    
    def get_symbol_addr(self, id):
        return self.get_symbol(id)['addr']
    
    def get_symbol_level(self, id):
        self.level_table.setdefault(id, -1)
        self.level_table[id] += 1
        return '_'+str(self.level_table[id])

class Helper():
    base_type = {'int': ir.IntType(32),
                 'real': ir.DoubleType(),
                 'char': ir.IntType(8),
                 'bool': ir.IntType(1)
                }

    IO_type = ['writeln', 'readln', 'write', 'read']

    write_op = {'int': "%i",
                'real': "%lf",
                'char': "%c",
                'bool': "%i",
                'string': "%s"
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
                
        raise Exception("invalid data type.")
    
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
        elif ir_type == ir.IntType(8) and isinstance(var, str):
            # convert char to int
            value = ord(var)
        else:
            value = var
        ir_var = ir.Constant(ir_type, value)
        return ir_var
