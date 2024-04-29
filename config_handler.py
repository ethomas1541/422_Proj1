# Author: Elijah Thomas

# Module for writing to and reading from a config.txt file that persists between launches of the program
# This means that the user only has to be asked ONCE for the login information

# Admin accounts have the ability to override this config file, changing to an instance on a different port 
# on the ix server, a different user on that instance, or a different database within that instance

# Of course, if they choose to override it, we just need to make a new config file with whatever changes they've made.

import fileinput
from os import remove

def write_config(lines:dict):
    try:
        # This raises an error if the con
        file = open("config.txt", "x")
        for key in lines:
            file.write(f"{key}: {lines[key]}\n")
    except:
        remove("config.txt")
        write_config(lines)

def read_config():
    ret = []
    for line in fileinput.input(files="config.txt", encoding="utf-8"):
        ret.append(line.partition(":")[2][:-1][1:])
    return ret