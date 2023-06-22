from mininet.topo import Topo

import re
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


topos = { 'mytopo': ( lambda: MyTopo() ) }
