import re
import os
import struct
import sys
sys.path.insert(0, '..')
import address_mapper


INSERT_COL = 3
OUTPUT_FOLDER = 'output'
INPUT_FOLDER = 'input'

def ensure_dir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)

ensure_dir(OUTPUT_FOLDER)

if not os.path.exists("dumped"):
    import arb_dump
mapping = address_mapper.get_mapping('dumped', INPUT_FOLDER, "arb")

inputdata = {}
for filename in ('area_names.tsv','chr_names.tsv'):
    with open(os.path.join(INPUT_FOLDER, filename), 'r', encoding = 'utf-8') as f:
        for line in f:
            line = line.rstrip('\r\n').split('\t')
            if len(line) < INSERT_COL + 1:
                continue
            if line[INSERT_COL] == '':
                continue
            basename = line[0]
            addr = int(line[1], 16)
            addr = mapping[filename][basename][addr]
            if re.match('mp_', line[INSERT_COL]):
                file, ref_addr = line[INSERT_COL].split(' ')
                ref_addr = int(ref_addr, 16)
                ref_addr = mapping[filename][file][ref_addr]
                try:
                    s = inputdata[file][ref_addr]
                except KeyError:
                    continue
            else:
                s = line[INSERT_COL]
            if line[0] not in inputdata:
                inputdata[line[0]] = {}
            inputdata[line[0]][addr] = s
for basename, inputdata2 in sorted(inputdata.items()):
    filename = basename + '.arb'
    with open(os.path.join('orig', filename), 'rb') as f:
        filedata = bytearray(f.read())
    offset = 0
    for addr, s in sorted(inputdata2.items()):
        addr += offset
        s = s.encode('cp932')
        if len(s) > 31:
            print('{}: {}: {}: Too long, max len is 31.'.format(
                basename, hex(addr), s.decode('cp932')))
            continue
        s = b''.join((s, b'\x00'))
        orig_size = struct.unpack('<I', filedata[addr:addr + 4])[0]
        filedata[addr:addr + 4 + orig_size] = (
            b''.join((struct.pack('<I', len(s)), s)))
        offset += len(s) - orig_size
    ensure_dir(os.path.join(OUTPUT_FOLDER, basename))
    with open(os.path.join(OUTPUT_FOLDER, basename, filename), 'wb') as f:
        f.write(filedata)
