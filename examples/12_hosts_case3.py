#!/usr/bin/env python

import os
from time import sleep
from mininet.examples.popen import monitorhosts
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from subprocess import call
from threading import Thread
from get_lost import Lost
import subprocess


def cmd_client(host, dst_host, port, flow_type, rate):
    flow = ''
    
    if flow_type == 'udp':
        flow = '-u'

    filename = str(host) + 'client' + str(port) + '.out'
    host.cmd( 'iperf3  ' + flow + ' -c ' + str(dst_host.IP()) + ' -p ' + str(port) + 
             ' -b ' + str(rate) + 'M -i 1 -t 5 ' \
             ' >> /home/mininet/Desktop/c3p/' + filename + ' & ')
    
def cmd_server(host, port):
    filename = str(host) + 'server' + str(port) + '.out'
    output_file = '/home/mininet/Desktop/c3p/' + filename
    cmd = 'iperf3  -s -i 1 -p ' + str(port) + ' >> /home/mininet/Desktop/c3p/' + filename + \
    ' & '
    host.cmd(cmd)

def set_normal_policing(controller, rate):
    port = 's2-eth5'
    cmd_policing_rate = "ovs-vsctl set interface {0} ingress_policing_rate={1}".format(
        port, rate)
    controller.cmd(cmd_policing_rate)

def turn_tx_off(h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12):
    h1.cmd('ethtool -K h1-eth0 tx off')
    h2.cmd('ethtool -K h2-eth0 tx off')
    h3.cmd('ethtool -K h3-eth0 tx off')
    h4.cmd('ethtool -K h4-eth0 tx off')
    h5.cmd('ethtool -K h5-eth0 tx off')
    h6.cmd('ethtool -K h6-eth0 tx off')
    h7.cmd('ethtool -K h7-eth0 tx off')
    h8.cmd('ethtool -K h8-eth0 tx off')
    h9.cmd('ethtool -K h9-eth0 tx off')
    h10.cmd('ethtool -K h10-eth0 tx off')
    h11.cmd('ethtool -K h11-eth0 tx off')
    h12.cmd('ethtool -K h12-eth0 tx off')

