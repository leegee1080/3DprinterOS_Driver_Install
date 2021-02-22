import datetime
import getpass
import re
import os
import socket

try:
    from paramiko import SSHClient
except ModuleNotFoundError:
    print("Module paramiko not installed...attemping to install.")
    os.system("pip install paramiko")
# import subprocess
# import sys

def Validate_IP(IP):
    regexIPv4 = "(([0-9]|[1-9][0-9]|1[0-9][0-9]|"\
            "2[0-4][0-9]|25[0-5])\\.){3}"\
            "([0-9]|[1-9][0-9]|1[0-9][0-9]|"\
            "2[0-4][0-9]|25[0-5])"

    regexIPv6 = "((([0-9a-fA-F]){1,4})\\:){7}"\
             "([0-9a-fA-F]){1,4}"

    check1 = re.compile(regexIPv4)
    check2 = re.compile(regexIPv6)

    if (check1.search(IP)):
        return True
    elif (check2.search(IP)):
        return True
    return False

def Return_TS(driver_code_line):
    regexTS = r"TS=([0-9]*)\s"
    TScheck = re.compile(regexTS)
    TSreturn = ""
    if(TScheck.search(driver_code_line)):
        TSreturn = TScheck.search(driver_code_line).group(1)
    return TSreturn

def Return_Token(driver_code_line):
    regexToken = r"token=(.*)'"
    Tokencheck = re.compile(regexToken)
    Tokenreturn = ""
    if(Tokencheck.search(driver_code_line)):
        Tokenreturn = Tokencheck.search(driver_code_line).group(1)
    return Tokenreturn

def End_Script(new_log_text):
    with open("log.txt", "w") as log_file:
         log_file.write(new_log_text)
    exit

def main():
    current_time = datetime.datetime.now()
    #start log file (create new file), append date and time
    log_text = f"----3DprinterOS Driver Install----\nLog started on {current_time.strftime('%H:%M:%S on %A, %B the %dth, %Y')}\n"

    #ask user for current password (user will always be 'root')
    print("What is the password for the root user?")
    user_password = getpass.getpass()

    #OPTIONAL!!
    #ask user if they would like to batch change pw for root user
    #ask user if they would like to run custom code
    #if yes then ask if user would like to run custom code with TScode and token filled in.

    #otherwise run default code
    try:
        with open("default-code.txt", "r") as default_code_file:
            print("Found default code file.")
            default_terminal_line = default_code_file.read()
    except IOError:
        print("File named 'default-code.txt' not found or has been changed.")
        exit()

    #declare 3 var to use later
    driver_codes = []
    ip_addresses = []
    code_pairs = []

    #declare the list that will have the ip addresses combined with the code pairs
    complete_pairs = []

    #open ip file
    #start loop until ip file has no more lines
    try:
        with open("printer-IPs.txt", "r") as ip_file:
            print("Found IP file.")      
    except IOError:
        print("File named 'printer-IPs.txt' not found.")
        End_Script(log_text)

    with open("printer-IPs.txt", "r") as ip_file:
        lines = ip_file.readlines()
        for line in lines:
            line = line.rstrip('\n')
            #check each line for correct ip address format
            if(Validate_IP(line)):
                #check ping the ip address
                if(os.system(f"ping -n 1 {line}") == 0):
                    #check attempt ssh with default usr and pw 'telnet $ssh-host $ssh-port'
                    new_client = SSHClient()
                    try:
                        new_client.connect(line, username='root', password=user_password)
                        new_client.close()
                    except TimeoutError:
                        log_text += f"!!!!SSH {line} is unreachable!!!!\n"
                else:
                    log_text += f"!!!!IP {line} is unreachable!!!!\n"
            else:
                log_text += f"!!!!Invalid ip {line} found!!!!\n"

    #open code file
    try:
        with open("driver-codes.txt", "r") as codes_file:
            print("Found driver-codes file.")
            lines = codes_file.readlines()
            for line in lines:
                line = line.rstrip('\n')
                if(line != "" and line != None):
                    driver_codes.append(line)
    except IOError:
        print("File named 'driver-codes.txt' not found.")
        End_Script(log_text)

    #create the code pair tuples
    for code in driver_codes:
        if(Return_TS(code) != "" and Return_Token(code) != ""):
            code_pairs.append((Return_TS(code), Return_Token(code)))
        else:
            continue

    #combine all the vars together and check if there is enough codes to go around
    pairs_counter = 0
    for ip in ip_addresses:
        temp_tuple = code_pairs[pairs_counter]
        complete_pairs.append((ip,temp_tuple(0),temp_tuple(1)))
        pairs_counter += 1
    #-----if there are no more codes -----> append log file('ip_address' has no code pair) --------> continue
    #-----if blank -----> continue
    #grab the TS code and token ---> ts_code, download_token
    #default_terminal_line_filled = default_terminal_line + (find replace the correct fields)
    #temp_tuple = (ip_address, default_terminal_line_filled)
    #place the code pairs with ip addresses in a list  'complete_pairs.append(temp_tuple)'
    #=======================

    #code_pairs should be a complete list of tuples that are a set

    #start loop until there are no more items in code_pairs
    #=======================
    #ssh into ip -----> code_pairs(0)
    #run code ----> code_pairs(1)
    #----if code ran with error -----> append log line('code_pairs(0)' failed to run code 'code_pairs(1)')
    #======================

    #if there are unused driver codes ----> append them to a file called 'unused-codes'
    #append log with time stamp and number of codes ran
    End_Script(log_text)
    return


if __name__ == "__main__":
    main()