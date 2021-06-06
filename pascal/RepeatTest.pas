program RepeatTest;

var 
    i : int = 0;

begin
    repeat
        i := i + 1
    until i % 7 = 0;
    WriteLn('i = ', i)
end
.