# -*- coding:utf-8 -*-
# spider exploits-db.com 0day of today or a few days ago
__author__="Wester"

import requests
from bs4 import BeautifulSoup
import sys, getopt
from termcolor import colored
import time


def get_vuls(date,type):

    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, compress',
               'Accept-Language': 'en-us;q=0.5,en;q=0.3',
               'Cache-Control': 'max-age=0',
               'Connection': 'keep-alive',
               'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
    }
    s = requests.Session()
    s.headers.update(headers)

    baseUrl ='https://www.exploit-db.com/'

    if type == 'web':
        source = s.get(baseUrl+'webapps')
    elif type == 'rce':
        source = s.get(baseUrl+'remote')
    elif type == 'local':
        source = s.get(baseUrl+'local')
    elif type == 'dos':
        source = s.get(baseUrl+'dos')

    #print web.text

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


def main(argv):
   date = ''
   type = ''
   try:
      opts,args = getopt.getopt(argv,"hd:t:")
      #print len(opts)
   except getopt.GetoptError:
      print '''
            Usage: python 0daySpider_expdb.py -d <date> -t <type>

            date fomat example:2016-12-29,Default(empty) is today,But not more than 7 days ago！！！

            type format (default web):
            web => Web Application Exploits;
            rce => Remote Code Execution Exploits;
            local => Local and Privilege Escalation Exploits;
            dos => Denial of Service and PoC Exploits

            example command: python 0daySpider_expdb.py -d 2016-12-29 -t web

            Remind again:Please don't set date too earily,because I just request one page vuls!!

            '''
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print '''
            Usage: python 0daySpider_expdb.py -d <date> -t <type>

            date fomat example:2016-12-29,Default(empty) is today,But not more than 7 days ago！！！

            type format:
            web => Web Application Exploits;
            rce => Remote Code Execution Exploits;
            local => Local and Privilege Escalation Exploits;
            dos => Denial of Service and PoC Exploits

            example command: python 0daySpider_expdb.py -d 2016-12-29 -t web

            Remind again:Please don't set date too earily,because I just request one page vuls!!

            '''
         sys.exit()
      elif opt == '-d':
         date = arg
      elif opt == '-t':
         type = arg
   if date == '' or date == '-t' or date == '-d':
       date = str(time.strftime("%Y-%m-%d", time.localtime()))
       print '\nuse default date:today'
   if type == '' or type == '-t' or type == '-d':
       type = 'web'
       print 'use default type:web'
   get_vuls(date,type)

if __name__ == "__main__":
    #print sys.argv[1:]
    if len(sys.argv[1:]) < 2 :
      print '''
            Usage: python 0daySpider_expdb.py -d <date> -t <type>

            date fomat example:2016-12-29,Default(empty) is today,But not more than 7 days ago！！！

            type format (default web):
            web => Web Application Exploits;
            rce => Remote Code Execution Exploits;
            local => Local and Privilege Escalation Exploits;
            dos => Denial of Service and PoC Exploits

            example command: python 0daySpider_expdb.py -d 2016-12-29 -t web

            Remind again:Please don't set date too earily,because I just request one page vuls!!

            '''
      sys.exit(2)
    else:
        main(sys.argv[1:])

