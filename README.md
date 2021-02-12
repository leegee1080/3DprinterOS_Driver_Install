# 3DprinterOS_Driver_Install

Script to automate the install of drivers on systems with recent firmware updates.

1. Open IPlist and DriverCodeList
2. Record to ip_list and driver_code_list.
3. Check each line of the lists and add lines to log file when codes/ips are bad.
4. ssh each ip then login, paste each code, make a log line, and move on to the next IP
5. save log lines to file
6. exit script

Options

1. Input to change p.w. of each root user
2. Separate input to run a custom line in the ssh before the driver code
3. Option to chose which ip the custom line is run on.

dont forget" pxssh for ssh
