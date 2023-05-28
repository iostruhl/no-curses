#! /bin/bash

cd
if [ -d "~/no-curses" ]
then
    cd no-curses
    git stash
    git pull
else
    git clone https://github.com/iostruhl/no-curses.git
fi
cd no-curses
python3 -m pip install -r client_requirements.txt

echo "alias play='python3 ~/oh-hell.py oh-hell.iostruhl.com:8080 Joey'" > ~/.profile
exec $SHELL

