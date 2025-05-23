import subprocess

# Definiere die PowerShell-Befehle
commands = [
    r"cd Student View",
    r"py -m streamlit run Main_Student_View.py --server.port 8080"
]

# PowerShell-Befehle joinen
command = "; ".join(commands)

# Führe den PowerShell-Code mit den obigen befehlen aus
result = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
