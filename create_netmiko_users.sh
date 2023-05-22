#! /bin/bash
read -p "New netmiko script user name: " uname
sudo useradd $uname -g 2000 -M
for i in $uname;
do
 echo $uname:${uname}.123 | sudo chpasswd ;
 sudo passwd $uname --expire ;
 #echo redhat | sudo passwd --expire $i;
done

read -p "Select what you want to do
1 : get Switches config.
2 : vlan change.
3 : scan new switches (not yet ready).
" input
case  $input in
 1) python3.10 /etc/profile.d/get_config.py;;
 2) python3.10 /etc/profile.d/set_vlan.py;;
 *) exit;;
esac
