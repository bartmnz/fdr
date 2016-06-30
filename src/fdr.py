#!#/usr/bin/env python3
'''
Created on Jun 30, 2016

@author: sbartholomew
'''
from socket import*
import sys
import select
from _socket import AF_INET
from cmath import sqrt
import os
import pwd
import threading
import re


class Make_server(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.address = ('localhost', port)
        self.server_socket = socket(AF_INET, SOCK_DGRAM)
        self.server_socket.bind(self.address)
        self.rValue = None
        self.recv_data = None
        self.quit_flag = False

    def stop(self):
        self.quit_flag = True
        
    def run(self):
        while(not self.quit_flag):
            self.recv_data, addr = self.server_socket.recvfrom(256)
#            TODO if recv_data is a valid string -- do whatever
            self.parse_input()
            if self.rvalue:
                self.server_socket.sendto(hex(self.rValue), addr)
                self.rValue = None
            #
        self.server_socket.close()

    def parse_input(self):
        re1 = '([f,d])'    # f or d
        re2 = '(\\d+)'    # Integer Number 1

        rg = re.compile(re1+re2, re.IGNORECASE | re.DOTALL)
        m = rg.search(self.recv_data)
        if m:
            to_call = {'f': "self.f_number", 'F': "self.f_number", 'd': "self.d_number", 'D': "self.d_number"}
            to_call[m.group(1)](m.group(2))

        else:
#            regular expression from http://docutils.sourceforge.net/docutils/utils/roman.py
            re1 = '(m)'
            re2 = 'M{0,4}'              # thousands - 0 to 4 M's
            re3 = '(CM|CD|D?C{0,3})'    # hundreds - 900 (CM), 400 (CD), 0-300 (0 to 3 C's),
                                        #     or 500-800 (D, followed by 0 to 3 C's)
            re4 = '(XC|XL|L?X{0,3})'    # tens - 90 (XC), 40 (XL), 0-30 (0 to 3 X's),
                                        #     or 50-80 (L, followed by 0 to 3 X's)
            re5 = '(IX|IV|V?I{0,3})'    # ones - 9 (IX), 4 (IV), 0-3 (0 to 3 I's),
                                        #     or 5-8 (V, followed by 0 to 3 I's)

            rg = re.compile(re1+re2+re3+re4+re5, re.IGNORECASE | re.DOTALL)
            m = rg.search(self.recv_data)
            if m:
                self.r_number(m.group(2))
        # else i don't care because its not a valid input

    def f_number(self, number):
# given a decimal n 0 -300 return the nth fibonacci number in hex
        if number >= 0 and number <= 300:
            self.rValue = ((1+sqrt(5))**number-(1-sqrt(5))**number)/(2**number*sqrt(5))
#               it's math -- sometimes its ugly

    def d_number(self, number):
        #given a decimal number 0 - 10^30 (inclusive) return number in hex
        if number >=0 and number <=10**30:
            self.rValue = number

    def r_number(self):
        #given a roman numeral between I and MMMM (inclusive) return number in hex
        # shamelessly taken from http://docutils.sourceforge.net/docutils/utils/roman.py
        romanNumeralMap = (('M',  1000),
                           ('CM', 900),
                           ('D',  500),
                           ('CD', 400),
                           ('C',  100),
                           ('XC', 90),
                           ('L',  50),
                           ('XL', 40),
                           ('X',  10),
                           ('IX', 9),
                           ('V',  5),
                           ('IV', 4),
                           ('I',  1))

        result = 0
        index = 0
        for numeral, integer in romanNumeralMap:
            while s[index:index+len(numeral)] == numeral:
                result += integer
                index += len(numeral)
        self.rValue = result


def main():
#get UID

    UID = pwd.getpwuid(os.getuid()).pw_uid
    print("UID is ", UID)

    serv1 = Make_server(UID)
    serv2 = Make_server(UID + 1000)
    serv3 = Make_server(UID + 2000)

    serv1.start()
    serv2.start()
    serv3.start()

    stop = input("Server running <quit> for QUIT")
    if stop == 'quit':
        serv1.stop()
        serv2.stop()
        serv3.stop()

    # make three threads as servers  
        # ports UID, UID + 1000, UID + 2000
    # listen for user input -- if quit -- interrupt threads set quit flag and join 

if __name__ == '__main__':
    main()
