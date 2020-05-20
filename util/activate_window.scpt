tell application "System Events"
    set frontAppProcess to first application process whose frontmost is true
end tell

tell frontAppProcess
    set frontAppWindowName to name of front window
end tell

if not frontAppWindowName contains "oh-hell.py" then
    tell application "Terminal"
        activate
        windows where name contains "oh-hell.py"
    end tell
    delay 0.5
end if
