#!/usr/bin/env python

import os
from time import sleep
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
from threading import Thread


def cmd_client(host, dst_host, port, flow_type, rate):    
    flow = ''
    if flow_type == 'udp':
        flow = '-u'

    filename = str(host) + 'client' + str(port) + '.out'

    host.cmd( 'iperf ' + flow + ' -c ' + str(dst_host.IP()) + ' -p ' + str(port) + 
             ' -b ' + str(rate) + 'M -i 1 -t 45 -e ' \
             ' > /home/mininet/Desktop/flow-data/' + filename +' & ')


def cmd_server(host, port, flow_type):
    flow = ''
    if flow_type == 'udp':
        flow = '-u'

    filename = str(host) + 'server' + str(port) + '.out'
    host.cmd( 'iperf ' + flow + ' -s -i 1 -p ' + str(port) + 
             ' > /home/mininet/Desktop/flow-data/' + filename + ' & ')
    
    

def turn_tx_off(h1, h2, h3, h4, h5, h6, h7, h8):
    h1.cmd('ethtool -K h1-eth0 tx off')
    h2.cmd('ethtool -K h2-eth0 tx off')
    h3.cmd('ethtool -K h3-eth0 tx off')
    h4.cmd('ethtool -K h4-eth0 tx off')
    
    h5.cmd('ethtool -K h5-eth0 tx off')
    h6.cmd('ethtool -K h6-eth0 tx off')
    h7.cmd('ethtool -K h7-eth0 tx off')
    h8.cmd('ethtool -K h8-eth0 tx off')


