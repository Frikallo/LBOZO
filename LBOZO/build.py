import base64, os, sys


def error(s):
    print(s)
    sys.exit(-1)


outpath = "C:\\Users\\noahs\\Desktop\\Repos\\LBOZO\\out"
additionaldata = "C:/Users/noahs/Desktop/Repos/LBOZO/LBOZO/src/.env;."


def build(program):
    command = "python3 -m PyInstaller -F --clean LBOZO/src/main.py -n {} --distpath {} --onefile".format(
        program, outpath
    )
    os.system(command)

    try:
        with open("out/{}.exe".format(program), "rb") as f:
            ret = f.read()
            output64 = base64.b64encode(ret)
    except:
        error("{} binary doesnt exist, compilation failed.".format(program))

    with open("out/base64{}".format(program), "wb") as f:
        f.write(output64)

    return output64


def build_dropper(dropper_name):
    command = "python3 -m PyInstaller -F --clean LBOZO/dropper.py -n {} --distpath {} --onefile".format(
        dropper_name, outpath
    )
    os.system(command)

    try:
        with open("out/{}.exe".format(dropper_name), "rb") as f:
            ret = f.read()
            output64 = base64.b64encode(ret)
    except:
        error("{} binary doesnt exist, compilation failed.".format(dropper_name))

    with open("out/base64{}".format(dropper_name), "wb") as f:
        f.write(output64)

    return output64


build("LBOZO")

build_dropper("DROPPER")
