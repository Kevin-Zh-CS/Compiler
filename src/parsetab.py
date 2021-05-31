
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = "leftORleftANDnonassocEQNEQnonassocLTGTLEQGEQleft+-left*/%rightUMINUSUPLUSNOTnonassocBRACKETSnonassocDANGLINGAND ARRAY ASSIGN BEGIN BOOL BREAK CASE CHAR CONST CONTINUE DO DOWNTO ELSE END EQ EXIT FOR FUNCTION GEQ GOTO GT ID IF INT LABEL LEQ LITERAL_BOOL LITERAL_CHAR LITERAL_INT LITERAL_REAL LITERAL_STRING LT NEQ NOT OF OR PROCEDURE PROGRAM RANGE REAL RECORD REPEAT RETURN STRING THEN TO TYPE UNTIL VAR WHILEprogram : PROGRAM ID ';' body '.'\n        body : local_list compound_stmt\n        local_list : local_list local\n                      | empty\n        local : VAR var_list\n        local : LABEL id_list ';'\n        local : CONST const_exp_list\n        local : header ';' body ';'\n        var_list : var_list var\n                    | var\n        var : id_list ':' vartype ';'\n               | id_list ':' vartype EQ exp ';'\n        const_exp_list : const_exp_list const_exp\n                          | const_exp\n        const_exp : id_list EQ literal ';'\n        id_list : ID comma_id_list\n        comma_id_list : comma_id_list ',' ID\n                         | empty\n        header : PROCEDURE ID '(' formal_list ')'\n                  | PROCEDURE ID '(' ')'\n        header : FUNCTION ID '(' formal_list ')' ':' vartype\n                    | FUNCTION ID '(' ')' ':' vartype\n        formal_list : formal semicolon_formal_list\n        formal : ID ':' vartype\n        semicolon_formal_list : semicolon_formal_list ';' formal\n                                 | empty\n        vartype : INT\n                   | REAL\n                   | BOOL\n                   | CHAR\n                   | STRING\n        vartype : ARRAY '[' LITERAL_INT ']' OF vartype\n                   | ARRAY '[' LITERAL_INT RANGE LITERAL_INT ']' OF vartype\n        semicolon_stmt_list : semicolon_stmt_list ';' stmt\n                               | empty\n        stmt : ID ':' non_label_stmt\n                | non_label_stmt\n        non_label_stmt : assign_stmt\n                          | call_stmt\n                          | for_stmt\n                          | if_stmt\n                          | while_stmt\n                          | repeat_stmt\n                          | case_stmt\n                          | goto_stmt\n                          | compound_stmt\n        assign_stmt : lvalue ASSIGN exp\n        for_stmt : FOR ID ASSIGN exp direction exp DO stmt\n        direction : DOWNTO\n                     | TO\n        while_stmt : WHILE exp DO stmt\n        repeat_stmt : REPEAT stmt semicolon_stmt_list UNTIL exp\n        case_stmt : CASE exp OF case_exp_list END\n        case_exp_list : case_exp_list ';' case_exp\n                         | case_exp\n        case_exp : exp ':' stmt\n        goto_stmt : GOTO ID\n        compound_stmt : BEGIN stmt semicolon_stmt_list END\n        call_stmt : ID '(' exp comma_exp_list ')'\n                     | vartype '(' exp ')'\n                     | ID '(' ')'\n        comma_exp_list : comma_exp_list ',' exp\n                          | empty\n        if_stmt : IF exp THEN stmt else_stmt\n        else_stmt : ELSE stmt \n                     | empty %prec DANGLING\n        lvalue : ID\n                  | ID '[' exp ']' %prec BRACKETS         \n        literal : LITERAL_INT\n                   | LITERAL_REAL\n                   | LITERAL_BOOL\n                   | LITERAL_CHAR\n                   | LITERAL_STRING\n        exp : call_stmt\n        exp : exp '+' exp\n               | exp '-' exp\n               | exp '*' exp\n               | exp '/' exp\n               | exp '%' exp\n               | exp EQ exp\n               | exp NEQ exp\n               | exp LT exp\n               | exp GT exp\n               | exp LEQ exp\n               | exp GEQ exp\n               | exp AND exp\n               | exp OR exp\n        exp : NOT exp\n               | '-' exp %prec UMINUS\n               | '+' exp %prec UPLUS\n        exp : '(' exp ')'\n        exp : ID\n        exp : literal\n        exp : ID '[' exp ']'\n        empty :"
    
