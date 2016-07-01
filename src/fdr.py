#!#/usr/bin/env python3
'''
Created on Jun 30, 2016

@author: sbartholomew
'''
from socket import*
import os
import pwd
import threading
import re


class Make_server(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.__address = ('localhost', port)
        self.__server_socket = socket(AF_INET, SOCK_DGRAM)
        self.__server_socket.bind(self.__address)
        self.__server_socket.setblocking(False)
        self.__rValue = None
        self.__recv_data = None
        self.__quit_flag = threading.Event()
        self.daemon = True

    def stop(self):
        self.__quit_flag.set()

    def run(self):
        while(not self.__quit_flag.is_set()):
            try:
                self.__recv_data, addr = self.__server_socket.recvfrom(256)
                self.__recv_data = str(self.__recv_data, 'utf-8')
    #            TODO if recv_data is a valid string -- do whatever
                self.parse_input()
                if self.__rValue:
                    self.__rValue = str(hex(self.__rValue))
                    self.__server_socket.sendto(
                        bytes(self.__rValue + '\0', 'utf-8'), addr)
                    self.__rValue = None
            except BlockingIOError:
                """ no data yet """
        self.__server_socket.close()

    def parse_input(self):
        re1 = '([f,d])'    # f or d
        re2 = '(\\d+)'    # Integer Number 1

        rg = re.compile(re1+re2, re.IGNORECASE | re.DOTALL)
        m = rg.search(self.__recv_data)
        if m:
            if m.group(1).lower() == 'f':
                self.f_number(int(m.group(2)))
            else:
                self.d_number(int(m.group(2)))

        else:  # http://docutils.sourceforge.net/docutils/utils/roman.py
            re1 = '(r)'
            re2 = '(M{0,4})'            # thousands - 0 to 4 M's
            re3 = '(CM|CD|D?C{0,4})'    # hundreds- 900 (CM) 400 (CD) 0-300 etc
            re4 = '(XC|XL|L?X{0,4})'    # tens - 90 (XC), 40 (XL), 0-30 etc
            re5 = '(IX|IV|V?I{0,4})'    # ones - 9 (IX), 4 (IV), 0-3 etc
#            this will give different results than Liam wants because he does
#            Roman numerals wrong.
            rg = re.compile(re1+re2+re3+re4+re5, re.IGNORECASE | re.DOTALL)
            m = rg.search(self.__recv_data)
            if m:
                self.r_number(m.group(2)+m.group(3)+m.group(4)+m.group(5))
        # else i don't care because its not a valid input

# given a decimal n 0 -300 return the nth Fibonacci number in hex
    def f_number(self, number):
        if number >= 0 and number <= 300:
            cur, count, prev = 0, 0, 1
            while count < number:
                prev, cur = cur, cur + prev
                count += 1
            self.__rValue = cur
#               it's math -- sometimes its ugly

# given a decimal number 0 - 10^30 ( inclusive ) return number in hex
    def d_number(self, number):
        if number >= 0 and number <= 10**30:
            self.__rValue = number

# given a Roman numeral between I and MMMM (inclusive) return number in hex
    def r_number(self, number):

        # from http://docutils.sourceforge.net/docutils/utils/roman.py
        romanNumeralMap = (('M',  1000), ('m', 1000),
                           ('CM', 900), ('cm', 900),
                           ('D',  500), ('d', 500),
                           ('CD', 400), ('cd', 400),
                           ('C',  100), ('c', 100),
                           ('XC', 90),  ('xc', 90),
                           ('L',  50),  ('l', 50),
                           ('XL', 40),  ('xl', 40),
                           ('X',  10),  ('x', 10),
                           ('IX', 9),   ('ix', 9),
                           ('V',  5),   ('v', 5),
                           ('IV', 4),   ('iv', 4),
                           ('I',  1),   ('i', 1))

        result = 0
        index = 0
        for numeral, integer in romanNumeralMap:
            while number[index:index+len(numeral)] == numeral:
                result += integer
                index += len(numeral)
        self.__rValue = result


def main():

    UID = pwd.getpwuid(os.getuid()).pw_uid

    serv1 = Make_server(UID)
    serv2 = Make_server(UID + 1000)
    serv3 = Make_server(UID + 2000)

    serv1.start()
    serv2.start()
    serv3.start()

    print("Server running on ports", UID, UID + 1000, UID + 2000)
    stop = input("<quit> for QUIT")

    if stop == 'quit':
        serv1.stop()
        serv2.stop()
        serv3.stop()
        serv1.join(timeout=1)
        serv2.join(timeout=1)
        serv3.join(timeout=1)

if __name__ == '__main__':
    main()