def clear_directory(directory):
    for file in os.listdir(directory):
        path = os.path.join(directory, file)
        if os.path.isfile(path):
            os.remove(path)
    # print('fininshed')


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
    # UserSwitch, OVSKernelSwitch
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
    h9 = net.addHost('h9', cls=Host, ip='10.0.0.9', defaultRoute=None,)
    h10 = net.addHost('h10', cls=Host, ip='10.0.0.10', defaultRoute=None,)
    h11 = net.addHost('h11', cls=Host, ip='10.0.0.11', defaultRoute=None,)
    h12 = net.addHost('h12', cls=Host, ip='10.0.0.12', defaultRoute=None,)

    
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
    net.addLink(s2, h9)
    net.addLink(s2, h10)
    net.addLink(s2, h11)
    net.addLink(s2, h12)


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

    # clear files in targeted directory
    directory = '/home/mininet/Desktop/c3p'
    clear_directory(directory)

    output = c0.cmd('ovs-vsctl set bridge s1 datapath_type=netdev; \
                    ovs-vsctl set bridge s1 protocols=OpenFlow13; \
                    ovs-vsctl set bridge s2 datapath_type=netdev; \
                    ovs-vsctl set bridge s2 protocols=OpenFlow13; \
                    \
                    ovs-ofctl add-meter s2 "meter=2,kbps,burst,band=type=drop,rate={0},burst_size=100" -O OpenFlow13; \
                    ovs-ofctl add-flow s2 "table=0,priority=5,ip,nw_dst=10.0.0.5,action=meter:2,output:1" -O OpenFlow13; \
                    \
                    ovs-ofctl add-meter s2 "meter=3,kbps,burst,band=type=drop,rate={0},burst_size=100" -O OpenFlow13; \
                    ovs-ofctl add-flow s2 "table=0,priority=5,ip,nw_dst=10.0.0.6,action=meter:3,output:2" -O OpenFlow13; \
                    \
                    ovs-ofctl add-meter s2 "meter=4,kbps,burst,band=type=drop,rate={0},burst_size=100" -O OpenFlow13; \
                    ovs-ofctl add-flow s2 "table=0,priority=5,ip,nw_dst=10.0.0.7,action=meter:4,output:3" -O OpenFlow13; \
                    \
                    ovs-ofctl add-meter s2 "meter=5,kbps,burst,band=type=drop,rate={0},burst_size=100" -O OpenFlow13; \
                    ovs-ofctl add-flow s2 "table=0,priority=5,ip,nw_dst=10.0.0.8,action=meter:5,output:4" -O OpenFlow13; \
                    \
                    '.format(10*1024))
    print(output)


    turn_tx_off(h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12) # this commmend is incredibly important

    sleep(3.0)

    servers = []


    servers.append(Thread(target=cmd_server, args=(h5, 5105)))
    servers.append(Thread(target=cmd_server, args=(h6, 5106)))
    servers.append(Thread(target=cmd_server, args=(h7, 5207)))
    servers.append(Thread(target=cmd_server, args=(h8, 5208)))

    servers.append(Thread(target=cmd_server, args=(h5, 5305)))
    servers.append(Thread(target=cmd_server, args=(h6, 5306)))
    servers.append(Thread(target=cmd_server, args=(h7, 5407)))
    servers.append(Thread(target=cmd_server, args=(h8, 5408)))

    
    for server in servers:
        server.start()
        sleep(0.1)

    
    # h1 and h2 send elephant flows
    speed_host12 = 8
    flow_host12 = 'udp'
    # h3 and h4 send mice flows
    speed_host34 = 2
    flow_host34 = 'udp'

    clients = []


    clients.append(Thread(target=cmd_client, args=(h1, h5, 5105, flow_host12, speed_host12)))
    clients.append(Thread(target=cmd_client, args=(h1, h6, 5106, flow_host12, speed_host12)))
    clients.append(Thread(target=cmd_client, args=(h3, h5, 5305, flow_host34, speed_host34)))
    clients.append(Thread(target=cmd_client, args=(h3, h6, 5306, flow_host34, speed_host34)))

    clients.append(Thread(target=cmd_client, args=(h2, h7, 5207, flow_host12, speed_host12)))
    clients.append(Thread(target=cmd_client, args=(h2, h8, 5208, flow_host12, speed_host12)))
    clients.append(Thread(target=cmd_client, args=(h4, h7, 5407, flow_host34, speed_host34)))
    clients.append(Thread(target=cmd_client, args=(h4, h8, 5408, flow_host34, speed_host34)))


    for client in clients:
        client.start()
        sleep(0.03) 

    
    lost_obj = Lost()
    losts = []

    limits = []
    for i in range(4):
        limits.append(10.0)

    limit = []
    for i in range(4):
        limit.append(10.0)

    coefficient = 2


    for i in range(1, 30):
        
        sleep(6.0) # x.1 is accpetable


        lost5105, total5105 = lost_obj.get_rate(h5, 5105)
        lost5106, total5106 = lost_obj.get_rate(h6, 5106)
        lost5207, total5207 = lost_obj.get_rate(h7, 5207)
        lost5208, total5208 = lost_obj.get_rate(h8, 5208)

        lost5305, total5305 = lost_obj.get_rate(h5, 5305)
        lost5306, total5306 = lost_obj.get_rate(h6, 5306)
        lost5407, total5407 = lost_obj.get_rate(h7, 5407)
        lost5408, total5408 = lost_obj.get_rate(h8, 5408)


        # if i > 8:
        #     one_piece = total5105 / 4
        #     total5105 = total5105 - one_piece
        #     lost5105 = lost5105 - one_piece

        #     second_piece = total5106 / 4
        #     total5106 = total5106 - second_piece
        #     lost5106 = lost5106 - second_piece

        lost_rate_h5 = (lost5105 + lost5305) / (total5105 + total5305)
        lost_rate_h6 = (lost5106 + lost5306) / (total5106 + total5306) 
        lost_rate_h7 = (lost5207 + lost5407) / (total5207 + total5407)
        lost_rate_h8 = (lost5208 + lost5408) / (total5208 + total5408)


        temp_list = [i, lost_rate_h5, lost_rate_h6, lost_rate_h7, lost_rate_h8,]
        print(temp_list)
        losts.extend(temp_list)
        
        # update limiting rate
        lost_list = [lost_rate_h5, lost_rate_h6, lost_rate_h7, lost_rate_h8,]

        # use c3p strategy independently
        # for hosts ranging from h5 to h8
        for h in range(0, 4):
            left = (h+4-1) % 4
            right = (h+1) % 4
            lost_sum = lost_list[h] * 2 - lost_list[left] - lost_list[right]
            limit[h] = limit[h] + coefficient * lost_sum

     
        print(limit)
        print()
        limits.extend(limit)
        
        
        # update limitation of flow speed in hosts ranging from h5 to h8

        for j in range(4):
            command = 'ovs-ofctl mod-meter s2 "meter={},kbps,burst,band=type=drop,rate={},burst_size={}" -O OpenFlow13; \
                        '.format(j+2, int(limit[j]*1024), 100)
            
            output = c0.cmd(command)
            # print(output)


        # limit the speed of elephant flows
        # if i == 8:
        #     print('elephant flow limiting begins')
        #     '''
        #     h1 -> h5
        #     h1 -> h6
        #     '''
        #     output = c0.cmd('ovs-ofctl add-meter s1 "meter=20,kbps,burst,band=type=drop,rate={0},burst_size=100" -O OpenFlow13; \
        #                 ovs-ofctl add-flow s1 "table=0,priority=10,ip,nw_src=10.0.0.1,nw_dst=10.0.0.5,action=meter:20,output:5" -O OpenFlow13; \
        #                     \
        #                     ovs-ofctl add-meter s1 "meter=21,kbps,burst,band=type=drop,rate={0},burst_size=100" -O OpenFlow13; \
        #                 ovs-ofctl add-flow s1 "table=0,priority=10,ip,nw_src=10.0.0.1,nw_dst=10.0.0.6,action=meter:21,output:6" -O OpenFlow13; \
        #                 '.format(15*1024))
        #     print(output)


        clients = []
        if i < 5:
            clients.append(Thread(target=cmd_client, args=(h1, h5, 5105, flow_host12, speed_host12)))
            clients.append(Thread(target=cmd_client, args=(h1, h6, 5106, flow_host12, speed_host12)))
        else:
            clients.append(Thread(target=cmd_client, args=(h1, h5, 5105, flow_host12, 20)))
            clients.append(Thread(target=cmd_client, args=(h1, h6, 5106, flow_host12, 20)))

        clients.append(Thread(target=cmd_client, args=(h3, h5, 5305, flow_host34, speed_host34)))
        clients.append(Thread(target=cmd_client, args=(h3, h6, 5306, flow_host34, speed_host34)))

        clients.append(Thread(target=cmd_client, args=(h2, h7, 5207, flow_host12, speed_host12)))
        clients.append(Thread(target=cmd_client, args=(h2, h8, 5208, flow_host12, speed_host12)))
        clients.append(Thread(target=cmd_client, args=(h4, h7, 5407, flow_host34, speed_host34)))
        clients.append(Thread(target=cmd_client, args=(h4, h8, 5408, flow_host34, speed_host34)))


        for client in clients:
            client.start()
            sleep(0.03) # cannot set sleeptime = 0, idealy 0.1s


    CLI(net)

    net.stop()

    # clear the network topology, switches and hosts 
    os.system('sudo mn -c')


if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
