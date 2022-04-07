@echo off
set race_config=%1
set ep_num=%2
set director_path=%3

for /L %%i in (1, 1, %ep_num%) do cmd /c wtorcs.exe -r %race_config%