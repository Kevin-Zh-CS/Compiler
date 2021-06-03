program RecursiveFunctionTest;

var
    i : int;

function Fibonacci(n : int) : int;
begin
    if n = 0 then
        Fibonacci := 0
    else 
    begin
        if n = 1 then
        begin
            Fibonacci := 1
        end
        else
        begin
            Fibonacci := Fibonacci(n - 1) + Fibonacci(n - 2)
        end
    end
end
;

begin
    for i := 1 to 10 do
        writeln(Fibonacci(i))
end
.