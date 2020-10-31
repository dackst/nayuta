import os
from functools import partial

if not os.path.exists("dumped"):
    os.makedirs("dumped")

def get_s(f, pos):
    saved_pos = f.tell()
    f.seek(pos)
    s = []
    for byte in iter(partial(f.read, 1), b'\x00'):
        s.append(byte)
    s = b''.join(s).decode('cp932')
    f.seek(saved_pos)
    return s

def generic_dump(filename, record_size, string_offset):
    output = []
    filesize = os.path.getsize(os.path.join('orig', filename + '.tbl'))
    with open(os.path.join('orig', filename + '.tbl'), 'rb') as f:
        pos = 0
        while pos < filesize:
            s = get_s(f, pos + string_offset)
            output.append((hex(pos + string_offset), s))
            pos += record_size
    with open(os.path.join('dumped', filename + '.tsv'), 'w', encoding = 'utf-8') as f:
        f.write('\n'.join('\t'.join((offset, s)) for offset, s in output))

generic_dump('helplib',     0x28,   0x8)
generic_dump('foodarea',    0x20,   0x2)
generic_dump('pc',          0x74,  0x20)

def generic_dump_multi(filename, initial_offset, record_size, offset_tuple):
    output = []
    filesize = os.path.getsize(os.path.join('orig', filename + '.tbl'))
    with open(os.path.join('orig', filename + '.tbl'), 'rb') as f:
        pos = initial_offset
        while pos < filesize:
            for offset, _type in offset_tuple:
                s = get_s(f, pos + offset)
                output.append((hex(pos + offset), _type, s))
            pos += record_size
    with open(os.path.join('dumped', filename + '.tsv'), 'w', encoding = 'utf-8') as f:
        first = True
        for offset, _type, s in output:
            if s == 'NULL':
                continue
            if first:
                first = False
            else:
                f.write('\n')
            f.write('{}\t{}\t{}'.format(offset, _type, s))
#filename, initial offset, record size, record structure
generic_dump_multi('questlib', 0, 0x13C,((0x14,   'quest name'),
                                         (0x44,   'client'),
                                         (0x64,   'line'),
                                         (0x98,   'line'),
                                         (0xCC,   'line'),
                                         (0x100,  'line')))
generic_dump_multi('monslib', 0, 0xC0,  ((0x1E,   'mon name'),
                                         (0x3E,   'line'),
                                         (0x5E,   'line'),
                                         (0x7E,   'line')))
generic_dump_multi('item', 0x10, 0x8C,  ((0x0,    'name'),
                                         (0x18,   'desc')))
filelist = ('fldlist0', 'fldlist1', 'fldlist2', 'fldlist3')
for filename in filelist:
    generic_dump_multi(filename, 0, 0x168,  ((0x2,      'name'),
                                             (0x56,     'desc'),
                                             (0x138,    'mission')))
