!#/usr/bin/env python3
'''
Created on Jun 30, 2016

@author: sbartholomew
'''
from socket import*
import sys
import select
from _socket import AF_INET


class Make_server():
    def __init__(self, port):
        self.address = ('localhost', port)
        self.server_socket = socket(AF_INET, SOCK_DGRAM)
        self.server_socket.bind(address)
        self.hex_ret = None
        self.recv_data = None
        self.quit_flag = False
    
    def listen(self):
        while(not self.quit_flag):
            self.recv_data, addr = server_socket.recvfrom(256)
            #TODO if recv_data is a valid string -- do whatever
            #server_socket.sendto(results, addr)
            #
        self.server_socket.close()
    
    def parse_input(self):
        re1='([f,d])'    # f or d 
        re2='(\\d+)'    # Integer Number 1

        rg = re.compile(re1+re2,re.IGNORECASE|re.DOTALL)
        m = rg.search(self.recv_data)
        if m:
            to_call = {'f':f_number, 'F': f_number, 'd':d_number, 'D':d_number}
            to_call[m.group(1)](m.group(2))
        
        else:
            re1='(m)'
            re2='(?:[M,D,C,L,X,V,I][M,D,C,L,X,V,I]+)' 
        
            rg = re.compile(re1+re2,re.IGNORECASE|re.DOTALL)
            m = rg.search(self.recv_data)
            if m:
                r_number(m.group(2))
        
        
    def f_number(self, number):
        #given a decimal n 0 -300 return the nth fibonacci number in hex
        
    def d_number(self):
        #given a decimal number 0 - 10^30 (inclusive) return number in hex
    
    def r_number(self):
        #given a roman numeral between I and MMMM (inclusive) return number in hex
    
    def  
    
    
def main():
    #get UID 
    
    # make three threads as servers  
        # ports UID, UID + 1000, UID + 2000

if __name__ == '__main__':
    main()
