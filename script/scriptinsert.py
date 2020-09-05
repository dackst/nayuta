import copy
import os
import pdb
import re
import struct

#specifies position of (first) string argument within each opcode
arg_pos = {
    0x07:   0,
    0x36:   1,
    0x3F:   0,
    0x40:   1,
    0x41:   3,
    0x98:   1,
    0xC1:   1,
    0xC9:   1,
    0xCE:   1}
#specifies location of pointer argument within each opcode
arg_pos_ptr = {
    0x7B:   1,
    0x7C:   1,
    0x7D:   0,
    0x80:   0,
    0x81:   0,
    0x83:   1}

#text opcodes / number of lines
#07	"1"
#36	1
#3F	1
#40	3
#41	10
#98	3
#C1	1
#C9	1
#CE	1

INPUT_FOLDER = 'merged'
OUTPUT_FOLDER = 'output'
INSERT_COL = 5

#Holds: addr, opcode/microcode number
class Op(object):
    def __init__(self, line):
        self.addr = int(line[0], 16)
        self.opcode = int(line[1], 16)
        self.code = line[3]
        self.text = [line[INSERT_COL]]
    def add_line(self, text):
        self.text.append(text)
    def __repr__(self):
        return '{} {}'.format(hex(self.addr), '\n'.join(self.text))
    def check_ref(self):
        if (re.match('mp_', self.text[0]) or
            re.match('noi', self.text[0]) or
            re.match('system', self.text[0])):
            self.ref, self.ref_addr = self.text[0].split(' ')
            self.ref_addr = int(self.ref_addr, 16)
        else:
            self.ref = False
    def get_args(self, origdata):
        end_pos, self.args = argparse(origdata, self.addr)
        self.size = 2 + len(b''.join(self.args))
    def adjust_speed(self, origdata):
        #only these opcodes can have speed parameters
        if self.opcode not in (0x40, 0x41, 0x98):
            return
        #check to see if opcode has speed parameter
        if 'W' not in self.code:
            return
        speed_pos = self.code.find('W') - 1
        orig_speed = int(self.code[speed_pos]) + 1
        dummy1, args, dummy2 = argparse2(origdata, self.addr)
        if self.opcode in (0x40, 0x98):
            orig_len = len(''.join(args[1:4])) - len(self.code)
        else:   #opcode = 0x41
            orig_len = len(''.join(args[3:13])) - len(self.code)
        new_len = len(''.join(self.text))
        #the speed parameter says how many frames per one character for
        #text display. So time (in frames) is length times speed.
        orig_time = orig_len * orig_speed
        #speed (characters per frame) is time divided by length
        #Rounds down. You could try rounding nearest.
        #I found rounding down gives a better experience. YMMV.
        new_speed = int(orig_time / new_len) - 1
        if new_speed < 0:   #0 is the fastest it can go (1 character per frame)
            new_speed = 0
        #writeback the new speed
        self.code = ''.join((
            self.code[:speed_pos], str(new_speed), self.code[speed_pos + 1:]))
        
            
    def bin(self):
        #had a problem with this being mutated over multiple calls
        args = copy.deepcopy(self.args)
        if self.opcode in (0x07, 0x36, 0x3F, 0xC1, 0xC9, 0xCE): #1 line
            if self.opcode == 0x07:
                text = copy.deepcopy('\n'.join(self.text))
            else:
                text = copy.deepcopy(set_length(self.text, 1)[0])
            arg = arg_pos.get(self.opcode)
            args[arg] = format_string(
                (self.code + text).encode('cp932'))
        elif self.opcode in (0x40, 0x98):
            text = copy.deepcopy(set_length(self.text, 3))
            text[0] = self.code + self.text[0]
            for arg, s in zip(range(1, 4), text):
                args[arg] = format_string(s.encode('cp932'))
        elif self.opcode == 0x41:
            text = copy.deepcopy(set_length(self.text, 10))
            text[0] = self.code + self.text[0]
            for arg, s in zip(range(3, 13), text):
                args[arg] = format_string(s.encode('cp932'))
        return b''.join((struct.pack('<BB', self.opcode, 0x80),
                         b''.join(args)))
            
def format_string(b):
    return b''.join((b'\xDF\x82', struct.pack('<I', len(b)), b))

def set_length(l, size, fillvalue = ''):
    '''extends l to size using fillvalue or truncates l to size'''
    if len(l) < size:
        l += [fillvalue] * (3 - len(l))
    elif len(l) > 3:
        l = l[:3]
    return l
    
def argparse(filedata, pos):
    '''get arguments of opcode at pos in binary'''
    if filedata[pos + 1] != 0x80:
        print('error')
    args = []
    pos += 2
    if pos == len(filedata):
        return pos, args
    while filedata[pos + 1] == 0x82:
        opcode = filedata[pos]
        if opcode in (0xDD, 0xDE):
            args.append(filedata[pos:pos+6])
            pos += 6
            continue
        size = struct.unpack('<I', filedata[pos + 2:pos + 6])[0]
        args.append(filedata[pos:pos+6+size])
        pos += 6 + size
    return pos, args

