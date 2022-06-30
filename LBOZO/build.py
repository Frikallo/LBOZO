import base64, os, sys


def error(s):
    print(s)
    sys.exit(-1)


def build(program):
    command = "python3 -m PyInstaller -F --clean LBOZO/src/main.py -n {}".format(
        program
    )
    os.system(command)

    try:
        with open("dist/{}.exe".format(program), "rb") as f:
            ret = f.read()
            output64 = base64.b64encode(ret)
    except:
        error("{} binary doesnt exist, compilation failed.".format(program))

    with open("dist/base64{}".format(program), "wb") as f:
        f.write(output64)

    return output64


build("LBOZO")
