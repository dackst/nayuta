import os
import io

# stuff to map addresses between my 4.15 dump and original jp dump

# read all addresses in file
def get_addresses(filename, filetype):
    addresses = []
    address_col = {"script": 0, "text": 0, "arg": 1, "arb": 1}[filetype]
    # one of "arg" and "arb" is probably a typo?

    # mostly copypasta from "load input" part of scriptinsert.py
    with io.open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\r\n').split('\t')
            try:
                addr = int(line[address_col], 16)

            except ValueError:
                continue
            if '_' in line[address_col] or "0x" not in line[address_col]:  #hacky
                continue
            if filetype == "script" and int(line[1], 16) in (0x06, 0x6B, 0xBC):
                continue
#            if filetype == "script" and line[4] == " ":  
            # there's a single line that's missing from the dumped 4.15 script
            # for some reason. in the dumped jp script, it's just a space?
                # print("why is this here", line)
                # continue
            addresses.append(addr)
    return addresses


# map "basename" and modified 4.15 line addresses to original jp addresses
# optional filetype parameter because the column containing addresses depends on the folder we're in
# 0: script, text
# 1: arg
# script files also have some additional metadata like opcodes

def get_mapping(original_folder, modified_folder, filetype="script"):
    # jp_to_mod = {}
    mod_to_jp = {}
    
    if filetype == "arb" or filetype == "arg":
        # relevant original names (mp_*) are inside one big file here, so need 3 parameters to access original jp address
        # filename: one of the big files, either chr_names.tsv or area_names.tsv
        # basename: mp*
        # modified_address: address from 4.15 dump
        for filename in os.listdir(modified_folder):
            mod_to_jp[filename] = {}
            basenames = []
            # with open(r'{}/{}.tsv'.format(original_folder, filename), 'r', encoding='utf-8') as f:
            with open(os.path.join(original_folder, filename), 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.rstrip('\r\n').split('\t')
                    basenames.append(line[0])

            # weee nested nested dictionaries
            for base in basenames:
                mod_to_jp[filename][base] = {}
            original_addresses = get_addresses(os.path.join(original_folder, filename), filetype)
            modified_addresses = get_addresses(os.path.join(modified_folder, filename), filetype)
            
            
         # make sure I didn't accidentally delete lines I shouldn't have while editing
            assert len(original_addresses) == len(
                modified_addresses), "missing addresses?" + str(
                len(original_addresses)) + " " + str(len(modified_addresses))       
            
            
            for i in range(len(original_addresses)):
                # you have other problems if there are any repeated addresses
                assert modified_addresses[i] not in mod_to_jp[filename][basenames[i]].keys()

                mod_to_jp[filename][basenames[i]][modified_addresses[i]] = original_addresses[i] 
               
        return mod_to_jp        
                    
                
        
    
    # for other files, we only care about the current filename
    for filename in os.listdir(modified_folder):
        basename = os.path.splitext(filename)[0] # remove file extension
        print("reading", basename)
        
        mod_to_jp[basename] = {}

        original_addresses = get_addresses(os.path.join(original_folder, filename), filetype)
        modified_addresses = get_addresses(os.path.join(modified_folder, filename), filetype)

        # make sure didn't accidentally delete lines I shouldn't have while editing
        assert len(original_addresses) == len(
            modified_addresses), "missing addresses?" + str(
                len(original_addresses)) + " " + str(len(modified_addresses))


        for i in range(len(original_addresses)):
            assert modified_addresses[i] not in mod_to_jp[basename].keys()
            mod_to_jp[basename][modified_addresses[i]] = original_addresses[i]

    return mod_to_jp
