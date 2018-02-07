import urllib2
import threading
import Queue
import urllib
import optparse

def build_wordlist(wordlist_file):
    # read in the wordlist_file
    fd = open(wordlist_file,"rb")
    raw_words = fd.readlines()
    fd.close()

    found_resume = False
    words = Queue.Queue()

    for word in raw_words:
        word = word.rstrip()

        if resume is not None:

            if found_resume:
                words.put(word)
            else:
                if word == resume:
                    found_resume = True
                    print "Resuming wordlist from: %s" % resume
        else:
            words.put(word)

    return words

def dir_bruter(word_queue, target_url, user_agent, extensions=None):

    while not word_queue.empty():
        attempt = word_queue.get()

        attempt_list = []

        # check to see if there is a file extension; if not,
        # it's a directory path we're bruting
        if "." not in attempt:
            attempt_list.append("/%s/" % attempt)
        else:
            attempt_list.append("/%s" % attempt)

        # if we want to bruteforce extensions
        if extensions:
            for extension in extensions:
                attempt_list.append("/%s%s" % (attempt,extension))

        # iterate over our list of attemps
        for brute in attempt_list:

            url = "%s%s" % (target_url, urllib.quote(brute))

            try:
                headers = {}
                headers["User-Agent"] = user_agent
                r = urllib2.Request(url,headers=headers)
                response = urllib2.urlopen(r)

                if len(response.read()):
                    print "[%d] => %s" % (response.code,url)

            except urllib2.URLError,e:
                if hasattr(e,'code') and e.code != 404:
                    print "!!! %d => %s" % (e.code,url)

                pass
"""
threads = 50 #options
target_url = "http://testphp.vulnweb.com" #options
wordlist_file = "/tmp/all.txt" #from SVNDigger options
user_agent = "Mozilla" #options
"""

resume = None

def main():
    parser = optparse.OptionParser('[-] Usage%prog '+ '-t <target url> -f <wordlist file> -a <user agent[moz OR chr]> [-T <threads>] [-e <extensions list file>]')
    parser.add_option('-t', dest='target_url', type='string', help='specify target url')
    parser.add_option('-f', dest='wordlist_file', type='string', help='specify wordlist file for brute force dirs attempts')
    parser.add_option('-a', dest='user_agent', type='string', help='specify user agent (moz for Mozilla, chr for Chrome)')
    parser.add_option('-T', dest='threads', type='int', help='specify number of threads (f.e. 50)')
    parser.add_option('-e', dest='extensions', type='string', help='specify extensions list file')
    (options, args) = parser.parse_args()

    if (options.target_url == None) | (options.wordlist_file == None):
        print parser.usage
        exit(0)

    wordlist_file = options.wordlist_file
    target_url = options.target_url

    if options.user_agent == "moz" or options.user_agent == None:
        user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0"
    elif options.user_agent == "chr":
        print "You use Chrome? Try Firefox"

    threads = options.threads or 50

    extensions = options.extensions or [".php",".bak",".orig",".inc"] #options

    word_queue = build_wordlist(wordlist_file)

    for i in range(threads):
        t = threading.Thread(target=dir_bruter,args=(word_queue,target_url,user_agent,extensions,))
        t.start()

if __name__ == '__main__':
    main()
