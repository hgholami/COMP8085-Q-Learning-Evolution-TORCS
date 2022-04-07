@echo off
set race_config=%1
set ep_num=%2
set director_path=%3
set race_config_name=%4

mkdir "%CD%\results\%race_config_name:~0,-4%"
xcopy %race_config%  "%CD%\config\raceman" /r/y/h/q

for /L %%i in (1, 1, %ep_num%) do cmd /c "wtorcs.exe -r ./config/raceman/%race_config_name%"