_lr_action_items = {'PROGRAM':([0,],[2,]),'$end':([1,8,],[0,-1,]),'ID':([2,11,12,13,14,16,17,32,33,34,35,36,37,44,45,49,50,57,58,59,60,61,65,66,67,68,81,86,89,90,92,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,119,120,122,125,157,163,164,166,174,175,176,177,179,183,185,190,200,203,],[3,19,47,47,47,53,54,62,69,69,19,69,79,47,-10,47,-14,93,69,69,69,69,69,69,69,69,-9,-13,128,128,19,69,19,69,69,69,69,69,69,69,69,69,69,69,69,69,69,19,69,165,69,-11,69,-15,69,69,-49,-50,19,19,69,128,-12,19,]),';':([3,9,15,18,20,21,22,23,24,25,26,27,28,29,38,39,40,41,42,47,48,55,56,64,69,70,71,72,73,74,75,77,79,83,84,88,91,94,96,98,115,116,117,121,124,126,130,131,134,138,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,156,159,160,165,168,169,170,173,178,180,181,182,184,188,189,192,195,196,197,198,201,202,205,206,],[4,-2,52,-95,-37,-38,-39,-40,-41,-42,-43,-44,-45,-46,-27,-28,-29,-30,-31,-95,85,92,-35,-74,-92,-93,-69,-70,-71,-72,-73,-95,-57,-16,-18,127,-58,-36,-61,-47,-90,-89,-88,92,163,166,-20,-95,-34,-60,-95,-75,-76,-77,-78,-79,-80,-81,-82,-83,-84,-85,-86,-87,-91,-51,185,-55,-17,-19,190,-26,-59,-64,-66,-94,-52,-53,200,-24,-22,-65,-56,-54,-32,-25,-21,-48,-33,]),'BEGIN':([4,6,7,10,11,35,44,45,49,50,52,57,81,85,86,92,101,120,127,163,166,179,183,200,203,],[-95,11,-4,-3,11,11,-5,-10,-7,-14,-95,11,-9,-6,-13,11,11,11,-8,-11,-15,11,11,-12,11,]),'VAR':([4,6,7,10,44,45,49,50,52,81,85,86,127,163,166,200,],[-95,12,-4,-3,-5,-10,-7,-14,-95,-9,-6,-13,-8,-11,-15,-12,]),'LABEL':([4,6,7,10,44,45,49,50,52,81,85,86,127,163,166,200,],[-95,13,-4,-3,-5,-10,-7,-14,-95,-9,-6,-13,-8,-11,-15,-12,]),'CONST':([4,6,7,10,44,45,49,50,52,81,85,86,127,163,166,200,],[-95,14,-4,-3,-5,-10,-7,-14,-95,-9,-6,-13,-8,-11,-15,-12,]),'PROCEDURE':([4,6,7,10,44,45,49,50,52,81,85,86,127,163,166,200,],[-95,16,-4,-3,-5,-10,-7,-14,-95,-9,-6,-13,-8,-11,-15,-12,]),'FUNCTION':([4,6,7,10,44,45,49,50,52,81,85,86,127,163,166,200,],[-95,17,-4,-3,-5,-10,-7,-14,-95,-9,-6,-13,-8,-11,-15,-12,]),'.':([5,9,91,],[8,-2,-58,]),'FOR':([11,35,57,92,101,120,179,183,203,],[32,32,32,32,32,32,32,32,32,]),'IF':([11,35,57,92,101,120,179,183,203,],[33,33,33,33,33,33,33,33,33,]),'WHILE':([11,35,57,92,101,120,179,183,203,],[34,34,34,34,34,34,34,34,34,]),'REPEAT':([11,35,57,92,101,120,179,183,203,],[35,35,35,35,35,35,35,35,35,]),'CASE':([11,35,57,92,101,120,179,183,203,],[36,36,36,36,36,36,36,36,36,]),'GOTO':([11,35,57,92,101,120,179,183,203,],[37,37,37,37,37,37,37,37,37,]),'INT':([11,33,34,35,36,57,58,59,60,61,65,66,67,68,82,92,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,119,120,122,157,164,167,172,174,175,176,177,179,183,185,186,191,203,204,],[38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,-49,-50,38,38,38,38,38,38,38,]),'REAL':([11,33,34,35,36,57,58,59,60,61,65,66,67,68,82,92,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,119,120,122,157,164,167,172,174,175,176,177,179,183,185,186,191,203,204,],[39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,-49,-50,39,39,39,39,39,39,39,]),'BOOL':([11,33,34,35,36,57,58,59,60,61,65,66,67,68,82,92,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,119,120,122,157,164,167,172,174,175,176,177,179,183,185,186,191,203,204,],[40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,-49,-50,40,40,40,40,40,40,40,]),'CHAR':([11,33,34,35,36,57,58,59,60,61,65,66,67,68,82,92,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,119,120,122,157,164,167,172,174,175,176,177,179,183,185,186,191,203,204,],[41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,-49,-50,41,41,41,41,41,41,41,]),'STRING':([11,33,34,35,36,57,58,59,60,61,65,66,67,68,82,92,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,119,120,122,157,164,167,172,174,175,176,177,179,183,185,186,191,203,204,],[42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,42,-49,-50,42,42,42,42,42,42,42,]),'ARRAY':([11,33,34,35,36,57,58,59,60,61,65,66,67,68,82,92,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,119,120,122,157,164,167,172,174,175,176,177,179,183,185,186,191,203,204,],[43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,-49,-50,43,43,43,43,43,43,43,]),'END':([18,20,21,22,23,24,25,26,27,28,29,55,56,64,69,70,71,72,73,74,75,79,91,94,96,98,115,116,117,134,138,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,156,159,160,173,178,180,181,182,184,195,196,197,205,],[-95,-37,-38,-39,-40,-41,-42,-43,-44,-45,-46,91,-35,-74,-92,-93,-69,-70,-71,-72,-73,-57,-58,-36,-61,-47,-90,-89,-88,-34,-60,-95,-75,-76,-77,-78,-79,-80,-81,-82,-83,-84,-85,-86,-87,-91,-51,184,-55,-59,-64,-66,-94,-52,-53,-65,-56,-54,-48,]),':':([19,46,47,64,69,70,71,72,73,74,75,83,84,96,115,116,117,128,133,138,141,142,143,144,145,146,147,148,149,150,151,152,153,154,158,165,171,173,181,],[57,82,-95,-74,-92,-93,-69,-70,-71,-72,-73,-16,-18,-61,-90,-89,-88,167,172,-60,-75,-76,-77,-78,-79,-80,-81,-82,-83,-84,-85,-86,-87,-91,183,-17,191,-59,-94,]),'(':([19,31,33,34,36,38,39,40,41,42,53,54,58,59,60,61,65,66,67,68,69,93,100,102,103,104,105,106,107,108,109,110,111,112,113,114,119,122,157,164,174,175,176,177,185,198,206,],[58,61,68,68,68,-27,-28,-29,-30,-31,89,90,68,68,68,68,68,68,68,68,58,58,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,68,-49,-50,68,-32,-33,]),'ASSIGN':([19,30,62,93,137,],[-67,60,100,-67,-68,]),'[':([19,43,69,93,],[59,80,119,59,]),'UNTIL':([20,21,22,23,24,25,26,27,28,29,56,64,69,70,71,72,73,74,75,77,79,91,94,96,98,115,116,117,121,134,138,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,156,173,178,180,181,182,184,195,205,],[-37,-38,-39,-40,-41,-42,-43,-44,-45,-46,-35,-74,-92,-93,-69,-70,-71,-72,-73,-95,-57,-58,-36,-61,-47,-90,-89,-88,157,-34,-60,-95,-75,-76,-77,-78,-79,-80,-81,-82,-83,-84,-85,-86,-87,-91,-51,-59,-64,-66,-94,-52,-53,-65,-48,]),'ELSE':([20,21,22,23,24,25,26,27,28,29,64,69,70,71,72,73,74,75,79,91,94,96,98,115,116,117,138,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,156,173,178,180,181,182,184,195,205,],[-37,-38,-39,-40,-41,-42,-43,-44,-45,-46,-74,-92,-93,-69,-70,-71,-72,-73,-57,-58,-36,-61,-47,-90,-89,-88,-60,179,-75,-76,-77,-78,-79,-80,-81,-82,-83,-84,-85,-86,-87,-91,-51,-59,-64,-66,-94,-52,-53,-65,-48,]),'NOT':([33,34,36,58,59,60,61,65,66,67,68,100,102,103,104,105,106,107,108,109,110,111,112,113,114,119,122,157,164,174,175,176,177,185,],[67,67,67,67,67,67,67,67,67,67,67,67,67,67,67,67,67,67,67,67,67,67,67,67,67,67,67,67,67,67,67,-49,-50,67,]),'-':([33,34,36,58,59,60,61,63,64,65,66,67,68,69,70,71,72,73,74,75,76,78,95,96,97,98,99,100,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,122,138,139,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,157,158,164,173,174,175,176,177,181,182,185,188,193,194,],[66,66,66,66,66,66,66,103,-74,66,66,66,66,-92,-93,-69,-70,-71,-72,-73,103,103,103,-61,103,103,103,66,66,66,66,66,66,66,66,66,66,66,66,66,66,-90,-89,-88,103,66,66,-60,103,-75,-76,-77,-78,-79,103,103,103,103,103,103,103,103,-91,103,66,103,66,-59,66,66,-49,-50,-94,103,66,103,103,103,]),'+':([33,34,36,58,59,60,61,63,64,65,66,67,68,69,70,71,72,73,74,75,76,78,95,96,97,98,99,100,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,122,138,139,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,157,158,164,173,174,175,176,177,181,182,185,188,193,194,],[65,65,65,65,65,65,65,102,-74,65,65,65,65,-92,-93,-69,-70,-71,-72,-73,102,102,102,-61,102,102,102,65,65,65,65,65,65,65,65,65,65,65,65,65,65,-90,-89,-88,102,65,65,-60,102,-75,-76,-77,-78,-79,102,102,102,102,102,102,102,102,-91,102,65,102,65,-59,65,65,-49,-50,-94,102,65,102,102,102,]),'LITERAL_INT':([33,34,36,58,59,60,61,65,66,67,68,80,87,100,102,103,104,105,106,107,108,109,110,111,112,113,114,119,122,157,162,164,174,175,176,177,185,],[71,71,71,71,71,71,71,71,71,71,71,123,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,71,187,71,71,71,-49,-50,71,]),'LITERAL_REAL':([33,34,36,58,59,60,61,65,66,67,68,87,100,102,103,104,105,106,107,108,109,110,111,112,113,114,119,122,157,164,174,175,176,177,185,],[72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,72,-49,-50,72,]),'LITERAL_BOOL':([33,34,36,58,59,60,61,65,66,67,68,87,100,102,103,104,105,106,107,108,109,110,111,112,113,114,119,122,157,164,174,175,176,177,185,],[73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,73,-49,-50,73,]),'LITERAL_CHAR':([33,34,36,58,59,60,61,65,66,67,68,87,100,102,103,104,105,106,107,108,109,110,111,112,113,114,119,122,157,164,174,175,176,177,185,],[74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,74,-49,-50,74,]),'LITERAL_STRING':([33,34,36,58,59,60,61,65,66,67,68,87,100,102,103,104,105,106,107,108,109,110,111,112,113,114,119,122,157,164,174,175,176,177,185,],[75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,-49,-50,75,]),'EQ':([38,39,40,41,42,47,51,63,64,69,70,71,72,73,74,75,76,78,83,84,95,96,97,98,99,115,116,117,118,124,138,139,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,158,165,173,181,182,188,193,194,198,206,],[-27,-28,-29,-30,-31,-95,87,107,-74,-92,-93,-69,-70,-71,-72,-73,107,107,-16,-18,107,-61,107,107,107,-90,-89,-88,107,164,-60,107,-75,-76,-77,-78,-79,None,None,-82,-83,-84,-85,107,107,-91,107,107,-17,-59,-94,107,107,107,107,-32,-33,]),')':([38,39,40,41,42,58,64,69,70,71,72,73,74,75,89,90,95,96,99,115,116,117,118,129,131,132,135,136,138,141,142,143,144,145,146,147,148,149,150,151,152,153,154,169,170,173,181,189,193,198,201,206,],[-27,-28,-29,-30,-31,96,-74,-92,-93,-69,-70,-71,-72,-73,130,133,-95,-61,138,-90,-89,-88,154,168,-95,171,173,-63,-60,-75,-76,-77,-78,-79,-80,-81,-82,-83,-84,-85,-86,-87,-91,-23,-26,-59,-94,-24,-62,-32,-25,-33,]),',':([47,64,69,70,71,72,73,74,75,83,84,95,96,115,116,117,135,136,138,141,142,143,144,145,146,147,148,149,150,151,152,153,154,165,173,181,193,],[-95,-74,-92,-93,-69,-70,-71,-72,-73,125,-18,-95,-61,-90,-89,-88,174,-63,-60,-75,-76,-77,-78,-79,-80,-81,-82,-83,-84,-85,-86,-87,-91,-17,-59,-94,-62,]),'THEN':([63,64,69,70,71,72,73,74,75,96,115,116,117,138,141,142,143,144,145,146,147,148,149,150,151,152,153,154,173,181,],[101,-74,-92,-93,-69,-70,-71,-72,-73,-61,-90,-89,-88,-60,-75,-76,-77,-78,-79,-80,-81,-82,-83,-84,-85,-86,-87,-91,-59,-94,]),'*':([63,64,69,70,71,72,73,74,75,76,78,95,96,97,98,99,115,116,117,118,138,139,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,158,173,181,182,188,193,194,],[104,-74,-92,-93,-69,-70,-71,-72,-73,104,104,104,-61,104,104,104,-90,-89,-88,104,-60,104,104,104,-77,-78,-79,104,104,104,104,104,104,104,104,-91,104,104,-59,-94,104,104,104,104,]),'/':([63,64,69,70,71,72,73,74,75,76,78,95,96,97,98,99,115,116,117,118,138,139,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,158,173,181,182,188,193,194,],[105,-74,-92,-93,-69,-70,-71,-72,-73,105,105,105,-61,105,105,105,-90,-89,-88,105,-60,105,105,105,-77,-78,-79,105,105,105,105,105,105,105,105,-91,105,105,-59,-94,105,105,105,105,]),'%':([63,64,69,70,71,72,73,74,75,76,78,95,96,97,98,99,115,116,117,118,138,139,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,158,173,181,182,188,193,194,],[106,-74,-92,-93,-69,-70,-71,-72,-73,106,106,106,-61,106,106,106,-90,-89,-88,106,-60,106,106,106,-77,-78,-79,106,106,106,106,106,106,106,106,-91,106,106,-59,-94,106,106,106,106,]),'NEQ':([63,64,69,70,71,72,73,74,75,76,78,95,96,97,98,99,115,116,117,118,138,139,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,158,173,181,182,188,193,194,],[108,-74,-92,-93,-69,-70,-71,-72,-73,108,108,108,-61,108,108,108,-90,-89,-88,108,-60,108,-75,-76,-77,-78,-79,None,None,-82,-83,-84,-85,108,108,-91,108,108,-59,-94,108,108,108,108,]),'LT':([63,64,69,70,71,72,73,74,75,76,78,95,96,97,98,99,115,116,117,118,138,139,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,158,173,181,182,188,193,194,],[109,-74,-92,-93,-69,-70,-71,-72,-73,109,109,109,-61,109,109,109,-90,-89,-88,109,-60,109,-75,-76,-77,-78,-79,109,109,None,None,None,None,109,109,-91,109,109,-59,-94,109,109,109,109,]),'GT':([63,64,69,70,71,72,73,74,75,76,78,95,96,97,98,99,115,116,117,118,138,139,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,158,173,181,182,188,193,194,],[110,-74,-92,-93,-69,-70,-71,-72,-73,110,110,110,-61,110,110,110,-90,-89,-88,110,-60,110,-75,-76,-77,-78,-79,110,110,None,None,None,None,110,110,-91,110,110,-59,-94,110,110,110,110,]),'LEQ':([63,64,69,70,71,72,73,74,75,76,78,95,96,97,98,99,115,116,117,118,138,139,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,158,173,181,182,188,193,194,],[111,-74,-92,-93,-69,-70,-71,-72,-73,111,111,111,-61,111,111,111,-90,-89,-88,111,-60,111,-75,-76,-77,-78,-79,111,111,None,None,None,None,111,111,-91,111,111,-59,-94,111,111,111,111,]),'GEQ':([63,64,69,70,71,72,73,74,75,76,78,95,96,97,98,99,115,116,117,118,138,139,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,158,173,181,182,188,193,194,],[112,-74,-92,-93,-69,-70,-71,-72,-73,112,112,112,-61,112,112,112,-90,-89,-88,112,-60,112,-75,-76,-77,-78,-79,112,112,None,None,None,None,112,112,-91,112,112,-59,-94,112,112,112,112,]),'AND':([63,64,69,70,71,72,73,74,75,76,78,95,96,97,98,99,115,116,117,118,138,139,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,158,173,181,182,188,193,194,],[113,-74,-92,-93,-69,-70,-71,-72,-73,113,113,113,-61,113,113,113,-90,-89,-88,113,-60,113,-75,-76,-77,-78,-79,-80,-81,-82,-83,-84,-85,-86,113,-91,113,113,-59,-94,113,113,113,113,]),'OR':([63,64,69,70,71,72,73,74,75,76,78,95,96,97,98,99,115,116,117,118,138,139,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,158,173,181,182,188,193,194,],[114,-74,-92,-93,-69,-70,-71,-72,-73,114,114,114,-61,114,114,114,-90,-89,-88,114,-60,114,-75,-76,-77,-78,-79,-80,-81,-82,-83,-84,-85,-86,-87,-91,114,114,-59,-94,114,114,114,114,]),'DO':([64,69,70,71,72,73,74,75,76,96,115,116,117,138,141,142,143,144,145,146,147,148,149,150,151,152,153,154,173,181,194,],[-74,-92,-93,-69,-70,-71,-72,-73,120,-61,-90,-89,-88,-60,-75,-76,-77,-78,-79,-80,-81,-82,-83,-84,-85,-86,-87,-91,-59,-94,203,]),'OF':([64,69,70,71,72,73,74,75,78,96,115,116,117,138,141,142,143,144,145,146,147,148,149,150,151,152,153,154,161,173,181,199,],[-74,-92,-93,-69,-70,-71,-72,-73,122,-61,-90,-89,-88,-60,-75,-76,-77,-78,-79,-80,-81,-82,-83,-84,-85,-86,-87,-91,186,-59,-94,204,]),']':([64,69,70,71,72,73,74,75,96,97,115,116,117,123,138,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,173,181,187,],[-74,-92,-93,-69,-70,-71,-72,-73,-61,137,-90,-89,-88,161,-60,-75,-76,-77,-78,-79,-80,-81,-82,-83,-84,-85,-86,-87,-91,181,-59,-94,199,]),'DOWNTO':([64,69,70,71,72,73,74,75,96,115,116,117,138,139,141,142,143,144,145,146,147,148,149,150,151,152,153,154,173,181,],[-74,-92,-93,-69,-70,-71,-72,-73,-61,-90,-89,-88,-60,176,-75,-76,-77,-78,-79,-80,-81,-82,-83,-84,-85,-86,-87,-91,-59,-94,]),'TO':([64,69,70,71,72,73,74,75,96,115,116,117,138,139,141,142,143,144,145,146,147,148,149,150,151,152,153,154,173,181,],[-74,-92,-93,-69,-70,-71,-72,-73,-61,-90,-89,-88,-60,177,-75,-76,-77,-78,-79,-80,-81,-82,-83,-84,-85,-86,-87,-91,-59,-94,]),'RANGE':([123,],[162,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'body':([4,52,],[5,88,]),'local_list':([4,52,],[6,6,]),'empty':([4,18,47,52,77,95,131,140,],[7,56,84,7,56,136,170,180,]),'compound_stmt':([6,11,35,57,92,101,120,179,183,203,],[9,29,29,29,29,29,29,29,29,29,]),'local':([6,],[10,]),'header':([6,],[15,]),'stmt':([11,35,92,101,120,179,183,203,],[18,77,134,140,156,195,196,205,]),'non_label_stmt':([11,35,57,92,101,120,179,183,203,],[20,20,94,20,20,20,20,20,20,]),'assign_stmt':([11,35,57,92,101,120,179,183,203,],[21,21,21,21,21,21,21,21,21,]),'call_stmt':([11,33,34,35,36,57,58,59,60,61,65,66,67,68,92,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,119,120,122,157,164,174,175,179,183,185,203,],[22,64,64,22,64,22,64,64,64,64,64,64,64,64,22,64,22,64,64,64,64,64,64,64,64,64,64,64,64,64,64,22,64,64,64,64,64,22,22,64,22,]),'for_stmt':([11,35,57,92,101,120,179,183,203,],[23,23,23,23,23,23,23,23,23,]),'if_stmt':([11,35,57,92,101,120,179,183,203,],[24,24,24,24,24,24,24,24,24,]),'while_stmt':([11,35,57,92,101,120,179,183,203,],[25,25,25,25,25,25,25,25,25,]),'repeat_stmt':([11,35,57,92,101,120,179,183,203,],[26,26,26,26,26,26,26,26,26,]),'case_stmt':([11,35,57,92,101,120,179,183,203,],[27,27,27,27,27,27,27,27,27,]),'goto_stmt':([11,35,57,92,101,120,179,183,203,],[28,28,28,28,28,28,28,28,28,]),'lvalue':([11,35,57,92,101,120,179,183,203,],[30,30,30,30,30,30,30,30,30,]),'vartype':([11,33,34,35,36,57,58,59,60,61,65,66,67,68,82,92,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,119,120,122,157,164,167,172,174,175,179,183,185,186,191,203,204,],[31,31,31,31,31,31,31,31,31,31,31,31,31,31,124,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,31,189,192,31,31,31,31,31,198,202,31,206,]),'var_list':([12,],[44,]),'var':([12,44,],[45,81,]),'id_list':([12,13,14,44,49,],[46,48,51,46,51,]),'const_exp_list':([14,],[49,]),'const_exp':([14,49,],[50,86,]),'semicolon_stmt_list':([18,77,],[55,121,]),'exp':([33,34,36,58,59,60,61,65,66,67,68,100,102,103,104,105,106,107,108,109,110,111,112,113,114,119,122,157,164,174,175,185,],[63,76,78,95,97,98,99,115,116,117,118,139,141,142,143,144,145,146,147,148,149,150,151,152,153,155,158,182,188,193,194,158,]),'literal':([33,34,36,58,59,60,61,65,66,67,68,87,100,102,103,104,105,106,107,108,109,110,111,112,113,114,119,122,157,164,174,175,185,],[70,70,70,70,70,70,70,70,70,70,70,126,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,70,]),'comma_id_list':([47,],[83,]),'formal_list':([89,90,],[129,132,]),'formal':([89,90,190,],[131,131,201,]),'comma_exp_list':([95,],[135,]),'case_exp_list':([122,],[159,]),'case_exp':([122,185,],[160,197,]),'semicolon_formal_list':([131,],[169,]),'direction':([139,],[175,]),'else_stmt':([140,],[178,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> PROGRAM ID ; body .','program',5,'p_program','yacc.py',30),
  ('body -> local_list compound_stmt','body',2,'p_body','yacc.py',35),
  ('local_list -> local_list local','local_list',2,'p_local_list','yacc.py',40),
  ('local_list -> empty','local_list',1,'p_local_list','yacc.py',41),
  ('local -> VAR var_list','local',2,'p_local1','yacc.py',50),
  ('local -> LABEL id_list ;','local',3,'p_local2','yacc.py',55),
  ('local -> CONST const_exp_list','local',2,'p_local3','yacc.py',60),
  ('local -> header ; body ;','local',4,'p_local4','yacc.py',65),
  ('var_list -> var_list var','var_list',2,'p_var_list','yacc.py',70),
  ('var_list -> var','var_list',1,'p_var_list','yacc.py',71),
  ('var -> id_list : vartype ;','var',4,'p_var','yacc.py',80),
  ('var -> id_list : vartype EQ exp ;','var',6,'p_var','yacc.py',81),
  ('const_exp_list -> const_exp_list const_exp','const_exp_list',2,'p_const_exp_list','yacc.py',90),
  ('const_exp_list -> const_exp','const_exp_list',1,'p_const_exp_list','yacc.py',91),
  ('const_exp -> id_list EQ literal ;','const_exp',4,'p_const_exp','yacc.py',100),
  ('id_list -> ID comma_id_list','id_list',2,'p_id_list','yacc.py',105),
  ('comma_id_list -> comma_id_list , ID','comma_id_list',3,'p_comma_id_list','yacc.py',111),
  ('comma_id_list -> empty','comma_id_list',1,'p_comma_id_list','yacc.py',112),
  ('header -> PROCEDURE ID ( formal_list )','header',5,'p_header1','yacc.py',121),
  ('header -> PROCEDURE ID ( )','header',4,'p_header1','yacc.py',122),
  ('header -> FUNCTION ID ( formal_list ) : vartype','header',7,'p_header2','yacc.py',130),
  ('header -> FUNCTION ID ( ) : vartype','header',6,'p_header2','yacc.py',131),
  ('formal_list -> formal semicolon_formal_list','formal_list',2,'p_formal_list','yacc.py',139),
  ('formal -> ID : vartype','formal',3,'p_formal','yacc.py',145),
  ('semicolon_formal_list -> semicolon_formal_list ; formal','semicolon_formal_list',3,'p_semicolon_formal_list','yacc.py',150),
  ('semicolon_formal_list -> empty','semicolon_formal_list',1,'p_semicolon_formal_list','yacc.py',151),
  ('vartype -> INT','vartype',1,'p_vartype1','yacc.py',161),
  ('vartype -> REAL','vartype',1,'p_vartype1','yacc.py',162),
  ('vartype -> BOOL','vartype',1,'p_vartype1','yacc.py',163),
  ('vartype -> CHAR','vartype',1,'p_vartype1','yacc.py',164),
  ('vartype -> STRING','vartype',1,'p_vartype1','yacc.py',165),
  ('vartype -> ARRAY [ LITERAL_INT ] OF vartype','vartype',6,'p_vartype2','yacc.py',170),
  ('vartype -> ARRAY [ LITERAL_INT RANGE LITERAL_INT ] OF vartype','vartype',8,'p_vartype2','yacc.py',171),
  ('semicolon_stmt_list -> semicolon_stmt_list ; stmt','semicolon_stmt_list',3,'p_semicolon_stmt_list','yacc.py',179),
  ('semicolon_stmt_list -> empty','semicolon_stmt_list',1,'p_semicolon_stmt_list','yacc.py',180),
  ('stmt -> ID : non_label_stmt','stmt',3,'p_stmt','yacc.py',189),
  ('stmt -> non_label_stmt','stmt',1,'p_stmt','yacc.py',190),
  ('non_label_stmt -> assign_stmt','non_label_stmt',1,'p_non_label_stmt','yacc.py',198),
  ('non_label_stmt -> call_stmt','non_label_stmt',1,'p_non_label_stmt','yacc.py',199),
  ('non_label_stmt -> for_stmt','non_label_stmt',1,'p_non_label_stmt','yacc.py',200),
  ('non_label_stmt -> if_stmt','non_label_stmt',1,'p_non_label_stmt','yacc.py',201),
  ('non_label_stmt -> while_stmt','non_label_stmt',1,'p_non_label_stmt','yacc.py',202),
  ('non_label_stmt -> repeat_stmt','non_label_stmt',1,'p_non_label_stmt','yacc.py',203),
  ('non_label_stmt -> case_stmt','non_label_stmt',1,'p_non_label_stmt','yacc.py',204),
  ('non_label_stmt -> goto_stmt','non_label_stmt',1,'p_non_label_stmt','yacc.py',205),
  ('non_label_stmt -> compound_stmt','non_label_stmt',1,'p_non_label_stmt','yacc.py',206),
  ('assign_stmt -> lvalue ASSIGN exp','assign_stmt',3,'p_assign_stmt','yacc.py',211),
  ('for_stmt -> FOR ID ASSIGN exp direction exp DO stmt','for_stmt',8,'p_for_stmt','yacc.py',216),
  ('direction -> DOWNTO','direction',1,'p_direction','yacc.py',222),
  ('direction -> TO','direction',1,'p_direction','yacc.py',223),
  ('while_stmt -> WHILE exp DO stmt','while_stmt',4,'p_while_stmt','yacc.py',228),
  ('repeat_stmt -> REPEAT stmt semicolon_stmt_list UNTIL exp','repeat_stmt',5,'p_repeat_stmt','yacc.py',233),
  ('case_stmt -> CASE exp OF case_exp_list END','case_stmt',5,'p_case_stmt','yacc.py',239),
  ('case_exp_list -> case_exp_list ; case_exp','case_exp_list',3,'p_case_exp_list','yacc.py',244),
  ('case_exp_list -> case_exp','case_exp_list',1,'p_case_exp_list','yacc.py',245),
  ('case_exp -> exp : stmt','case_exp',3,'p_case_exp','yacc.py',256),
  ('goto_stmt -> GOTO ID','goto_stmt',2,'p_goto_stmt','yacc.py',262),
  ('compound_stmt -> BEGIN stmt semicolon_stmt_list END','compound_stmt',4,'p_compound_stmt','yacc.py',267),
  ('call_stmt -> ID ( exp comma_exp_list )','call_stmt',5,'p_call_stmt','yacc.py',273),
  ('call_stmt -> vartype ( exp )','call_stmt',4,'p_call_stmt','yacc.py',274),
  ('call_stmt -> ID ( )','call_stmt',3,'p_call_stmt','yacc.py',275),
  ('comma_exp_list -> comma_exp_list , exp','comma_exp_list',3,'p_comma_exp_list','yacc.py',286),
  ('comma_exp_list -> empty','comma_exp_list',1,'p_comma_exp_list','yacc.py',287),
  ('if_stmt -> IF exp THEN stmt else_stmt','if_stmt',5,'p_if_stmt','yacc.py',296),
  ('else_stmt -> ELSE stmt','else_stmt',2,'p_else_stmt','yacc.py',301),
  ('else_stmt -> empty','else_stmt',1,'p_else_stmt','yacc.py',302),
  ('lvalue -> ID','lvalue',1,'p_lvalue','yacc.py',311),
  ('lvalue -> ID [ exp ]','lvalue',4,'p_lvalue','yacc.py',312),
  ('literal -> LITERAL_INT','literal',1,'p_literal','yacc.py',320),
  ('literal -> LITERAL_REAL','literal',1,'p_literal','yacc.py',321),
  ('literal -> LITERAL_BOOL','literal',1,'p_literal','yacc.py',322),
  ('literal -> LITERAL_CHAR','literal',1,'p_literal','yacc.py',323),
  ('literal -> LITERAL_STRING','literal',1,'p_literal','yacc.py',324),
  ('exp -> call_stmt','exp',1,'p_exp1','yacc.py',329),
  ('exp -> exp + exp','exp',3,'p_exp2','yacc.py',334),
  ('exp -> exp - exp','exp',3,'p_exp2','yacc.py',335),
  ('exp -> exp * exp','exp',3,'p_exp2','yacc.py',336),
  ('exp -> exp / exp','exp',3,'p_exp2','yacc.py',337),
  ('exp -> exp % exp','exp',3,'p_exp2','yacc.py',338),
  ('exp -> exp EQ exp','exp',3,'p_exp2','yacc.py',339),
  ('exp -> exp NEQ exp','exp',3,'p_exp2','yacc.py',340),
  ('exp -> exp LT exp','exp',3,'p_exp2','yacc.py',341),
  ('exp -> exp GT exp','exp',3,'p_exp2','yacc.py',342),
  ('exp -> exp LEQ exp','exp',3,'p_exp2','yacc.py',343),
  ('exp -> exp GEQ exp','exp',3,'p_exp2','yacc.py',344),
  ('exp -> exp AND exp','exp',3,'p_exp2','yacc.py',345),
  ('exp -> exp OR exp','exp',3,'p_exp2','yacc.py',346),
  ('exp -> NOT exp','exp',2,'p_exp3','yacc.py',351),
  ('exp -> - exp','exp',2,'p_exp3','yacc.py',352),
  ('exp -> + exp','exp',2,'p_exp3','yacc.py',353),
  ('exp -> ( exp )','exp',3,'p_exp4','yacc.py',358),
  ('exp -> ID','exp',1,'p_exp5','yacc.py',363),
  ('exp -> literal','exp',1,'p_exp6','yacc.py',368),
  ('exp -> ID [ exp ]','exp',4,'p_exp7','yacc.py',373),
  ('empty -> <empty>','empty',0,'p_empty','yacc.py',380),
]
