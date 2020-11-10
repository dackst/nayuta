#!/bin/sh

# script to build outside windows, but requires a wineprefix with python 3 installed
export WINEPREFIX=

# insert stuff ------------
cd script
python3 scriptinsert.py

cd ../arg
python3 arb_insert.py

cd ../EBOOT
python3 nayuta_eboot_insert_v2.py

cd ../text
python3 textinsert.py

cd ../misc
python3 misc.py

# start copying stuff ------------
cd ..

python3 copy_all.py

# build ----------
wine cmd /c _build.bat



