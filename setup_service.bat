call nssm.exe install mis_weekly_rep_gen_service "%cd%\run_server.bat"
call nssm.exe set mis_weekly_rep_gen_service AppStdout "%cd%\logs\mis_weekly_rep_gen_service.log"
call nssm.exe set mis_weekly_rep_gen_service AppStderr "%cd%\logs\mis_weekly_rep_gen_service.log"
call sc start mis_weekly_rep_gen_service