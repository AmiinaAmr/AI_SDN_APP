Exp1 Adding flow in a sample topologie  manuellement
******************************************************


1-

sudo mn --custom mininet/custom/sample.py --topo=mytopo --controller=none

2-

 sh ovs-ofctl dump-flows s1


3- 

pingall

4-

sh ovs-ofctl add-flows s1 dl_src=00:00:00:00:00:02,dl_dst=00:00:00:00:00:01,actions=output:1
sh ovs-ofctl add-flows s1 dl_src=00:00:00:00:00:01,dl_dst=00:00:00:00:00:02,actions=output:2

5-

 sh ovs-ofctl dump-flows s1

6-

pingall


Exp2 Ading flow in a sample topologie  with controller
********************************************************

 ryu-manager ryu/ryu/app/simple_switch_13.py 


1-

sudo mn --custom mininet/custom/sample.py --topo=mytopo --controller=remote,ip=0.0.0.0,port=6633

2-

 sh ovs-ofctl dump-flows s1


3- 

pingall

4-

 sh ovs-ofctl dump-flows s1


Exp3Ading flow in a sample topologie  with controller
********************************************************

sudo mn --custom mininet/custom/2tierSDN.py --topo=mytopo --topo=mytopo --controller=remote,ip=0.0.0.0,port=6633

 ryu-manager ryu/ryu/app/simple_switch_13.py 


2-
 sh ovs-ofctl dump-flows s1
 sh ovs-ofctl dump-flows s7
 sh ovs-ofctl dump-flows s8
3- 

pingall

4-

 sh ovs-ofctl dump-flows s1
 sh ovs-ofctl dump-flows s7
 sh ovs-ofctl dump-flows s8








