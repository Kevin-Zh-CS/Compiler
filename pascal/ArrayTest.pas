program ArrayTest;
const
	l = 2;
	r = 8;
var
	iv : int;
	a : array[2..8] of int;

begin
	iv := 0;  
	for iv := l to r do
	begin
		a[iv] := iv
	end;
	for iv := l to r do
	begin
		writeln(a[iv])
	end
end
.
