# copy pasta of flame's copy_* python scripts

# it should also now work outside of a windows python installation. 
# Of course, it should also work in a windows python installation

# also now works for script/system, script/noi, and new final boss texture

import os
import shutil
import packed_lib
from contextlib import suppress

# choose another unpacked ISO folder if you want
target_dir = 'ISO'

def packed_update(file_list, packed_list):
    '''
    modify files in packed_list so they don't 
    overwrite changes to files in file_list
    '''
    for packed_file in packed_list:
        with open(packed_file, 'rb') as f:
            packed = packed_lib.packed_file(f)
        while True:
            for file in packed.TOC:
                if file.name in file_list:
                    packed.remove(file.name)
                    break
            else:
                break
        if packed.updated:
            with open(packed_file, 'wb') as f:
                f.write(packed.bin())


def copy_arb():
    src_path = r'arg/output'
    tgt_path = target_dir + r'/PSP_GAME/USRDIR/map'
    filelist = os.listdir(src_path)

    for i, filename in enumerate(filelist):
        shutil.copy(
            '{}/{}/{}.arb'.format(src_path, filename, filename),
            '{}/{}/{}.arb'.format(tgt_path, filename, filename)
        )
        filelist[i] = filename + '.arb'

    packed_path = target_dir + r'/PSP_GAME/USRDIR/pack/map'
    packed_list = tuple(filter(lambda x: '.mpp' in x, os.listdir(packed_path)))
    packed_list = ['{}/{}'.format(packed_path, i) for i in packed_list]

    packed_update(filelist, packed_list)

def copy_script():
    script_path = r'script/output'
    filelist = tuple(filter(lambda x: '.bin' in x, os.listdir(script_path)))
    text_path = target_dir + r'/PSP_GAME/USRDIR/script'

    for filename in filelist:
        shutil.copy(
            '{}/{}'.format(script_path, filename),
            '{}/{}'.format(text_path, filename)
        )

    packed_path = target_dir + r'/PSP_GAME/USRDIR/pack/map'
    packed_list = list(os.listdir(packed_path))
    packed_list = ['{}/{}'.format(packed_path, i) for i in packed_list]
    packed_list.append(target_dir + r'/PSP_GAME/USRDIR/pack/global/first.dat')

    packed_update(filelist, packed_list)

def copy_img():
    src_path = 'img'

    #manual images
    filelist = tuple('{}/{}'.format(src_path, x) for x in filter(
        lambda x: x.startswith('h_') and x.endswith('.itp'), os.listdir(src_path)))
    for filename in filelist:
        shutil.copy(filename, target_dir + r'/PSP_GAME/USRDIR/visual/help')

    # chapter start/end titles
    filelist = tuple('{}/{}'.format(src_path, x) for x in filter(
        lambda x:  x.startswith('p_') and x.endswith('.itp'), os.listdir(src_path)))
    for filename in filelist:
        shutil.copy(filename, target_dir + r'/PSP_GAME/USRDIR/visual/event')

    #save file images
    for filename in ('{}/{}'.format(src_path, x) for x in (
        'icon_new.png', 'icon0.png', 'pic1.png')):
        shutil.copy(filename, target_dir + r'/PSP_GAME/USRDIR/savefile')
    shutil.copy(r'{}/icon0.png'.format(src_path), target_dir + r'/PSP_GAME/ICON0.PNG')
    shutil.copy(r'{}/pic1.png'.format(src_path), target_dir + r'/PSP_GAME/PIC1.PNG')

    # movies
    shutil.copy(r'{}/nyt_op.pmf'.format(src_path), target_dir + r'/PSP_GAME/USRDIR/movie')
    shutil.copy(r'{}/nyt_ed1.pmf'.format(src_path), target_dir + r'/PSP_GAME/USRDIR/movie')

    #"system" images
    filelist = [
        'm_field0.itp', 'm_field2.itp', 'm_field3.itp', 'm_main.itp',
        'm_mons.itp', 'm_quest.itp', 'title0.it3', 'title1.it3', 'title2.it3']
    for filename in filelist:
        shutil.copy('{}/{}'.format(src_path, filename),
                    target_dir + r'/PSP_GAME/USRDIR/system')

    packed_list = [
        target_dir + r'/PSP_GAME/USRDIR/pack/global/first.dat',
        target_dir + r'/PSP_GAME/USRDIR/pack/global/global.dat'
    ]

    # final boss attack name texture
    shutil.copy('{}/{}'.format(src_path, 'ef_03_21.itp'), 
                target_dir + r'/PSP_GAME/USRDIR/efx/tex')
    filelist.append('ef_03_21.itp')
    packed_list.append(target_dir + r'/PSP_GAME/USRDIR/pack/map/mp_8099.mpp')

    packed_update(filelist, packed_list)

def copy_text():
    src_path = r'text/output'
    filelist = tuple(filter(lambda x: '.tbl' in x or '.tbb' in x,
                        os.listdir(src_path)))
    tgt_path = target_dir + r'/PSP_GAME/USRDIR/text'

    for filename in filelist:
        shutil.copy(
            '{}/{}'.format(src_path, filename),
            '{}/{}'.format(tgt_path, filename)
        )

    packed_path = target_dir + r'/PSP_GAME/USRDIR/pack/map'
    packed_list = list(filter(lambda x: '.mpp' in x, os.listdir(packed_path)))
    packed_list = ['{}/{}'.format(packed_path, x) for x in packed_list]
    packed_list.append(target_dir + r'/PSP_GAME/USRDIR/pack/global/first.dat')
    packed_list.append(target_dir + r'/PSP_GAME/USRDIR/pack/global/global.dat')
    packed_update(filelist, packed_list)

    #questlib.tbb and m_quest.itp are in these
    #that's all that's there so we're just going to delete them
    with suppress(FileNotFoundError):
        os.remove(target_dir + r'/PSP_GAME/USRDIR/pack/script/mp_0004.2pp')
        os.remove(target_dir + r'/PSP_GAME/USRDIR/pack/script/mp_0004c.2pp')
        os.remove(target_dir + r'/PSP_GAME/USRDIR/pack/script/mp_0004d.2pp')

def copy_eboot_misc():
    #EBOOT
    shutil.copy(r'EBOOT/EBOOT.BIN', target_dir + r'/PSP_GAME/SYSDIR')

    #PARAM.SFO
    shutil.copy(r'misc/PARAM.SFO', target_dir + r'/PSP_GAME')

    #misc files
    shutil.copy(r'misc/detail.txt', target_dir + r'/PSP_GAME/USRDIR/savefile')
    shutil.copy(r'misc/dtitle.txt', target_dir + r'/PSP_GAME/USRDIR/savefile')
    shutil.copy(r'misc/title.txt', target_dir + r'/PSP_GAME/USRDIR/savefile')

    #delete UPDATE folder (not needed)
    shutil.rmtree(target_dir + r'/PSP_GAME/SYSDIR/UPDATE', ignore_errors = True)


if __name__ == "__main__":
    copy_arb()
    copy_eboot_misc()
    copy_img()
    copy_script()
    copy_text()
