#!/usr/bin/env python3
import re
import sys
import requests
"""
#****************************************************************#
#           Author        - pyCity                               #
#           Date          - 6/21/2019                            #
#           Version       - 0.1.dev                              #
#                                                                #
#           Usage         - python3 proxypy.py                   #
#                                                                #
#           Goal          - Obtain proxies on demand             #
#                                                                #
#           Description   - Quick script to scrape               #
#                           https://free-proxy-list.net/         #
#                           for viable proxies                   #
#                                                                #
#****************************************************************#
"""


def usage():
    print("ProxyPy accepts one command line argument for the "
          "number of proxies to scrape as well as user input if no args "
          "are supplied\npython pscrape.py 5 (Scrape 5 proxies)"
          " || python pscrape.py (Get user input)\n")


def make_request():
    """
    Function to pull source code from free-proxy-list.net.

    :returns response:  Array of data containing proxy information
    """

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 '
                      '(KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Encoding': 'gzip',
        'Content-Type': 'text/html; charset=utf-8',
    }

    # Make a request and store text in response variable
    response = requests.get('https://free-proxy-list.net/', headers=headers).text

    # Regex to extract port and ip from the response source.
    return re.findall(r"<tr><td>[^<]*</td><td>[^<]*</td><td>[^<]*</td><td"
                      r" class='hm'>[^<]*</td><td>[^<]*</td><td class='hm'>[^<]*</td><td "
                      r"class='hx'>[^<]*</td><td class='hm'>[^<]*</td></tr>", response)


def parse_request(number):
    """
    Function that calls make_request and parses the data returned.

    :param number:     Number of proxies to download
    :returns proxies:  Array of parsed proxies
    """

    proxies = []

    if number > 300:
        number = 300

    proxy = make_request()[:number]
    for match in proxy:
        result = match.split('</td>')  # Format proxy IP by splitting off '</td>'
        ip_address = result[0].strip('<tr><td>')  # Strip '<tr><td>' from first element
        port = result[1].strip('</td>')  # Format proxy port by stripping '</td>'

        # Slice fifth index of result list, strip ''<td class='hx'>'', check if it is equal to 'yes'
        if result[6].strip('<td class=\'hx\'>') == 'yes':
            protocol = 'https'
        else:
            protocol = 'http'
        proxies.append(protocol + '://' + ip_address + ':' + port)

    return proxies


def main():
    print("\033[94mWelcome to ProxyPy\n")

    # Verify the correct number of args are entered
    if len(sys.argv) == 2:
        proxies = parse_request(int(sys.argv[1]))
    elif len(sys.argv) != 1:
        exit(usage())

    else:
        while True:
            try:
                answer = int(input("Enter the number of proxies to scrape (300 max): \n"))
            except ValueError:
                print("Please enter an integer")
                continue
            else:
                proxies = parse_request(answer)
                break

    # Print proxies
    for proxy in proxies:
        print("\033[92m", proxy)


if __name__ == '__main__':
    main()
