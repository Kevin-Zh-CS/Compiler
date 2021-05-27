import llvmlite.ir as ir  

def get_type(self, t):
    if t in ('int', 'integer'):
        return ir.IntType(32)
    elif t in ('real'):
        return ir.DoubleType()
    elif t in ('char'):
        return ir.IntType(8)
    elif t in ('boolean'):
        return ir.IntType(1)
    elif t in ('void'):
        return ir.VoidType()
    else:
        raise Exception('invalid type name')
