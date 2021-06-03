program ArrayTest;
const
	l = 1;
	r = 6;
var
	iv : int;
	a : array[1..6] of int;

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
