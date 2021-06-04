import llvmlite.binding as llvm
from yacc import Parser
import tempfile
import subprocess
import os
import argparse

_rtlib = os.path.join(os.path.dirname(__file__), 'lib.c')


def optimize(ir, args):
    llvm_module = llvm.parse_assembly(ir)
    pmb = llvm.create_pass_manager_builder()
    pmb.opt_level = args.optimization_level
    pm = llvm.create_module_pass_manager()
    pmb.populate(pm)
    pm.run(llvm_module)
    return llvm_module


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("input_file", help='specify the input file')
    args.add_argument("-O", "--optimization_level", type=int, help="specify the optimization level", default=2)
    args.add_argument("-ir", "--ir_file", help="generate ir code")
    args.add_argument("-asm", "--asm_file", help="generate machine code")
    args.add_argument("-o", "--output_file", help="output file name", default="a.out")
    args = args.parse_args()

    parser = Parser()  # syntax analysis

    with open(args.input_file) as fin:
        root = parser.parse(fin.read().lower())
    root.irgen()  # intermediate representation generation

    if args.ir_file:
        with open(args.ir_file,"w")as ir:
            ir.write(str(root.module))
    # Convert textual LLVM IR into in-memory representation.

    llvm_module = optimize(str(root.module), args)
    # Compile the module to machine code using MCJIT
    output_file = "-o " + args.output_file.strip()
    with tempfile.NamedTemporaryFile(suffix='.ll') as f:
        f.write(str(llvm_module).encode('utf-8'))
        f.flush()
        subprocess.check_output(["clang", output_file,'-DNEED_MAIN', f.name, _rtlib])

    tm = llvm.Target.from_default_triple().create_target_machine()
    # Compile the module to machine code using MCJIT
    with llvm.create_mcjit_compiler(llvm_module, tm) as ee:
        ee.finalize_object()
        if args.asm_file:
            with open(args.asm_file, 'w') as f:
                f.write(tm.emit_assembly(llvm_module))