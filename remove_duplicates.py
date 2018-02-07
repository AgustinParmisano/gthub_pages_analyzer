user_array = []
filename = "black_backup.txt"

try:
    with open("black.txt", 'r+') as f:
        lineList = f.readlines()
        users = list(set(lineList))

        with open("black_backup.txt", "a") as myfile:
            for user in users:
                if user != " " and user != "\n" and (len(user) > 1):
                    print "[+] Writing " + str(user) + " into file " + str(filename)
                    myfile.write(user)

except Exception as e:
    print "[-] Cant open file for reading " + filename
    print "Exception " + str(e)
