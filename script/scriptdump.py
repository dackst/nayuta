import os
import pdb
import struct

from itertools import zip_longest

#text opcodes / lines
#07	"1"
#36	1
#3F	1
#40	3
#41	10
#98	3
#C1	1
#C9	1
#CE	1

emote_dic = {
    0x0:    'Question',
    0x2:    'Exclamation',
    0x10:   'Sweatdrop',
    0x14:   'Coldsweat',
    0x18:   'Ellipsis',
    0x27:   'Surprise',
    0x39:   'Discovery'}
#
def argparse(filedata, pos):
    '''get arguments of opcode at pos'''
    if filedata[pos + 1] != 0x80:
        print('error')
    args = []
    pos += 2
    if pos == len(filedata):
        return pos, args
    while filedata[pos + 1] == 0x82:
        opcode = filedata[pos]
        if opcode == 0xDD:
            args.append(struct.unpack('<I', filedata[pos + 2:pos + 6])[0])
            pos += 6
            continue
        if opcode == 0xDE:
            args.append(struct.unpack('<f', filedata[pos + 2:pos + 6])[0])
            pos += 6
            continue
        size = struct.unpack('<I', filedata[pos + 2:pos + 6])[0]
        pos += 6
        if opcode == 0xDF:
##            print(hex(pos))
            args.append(filedata[pos:pos + size].decode('cp932'))
        elif opcode == 0xE0:
            args.append('')
        pos += size
    return pos, args

def split_code(s):
    if s == '':
        return '', ''
    pos = 0
    while s[pos] == '#':
        while s[pos] not in ('cxyACEMNWS'):
            pos += 1
        pos += 1
    code = s[:pos]
    s = s[pos:]
    return code, s

def strip_list(l):
    try:
        while not l[-1]:
            l = l[:-1]
    except IndexError:
        pass
    return l

def dic_update(filename, pos, text):
    '''if s in dic return dic[s]; if not put s in dic and return '' '''
    if text in script_dic:
        return script_dic[text]
    script_dic[text] = '{} {}'.format(filename, hex(pos))
    return ''

def ensure_dir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)

def scriptdump(filename):
    with open(r'orig\{}.bin'.format(filename), 'rb') as f:
        filedata = f.read()
    pos = 0x18
    EOF = struct.unpack('<I',filedata[pos + 0x24:pos+ 0x28])[0]

    indexdata = []
    while pos < EOF:
        addr = struct.unpack('<I',filedata[pos + 0x24:pos + 0x28])[0]
        name = filedata[pos:filedata.find(b'\x00',pos)].decode('cp932')
        indexdata.append((name, addr))
        pos += 0x28
    indexdata.append(('', len(filedata)))

    output = [filename]
    for i, (name, addr) in enumerate(indexdata[:-1]):
        output.append(name)
        end_addr = indexdata[i + 1][1]
        while pos < end_addr:
            opcode = filedata[pos]
            pos_saved = pos
            pos, args = argparse(filedata, pos)
            code = ''
            ref = ''
            if opcode == 0x06:                  #animation
                name = args[0]
                text = [args[1]]
            elif opcode == 0x07:                #system text
                name = 'System'
                code, s = split_code(args[0])
##                ref = dic_update(filename, pos_saved, s)
                text = s.split('\\n')
            elif opcode == 0x36:                #choicebox
                name = 'Choice'
##                ref = dic_update(filename, pos_saved, args[1])
                text = [args[1]]
            elif opcode == 0x3F:                #non-standard bubble name
                name = 'Name'
##                ref = dic_update(filename, pos_saved, args[0])
                text = [args[0]]
            elif opcode == 0x40:                #wide box
                name = args[0]
                code, args[1] = split_code(args[1])
                text = strip_list(args[1:4])
##                ref = dic_update(filename, pos_saved, '\n'.join(text))
            elif opcode == 0x41:                #system text (10 lines)
                name = 'None'
                code, args[3] = split_code(args[3])
                text = strip_list(args[3:13])
##                ref = dic_update(filename, pos_saved, '\n'.join(text))
            elif opcode in (0x6B, 0xBC):        #emoticon
                name = args[0]
                text = [emote_dic.get(args[2], 'Unknown')]
            elif opcode == 0x98:                #bubble
                name = args[0]
                code, args[1] = split_code(args[1])
                text = strip_list(args[1:4])
##                ref = dic_update(filename, pos_saved, '\n'.join(text))
            elif opcode == 0xC1:                #system text
                name = 'System'
                text = [args[3]]
##                ref = dic_update(filename, pos_saved, args[3])
            elif opcode == 0xC9:                #teleportal (yes/no box)
                name = 'YesNoBox'
                text = [args[1]]
            elif opcode == 0xCE:                #objective
                name = 'Objective'
                text = [args[1]]
            else:
                continue
            #skip blanks
            if ''.join(text) == '':
                continue
            #dictionary lookup & update
            if opcode not in (0x06, 0x6B, 0xBC):
                ref = dic_update(filename, pos_saved, '\n'.join(text))
            else:
                ref = ''
            output.append((hex(pos_saved),
                           '0x{:02X}'.format(opcode),
                           name, code, text, [ref]))
    with open(r'dumped\{}.tsv'.format(filename), 'w', encoding='utf-8') as f:
        first = True
        for item in output:
            if first:
                first = False
            else:
                f.write('\n')
            if type(item) is str:
                f.write(item)
                continue
            pos, opcode, name, code, text, ref = item
            f.write('\t'.join((pos, opcode, name, code, '')))
            f.write('\n\t\t\t\t'.join(
                '{}\t{}'.format(a, b) for a, b in zip_longest(
                    text, ref, fillvalue = '')))

ensure_dir('dumped')
script_dic = {}
##scriptdump('mp_0000')
for filename in os.listdir('orig'):
    print(filename)
    scriptdump(os.path.splitext(filename)[0])
