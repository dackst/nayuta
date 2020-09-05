import os
import struct
import pdb

def get_s(filedata, pos):
    return filedata[pos:filedata.find(b'\x00', pos)].decode('cp932')

s_dic = {}
area_names = []
chr_names = []
for filename in os.listdir('orig'):
    basename = os.path.splitext(filename)[0]
    with open(r'orig\{}'.format(filename), 'rb') as f:
        filedata = f.read()
    pos = -1
    for x in range(3):
        pos = filedata.find(b'\xFF\x7F', pos + 1)
    pos += 2
    s = get_s(filedata, pos + 4)
    if s in s_dic:
        s = s_dic[s]
    else:
        s_dic[s] = '{} {}'.format(basename, hex(pos))
    area_names.append((basename, hex(pos), 'area name', s))

    pos = 0
    while filedata.find(b'\x0C\x40', pos) != -1:
        pos = filedata.find(b'\x0C\x40', pos) + 12
        if filedata[pos - 2] != 0xFF:
            continue
        pos += struct.unpack('<I', filedata[pos:pos+4])[0] + 6
        if filedata[pos - 2] != 0xFF:
            continue
        s = get_s(filedata, pos + 4)
        if s == '':
            continue
        if s in s_dic:
            s = s_dic[s]
        else:
            s_dic[s] = '{} {}'.format(basename, hex(pos))
        chr_names.append((basename, hex(pos), 'chr name', s))
        
with open('area_names.tsv', 'w', encoding = 'utf-8') as f:
    f.write('\n'.join('\t'.join(x) for x in area_names))
with open('chr_names.tsv', 'w', encoding = 'utf-8') as f:
    f.write('\n'.join('\t'.join(x) for x in chr_names))

