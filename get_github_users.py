import os
import time

user_array = []
filename = "black.txt"

try:
    with open(filename, 'r+') as f:
        lineList = f.readlines()
        last_index = len(lineList) + 1 #int(lineList[-1].split(" ")[2].split("\n")[0])
        print "[!] Starting from last index: " + str(last_index)

    try:
        with open(filename, "a") as myfile:

            for i in range(last_index,10000000,30):
                request = 'curl -i https://api.github.com/users' + '\?since\=' + str(i) + '| grep "login" | cut -d" " -f6 | cut -d"," -f1'
                users = os.popen(str(request)).read()

                try:
                    users = users.replace('"', '')
                    users = users.split("\n")
                    time.sleep(1)
                    if users == ['']:
                        print "\n[-] GitHub API Max ussage reached, please wait and try again later . . ."
                        print "\n[!] Leaving at index: " + str(i)
                        break
                    else:
                        for user in users:
                            if user != " " and user != "\n" and (len(user) > 1):
                                user_array.append(user)

                        user_array = list(set(user_array))
                        for user in user_array:
                            print "[+] Writing " + str(user) + " into file " + str(filename)
                            myfile.write(user + "\n")

                except Exception as e:
                    print "[-] Cant analize users"
                    print "Exception " + str(e)

    except Exception as e:
        print "[-] Cant open file for appending " + filename
        print "Exception " + str(e)

except Exception as e:
    print "[-] Cant open file for reading " + filename
    print "Exception " + str(e)
