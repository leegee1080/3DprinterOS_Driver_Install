import datetime, getpass, re, os, socket

version = 0.9

print(f"\n\nYou are using version {version} of the 3DprinterOS Driver Install Script by Mitchell Greene.")
usage_warning = input("\tBy pressing 'enter' you accept that useage of this program is at your own risk.\n\tIf you do not accept these terms, close this program by pressing 'CTRL-C'.\n\n")


try:
    import paramiko
except ModuleNotFoundError:
    print("Module paramiko not installed...attemping to install.")
    os.system("python -m pip install paramiko")

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

def Command_Constructor(code_template, first_code, second_code):
    command = code_template
    command= re.sub("!TSCODE!", first_code, command)
    command= re.sub("!TOKEN!", second_code, command)
    return command

def Check_3dPos_Client_Port(ip_to_check):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((ip_to_check, 8008))
    if result == 0:
        print("3dPOS is running.")
        sock.close()
        return f"3dPOS on IP({ip_to_check}) is running.\n"
    else:
        print("3dPOS is not running.")
        sock.close()
        return f"!!!!3dPOS on IP({ip_to_check}) is unreachable!!!!\n"
    
def End_Script(new_log_text):
    current_time = datetime.datetime.now()
    log_folder = r"logs\log_"
    print(f"Exiting script and writing log file to {log_folder}...")
    with open(f"{log_folder}{current_time.strftime('%H-%M-%S_%d-%Y')}.txt", "w") as log_file:
         log_file.write(new_log_text)
    exit



def main():
    use_default_codes = False
    driver_codes = []
    ip_addresses = []
    code_pairs = []
    template_code = ""

    #declare the list that will have the ip addresses combined with the code pairs
    complete_pairs = []

    current_time = datetime.datetime.now()
    #start log file (create new file), append date and time
    log_text = f"----3DprinterOS Driver Install----\nLog started on {current_time.strftime('%H:%M:%S on %A, %B the %dth, %Y')}\n"

    #ask user for current password (user will always be 'root')
    print("What is the password for the root user?")
    user_password = getpass.getpass()

# ====================================================
    #OPTIONAL!!
    #ask user if they would like to batch change pw for root user
    #ask user if they would like to run custom code
    while(True):
        playeranswer = input("What would you like to do? \n (Type 'pw' change password, 'rc' for run custom code, or 'di' 3dPOS driver install.)")
        if(playeranswer == "pw"):
            print("Enter the password you would like to apply.")
            new_user_password1 = getpass.getpass()
            print("Re-Enter the password you would like to apply.")
            new_user_password2 = getpass.getpass()
            if(new_user_password1 == new_user_password2):
                new_user_password = new_user_password1
                template_code = "passwd"
                break
            else:
                print("The passwords you entered do not match. Returning to main menu.")
                continue
        if(playeranswer == "rc"):
            template_code = input("What is the code you would like to use?")
            print(f"The code to be used on each IP in the 'ip_addresses' file is: {template_code}")
            input("Press enter to confirm.")
            break
        if(playeranswer == "di"):
            try:
                default_code_file_folder = r"src\default-code.txt"
                with open(default_code_file_folder, "r") as default_code_file:
                    print("Found default code file.")
                    template_code = default_code_file.read()
                    use_default_codes = True
            except IOError:
                print("File named 'default-code.txt' not found or has been changed.")
                exit()
            break
        else:
            print("Enter a valid response.")
    #overwrite template_code

