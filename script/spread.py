#!/bin/python

# reformat script lines 
# useful for pasting into automatic spellcheckers or 
# side by side comparisons with japanese


import os

COL = 4
folder = "input/" # folder containing eng script 
jp_folder = "dumped/" # folder contained jp script

filenames = os.listdir(folder)
filenames.sort()

new_file = "spread.tsv"

def is_ani(text):
    '''
    determine if text of a line is animation
    '''

    if text.startswith("ANI"): # helpfully labeled
        return True

    other_text = set(
        ["Exclamation",
        # "Voice",
        "Surprise",
        "Coldsweat",
        "Sweatdrop",
        "Ellipsis",
        "Unknown",
        "MOT_PANIC",
        "BE_TAIL_BTL",
        "Question"
        ])

    return text in other_text


def scan_file_name(filename):
    '''
    scan through a given file, and return a list of 
    each line of dialogue that goes in a text box.

    now includes speaker and event namess
    '''

    with open(filename) as f:
        print("scanning", filename)
        text = ""
        lines = [] 
        line_num = 0
        for line in f.readlines():
            line = line.rstrip("\t\n").split("\t")
            line_num += 1
            
            # skip lines not long enough
            if len(line) < 2: 
                continue

            # construct lines
            if line[0]: # start of new dialog box
                if (text and # skip rows with empty text column
                     not is_ani(text)): #skip animations
                    # store existing line of dialog
                    lines.append(text)

                if is_ani(line[COL]):
                    text = ''
                    continue
                text = line[2] + '\t' + line[3] + '\t' + line[COL]
            else:

                if text.startswith("("): 
                # subsequent lines of inner thoughts start with a space
                    text += "" + line[COL]
                else:
                   text += " " + line[COL]   

        # check last line of file
        if (text and # skip rows with empty text column
            not is_ani(text)): #skip animations
            # store existing line of dialog
            lines.append(text)


    return lines




all_lines = []

for filename in filenames[:]:
    # scan eng lines
    lines = scan_file_name(folder + filename)

    # jp lines
    jp_lines = scan_file_name(jp_folder + filename)
    for i in range(len(lines)):
        lines[i] += jp_lines[i][jp_lines[i].index('\t'):]

    if lines:
        all_lines.extend(lines)

# write to new file
if all_lines:
    with open(new_file, "w") as newfile:
        for line in all_lines:
            print(line, file=newfile)
