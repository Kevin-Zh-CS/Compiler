# Compiler

* pascal

  test code files in Pascal

### Setup

This project has following  requirements:

* python>=3.6

* llvmlite
* Clang compiler
* ply

To ensure your work space correct, we suggest to use virtual enviroment. 

if you don't have a python3 environment:

```
conda create -n pas_compiler python=3.8
conda activate pas_compiler
```

Then install the required packages:

```
pip install -r requirements.txt
```

you also have to install clang. this process will be omittd here.

### Run Pas_compiler

```
python src/main.py <input_file> 
		<-o output_file>    # output_file name, "a.out" as default
  	<-O optim_level>    # optimization_level, 2 as default
  	<-ir ir_file>       # ir file name, program won't output ir file as default
  	<-asm asm_file>     # asm file name, won't output machine code as default
```

to take a quick example, you can use:

```
python src/main.py pascal/NestedFunctionTest.pas
```

### src

main.py : implement lexical analysis, syntax analysis, intermediate representation generation and target code generation

lexer.py : lexical analysis
yacc.py : syntax analysis
ast.py : AST nodes and the corresponding irgen() methods
helper.py : implement symbol table and other helper methods