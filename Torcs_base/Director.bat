@echo off
set /a ep_num=1
set race_config_name=quickrace_CG1_1Lap.xml

set /a pop_size=5
set /a gen_num=2
set /a elite_size=2

set /a curr_ind=0
set /a curr_gen=0

set director_path=%~dp0
set elite_path=%director_path%/elites
set race_config=%director_path%/race_configs/%race_config_name%
set qtable=%director_path%qtable.csv

::SET PATH TO TORCS INSTALLATION DIRECTORY AS ARGUMENT
:: example Director.bat "c:\Program Files (x86)\torcs"

if [%1]==[] goto error_path
set sim_path=%1
set torcs_path=%sim_path%wtorcs.exe

goto setup

:error_path
echo No path to TORCS executable was provided
goto :eof

:setup
setlocal
set /a curr_elite_id=1
:creat_elites
copy "%qtable%" "%elite_path%\qtable%curr_elite_id%.csv"
set /a curr_elite_id+=1
if not %curr_elite_id% gtr %elite_size% goto creat_elites
endlocal

set /a individuals_per_elite=%pop_size%/%elite_size%
echo %individuals_per_elite%
goto run_sym

:run_sym
echo Running experiment with individual %curr_ind% in generation %curr_gen%...

start "ai_client" py pyclient.py --maxEpisodes=%ep_num%
::--numElites=%elite_size% --individual=%curr_elite%
::start /wait "torcs_sim" /d %sim_path% call "%director_path%Torcs_Sim.bat" "%race_config%" %ep_num%

cd %sim_path%
setlocal
call "%director_path%Torcs_Sim.bat" "%race_config%" %ep_num% "%director_path%" "%race_config_name%"
endlocal
cd /d %director_path%

::taskkill /FI "WINDOWTITLE eq torcs_sim"
::taskkill /FI "WINDOWTITLE eq ai_client"
echo Individual %curr_ind% trained...

set /a curr_ind+=1
if not %curr_ind% geq %pop_size% goto run_sym

echo Generation %curr_gen% done...

exit /B 1