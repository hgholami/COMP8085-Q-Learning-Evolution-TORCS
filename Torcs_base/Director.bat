@echo off
set ep_num=10
set director_path=%~dp0
set race_config=%director_path%quickrace_custom.xml

::SET PATH TO TORCS INSTALLATION DIRECTORY AS ARGUMENT
:: example Director.bat "c:\Program Files (x86)\torcs"

if [%1]==[] goto error_path
set sim_path=%1
set torcs_path=%sim_path%wtorcs.exe

if [%2]==[reset] goto reset

goto :run_sym

:error_path
echo No path to TORCS executable was provided
goto :eof

:reset
echo Resetting before experiment...
goto run_sym

:run_sym
echo Running experiment...
start "ai_client" py pyclient.py --maxEpisodes=%ep_num%
::start /wait "torcs_sim" /d %sim_path% call "%director_path%Torcs_Sim.bat" "%race_config%" %ep_num%

cd %sim_path%
call "%director_path%Torcs_Sim.bat" "%race_config%" %ep_num% "%director_path%"
cd /d %director_path%

::taskkill /FI "WINDOWTITLE eq torcs_sim"
::taskkill /FI "WINDOWTITLE eq ai_client"
exit /B 1