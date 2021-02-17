#start log file (create new file), append date and time

#ask user for current password (user will always be 'root')
#ask user if they would like to batch change pw for root user
#ask user if they would like to run custom code
#if yes then ask if user would like to run custom code with TScode and token filled in.

#otherwise run default code with TScode and token filled in.
#default_terminal_line = (TS={!TSCODEVAR!} && CURTS="$(date +%s)" && if [ $((TS-60)) -gt $((CURTS)) ]; then date --set="@$TS"; fi; cd /root/ && rm -f cacert.pem && curl -fsSOL https://curl.se/ca/cacert.pem && export CURL_CA_BUNDLE=/root/cacert.pem || if [ -f /usr/lib/python3/dist-packages/certifi/cacert.pem ]; then export CURL_CA_BUNDLE=/usr/lib/python3/dist-packages/certifi/cacert.pem; fi; curl -f -sS 'https://duke.3dprinteros.com/noauth/download_u3_installation?dtoken={!TOKENVAR!}' | bash)
#default_terminal_line_filled = ""
#code_pairs = ""

#open ip file
#start loop until ip file has no more lines
#========================
#temp_ip = current line of ip file
#check each line for correct ip address format
#check ping the ip address
#check attempt ssh with default usr and pw 'telnet $ssh-host $ssh-port'
#-----if the ip address is not valid/failed ping/failed ssh--->append ('ip_address' is not valid/offline/not in dev mode) to log----------> then continue
#-----else ----> grab the ip address --> ip_address.append(temp_ip)
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