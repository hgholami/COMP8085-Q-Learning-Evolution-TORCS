#!/usr/bin/env python
'''
Created on Apr 4, 2012

@author: lanquarden

Edited by: Ahmed Raafat
'''
import os
import sys
import argparse
import socket
import driver
import carState
import GetState2
import common



if __name__ == '__main__':
    pass

# Configure the argument parser
parser = argparse.ArgumentParser(description = 'Python client to connect to the TORCS SCRC server.')

parser.add_argument('--host', action='store', dest='host_ip', default='localhost',
                    help='Host IP address (default: localhost)')
parser.add_argument('--port', action='store', type=int, dest='host_port', default=3001,
                    help='Host port number (default: 3001)')
parser.add_argument('--id', action='store', dest='id', default='SCR',
                    help='Bot ID (default: SCR)')
parser.add_argument('--maxEpisodes', action='store', dest='max_episodes', type=int, default=1,
                    help='Maximum number of learning episodes (default: 1)')
parser.add_argument('--maxSteps', action='store', dest='max_steps', type=int, default=0,
                    help='Maximum number of steps (default: 0)')
parser.add_argument('--track', action='store', dest='track', default=None,
                    help='Name of the track')
parser.add_argument('--stage', action='store', dest='stage', type=int, default=3,
                    help='Stage (0 - Warm-Up, 1 - Qualifying, 2 - Race, 3 - Unknown)')
parser.add_argument('--individual', action='store', dest='individual', type=str, default=None,
                    help='individual of each qtable')
parser.add_argument('--v', action='store_true', dest='view', help='View current run in GUI')
parser.add_argument('--numElites', action='store', dest='numElites', type=int, default=1,
                    help='Give the number of elites we want')

arguments = parser.parse_args()

# Print summary
print ('Connecting to server host ip:', arguments.host_ip, '@ port:', arguments.host_port)
print ('Bot ID:', arguments.id)
print ('Maximum episodes:', arguments.max_episodes)
print ('Maximum steps:', arguments.max_steps)
print ('Track:', arguments.track)
print ('Stage:', arguments.stage)
print ('*********************************************')

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error as msg:
    print ('Could not make a socket.')
    sys.exit(-1)

# one second timeout
sock.settimeout(1.0)

shutdownClient = False
curEpisode = 0

verbose = False

#d = driver.Driver(arguments.stage)
d = driver.Driver(arguments.stage, arguments.individual)

while not shutdownClient:
    while True:
        print ('Sending id to server: ', arguments.id)
        buf = arguments.id + d.init()
        print ('Sending init string to server:', buf)
        #print("Localhost: ", arguments.host_ip)
        try:
            sock.sendto(buf.encode('utf-8'), (arguments.host_ip, arguments.host_port))
        except socket.error as msg:
            print ("Failed to send data...Exiting...")
            sys.exit(-1)
            
        try:
            buf, addr = sock.recvfrom(1000)
            buf = buf.decode('utf-8')
            #print("buffer: ", buf)
        except socket.error as msg:
            print ("didn't get response from server...")
        
        if buf.find('***identified***') >= 0:
            print ('Received: ', buf)
            break

    currentStep = 0

    while True:
     
        #print(State(d.state.sensors["speedX"],))
        # wait for an answer from server
        buf = None
        try:
            buf, addr = sock.recvfrom(1000)
            buf = buf.decode('utf-8')
        except socket.error as msg:
            print ("didn't get response from server...")
        
        if verbose:
            print ('Received: ', buf)
        
        if buf != None and buf.find('***shutdown***') >= 0:
            #d.onShutDown()
            #shutdownClient = True
            print ('Client Shutdown')
            #print(d.table) #Prints the Qtable

            #Creates Xcel File filled with Qtable
            #d.table.to_csv(path_or_buf="./tempQtable.csv",index=False)
            
            break
        
        if buf != None and buf.find('***restart***') >= 0:
            d.onRestart()
            print ('Client Restart')
            #d.table.to_csv(path_or_buf="./tempQtable.csv",index=False)
            f=open("./episode.txt","r")
            x=int(f.read())+1
            f.close()
            f=open("./episode.txt","w")
            f.write(str(x))
            f.close()
            print("Episod number = "+str(x))
            #execfile('./pyclient.py')  #Do After first iteration
            #exec(open("./pyclient.py").read())
            break
        
        currentStep += 1
        if currentStep != arguments.max_steps:
            #print("currentStep = ",currentStep)
            if buf != None:
                buf = d.drive(buf, arguments.view)
                #print(d.state.getDistRaced())
        else:
            buf = '(meta 1)'
        
        if verbose:
            print ('Sending: ', buf)
        
        if buf != None:
            try:
                sock.sendto(buf.encode('utf-8'), (arguments.host_ip, arguments.host_port))
            except socket.error as msg:
                print ("Failed to send data...Exiting...")
                sys.exit(-1)
    
    curEpisode += 1
    print ("---------------------curEpisode-------------:", curEpisode)
    if curEpisode == arguments.max_episodes:
        if not arguments.view:
            common.selection(d, arguments.numElites)
        shutdownClient = True
    d = driver.Driver(arguments.stage, None, d.table)


sock.close()



