program prog;

var
    I: Integer;
begin
    Write('parametros: ');
    for I := 1 to ParamCount do
        Write(ParamStr(I), ' ');
    WriteLn();
end.
