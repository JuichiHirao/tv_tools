# New-Item -ItemType SymbolicLink -Path net_contents_arrangement.ps1 -Target "C:\Users\JuichiHirao\PycharmProjects\tv_tools\bin\net_contents_arrangement.ps1"
param( $param, $param2, $param3 )

C:\Users\JuichiHirao\PycharmProjects\tv_tools\venv\Scripts\Activate.ps1
Set-Variable PYTHONPATH=.
cd C:\Users\JuichiHirao\PycharmProjects\tv_tools
py.exe C:\Users\JuichiHirao\PycharmProjects\tv_tools\net_contents_arrangement.py $param $param2 $param3
cd C:\Users\JuichiHirao
