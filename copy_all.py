# copy pasta of flame's copy_* python scripts, but without the packing that doesn't seem to totally work

# due to weird mixing of hardcoded slashes and os.path.join i don't care enough to completely rewrite, only works on windows

import os
import shutil

def copy_arb():
    src_path = r'arg\output'
    tgt_path = r'ISO\PSP_GAME\USRDIR\map'
    filelist = tuple(filter(lambda x: '.arb' in x, os.listdir(src_path)))

    for filename in filelist:
        basename = os.path.splitext(filename)[0]
        shutil.copy(
            os.path.join(src_path, filename),
            os.path.join(tgt_path, basename, filename))

def copy_script():
    script_path = r'script\output'
    filelist = tuple(filter(lambda x: '.bin' in x, os.listdir(script_path)))
    text_path = r'ISO\PSP_GAME\USRDIR\script'

    for filename in filelist:
        shutil.copy(
            os.path.join(script_path, filename),
            os.path.join(text_path, filename))

def copy_img():
    src_path = 'img'

    #manual images
    filelist = tuple(os.path.join(src_path, x) for x in filter(
        lambda x: 'h_' in x and '.itp' in x, os.listdir(src_path)))
    for filename in filelist:
        shutil.copy(filename, r'ISO/PSP_GAME/USRDIR/visual/help')

    #save file images
    for filename in (os.path.join(src_path, x) for x in (
        'icon_new.png', 'icon0.png', 'pic1.png')):
        shutil.copy(filename, r'ISO/PSP_GAME/USRDIR/savefile')
    shutil.copy(r'{}/icon0.png'.format(src_path), r'ISO/PSP_GAME/ICON0.PNG')
    shutil.copy(r'{}/pic1.png'.format(src_path), r'ISO/PSP_GAME/PIC1.PNG')

    #"system" images
    filelist = (
        'm_field0.itp', 'm_field2.itp', 'm_field3.itp', 'm_main.itp',
        'm_mons.itp', 'm_quest.itp', 'title0.it3', 'title1.it3', 'title2.it3')
    for filename in filelist:
        shutil.copy(os.path.join(src_path, filename),
                    r'ISO/PSP_GAME/USRDIR/system')
    
def copy_text():
    src_path = r'text\output'
    filelist = tuple(filter(lambda x: '.tbl' in x or '.tbb' in x,
                        os.listdir(src_path)))
    tgt_path = r'ISO\PSP_GAME\USRDIR\text'

    for filename in filelist:
        shutil.copy(
            os.path.join(src_path, filename),
            os.path.join(tgt_path, filename))

def copy_eboot_misc():
    #EBOOT
    shutil.copy(r'EBOOT\EBOOT.BIN', r'ISO\PSP_GAME\SYSDIR')

    #PARAM.SFO
    shutil.copy(r'misc\PARAM.SFO', r'ISO\PSP_GAME')

    #misc files
    shutil.copy(r'misc\detail.txt', r'ISO\PSP_GAME\USRDIR\savefile')
    shutil.copy(r'misc\dtitle.txt', r'ISO\PSP_GAME\USRDIR\savefile')
    shutil.copy(r'misc\title.txt', r'ISO\PSP_GAME\USRDIR\savefile')

    #delete UPDATE folder (not needed)
    shutil.rmtree(r'ISO\PSP_GAME\SYSDIR\UPDATE', ignore_errors = True)


if __name__ == "__main__":
    copy_arb()
    copy_eboot_misc()
    copy_img()
    copy_script()
    copy_text()
    copy_text()