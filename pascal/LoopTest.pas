program LoopTest;

var 
    i : int;

begin
    for i := 9 downto 5 do
    begin
        writeln(i)
    end
    ;

    while i > 0 do 
    begin 
        writeln(i);
        i := i - 1
    end

end
.