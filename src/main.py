import llvmlite.binding as llvm
from yacc import Parser

if __name__ == '__main__':
    
    parser = Parser()   # syntax analysis

    fin = open("/Users/xy/Compiler/pascal/NestedFunctionTest.pas")
    root = parser.parse(fin.read().lower())
    fin.close()

    root.irgen()    # intermediate representation generation

    print('=== LLVM IR')
    print(root.module)  # print ir

    # Convert textual LLVM IR into in-memory representation.
    llvm_module = llvm.parse_assembly(str(root.module))
    tm = llvm.Target.from_default_triple().create_target_machine()

    # Compile the module to machine code using MCJIT
    with llvm.create_mcjit_compiler(llvm_module, tm) as ee:
        ee.finalize_object()
        print('=== Assembly')
        print(tm.emit_assembly(llvm_module))    # print assembly

        # cfptr = ee.get_function_address("cal")

        # from ctypes import CFUNCTYPE, c_int
        # # To convert an address to an actual callable thing we have to use
        # # CFUNCTYPE, and specify the arguments & return type.
        # cfunc = CFUNCTYPE(c_int, c_int)(cfptr)

        # # Now 'cfunc' is an actual callable we can invoke
        # res = cfunc(15, 5)
        # print('The result is', res)