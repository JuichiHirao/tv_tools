# New-Item -ItemType SymbolicLink -Path search_tv.ps1 -Target "C:\Users\JuichiHirao\PycharmProjects\tv_tools\bin\search_tv.ps1"
param( $param, $param2 )

C:\Users\JuichiHirao\PycharmProjects\tv_tools\venv\Scripts\Activate.ps1
cd C:\Users\JuichiHirao\PycharmProjects\tv_tools
Set-Variable PYTHONPATH=.
python.exe C:\Users\JuichiHirao\PycharmProjects\tv_tools\search_tv.py $param $param2
cd C:\Users\JuichiHirao
