Option Explicit
Dim shell, fso, root, pythonw
Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
root = fso.GetParentFolderName(fso.GetParentFolderName(WScript.ScriptFullName))
pythonw = root & "\.venv\Scripts\pythonw.exe"
shell.CurrentDirectory = root
shell.Run Chr(34) & pythonw & Chr(34) & " " & Chr(34) & root & "\app.py" & Chr(34), 0, False
WScript.Sleep 2200
shell.Run "http://127.0.0.1:8770", 1, False
