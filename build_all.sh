#!/bin/sh

# script to build outside windows, but requires a wineprefix with python 3 installed
export WINEPREFIX=


cd ../arg
python3 arb_insert.py

cd ../EBOOT
python3 nayuta_eboot_insert_v2.py

cd script
python3 scriptinsert.py

cd ../text
python3 textinsert.py

cd ../misc
python3 misc.py

# start copying stuff ------------
cd ..

cp -r arg/output/* ISO/PSP_GAME/USRDIR/map

cp script/output/* ISO/PSP_GAME/USRDIR/script

cp img/h_* ISO/PSP_GAME/USRDIR/visual/help
cp img/*.png ISO/PSP_GAME/USRDIR/savefile
cp img/icon0.png ISO/PSP_GAME/ICON0.PNG
cp img/pic1.png ISO/PSP_GAME/PIC1.PNG
cp img/m_* ISO/PSP_GAME/USRDIR/system
cp img/title* ISO/PSP_GAME/USRDIR/system

cp text/output/* ISO/PSP_GAME/USRDIR/text

cp EBOOT/EBOOT.BIN ISO/PSP_GAME/SYSDIR

cp misc/PARAM.SFO ISO/PSP_GAME

cp misc/detail.txt ISO/PSP_GAME/USRDIR/savefile
cp misc/dtitle.txt ISO/PSP_GAME/USRDIR/savefile
cp misc/title.txt ISO/PSP_GAME/USRDIR/savefile

rm ISO/PSP_GAME/SYSDIR/UPDATE


# build ----------
wine cmd /c _build.bat