#===================================================

    #open ip file
    #start loop until ip file has no more lines
    print("-------Validating IPs.-------")
    try:
        with open(r"userfiles\printer-IPs.txt", "r") as ip_file:
            print("Found IP file.")      
    except IOError:
        print("File named 'printer-IPs.txt' not found.")
        End_Script(log_text)

    with open(r"userfiles\printer-IPs.txt", "r") as ip_file:
        lines = ip_file.readlines()
        for line in lines:
            line = line.rstrip('\n')
            print(f"Testing: ({line}).")
            #check each line for correct ip address format
            if(Validate_IP(line)):
                #check ping the ip address
                if(os.system(f"ping -n 1 {line}") == 0):
                    #check attempt ssh with default usr and pw 'telnet $ssh-host $ssh-port'
                    new_client = paramiko.SSHClient()
                    new_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
                    try:
                        new_client.connect(line, username='root', password=user_password)
                        new_client.close()
                        ip_addresses.append(line)
                    except (TimeoutError, paramiko.ssh_exception.AuthenticationException, paramiko.ssh_exception.NoValidConnectionsError) as exceptions:
                        log_text += f"!!!!SSH error: {exceptions} on IP: {line}!!!!\n"
                else:
                    log_text += f"!!!!IP {line} is unreachable!!!!\n"
            else:
                log_text += f"!!!!Invalid ip {line} found!!!!\n"
    print("-------Finished validating IPs.-------")

    if(ip_addresses == 0):
        print("There are no usuable IP addresses.")
        End_Script(log_text)

    #open code file
    try:
        with open(r"userfiles\driver-codes.txt", "r+") as codes_file:
            print("Found driver-codes file.")
            lines = codes_file.readlines()
            for line in lines:
                line = line.rstrip('\n')
                if(line != "" and line != None):
                    driver_codes.append(line)
            codes_file.seek(0, 0)
            codes_file.write("")
            codes_file.truncate(0)
    except IOError:
        print("File named 'driver-codes.txt' not found.")
        End_Script(log_text)

    if(use_default_codes):
        #create the code pair tuples
        print("-------Creating code pairs.-------")
        for code in driver_codes:
            print(f"Combining: {code}.")
            if(Return_TS(code) != "" and Return_Token(code) != ""):
                code_pairs.append((Return_TS(code), Return_Token(code)))
            else:
                continue

        #combine all the vars together and check if there is enough codes to go around
        for index, ip in enumerate(ip_addresses):
            print(f"Combining: ({ip}).")
            try:
                temp_tuple = code_pairs[index]
                complete_pairs.append((ip,temp_tuple[0],temp_tuple[1]))
            except IndexError:
                log_text += f"!!!!{ip} does not have a code pair!!!!\n"
    else:
        for ip in ip_addresses:
            print(f"Combining: ({ip}).")
            complete_pairs.append((ip,template_code,None))
    print("-------Finished creating code pairs.-------")


    #start loop until there are no more items in complete_pairs
    if(len(complete_pairs) > 0):
        print("-------Execute code pairs.-------")
        for pair in complete_pairs:
            print(f"Executing: {pair}.")
            new_client = paramiko.SSHClient()
            new_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            try:
                new_client.connect(pair[0], port=22, username='root', password=user_password)

                if(use_default_codes):
                    constructed_command = Command_Constructor(template_code, pair[1], pair[2])
                else:
                    constructed_command = template_code

                print(f"Constructed code to execute on IP {pair[0]}: {constructed_command}")
                log_text += f"Constructed code to execute on IP {pair[0]}: {constructed_command}\n"
                ssh_stdin, ssh_stdout, ssh_stderr = new_client.exec_command(constructed_command)

                output = ssh_stdout.read() #Reading output of the executed command
                print("output:", output) 
                log_text += f"---constructed code output-----> {output}\n"

                error = ssh_stderr.read() #Reading the error stream of the executed command
                print("err", error, len(error))
                log_text += f"---constructed code error-----> {error, len(error)}\n\n"

                new_client.close()
            except (TimeoutError, paramiko.ssh_exception.AuthenticationException) as exceptions:
                log_text += f"!!!!SSH error on the code ex. stage: {exceptions} on IP: {pair[0]}!!!!\n"
            continue
        print("-------Finished execute code pairs.-------")
    else:
        print("No code pairs to execute.")
        log_text += "No code pairs to execute.\n"

    for ip in ip_addresses:
        log_text += Check_3dPos_Client_Port(ip)

    #if there are unused driver codes ----> append them to a file called 'unused-codes'
    #append log with time stamp and number of codes ran
    End_Script(log_text)
    return


if __name__ == "__main__":
    main()