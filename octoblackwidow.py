import os
import time
import urllib2
import urllib
import optparse

urls_array = []
usersfile = "black.txt"
urlsfile = "urlsfile.txt"
user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0"


def url_checker(target_url, user_agent, urls_array):
    print "[+] Analising user page with url: " + str(target_url)

    try:
        headers = {}
        headers["User-Agent"] = user_agent
        r = urllib2.Request(target_url,headers=headers)
        response = urllib2.urlopen(r)

        if len(response.read()):
            print "[%d] => %s" % (response.code,url)
            urls_array.append((response.code,url))

            try:
                with open(urlsfile, "a") as myfile:
                    urls_array = list(set(urls_array))

                    for urlcode in urls_array:
                        print "[+] Writing code " + str(urlcode[0]) + " for URL " + str(urlcode[1]) + " into file " + str(urlsfile)
                        myfile.write(str(urlcode[0]) + " " + str(urlcode[1]) + "\n")

            except Exception as e:
                print "[-] Cant open file for appending " + urlsfile
                print "Exception " + str(e)
                raise

    except urllib2.URLError,e:
        if hasattr(e,'code') and e.code != 404:
            print "!!! %d => %s" % (e.code,url)

        pass


try:
    with open(usersfile, 'r+') as f:
        lineList = f.readlines()

        for user_name in lineList:
            try:

                user_name = user_name.rstrip()
                url = 'http://' + str(user_name) + '.github.io'
                url_checker(url,user_agent,urls_array)

            except Exception as e:
                print "[-] Cant analize users"
                print "Exception " + str(e)


except Exception as e:
    print "[-] Cant open file for reading " + usersfile
    print "Exception " + str(e)
