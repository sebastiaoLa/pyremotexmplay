#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author: Daddiego Lucas

"""
import sys,os

def check_os():
    if (os.name != "nt"):
        print("Sorry, this server only works in Windows")
        sys.exit()
    

def main():
    check_os()    
    from server import Server
    print("XMPlay Remote Control Server")
    print("")
    ip = raw_input("Write the listening address(0.0.0.0 by default): ")
    if (ip == ""):
        ip = "0.0.0.0"
        
    port = raw_input("Write the listening port(9999 by default): ")
    if (port == ""):
        port = "9999"
        
    port = int(port)
    
    threadServer = Server(1,(ip,port))
    threadServer.daemon = True
    threadServer.start()
    print("Server Started!")
    while (raw_input("Write exit to quit: ") != "exit"):
        os.system("cls")
        pass
    
    threadServer.stop_server()
    sys.exit()

#It's down there because main has to be defined before.
if (__name__ == "__main__"):
    main()
