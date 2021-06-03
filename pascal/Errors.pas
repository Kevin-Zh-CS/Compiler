program Errors;
{ ------------------------------------------------------------ }
var
i, n: int;
c: char;
r: Real;
b: Bool;
s: string = 'a string';
a_i: array[5] of int;
{ ------------------------------------------------------------ }
procedure print_hello(s: String);
begin
  writeln(s)
end;
{ ------------------------------------------------------------ }
BEGIN
{ 这个block里所有语句都是错误语句，不同类型用注释隔开 }
{ incorrect type of parameters}
print_hello(5);
{ incorrect number of parameters}
print_hello();
{ unsupported unsupported type conversion }
b := bool(s);
{ unsupported operand type(s) }
i := b + r;
a_i[0] := 'a';
c := int(r);

n := 5;
for i := 0 to 5 do
    a_i[i] := i
end.