from netmiko import Netmiko
import sys
#!pip install tabulate
from tabulate import tabulate  
import logging

logging.basicConfig(filename='netmiko_global.log', level=logging.DEBUG)
logger = logging.getLogger("netmiko")
   

#------------------------- GLOBAL PARAMS -------------------------#
# if you want to use some global params
#
# device1= {"host":"192.168.200.26",
#                "password":"admin",
#                "username":"admin",
#                "port":22,
#                "secret":"admin",
#                "device_type":"cisco_ios"}
#------------------------- && -------------------------#

#- This function for vlan port assignment -#
def cisco_vlan_changer(ip,username="admin",password="admin",port=22,secret="admin",device_type="cisco_ios"):
    sh_int_desc="sh inter desc"
    sh_int_status="sh interfaces status "
    sh_vlan="sh vlan"
    with open("switches.txt") as f:
        host_ip=[(f.read().splitlines())     ]
   
    conn = Netmiko(host=ip,password=password,username=username,port=port,secret=secret,device_type=device_type)
    try:
            conn.enable()
            #-or if you do not want to show VLAN info you can use REGEX like this: "sh interfaces description | inc /" -#
            output=conn.send_command(sh_int_status, use_textfsm= True) 
            #- We are set first row of list to make HEADER-#-#
            table=[["NUMBER","Port","Name","Status","Vlan","Dublex","Speed","Type"]]
            for i in  range(len(output)):
                if output[i]["name"]=="":
                    #-if port has no description we will see "NONE" to be more readable-#
                    table.append([[i],output[i]["port"],'NONE',
                                  output[i]["status"],output[i]["vlan"],
                                  output[i]["duplex"],output[i]["speed"],
                                  output[i]["type"]])
                else:
                    table.append([[i],output[i]["port"],output[i]["name"],
                                  output[i]["status"],output[i]["vlan"],
                                  output[i]["duplex"],output[i]["speed"],
                                  output[i]["type"]])
                    #-We will use tabulate library for more readable output-#
            print(tabulate(table,headers="firstrow",tablefmt="fancy_grid"))
    except Exception as e:
            print (f"Something wrent wrong : {e}")
    else:
        print("*"*13 +"SUCCESS"+ "*"*13+"\n")
        
    port_id=int(input("Which Port ID do you want to change?"))
    while(True):
        print(f"Do you want to continous with Port '{port_id}', press : Y/N")
        if input().upper()=="Y":
            break
        else:
            port_id=int(input("Select a new port Number : "))
    
    #-------------------------- GET PORT NAME/ID --------------------------#
    #- Getting real port number ex:Eth0/0,Twe1/0/3, Hundred1/1/1 etc. -#
    port_id=output[port_id]["port"]
    sh_port_id="sh run interface "+str(port_id)
    #-sending command "sh run interface -id-"-#
    print("\n"+"*"*50)
    print(f" Info's -{sh_port_id}- :\n")
    #- Our output will be : "sh_port_id_output:<class 'str'>", because "use_textfsm= True" does not work. We have  to take our parsel-#
    sh_port_id_output=conn.send_command(sh_port_id, use_textfsm= True) 
    #- and now : sh_port_id_output: <class 'list'> easy to use-#
    sh_port_id_output=sh_port_id_output.splitlines()
    #- Some info not usable for me. example : index[0]:"Building configuration...", index[1]:"Current configuration : 90 bytes",
    # index[2]:"!",last index:"end" .... -#
    #- I deleted unnecessary information -#
    sh_port_id_output=sh_port_id_output[5:-1]
    #- sh run int "sh_port_id"-#
    [print(i) for i in sh_port_id_output]
    print("*"*50)
    
    #-------------------------- GET VLANS --------------------------#
    output = conn.send_command(sh_vlan)
    output=output.splitlines()
    #- I need to see this range "int((len(output))/2)-10" this formul every time will show only usable vlan range you not will see Vlan 1002-1005 and like :
    #VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
    # ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
    # 1    enet  100001     1500  -      -      -        -    -        0      0
    # 10   enet  100010     1500  -      -      -        -    -        0      0
    # 12   enet  100012     1500  -      -      -        -    -        0      0
    # 13   enet  100013     1500  -      -      -        -    -        0      0
    # VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2
    # ---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------
    # 14   enet  100014     1500  -      -      -        -    -        0      0
    # you will not see ...
    output_length=(int((len(output))/2)-13)
    #normally (int((len(output))/2)-10) enough but I will index iteration i=i+3 for delete last 3 line: 
    # index0 = []
    # index1 = ['VLAN', 'Name', 'Status', 'Ports']
    # index2 = ['----', '--------------------------------', '---------', '-------------------------------']
    # index3 = ['1', 'default', 'active', 'Et0/2,', 'Et0/3,', 'Et1/0,', 'Et1/1,', 'Et1/2,', 'Et1/3,', 'Et2/0,', 'Et2/1,', 'Et2/2,', 'Et2/3']
    # I will start print the list from the 3rd index or delete first 3line -#
    all_switch_vlan_id=[]# for store vlan ID's
    for i in range(output_length):
        output[i]=output[i+3].split()
        all_switch_vlan_id.append(output[i][0])
    get_new_vlan_id=int(input("Please write new VLAN ID: "))
    set_new_vlan_id=[f"interface {port_id}","sw mode acc",f"switch acc vlan {get_new_vlan_id}"]
    
    conn.config_mode()
    print(conn.send_config_set(set_new_vlan_id))
    #["inte et 1/1","sw mo acc ","sw acc vl 99"]
    print("*"*50)
    print(conn.send_command(sh_port_id))
    conn.save_config()
    #-disconnect from device-#
    conn.disconnect()
    
def print_switch_ip():
    with open("switches.txt") as f :
        print(f.read())
print_switch_ip()
ip = str(input("Please write ip to connection : "))
cisco_vlan_changer(ip=ip)
