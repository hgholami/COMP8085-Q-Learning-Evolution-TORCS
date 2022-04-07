@echo off
set race_config=%1
set ep_num=%2

for /L %%i in (1, 1, %ep_num%) do cmd /c wtorcs.exe -r %race_config%

exit