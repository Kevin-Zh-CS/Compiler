program NestedFunctionTest;
{ ------------------------------------------------------------ }
var
a, b: int;
{ ------------------------------ }
function gcd(a: Int; b: Int): Int;
function my_mod(a: Int; b: Int): Int;
begin
	my_mod := a % b
end;
begin
	if b = 0 then
		gcd := a
	else
		gcd := gcd(b, my_mod(a, b))
end;
{ ------------------------------------------------------------ }
begin
	WriteLn('Please enter two integers: ');
	Read(a, b);
	WriteLn('gcd(', a, ',', b, ') = ', gcd(a, b))
end.