# -*- coding:utf-8 -*-
# spider exploits-db.com 0day of today or a few days ago
__author__="Wester"

import requests
from bs4 import BeautifulSoup
import sys, getopt
from termcolor import colored
import time
import argparse


def get_vuls(date,type):

    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, compress',
               'Accept-Language': 'en-us;q=0.5,en;q=0.3',
               'Cache-Control': 'max-age=0',
               'Connection': 'keep-alive',
               'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
    }
   
    urls = {
            'web': 'https://www.exploit-db.com/webapps',
            'rce': 'https://www.exploit-db.com/remote',
            'local': 'https://www.exploit-db.com/local',
           'dos':'https://www.exploit-db.com/dos'
         }

    baseUrl = urls.get(type)
    if baseUrl == None:
        baseUrl = 'https://www.exploit-db.com/webapps'
        print 'use default type:web'
    #print baseUrl
    source = requests.get(baseUrl,headers=headers)
  
    # parser html
    soup = BeautifulSoup(source.text,"html.parser")

    trs = soup.table.tbody.find_all("tr")

    #print len(trs)

    vuls = [[] for i in range(len(trs))]

    i = 0

    # test
    #print trs[0].find('td', {'class': 'date'})
    #print trs[0].find('td', {'class': 'description'}).a.get('href')
    # test


    while (i < len(trs)):
        vuls[i].append(trs[i].find('td', {'class': 'date'}).string)
        vuls[i].append(trs[i].find('td', {'class': 'description'}).a.get('href'))
        vuls[i].append((trs[i].find('td', {'class': 'description'}).a.string).strip())
        vuls[i].append((trs[i].find('td', {'class': 'author'}).a.string).strip())
        i+=1

    print '\nThe date that being searched:'+colored(date,'green')
    print 'The type that you choice:'+colored(type,'green')
    print "-" * 80
    count = 0
    for m in vuls:
            if m[0] == date:
                count+=1
                print colored('vul date: ','green')+m[0]
                print colored('vul link: ','red')+m[1]
                print colored('vul title: ','cyan')+m[2]
                print colored('vul author: ','green')+m[3]
                print "-" * 80
    if count == 0:
        print 'Sorry,no result for your search conditionals'
    else:
        print 'Aha,I have found '+colored(str(count),'red')+' vul for your search conditionals'


def main():
   today = str(time.strftime("%Y-%m-%d", time.localtime()))
   parser = argparse.ArgumentParser()
   parser.add_argument('-d',"-date","--date",
                       help="date fomat example:2016-12-29,Default(empty) is today,But not more than 7 days ago！！！",
                        action = 'store',
                        dest ='date',
                        default =today,
                         type=str)
   parser.add_argument('-t',"-type","--type",
                       help = '''
                       type format (default web):
                            web => Web Application Exploits;
                            rce => Remote Code Execution Exploits;
                            local => Local and Privilege Escalation Exploits;
                            dos => Denial of Service and PoC Exploits
                              ''',
                        action = 'store',
                        dest ='type',
                        default="web",
                        type=str) 

   args = parser.parse_args()
   d = args.date
   t = args.type     
   get_vuls(d,t)

if __name__ == "__main__":
    main()

