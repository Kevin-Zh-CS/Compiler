program GotoTest;

var 
    i : int;
label
    lb;

begin
    i := 2;
lb:
    writeln('a');
    i := i - 1;
    if i > 0 then
        goto lb
end
.