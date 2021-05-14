program sample;
{ ------------------------------------------------------------ }
const
PI = 3.1415926;
RST = False;
PTR = Nil;	{ pointer }
MSG = 'A simple test.';
type
MONTHS = (JAN, FEB, MAR, APR);	{ Enumerate }
Books = record	{ similar to structure? }
	title: array[1..50] of Char;
	id: Integer;	{ optional semicolon }
end;
Number = Integer;	{ typedef }

var
tcase, a, b: Integer;
num: Number;
c: Char = 'a';
r: Real;
bl: Boolean = True;
e: MONTHS;	{ e := JAN; integer(e)}
s: String = 'Hello';	{ only support single quote }
str: array[-1..1] of char = ('s', 't', 'r');
book: Books;
file_type: file of Real;
{ ------------------------------ }
function gcd(a: Integer; b: Integer): Integer;	{ header }
{ local declaration }
function my_mod(a: Integer; b: Integer): Integer;
begin
	my_mod := a mod b
end;
{ local declaration end }
begin
	if b = 0 then
		gcd := a	{ * no semicolon }
	else
		gcd := gcd(b, my_mod(a, b));	{ gcd can be both return value or function name }
end;
{ ------------------------------------------------------------ }
begin
	book.title := 'BooK';

	a := Integer(c) + Integer(num);	{ + - * / %  }
	if (a <> 0) then	{ = <> > < >= <= }
	begin
		if True and bl then	{ or not }
		begin
			a := 1;
			a := not a;
			WriteLn('hi');
		end	{ no semicolon }
		else if True then
			WriteLn('hi');
	end;

	case a of
		1: WriteLn('1');
		2, 3: WriteLn('2')
	else
		WriteLn('msg0', a);
		WriteLn('msg1', a)
	end;

	a := 0;
	repeat
		a := a + 1	{ optional semi }
	until a >= 5;

	for a := 0 to 3 do
		WriteLn('a = ', a);

	Read(tcase);	{ Readln(...) }
	while tcase > 0 do
	begin
		tcase := tcase - 1;
		Read(a, b);
		Writeln(gcd(a, b));	{ Write(...) }
	end	{ optional semicolon }
end.	{ end with period }