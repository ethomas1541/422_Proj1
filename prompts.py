# Author: Elijah Thomas
# Last modified: April 27 2024
# Group 5

# Module for rapidly providing SQ3R-related prompt material stored in the static file guide_prompts.txt

import fileinput
from random import randint

prompts=[]

# Very simple function for parsing guide_prompts.txt into an array
def load_file():
    for line in fileinput.input(files=("guide_prompts.txt"), encoding="utf-8"):
        #                   v cut off the newline character in each line
        prompts.append(line[:-1])
    # print(prompts)

# Return a random prompt from the array
# This makes CYCLE_prompts a bit of a misnomer, but that's a very trivial detail.
def get_prompt():
    if not len(prompts):
        load_file()
    return prompts[randint(0, len(prompts) - 1)]
    