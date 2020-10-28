
echo Inserting arb files...
chdir arg
py -3 .\arb_insert.py
pause

echo "Inserting 'script' files..."
chdir ../script
py -3 scriptinsert.py
pause

echo "Inserting 'text' files..."
chdir ../text
py -3 textinsert.py
pause

echo Inserting eboot...
chdir ../EBOOT
py -3 nayuta_eboot_insert_v2.py
pause

echo misc
chdir ../misc
py -3 misc.py
chdir ..

echo Copying to ISO folder...
py -3 copy_all.py

pause

call _build.bat
pause