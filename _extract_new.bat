@echo off
if [%1]==[] goto error

echo Extracting files...
cd /d %~dp0
py -3 extract.py %1 ISO
py -3 setup.py
echo Finished.
goto :end

:error
echo Please drag and drop your original ISO over _extract.bat
echo instead of double clicking.
echo.

:end
pause
