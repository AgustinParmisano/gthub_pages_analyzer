import os

resultfile = "zapresultfile.txt"
urlsfile = "vulnerablesites.txt"

try:
    with open(urlsfile, 'r+') as f:
        lineList = f.readlines()

        print "[!] Starting analisis for URLS in file: " + str(urlsfile)

        for url in lineList:

            try:
                url = url.split(" ")[1]
                url = url.rstrip()
                request = 'zap-cli --zap-path /usr/share/zaproxy --api-key 12345 quick-scan -s xss,sqli --spider -r  --self-contained -o "-config api.key=12345" -s xss ' + str(url)

                print "[!] Analyzing url " + str(url) + " with Owasp ZAP Cli for common vulnerabilities."
                print "This may take a few minutes. Please wait . . ."

                result = os.popen(str(request)).read()

                print "[+] Analisis completed. Writing results into " + str(resultfile)

                try:

                    with open(resultfile, "a") as myfile:
                        myfile.write("Owasp ZAP Cli analisis for url: " + str(url) + "\n")
                        myfile.write(str(result) + "\n")
                        myfile.write("+--------------------------------------------------------------+ \n")
                        myfile.write("\n")

                except Exception as e:
                    print "[-] Cant open file for appending " + resultfile
                    print "Exception " + str(e)

            except Exception as e:
                print "[-] Cant perform analisis with Owasp ZAP Cli "
                print "Exception " + str(e)

except Exception as e:
    print "[-] Cant open file for reading " + urlsfile
    print "Exception " + str(e)
