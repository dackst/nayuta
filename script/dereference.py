
import os
import sys
from spread import is_ani
# dereference any refs in script now, rather than at insertion to prevent confusion

# this reads over all input script files once to compile references
# then reads them again to dereference them, and writes new files

# originally written in attept to switch to 2015 python 2 script inserter, 
# which doesn't support the references to repeated text in the 2017 python 3 version.
# however, the item bug in the 2017 version was eventually fixed, while
# using the 2015 version still produces different bugs


INPUT_FOLDER = 'input'
OUTPUT_FOLDER = 'input-deref'
COL = 4 # column containing text to be inserted in script files

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)
    
def is_ref(line):
    '''
    determine if line is a reference
    
    reference pointers can be in the insert
    column as well as the next column over
    '''
    if len(line) < COL + 1: # too short
        return False

    if is_ani(line[COL]):
        return False

    ref_markers = ["_", "system 0x", "noi 0x"]

    if len(line) > COL + 1:
        return any([i in line[COL+1] for i in ref_markers])
    else:
        return any([i in line[COL] for i in ref_markers])




data = {} # dict mapping basename and address to a list containing each line of text

def scan(filename):
    # scan file and add text to data dictionary
    with open(filename, encoding='utf-8') as f:
        print("scanning", filename)
        #remove extension or directory from filename
        basename = os.path.split(filename)[-1].split(".")[0] 

        data[basename] = {}
        text = [] # should be list containing each line of a text box
        address = ""
        for line in f.readlines():
            
            line = line.rstrip("\t\r\n").split("\t")

            if len(line) < 2:
                continue

            if line[0]:
                if text and address: # store previous text 
                    assert address not in data[basename].keys()
                    data[basename][address] = text
                try:
                    address = int(line[0], 16)
                except ValueError:  
                    # this should have already been skipped in len(line) < 2 part
                    print(line)
                    exit()
                address = line[0]
                text = [line[COL]]
            else:
                text.append(line[COL])
       
        
        assert address not in data[basename].keys()
        data[basename][address] = text
    return data



def main():
    # read through all files once
    for filename in os.listdir(INPUT_FOLDER):
        data = scan(os.path.join(INPUT_FOLDER, filename))


    # read again to deref
    for filename in os.listdir(INPUT_FOLDER):
        output = []
        modified = False
        with open(os.path.join(INPUT_FOLDER, filename), encoding='utf-8') as f:
            prev_ref = False # True if previously processed line had a reference
            for _line in f.readlines():
                line = _line.rstrip("\t\r\n").split("\t")
                print(filename, line)

                if is_ref(line):
                    ref = line[-1]
                    ref_basename, ref_address = ref.split(" ")
                    text = data[ref_basename][ref_address]
                    prev_ref = True
                    modified = True

                    # replace old entry with first line of dereferenced text
                    line[COL] = text[0]

                    #keep the reference in output just in case
                    if len(line) == COL + 1:
                        line.append(ref) 

                    # format to be printed to tsv
                    output.append("\t".join(line))
                    for i in text[1:]: # add any other lines of dereferenced text
                        # output.append("\t\t\t\t" + i)
                        output.append("\t" * COL + i + "\t")

                # skip lines that are continuations of a previously derefernced line
                elif prev_ref and not line[0]: 
                    continue
                elif len(line) < COL + 2: # add tabs so each row has same number of cols
                    while len(line) < COL + 2:
                        line.append("")
                    modified = True
                    prev_ref = False
                    output.append("\t".join(line))
                else: # do nothing
                    prev_ref = False
                    output.append(_line.strip('\r\n'))

        # skip writing file if nothing to dereference
        if not modified:
            continue

        with open(os.path.join(OUTPUT_FOLDER, filename), "w", encoding='utf-8') as newfile:
            for line in output:
                print(line, file=newfile)
                



main()



