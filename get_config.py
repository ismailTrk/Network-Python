from netmiko import ConnectHandler
import threading
import time
import logging
##########################GLOBAL VALUES##########################
threads=[]

##########################PROC TIME CALC#########################
start_time = time.time()

##########################GET NETMIKO LOG########################
logging.basicConfig(filename='/tmp/netmiko.log', level=logging.DEBUG)
logger = logging.getLogger("netmiko")

##########################WIDGET BAR#############################
#will update
#
#################################################################

def get_cisco_config(cisco_device):
    try:
        conn=ConnectHandler(**cisco_device)
        conn.enable()
        time.sleep(0.2)
        get_name=conn.find_prompt()[:-1]
    except Exception as e:
        print(f"\nerr_host: {cisco_device['host']} ")
    else:
        get_conf=conn.send_command("sh run")
        #print(get_name,get_conf)
        conn.disconnect()

    with open(f"/tmp/{get_name}.txt","w") as f :
        f.write(get_conf)

with open("/tmp/switches.txt") as f:
    device=f.read().splitlines()

for ip in device:
    cisco_device={"host":ip,
                  "username":"admin",
                  "password":"admin",
                  "port":22,
                  "secret":"admin",
                  "device_type":"cisco_ios"
                 }
    th=threading.Thread(target=get_cisco_config,args=(cisco_device,))
    threads.append(th)
[th.start() for th in threads]
[th.join() for th in threads]
print(time.time()-start_time)
