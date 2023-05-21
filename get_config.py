from netmiko import ConnectHandler
import threading
import time 
import logging
##########################GLOBAL VALUES##########################
threads=[]
output=[]
##########################PROC TIME CALC#########################
start_time = time.time()
##########################GET NETMIKO LOG########################
logging.basicConfig(filename='netmiko.log', level=logging.DEBUG)
logger = logging.getLogger("netmiko")

##########################WIDGET BAR#############################


#################################################################

def get_cisco_names(cisco_device):
    try:
        conn=ConnectHandler(**cisco_device)
        conn.enable() 
        get_name=conn.find_prompt()[:-1]                
    except Exception as e:
        print(f"\nerr_host: {cisco_device['host']} ")
    else:
        get_conf=conn.send_command("sh run")         
        #print(get_name,get_conf)
        conn.disconnect()
    # bck/{get_name} --> your backup directory path
    with open(f"bck/{get_name}.txt","w") as f :
        f.write(get_conf)

with open("switches.txt") as f:
    device=f.read().splitlines()    


for ip in device:
    cisco_device={"host":ip,
                  "username":"admin",
                  "password":"admin",
                  "port":22,
                  "secret":"admin",
                  "device_type":"cisco_ios"
                 }
    th=threading.Thread(target=get_cisco_names,args=(cisco_device,))
    threads.append(th)
for th in threads:
    th.start() 
for th in threads:
    th.join()
stop_time = time.time()
print(stop_time-start_time)