def argparse2(filedata, pos):
    '''get arguments of opcode at pos in integer/float/string'''
    if filedata[pos + 1] != 0x80:
        print('error')
    args = []
    arg_pos = []
    pos += 2
    if pos == len(filedata):
        return pos, args, arg_pos
    while filedata[pos + 1] == 0x82:
        arg_pos.append(pos)
        opcode = filedata[pos]
        if opcode == 0xDD:
            args.append(struct.unpack('<i', filedata[pos + 2:pos + 6])[0])
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
    return pos, args, arg_pos

def ensure_dir(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)

def scriptinsert(filename):
    with open(r'orig\{}.bin'.format(filename), 'rb') as f:
        filedata = bytearray(f.read())
    origdata = bytes(filedata)
    pos = 0x18
    EOF = struct.unpack('<I',filedata[pos + 0x24:pos+ 0x28])[0]

    #load absolute ptrs in functions table
    abs_ptrs = []
    while pos < EOF:
        abs_ptrs.append(
            [pos + 0x24,
             struct.unpack('<I',filedata[pos + 0x24:pos + 0x28])[0]])
        pos += 0x28

    #load relative pointers (in opcodes)                
    rel_ptrs = []
    pos = abs_ptrs[0][1]   #start of first function
    while pos < len(filedata):
        opcode = filedata[pos]
        pos_saved = pos
        pos, args, arg_pos = argparse2(filedata, pos)
        if opcode in (0x7B, 0x7C, 0x7D, 0x80, 0x81, 0x83):  #ptr opcodes
            arg = arg_pos_ptr.get(opcode)
            #This makes them un-relative
            rel_ptrs.append([arg_pos[arg] + 2, arg_pos[arg] + 6 + args[arg]])


    #perform the insert
    offset = 0
    for key in sorted(inputdata[filename]):
        op = inputdata[filename][key]
        op.get_args(origdata)
        op.check_ref()

        #resolve ref
        if op.ref:
            try:
                op.text = inputdata[op.ref][op.ref_addr].text
            except KeyError:
                print('{}: Ref {} {} not found'.format(
                    hex(op.addr), op.ref, op.ref_addr))
                continue
                    
        if ''.join(op.text) == '':
            print('{}: {}: Blank input'.format(filename, hex(op.addr)))
            continue

        op.adjust_speed(origdata)

        addr = op.addr + offset
        if filedata[addr:addr + 2] != struct.pack('<BB', op.opcode, 0x80):
            pdb.set_trace()
            print('error')
            print(hex(addr))
            print(op.code)
            quit()
        end = addr + op.size
        filedata[addr:end] = op.bin()


        for i, (pos, tgt) in enumerate(abs_ptrs):
            if tgt > addr:
                abs_ptrs[i][1] += len(op.bin()) - op.size

        for i, (pos, tgt) in enumerate(rel_ptrs):
            if pos > addr:
                rel_ptrs[i][0] += len(op.bin()) - op.size
            if tgt > addr:
                rel_ptrs[i][1] += len(op.bin()) - op.size
        offset += len(op.bin()) - op.size
##        print(len(op.bin()), op.size, offset)

    # Write-back pointers
    for ptr, tgt in abs_ptrs:
        filedata[ptr:ptr + 4] = struct.pack('<I', tgt)

    # Write-back relative pointers
    for ptr, tgt in rel_ptrs:
        tgt = tgt - (ptr + 4)
        filedata[ptr:ptr + 4] = struct.pack('<i', tgt)

    with open(r'{}\{}.bin'.format(OUTPUT_FOLDER, filename), 'wb') as f:
        f.write(filedata)

ensure_dir(OUTPUT_FOLDER)
print('Load input')
inputdata = {}
for filename in (os.path.splitext(x)[0] for x in os.listdir(INPUT_FOLDER)):
    basename = os.path.splitext(filename)[0]
    inputdata[basename] = {}

    #load input
    with open(r'{}\{}.tsv'.format(
        INPUT_FOLDER, basename), 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\r\n').split('\t')
            if line[0] == '':
                inputdata[basename][addr].add_line(line[INSERT_COL])
            try:
                addr = int(line[0], 16)
            except ValueError:
                continue
            if '_' in line[0]:  #hacky
                continue
            if int(line[1], 16) in (0x06, 0x6B, 0xBC):
                continue
            op = Op(line)
            addr = op.addr
            inputdata[basename][addr] = op
print('Insert')
for filename in (os.path.splitext(x)[0] for x in os.listdir(INPUT_FOLDER)):
    print(filename)
    scriptinsert(filename)
##scriptinsert('mp_0000')
