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

log_dir = "./mininet-log"

# IPERF SETTINGS
sampling_interval = '1'  # seconds

class MyTopo( Topo ):
    "Simple topology example."
    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

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
        
def start_network():
#print "Starting Network"
    topo = MyTopo()
    c0 = RemoteController('c0', ip='0.0.0.0',port=6633)
    net = Mininet(topo=topo, link=TCLink,controller=c0)
    net.start()

    h1 = net.get('h1')
    h2 = net.get('h2')
    h3 = net.get('h3')
    h4 = net.get('h4')
    h5 = net.get('h5')
    h6 = net.get('h6')
    hosts = [h1, h2, h3, h4, h5, h6]
    
    generate_flows_from_csv(hosts,"dataset/NSL_KDD_Test.csv")

    CLI(net)
    net.stop()

def generate_flows_from_csv(hosts, csv_file):
    "Generate flows using attributes from the given CSV file."
    if not path.exists(log_dir):
         mkdir(log_dir)
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            src = random.choice(hosts)
            dst = random.choice(hosts)
            flow_attributes = {
                "duration": int(row[0]),
                "protocol_type": row[1],
            }
            sendFlow(src, dst, **flow_attributes)

def sendFlow(src, dst, **kwargs):
    "Add a flow with attributes between source and destination hosts."
    # Start iperf server on destination host
    server_cmd = "iperf -s "
    if kwargs["protocol_type"]=="udp":
         server_cmd += " -u "
    server_cmd += " -p "
    server_cmd += "80"
    server_cmd += " -i "
    server_cmd += sampling_interval
    server_cmd += " > "
    server_cmd += log_dir + "/generated_flow" + ".txt 2>&1 "
    server_cmd += " & "
    # Start iperf client on source host to send traffic to the destination
    client_cmd = "iperf -c "
    client_cmd += dst.IP() + " "
    if kwargs["protocol_type"]=="udp":
         client_cmd += " -u "
    client_cmd += " -p "
    client_cmd += "80"
    client_cmd += " -t "
    client_cmd += str(kwargs["duration"])
    client_cmd += " & "

    # send the cmd
    dst.cmd(server_cmd)
    src.cmd(client_cmd)

        

start_network()

