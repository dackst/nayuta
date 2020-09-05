import re
import os
import struct

INSERT_COL = 4
OUTPUT_FOLDER = 'output'

def ensure_dir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)

ensure_dir(OUTPUT_FOLDER)

inputdata = {}
for filename in ('area_names.tsv', 'chr_names.tsv'):
    with open(filename, 'r', encoding = 'utf-8') as f:
        for line in f:
            line = line.rstrip('\r\n').split('\t')
            if len(line) < 5:
                continue
            if line[INSERT_COL] == '':
                continue
            addr = int(line[1], 16)
            if re.match('mp_', line[INSERT_COL]):
                file, ref_addr = line[INSERT_COL].split(' ')
                ref_addr = int(ref_addr, 16)
                try:
                    s = inputdata[file][ref_addr]
                except KeyError:
                    continue
            else:
                s = line[INSERT_COL]
            if line[0] not in inputdata:
                inputdata[line[0]] = {}
            inputdata[line[0]][addr] = s
for filename, inputdata2 in sorted(inputdata.items()):
    with open(r'orig\{}.arb'.format(filename), 'rb') as f:
        filedata = bytearray(f.read())
    offset = 0
    for addr, s in sorted(inputdata2.items()):
        addr += offset
        s = s.encode('cp932')
        if len(s) > 31:
            print('{}: {}: {}: Too long, max len is 31.'.format(
                filename, hex(addr), s.decode('cp932')))
            continue
        s = b''.join((s, b'\x00'))
        orig_size = struct.unpack('<I', filedata[addr:addr + 4])[0]
        filedata[addr:addr + 4 + orig_size] = (
            b''.join((struct.pack('<I', len(s)), s)))
        offset += len(s) - orig_size
    with open(r'{}\{}.arb'.format(OUTPUT_FOLDER, filename), 'wb') as f:
        f.write(filedata)
