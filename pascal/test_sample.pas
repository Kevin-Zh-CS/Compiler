program test_sample;
{ ------------------------------------------------------------ }
const
pi = 3.14159;
var
a : int;
r : real;
c : char = 'a';
label
lb;

{ ------------------------------ }
procedure print_end();
begin
    writeln('function ends.')
end;

function gcd(a: Int; b: Int): Int;	{ header }
{ local declaration }
const
e = 2.718;
var
array1: array[1..3] of int;
str : string = 'e =';
function sum(a: Int; b: Int; c: array[2] of int): Int;
begin
	sum := a + b
end;
{ local declaration end }
begin
    array1[0] := 2;
    if array1[0] = 2 then
    begin
        if 3 <= 2 then
            gcd := -3
        else begin
            array1[1] := 3;
            gcd := sum(a, b, array1)*array1[1];
            writeln('test rst : ', gcd)
        end
    end
    else gcd := int(5.0);

    gcd := 0;
    while gcd <= 6 do 
    begin
        gcd := gcd + 1
    end;

lb:    if gcd < 20 then
    begin
        gcd := gcd + 1;
        goto lb
    end;

    gcd := 1;
    case gcd of
    1 : gcd := 10086;
    2 : gcd := 210;
    3 : gcd := 345
    end;
    
    c := 'a';

    writeln(int(c));

    repeat
        gcd := gcd + 1
    until gcd % 2 = 0;

    for a := 5 downto -2 do
        writeln(a);

    writeln(str, ' ', a);
    print_end()

    {goto lb}
end;
{ ------------------------------ }

BEGIN 
r := 1.0
{ a := gcd(1, 2) }
{ array1[0] := 'a'; }
{ bl := gcd(a, b) + -5 }
end.