@ECHO OFF

call prep_env.py %*
call %1\monarch\monarch_xp.bat DEBUG
call build_env.py %*
