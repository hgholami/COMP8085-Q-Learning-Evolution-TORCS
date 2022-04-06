@echo off
set ep_num=100

FOR /L %%i IN (1, 1, %ep_num%) DO wtorcs.exe -r quickrace_custom.xml