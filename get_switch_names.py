from netmiko import ConnectHandler
import threading
import time
import logging


class get_names:

#------------------------- GLOBAL PARAMS -------------------------#
# if you want to use some global params
#
# TO THREADS
    threads=[]
# TO GET LOG
    logging.basicConfig(filename='/tmp/netmiko_get_names.log', level=logging.DEBUG)
    logger = logging.getLogger("ssh")
#
#
#
#------------------------- && -------------------------#


    def get_cisco_names(cisco_device):

        try:
            conn=ConnectHandler(**cisco_device)
            conn.enable()
            get_name=conn.find_prompt()[:-1]
        except Exception as e:
            print(f"\n err_host: ???:{cisco_device['host']}:\t{e}")
        else:
            print(f"{get_name}:{cisco_device['host']}\n{'-'*30}")
            conn.disconnect()
    def read_ip(path="switches.txt"):
      with open("/tmp/switches.txt") as f:
         ip=f.read().splitlines()
         return ip



    for ip in read_ip():
        cisco_device={"host":ip,
                      "username":"admin",
                      "password":"admin",
                      "port":22,
                      "secret":"admin",
                      "device_type":"cisco_ios"
                     }
        th=threading.Thread(target=get_cisco_names,args=(cisco_device,))
        threads.append(th)

    [th.start() for th in threads]
    [th.join() for th in threads]
