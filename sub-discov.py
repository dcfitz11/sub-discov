import ssl
import requests
import time
from requests_html import HTMLSession
import pyfiglet
from colorama import *
init(autoreset=True)

# COLOR VARIABLES:
reset = Fore.RESET
red = Fore.RED
yellow = Fore.YELLOW
green = Fore.GREEN
magenta = Fore.MAGENTA


class Banner:
    ascii_banner = pyfiglet.figlet_format("SUB-DISCOV")
    print(yellow + ascii_banner)
    print("\tA subdoman brute forcing tool")


class ValidURL:
    """Validate that the URL is reachable"""
    def __init__(self, url):
        self.url = url
        self.session = HTMLSession()
        self.r = requests.get(self.url)
        self.val_url()

    def val_url(self):
        if len(self.url) == 0:
            print("\n{0}No web page was entered.".format(red))

        else:
            try:
                print(yellow + "\n[+] Attempting to establish connection to " + self.url + "...")
                self.r = self.session.get(self.url)
                if self.r.status_code == 200:
                    print(yellow + "\t[-]" + reset + "Connection Successful")
                    print(yellow + "\t[-]" + reset + "Connected to " + self.url + " on " + time.ctime())
                else:
                    print("\t[-]Connection to " + self.url + " received a status code "
                          "of " + red + str(self.r.status_code))
                    exit()
            except (ConnectionError, requests.exceptions.ConnectionError):
                print(self.r.status_code)
                print("\n" + red + "Failed to establish a connection to " + self.url)
                exit()


class SubFuzz:
    """Brute-force subdomains"""
    def __init__(self, url):
        self.url = url
        self.r = requests.get(self.url)
        self.sub_domains_list = []
        self.good_subs = []
        self.prep()

    def prep(self):
        with open("subdomains.txt", "r") as f_obj:
            for subdomain in f_obj. readlines():
                subdomain = subdomain.strip("\n")
                domain = self.url.replace("https://", "")
                self.sub_domains_list.append(subdomain + "." + domain)
        self.brute()

    def brute(self):
        http_codes = [200]
        print("\n{0}[+] Subdomain Discovery:".format(yellow))
        for line in self.sub_domains_list:
            link = "https://" + line

            try:
                r = requests.get(link)
                if r.status_code == 200 or r.status_code == 401:
                    print(line + " HTTP Status Code: " + green + str(r.status_code) + reset + " - " + str(len(r.content)) + " bytes")
                    self.good_subs.append(link)
                else:
                    print(line + " HTTP Status Code: " + red + str(r.status_code) + reset + " - " + str(len(r.content)) + " bytes")
            except KeyboardInterrupt:
                self.results()
            except(ssl.SSLCertVerificationError, requests.exceptions.SSLError, requests.exceptions.ConnectionError):
                pass
        self.results()

    def results(self):
        print("\n{0}[+] Results:".format(yellow))
        for line in self.good_subs:
            print(line)
        exit()


#  SUB-DOMAIN DISCOVERY TASKS
b = Banner()

target_url = input("\n{0}[+] Enter a URL: ".format(yellow))
ValidURL(target_url)
SubFuzz(target_url)
