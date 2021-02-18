import datetime
import getpass
import re
import os
import socket

def Validate_IP(IP):
    regexIPv4 = "(([0-9]|[1-9][0-9]|1[0-9][0-9]|"\
            "2[0-4][0-9]|25[0-5])\\.){3}"\
            "([0-9]|[1-9][0-9]|1[0-9][0-9]|"\
            "2[0-4][0-9]|25[0-5])"

    regexIPv6 = "((([0-9a-fA-F]){1,4})\\:){7}"\
             "([0-9a-fA-F]){1,4}"

    check1 = re.compile(regexIPv4)
    check2 = re.compile(regexIPv6)

    if (re.search(check1, IP)):
        return True
    elif (re.search(check2, IP)):
        return True
    return False

def main():
    current_time = datetime.datetime.now()
    #start log file (create new file), append date and time
    log_text = f"----3DprinterOS Driver Install----\nLog started on {current_time.strftime('%H:%M:%S on %A, %B the %dth, %Y')}\n"

    #ask user for current password (user will always be 'root')
    print("What is the password for the root user?")
    user_password = getpass.getpass()

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

    #declare two var to use later
    code_pairs = ""
    ip_addresses = ""

    #open ip file
    #start loop until ip file has no more lines
    #========================
    try:
        with open("printer-IPs.txt", "r") as ip_file:
            print("Found IP file.")
            lines = ip_file.readlines()
            for line in lines:
                line = line.rstrip('\n')
                #check each line for correct ip address format
                if(Validate_IP(line)):
                    #check ping the ip address
                    if(os.system(f"ping -n 1 {line}") == 0):
                        #check attempt ssh with default usr and pw 'telnet $ssh-host $ssh-port'
                        try:
                            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                            test_socket.connect(line, 22)
                            ip_addresses += (line)
                        except Exception:
                            log_text += f"!!!!IP {line} ssh error!!!!\n"
                        test_socket.close()
                    else:
                        log_text += f"!!!!IP {line} is unreachable!!!!\n"
                else:
                    log_text += f"!!!!Invalid ip {line} found!!!!\n"
            print(ip_addresses)
    except IOError:
        print("File named 'printer-IPs.txt' not found.")
        exit()     
    #=======================

    #open code file
    #start loop until ip_address has no more indexes
    #=======================
    #-----if there are no more codes -----> append log file('ip_address' has no code pair) --------> continue
    #temp_code = current line of code file
    #check the code to make sure its not blank
    #-----if blank -----> continue
    #grab the TS code and token ---> ts_code, download_token
    #default_terminal_line_filled = default_terminal_line + (find replace the correct fields)
    #temp_tuple = (ip_address, default_terminal_line_filled)
    #place the code pairs with ip addresses in a list  'code_pairs.append(temp_tuple)'
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
    with open("log.txt", "w") as log_file:
         log_file.write(log_text)


if __name__ == "__main__":
    main()