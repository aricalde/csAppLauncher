set local_storage to "/usr/local/coatlicue/"

tell application "Finder"
	try
		do shell script "python " & local_storage & "csAppLauncher/csAppLauncher.py config.yml"
	on error
		display dialog "Error!
Send a ticket to support"
	end try
end tell