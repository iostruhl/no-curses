tell application "System Events"
    set frontAppProcess to first application process whose frontmost is true
end tell

set isFocused to false
tell frontAppProcess
    if the (count of windows) is not 0 then
        set isFocused to (name of front window contains "oh-hell.py")
    end if
end tell

if not isFocused then
    tell application "System Events"
        tell process "Terminal"
            try
                set clientWindow to (first window whose name contains "oh-hell.py")
                perform action "AXRaise" of clientWindow
                do shell script "open -a Terminal"
                delay 1
            end try
        end tell
    end tell
end if
