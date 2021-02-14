import os
import sys
sys.path.insert(0, '..')
import falcom_compress
import address_mapper

INPUT_FOLDER = 'input'
OUTPUT_FOLDER = 'output'

if not os.path.exists("dumped"):
    import textdump
mapping = address_mapper.get_mapping('dumped', INPUT_FOLDER, "text")

def ensure_dir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)

def insert(filename, insert_col, compression_offset, length_limits = None):
    print(filename)
    with open(os.path.join('orig', filename + '.tbl'), 'rb') as f:
        filedata = bytearray(f.read())
    inputdata = []
    with open(os.path.join(INPUT_FOLDER, filename + '.tsv'), 'r', encoding = 'utf-8') as f:
        for line in f:
            line = line.rstrip('\r\n').split('\t')
            if len(line) < insert_col + 1:           #skip line at EOF
                continue
            if line[insert_col] == '':  #skip blanks
                continue
            if line[0] != '':
                addr = int(line[0], 16)
                addr = mapping[filename][addr]
                #get line description (or None if no description)
                if type(length_limits) is dict:
                    desc = line[1]
                else:
                    desc = None
                inputdata.append([addr, desc, line[insert_col]])
            else:                       #add to previous line
                inputdata[-1][2] += ''.join(('\\n', line[insert_col]))
    for addr, desc, s in inputdata:
        s = s.encode('cp932')
        if length_limits:
            if type(length_limits) is int:
                length_limit = length_limits
            else:
                try:
                    length_limit = length_limits[desc]
                except KeyError:
                    print('Length checking error: {}'.format(desc))
                    continue
            if len(s) > length_limit:
                print('{}: {}: Too long, max {} bytes'.format(
                    hex(addr), s.decode('cp932'), length_limit))
                continue

        s = b''.join((s, b'\x00' * (length_limit - len(s))))
        filedata[addr:addr + len(s)] = s
    unc_output = False
    #uncomment for uncompressed output
##    unc_output = True
    if compression_offset == -1 or unc_output:
        with open(os.path.join(OUTPUT_FOLDER, filename + '.tbl'), 'wb') as f:
            f.write(filedata)
    else:
        with open(os.path.join(OUTPUT_FOLDER, filename + '.tbb'), 'wb') as f:
            with open(os.path.join('orig', filename + '.tbb'), 'rb') as g:
                f.write(g.read(compression_offset))
            f.write(falcom_compress.compress_FALCOM3(filedata))

ensure_dir(OUTPUT_FOLDER)
for fldlist in ('fldlist0', 'fldlist1', 'fldlist2', 'fldlist3'):
    insert(fldlist, insert_col = 2, compression_offset = 0x1F,
           length_limits = {'name': 23, 'desc': 63, 'mission': 47})
insert('item',      insert_col = 2, compression_offset = -0x1,
       length_limits = {'name': 23, 'desc': 77})
insert('monslib',   insert_col = 2, compression_offset = 0x1F,
       length_limits = {'mon name': 31, 'line': 31})
insert('questlib',  insert_col = 2, compression_offset = 0x1F,
       length_limits = {'quest name': 47, 'client': 31, 'line': 51})
insert('foodarea',  insert_col = 1, compression_offset = 0x1F,
      length_limits = 25)
insert('helplib',   insert_col = 1, compression_offset = 0x1F,
      length_limits = 31)
insert('pc',        insert_col = 1, compression_offset = 0x23,
      length_limits = 15)
#has description:
#fldlist[0123], item, monslib, questlib
#no description:
#foodarea, helplib, pc
