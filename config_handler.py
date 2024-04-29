# Author: Elijah Thomas

# Module for writing to and reading from a config.txt file that persists between launches of the program
# This means that the user only has to be asked ONCE for the login information

# Admin accounts have the ability to override this config file, changing to an instance on a different port 
# on the ix server, a different user on that instance, or a different database within that instance

# Of course, if they choose to override it, we just need to make a new config file with whatever changes they've made.

import fileinput
from os import remove

def write_config(lines:dict):
    """
    Arg: lines:dict
        Dictionary to be written, in "key: value\n" format, to config.txt, line-by-line

    No return value
    """
    try:
        # This raises an error if the config.txt file already exists
        file = open("config.txt", "x")
        for key in lines:
            file.write(f"{key}: {lines[key]}\n")
    except:
        # ...In which case, overwrite it!
        remove("config.txt")
        write_config(lines)

def read_config():
    """
    No arguments

    Return value: ret:list
        A list of the "values", (i.e., anything between a semicolon and a \n) found in the file
    """
    ret = []
    for line in fileinput.input(files="config.txt", encoding="utf-8"):
        # Does just what the docstring says; takes the characters after the semicolon, shears off the prepended space
        # and the appended newline character, appends the remaining string to ret
        # The [2] slice takes characters after the semicolon
        # The [:-1] and [1:] slices respectively cut off the last and first characters which are unwanted.
        # Ordering doesn't matter with those two.
        ret.append(line.partition(":")[2][:-1][1:])
    return ret