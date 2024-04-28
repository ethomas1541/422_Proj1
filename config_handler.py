import fileinput

def write_config(lines:dict):
    try:
        file = open("config.txt", "x")
        for key in lines:
            file.write(f"{key}: {lines[key]}\n")
    except:
        pass

def read_config():
    ret = []
    for line in fileinput.input(files="config.txt", encoding="utf-8"):
        ret.append(line.partition(":")[2][:-1][1:])
    return ret