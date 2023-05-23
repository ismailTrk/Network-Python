#! /bin/bash
#  your target group_id:2000 for trigger this script!

if [[ $(id -G | grep -ow 2000) = 2000 ]];
then
 echo WELCOME TO PYTHON SCRIPT!
 python3.10 /etc/profile.d/get_config.py
 exit
 exit
 exit
else
 echo Connected :Welcome $USER
fi
