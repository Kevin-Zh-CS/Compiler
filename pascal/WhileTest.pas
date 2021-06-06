program WhileTest;

var 
    i : int;

begin
    i := int('m');
    while Char(i) > 'f' do 
    begin 
        writeln(char(i));
        i := i - 1
    end
end
.