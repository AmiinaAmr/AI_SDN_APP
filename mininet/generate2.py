from time import sleep
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.link import TCLink
from scapy.all import *
import csv
import random
import re
from os import path
from os import mkdir
import logging
import sys
log_dir = "./mininet-log"

# IPERF SETTINGS
sampling_interval = '1'  # seconds

class MyTopo( Topo ):
    "Simple topology example."
    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )
        logging.basicConfig(filename='debug.log', level=logging.DEBUG)

        # Add hosts and switches

        h1 = self.addHost('h1', mac='00:00:00:00:00:01')
        h2 = self.addHost('h2', mac='00:00:00:00:00:02')
        h3 = self.addHost('h3', mac='00:00:00:00:00:03')
        h4 = self.addHost('h4', mac='00:00:00:00:00:04')
        h5 = self.addHost('h5', mac='00:00:00:00:00:05')
        h6 = self.addHost('h6',  mac='00:00:00:00:00:06')
        s1 = self.addSwitch('s1', mac='00:00:00:00:00:07', dpid='1')
        s2 = self.addSwitch('s2', mac='00:00:00:00:00:08', dpid='2')
        s3 = self.addSwitch('s3', mac='00:00:00:00:00:09',  dpid='3')
        s4 = self.addSwitch('s4', mac='00:00:00:00:00:10',  dpid='4')
        s5 = self.addSwitch('s5', mac='00:00:00:00:00:11', dpid='5')
        s6 = self.addSwitch('s6', mac='00:00:00:00:00:12',  dpid='6')
        s7 = self.addSwitch('s7', mac='00:00:00:00:00:13', dpid='7')
        s8 = self.addSwitch('s8', mac='00:00:00:00:00:14',  dpid='8')

        # Add links

        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(h3, s3)
        self.addLink(h4, s4)
        self.addLink(h5, s5)
        self.addLink(h6, s6)

        self.addLink(s1, s7)
        self.addLink(s1, s8)
        self.addLink(s2, s7)
        self.addLink(s2, s8)
        self.addLink(s3, s7)
        self.addLink(s3, s8)
        self.addLink(s4, s7)
        self.addLink(s4, s8)
        self.addLink(s5, s7)
        self.addLink(s5, s8)
        self.addLink(s6, s7)
        self.addLink(s6, s8)
def pingall():
    # Ping all hosts to all other hosts
    for src in hosts:
        for dst in hosts:
            if src != dst:  # Exclude self-ping
                output = src.cmd('ping -c 4', dst.IP())  # Execute the ping command
                       
def start_network():
    print ("Starting Network")
    topo = MyTopo()
    c0 = RemoteController('c0', ip='0.0.0.0',port=6633)
    net = Mininet(topo=topo, link=TCLink,controller=c0)
    print("\nStarting network ...\n")
    net.start()
    h1 = net.get('h1')
    h2 = net.get('h2')
    h3 = net.get('h3')
    h4 = net.get('h4')
    h5 = net.get('h5')
    h6 = net.get('h6')
    hosts = [h1, h2, h3, h4, h5, h6]
    
    s1 = net.get('s1')
    s2 = net.get('s2')
    s3 = net.get('s3')
    s4 = net.get('s4')
    s5 = net.get('s5')
    s6 = net.get('s6')
    s7 = net.get('s7')
    s8 = net.get('s8')    
    switches = [s1, s2, s3, s4, s5, s6, s7, s8]
     
    # Generate flows
    print("Generate flows")
    
    h1.cmd('iperf -s -p 5001 >> generate2_logs.txt &')
    h2.cmd('iperf -s -p 5002 >> generate2_logs.txt &')
    h3.cmd('iperf -c {} -p 5001 -t 60 -i 1 & >> generate2_logs.txt '.format(h1.IP()))
    h4.cmd('iperf -c {} -p 5001 -t 60 -i 1 & >> generate2_logs.txt '.format(h1.IP()))
    h5.cmd('iperf -c {} -p 5002 -t 60 -i 1 & >> generate2_logs.txt '.format(h2.IP()))
    h6.cmd('iperf -c {} -p 5002 -t 60 -i 1 & >> generate2_logs.txt '.format(h2.IP()))

    # Wait for the flows to complete
    net.waitConnected()

    # Enter the Mininet CLI for further interaction
    CLI(net)
    # Stop the network
    net.stop()    
    
start_network()
