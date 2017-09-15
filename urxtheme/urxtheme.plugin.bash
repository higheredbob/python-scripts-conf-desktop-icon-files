#!/usr/bin/env bash

# This is a plugin that I use, as a part of an overall modular scripting loader I created
# based off two bash plugin systems I saw some time ago. 
# I liked the idea, so I wrote my own, if you intend to use the below you will either need 
# to source it, and run the command during init or incorperate it into your own plugin scripts
# don't forget to chage the path!

urxtheme()
{
    local thmz=/${HOME}/\.path/to/urxvthemes
    local active=/${HOME}/\.path/to/urxvthemes/loaded/active
    ls ${thmz}
    echo "enter your theme selection"
    read answer
    if [ -f "$thmz/$answer" ]; then
        (command /bin/cat /{$HOME}/\.path/to/urxvthemes/urxvtconfig) > /{$HOME}/\.path/to/urxvthemes/loaded/active
        (command /bin/cat /{$HOME}/\.path/to/urxvthemes/${answer}) >> /{$HOME}/\.path/to/urxvthemes/loaded/active
        command /usr/bin/xrdb -load /{$HOME}/\.path/to/urxvthemes/loaded/active
        echo "success: set theme ${answer}"
    else
        echo "fail"
fi
}

