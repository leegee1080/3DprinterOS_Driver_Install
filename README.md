# 3DprinterOS_Driver_Install

Script to automate the install of drivers on systems with recent firmware updates.

1. Open IPlist and DriverCodeList
2. Record to ip_list and driver_code_list.
3. Check each line of the lists and add lines to log file when codes/ips are bad.
4. ssh each ip then login, paste each code, make a log line, and move on to the next IP
5. save log lines to file
6. exit script


Instructions for use:
1. Fill the two text files in the 'userfiles' folder.
2. Run __main__.py
