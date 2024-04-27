import fileinput
from random import randint

prompts=[]

def load_file():
    for line in fileinput.input(files=("guide_prompts.txt"), encoding="utf-8"):
        prompts.append(line[:-1])
    # print(prompts)

def get_prompt():
    if not len(prompts):
        load_file()
    return prompts[randint(0, len(prompts) - 1)]
    