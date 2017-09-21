#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
@Author: Daddiego Lucas

"""
import sys,os

def main():
    from server import Server
    print("XMPlay Remote Control Server")
    print("")
    threadServer = Server()
    threadServer.start()
    print("Server Started!")
    print("write exit anytime to exit")
    while (raw_input() != "exit"):
        pass
    
    threadServer.para()
    sys.exit()

#It's down there because main has to be defined before.
if (__name__ == "__main__"):
    main()