def myNetwork():

    # ryu location
    # /usr/lib/python3/dist-packages/ryu/app
    
    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/8')

    # info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=RemoteController,
                      ip='127.0.0.1',
                      protocol='tcp',
                      port=6633)

    # info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, dpid='0000000000000001')
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch, dpid='0000000000000002')

    # info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1', defaultRoute=None,)
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2', defaultRoute=None,)
    h3 = net.addHost('h3', cls=Host, ip='10.0.0.3', defaultRoute=None,)
    h4 = net.addHost('h4', cls=Host, ip='10.0.0.4', defaultRoute=None,)
    h5 = net.addHost('h5', cls=Host, ip='10.0.0.5', defaultRoute=None,)
    h6 = net.addHost('h6', cls=Host, ip='10.0.0.6', defaultRoute=None,)
    h7 = net.addHost('h7', cls=Host, ip='10.0.0.7', defaultRoute=None,)
    h8 = net.addHost('h8', cls=Host, ip='10.0.0.8', defaultRoute=None,)


    # info( '*** Add links\n')
    net.addLink(s1, h1)
    net.addLink(s1, h2)
    net.addLink(s1, h3)
    net.addLink(s1, h4)
    net.addLink(s2, h5) # net.addLink(s2, h5, cls=TCLink, bw = 10)
    net.addLink(s2, h6)
    net.addLink(s2, h7)
    net.addLink(s2, h8)
    net.addLink(s1, s2)

    # get instances of controller, switches and hosts
    c0 = net.get('c0')
    s1, s2 = net.get('s1', 's2')
    h1, h2, h3, h4, h5, h6, h7, h8 = net.get('h1', 'h2', 'h3', 'h4', 
                                             'h5', 'h6', 'h7', 'h8')

    info( '*** Starting network\n')
    net.build()

    # starting controllers
    for controller in net.controllers:
        controller.start()

    # starting switches
    net.get('s1').start([c0])
    net.get('s2').start([c0])

    info( '*** Testing connectivity of all hosts\n')
    net.pingAll()

    
    output = c0.cmd('ovs-vsctl set bridge s2 datapath_type=netdev; \
                    ovs-vsctl set bridge s2 protocols=OpenFlow13; \
                    ovs-vsctl set bridge s1 datapath_type=netdev; \
                    ovs-vsctl set bridge s1 protocols=OpenFlow13; \
                    \
                    ovs-ofctl add-meter s2 "meter=2,kbps,burst,band=type=drop,rate=5120,burst_size=5120" -O OpenFlow13; \
                    ovs-ofctl add-flow s2 "table=0,priority=5,ip,nw_dst=10.0.0.5,action=meter:2,output:1" -O OpenFlow13; \
                    \
                    ovs-ofctl add-meter s2 "meter=3,kbps,burst,band=type=drop,rate=5120,burst_size=5120" -O OpenFlow13; \
                    ovs-ofctl add-flow s2 "table=0,priority=5,ip,nw_dst=10.0.0.6,action=meter:3,output:2" -O OpenFlow13; \
                    \
                    ovs-ofctl add-meter s2 "meter=4,kbps,burst,band=type=drop,rate=5120,burst_size=5120" -O OpenFlow13; \
                    ovs-ofctl add-flow s2 "table=0,priority=5,ip,nw_dst=10.0.0.7,action=meter:4,output:3" -O OpenFlow13; \
                    \
                    ovs-ofctl add-meter s2 "meter=5,kbps,burst,band=type=drop,rate=5120,burst_size=5120" -O OpenFlow13; \
                    ovs-ofctl add-flow s2 "table=0,priority=5,ip,nw_dst=10.0.0.8,action=meter:5,output:4" -O OpenFlow13; \
                    ')
    print(output)

    
    turn_tx_off(h1, h2, h3, h4, h5, h6, h7, h8) # this commmend is incredibly important

    sleep(0)

    speed_host12 = 2
    speed_host34 = 8
    flow_host12 = 'udp'
    flow_host34 = 'udp'

    sleep(5.0)

    servers = []
    servers.append(Thread(target=cmd_server, args=(h8, 5048, flow_host34)))
    servers.append(Thread(target=cmd_server, args=(h5, 5035, flow_host34)))
    servers.append(Thread(target=cmd_server, args=(h6, 5046, flow_host34)))
    servers.append(Thread(target=cmd_server, args=(h7, 5037, flow_host34)))
    servers.append(Thread(target=cmd_server, args=(h8, 5028, flow_host12)))
    servers.append(Thread(target=cmd_server, args=(h5, 5015, flow_host12)))
    servers.append(Thread(target=cmd_server, args=(h6, 5026, flow_host12)))
    servers.append(Thread(target=cmd_server, args=(h7, 5017, flow_host12)))
    
    for server in servers:
        server.start()
        sleep(0.02)
    
    clients = []
    clients.append(Thread(target=cmd_client, args=(h1, h5, 5015, flow_host12, speed_host12)))
    clients.append(Thread(target=cmd_client, args=(h1, h7, 5017, flow_host12, speed_host12)))
    clients.append(Thread(target=cmd_client, args=(h2, h6, 5026, flow_host12, speed_host12)))
    clients.append(Thread(target=cmd_client, args=(h2, h8, 5028, flow_host12, speed_host12)))
    clients.append(Thread(target=cmd_client, args=(h3, h5, 5035, flow_host34, speed_host34)))
    clients.append(Thread(target=cmd_client, args=(h3, h7, 5037, flow_host34, speed_host34)))
    clients.append(Thread(target=cmd_client, args=(h4, h6, 5046, flow_host34, speed_host34)))
    clients.append(Thread(target=cmd_client, args=(h4, h8, 5048, flow_host34, speed_host34)))

    for client in clients:
        client.start()
        sleep(0.02)


    case_id = '0x02'

    sleep(3.0) # why the sleeping time does not affect executing instructions?

    if case_id == '0x00':
        pass
    elif case_id == '0x01' or case_id == '0x02':
        output = c0.cmd('ovs-ofctl add-meter s1 "meter=10,kbps,band=type=drop,rate=5120" -O OpenFlow13; \
                        ovs-ofctl add-flow s1 "table=0,priority=10,ip,nw_src=10.0.0.3,nw_dst=10.0.0.7,action=meter:10,output:5" -O OpenFlow13; \
                        \
                        ovs-ofctl add-meter s1 "meter=11,kbps,band=type=drop,rate=5120" -O OpenFlow13; \
                        ovs-ofctl add-flow s1 "table=0,priority=10,ip,nw_src=10.0.0.4,nw_dst=10.0.0.8,action=meter:11,output:5" -O OpenFlow13; \
                        ')
    elif case_id == '0x03':
        output = c0.cmd('ovs-ofctl add-meter s1 "meter=10,kbps,band=type=drop,rate=5120" -O OpenFlow13; \
                        ovs-ofctl add-flow s1 "table=0,priority=10,ip,nw_src=10.0.0.3,nw_dst=10.0.0.7,action=meter:10,output:5" -O OpenFlow13; \
                        \
                        ovs-ofctl add-meter s1 "meter=11,kbps,band=type=drop,rate=5120" -O OpenFlow13; \
                        ovs-ofctl add-flow s1 "table=0,priority=10,ip,nw_src=10.0.0.4,nw_dst=10.0.0.8,action=meter:11,output:5" -O OpenFlow13; \
                        \
                        ovs-ofctl add-meter s1 "meter=12,kbps,band=type=drop,rate=5120" -O OpenFlow13; \
                        ovs-ofctl add-flow s1 "table=0,priority=10,ip,nw_src=10.0.0.1,nw_dst=10.0.0.7,action=meter:12,output:5" -O OpenFlow13; \
                        \
                        ovs-ofctl add-meter s1 "meter=13,kbps,band=type=drop,rate=5120" -O OpenFlow13; \
                        ovs-ofctl add-flow s1 "table=0,priority=10,ip,nw_src=10.0.0.2,nw_dst=10.0.0.8,action=meter:13,output:5" -O OpenFlow13; \
                        \
                        ')

    CLI(net)

    net.stop()

    # clear the network topology, switches and hosts 
    os.system('sudo mn -c')


if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
